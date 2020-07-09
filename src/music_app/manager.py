import json
from json.decoder import JSONDecodeError
from statistics import mean
from typing import Optional, List, Type, Tuple, Dict, Union

from src.database.errors import RecordAlreadyExists, PreconditionFailed, RecordNotFound, DbGenericError, \
    SchemaValidationError
from src.database.models import SongRecord
from src.music_app.errors import MusicAppApiError, MusicAppErrorType, MusicAppSimpleError
from src.music_app.models import SongDbRecord, Model, Status

from src.request_parser.data_parser import RequestDataParser
from src.request_parser.song_data_parser import SongRequestDataParser
from src.service.errors import SongsServiceError
from src.service.health import HealthService
from src.service.songs import SongsService


class MusicAppManager:
    def __init__(
            self,
            requester_ip: Optional[str] = None,
            items_per_page: Optional[int] = 20
    ):
        self.requester_ip = requester_ip
        self.songs_service = SongsService(collection=SongRecord, default_page_size=items_per_page)

    def batch_create_songs(self, request_data: dict) -> Tuple[List[int], List[int]]:
        try:
            parsed_songs = []
            for song_data in request_data.get('songs', []):
                # This way, we can return error if song_data for any of the songs is bad before any records are
                # inserted in DB. Hence, we will not run into issues where half of the records in request are in DB,
                # and rest are not, and request fails.
                parsed_songs.append(self.__parse_request_data(parser=SongRequestDataParser, request_data=song_data))

            return self.songs_service.batch_upload(parsed_songs)

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Cannot create new song record in database'
            )

    def create_song(self, request_data: dict) -> SongDbRecord:
        try:
            song = self.__parse_request_data(parser=SongRequestDataParser, request_data=request_data)
            return self.songs_service.create_record(song)

        except RecordAlreadyExists:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_ALREADY_EXISTS,
                message="Song already exists"
            )

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Cannot create new song record in database'
            )

    def get_song(self, song_id: int, version: Optional[int] = None) -> SongDbRecord:
        try:
            return self.songs_service.get_record(record_id=song_id, version=version)

        except PreconditionFailed:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.READ_FAILED_VERSION_MISMATCH,
                message="Song record with version `{}` does not exist. Please try again without `If-None-Match` "
                        "header".format(version)
            )

        except RecordNotFound:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_NOT_FOUND,
                message="Song with given id `{}` not found".format(song_id)
            )

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to retrieve requested song'
            )

    def update_song(self, song_id: int, request_data: dict, version: Optional[int] = None) -> SongDbRecord:
        try:
            return self.songs_service.update_record(
                record_id=song_id,
                updates=self.songs_service.build_update_expression(**request_data),
                version=version
            )

        except TypeError:
            # Raised from build_update_expression() when invalid field is provided in request_data
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_DATA_INVALID,
                message='Invalid fields provided for updating song record'
            )

        except SchemaValidationError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_DATA_INVALID,
                message='Invalid data provided for updating song record'
            )

        except PreconditionFailed:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.UPDATE_FAILED_VERSION_MISMATCH,
                message='Failed to update song because specified version `{}` is outdated. Please retrieve latest '
                        'version before updating'.format(version)
            )

        except DbGenericError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.DB_PERSISTENCE_ERROR,
                message='Could not store data you provided to persistent data storage. Please try again later.'
            )

        except SongsServiceError as ex:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_DATA_INVALID,
                message='Invalid data provided for updating song'
            )

        except RecordNotFound:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_NOT_FOUND,
                message='No song found with `{}`'.format(song_id)
            )

    def delete_song(self, song_id: int) -> bool:
        try:
            return self.songs_service.delete_record(record_id=song_id)

        except RecordNotFound:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_NOT_FOUND,
                message="Song with given id `{}` not found for deletion".format(song_id)
            )

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to delete requested song'
            )

    def get_all_songs(self, start: int = 1, page_size: int = 20) -> Tuple[List[SongDbRecord], str]:
        try:
            return self.songs_service.get_all_records(start=start, page_size=page_size)

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to retrieve songs from database'
            )

    def get_average_rating(self, song_id: int) -> Dict[str, Optional[Union[int, float]]]:
        try:
            song = self.get_song(song_id=song_id)
            rating_stats = dict(average=None, lowest=None, highest=None)
            if song.rating:
                rating_stats['average'] = mean(song.rating)
                rating_stats['lowest'] = min(song.rating)
                rating_stats['highest'] = max(song.rating)

            return rating_stats

        except RecordNotFound:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SONG_NOT_FOUND,
                message="Song with given id `{}` not found".format(song_id)
            )

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to get rating for song with `{}`'.format(song_id)
            )

    def get_average_difficulty(self, level: int = -1) -> float:
        try:
            return self.songs_service.get_average_song_difficulty(level=level)

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to get average difficulty for songs at level `{}`'.format(level)
            )

    def search_songs(
            self,
            search_text: str,
            start: int = 0,
            page_size: int = 20
    ) -> Tuple[List[SongDbRecord], str]:
        try:
            return self.songs_service.search_songs_titles_and_artist(
                search_text=search_text,
                start=start,
                page_size=page_size
            )

        except SongsServiceError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.SERVICE_UNAVAILABLE_ERROR,
                message='Unable to retrieve songs from database'
            )

    def __parse_request_data(self, parser: Type[RequestDataParser], request_data: dict) -> Type[Model]:
        req_parser = parser(request_data=request_data)
        if not req_parser.is_valid():
            raise MusicAppApiError(
                code=MusicAppErrorType.INVALID_REQUEST_DATA,
                api_error=req_parser.get_api_error()
            )

        return req_parser.get_model()

    def parse_request_data_as_json(self, request_data: Union[bytes, dict]) -> dict:
        if not request_data:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.REQUEST_BODY_EMPTY,
                message='No JSON data provided in request body'
            )

        try:
            return json.loads(request_data)
        except JSONDecodeError:
            raise MusicAppSimpleError(
                code=MusicAppErrorType.REQUEST_BODY_INVALID_JSON,
                message='Invalid JSON format provided in request body'
            )

    def status(self) -> Status:
        health_service = HealthService(service=self.songs_service)
        health_status = health_service.check_all()
        # TODO: More logging about status
        if health_status is False:
            return Status(
                message="Service is down",
                status="down",
                statusCode=503
            )

        return Status(
            message="Service is up",
            status="ok",
            statusCode=200
        )
