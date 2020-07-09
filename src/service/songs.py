from contextlib import suppress
from datetime import datetime
from typing import List, Dict, Any, Type, Tuple, Optional

from mongoengine import NotUniqueError, Q, DoesNotExist, ValidationError, FieldDoesNotExist
from mongoengine import Document

# pylint: disable=no-name-in-module, C0326
from pydantic import constr, conint

from src.database.errors import SchemaValidationError, RecordAlreadyExists, PreconditionFailed, RecordNotFound, \
    InvalidDataError, DbGenericError
from src.database.helpers import paginate_records, get_int_field_filter, get_string_field_filter
from src.database.models import SongRecord
from src.lib.configuration.validate import RELEASE_DATE_REGEX
from src.music_app.models import Song, SongDbRecord


class SongsService:
    def __init__(self, collection: Type[Document] = SongRecord, default_page_size: int = 10):
        self.collection = collection
        self.default_page_size = default_page_size

    def batch_upload(self, records: List[Song]) -> Tuple[List[int], List[int]]:
        new_song_ids = []
        existing_song_ids = []
        for record in records:
            try:
                song_record: SongDbRecord = self.create_record(record)
                new_song_ids.append(song_record.song_id)

            except RecordAlreadyExists as ex:
                # If a record already exists, add its ID to existing song IDs instead of failing. This is batch op.
                existing_song_ids.append(ex.existing_record_id)

        return new_song_ids, existing_song_ids

    def create_record(self, record: Song) -> SongDbRecord:
        try:
            with suppress(DoesNotExist):
                song_from_db = self.collection.objects.get(song_hash=record.hash)
                if song_from_db is not None:
                    # Similar record already exists in database
                    raise RecordAlreadyExists(existing_record_id=song_from_db.song_id)

            song_data = vars(record)
            song_data["created_at"] = datetime.utcnow()
            song_data["last_modified_at"] = datetime.utcnow()
            song_data["song_hash"] = record.hash

            song_db_record = self.collection(**song_data).save()

            return SongDbRecord.load(song_db_record.to_json())

        except (NotUniqueError, RecordAlreadyExists) as ex:
            raise RecordAlreadyExists(existing_record_id=getattr(ex, "existing_record_id", None))

        except ValidationError as ex:
            raise SchemaValidationError from ex

        except FieldDoesNotExist as ex:
            raise InvalidDataError from ex

        except Exception as ex:
            raise DbGenericError from ex

    def get_record(self, record_id: int, version: Optional[int] = None) -> SongDbRecord:
        try:
            song_record = self.collection.objects.get(song_id=record_id)
            if version is not None and song_record.version != version:
                raise PreconditionFailed

            return SongDbRecord.load(song_record.to_json())

        except DoesNotExist:
            raise RecordNotFound

        except PreconditionFailed:
            raise PreconditionFailed

        except Exception as ex:
            raise DbGenericError from ex

    def update_record(self, record_id: int, updates: Dict[str, Any], version: Optional[int] = None) -> SongDbRecord:
        try:
            song = self.collection.objects.get(song_id=record_id)
            if version is not None and song.version != version:
                raise PreconditionFailed

            updates['set__version'] = song.version + 1
            song.update(**updates, last_modified_at=datetime.utcnow())
            song.reload()

            return SongDbRecord.load(song.to_json())

        except DoesNotExist:
            raise RecordNotFound

        except ValidationError as ex:
            raise SchemaValidationError from ex

        except FieldDoesNotExist as ex:
            raise InvalidDataError from ex

        except Exception as ex:
            raise DbGenericError from ex

    def delete_record(self, record_id: int) -> bool:
        try:
            _ = self.collection.objects.get(song_id=record_id).delete()

            return True

        except DoesNotExist:
            raise RecordNotFound

        except Exception as ex:
            raise DbGenericError from ex

    @staticmethod
    def build_update_expression(
            artist: Optional[str] = None,
            title: Optional[str] = None,
            difficulty: Optional[conint(ge=0)] = None,
            level: Optional[conint(ge=0)] = None,
            rating: Optional[conint(ge=1, le=5)] = None,
            released: Optional[constr(regex=RELEASE_DATE_REGEX)] = None
    ) -> Dict[str, Any]:  # pylint: disable=C0326
        updates = dict()

        if artist is not None:
            updates['set__artist'] = artist

        if title is not None:
            updates['set__title'] = title

        if difficulty is not None:
            updates['set__difficulty'] = difficulty

        if level is not None:
            updates['set__level'] = level

        if rating is not None:
            updates['push__rating'] = rating

        if released is not None:
            updates['set__released'] = released

        return updates

    def search_songs_titles_and_artist(
            self,
            search_text: str,
            start: int = 0,
            page_size: Optional[int] = None
    ) -> Tuple[List[SongDbRecord], str]:
        songs = self.collection.objects.filter(Q(title__icontains=search_text) | Q(artist__icontains=search_text))
        if songs and start < songs.first().song_id:
            start = songs.first().song_id
        songs, anchor = paginate_records(
            query_set=songs,
            start=start,
            page_size=page_size or self.default_page_size
        )
        songs_records = [SongDbRecord.load(song.to_json()) for song in songs]

        return songs_records, anchor

    def get_all_records(
            self,
            start: Optional[int] = 0,
            page_size: Optional[int] = None
    ) -> Tuple[List[SongDbRecord], str]:
        songs, anchor = paginate_records(
            query_set=self.collection.objects(),
            start=start,
            page_size=page_size or self.default_page_size
        )
        songs_records = [SongDbRecord.load(song.to_json()) for song in songs]

        return songs_records, anchor

    def get_average_song_difficulty(self, level: int = -1) -> float:
        filters = {}
        if level is not None and level > 0:
            filters = get_int_field_filter(field_name="level", min_value=level, max_value=level)

        return self.collection.objects.filter(**filters).average('difficulty')

    def build_title_artist_filter(
            self,
            content: str,
            case_sensitive: bool = False,
            strict: bool = False
    ) -> Dict[str, Any]:
        filters = dict()

        filters.update(
            get_string_field_filter(
                field_name='artist',
                value=content,
                case_sensitive=case_sensitive,
                strict=strict
            )
        )
        filters.update(
            get_string_field_filter(
                field_name='level',
                value=content,
                case_sensitive=case_sensitive,
                strict=strict
            )
        )

        return filters
