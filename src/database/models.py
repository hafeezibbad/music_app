from datetime import datetime
import random
from typing import List

# pylint: disable=E0611, E1101
from pydantic import constr, conint

from src.database.db import db
from src.lib.configuration.validate import RELEASE_DATE_REGEX, StrictNonEmptyStr, RELEASE_DATE_FORMAT, HASH_REGEX
from src.lib.helpers import generate_random_date
from src.music_app.models import get_hash


class SongRecord(db.Document):
    song_id = db.SequenceField(primary_key=True)
    artist: StrictNonEmptyStr = db.StringField(max_length=128)
    title: StrictNonEmptyStr = db.StringField(max_length=128)
    difficulty: float = db.FloatField()
    level: int = db.IntField(min_value=1)
    rating: List[int] = db.ListField(db.IntField(min_value=1, max_value=5))
    released: StrictNonEmptyStr = db.StringField(regex=RELEASE_DATE_REGEX)
    song_hash: constr(regex=HASH_REGEX) = db.StringField(regex=HASH_REGEX)
    version: conint(ge=0) = db.IntField(min_value=0)
    created_at: datetime = db.DateTimeField()
    last_modified_at: datetime = db.DateTimeField(required=True, default=datetime.utcnow())

    def to_json(self):  # pylint: disable=W0221
        return {
            "song_id": str(self.song_id),
            "artist": self.artist,
            "title": self.title,
            "difficulty": self.difficulty,
            "level": self.level,
            "rating": self.rating,
            "released": self.released,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "last_modified_at": self.last_modified_at.isoformat(),
            "song_hash": self.hash
        }

    @property
    def hash(self):
        return get_hash(self.artist, self.title, self.difficulty, self.level, self.released)

    @staticmethod
    def generate_fake(entries: int = 200):
        # pylint: disable=import-outside-toplevel
        import forgery_py
        from mongoengine import ValidationError, NotUniqueError
        fakes = 0
        while fakes < entries:
            try:
                SongRecord(
                    artist=forgery_py.internet.user_name(),
                    title=forgery_py.lorem_ipsum.word(),
                    difficulty=random.uniform(1, 20),
                    level=random.randint(1, 50),
                    released=generate_random_date(date_format=RELEASE_DATE_FORMAT)
                ).save()

                fakes += 1

            except (ValidationError, NotUniqueError, Exception):
                pass
