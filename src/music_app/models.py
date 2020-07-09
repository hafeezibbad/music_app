import hashlib

from typing import List, Optional

from pydantic import BaseModel, constr, conint, confloat  # pylint: disable=no-name-in-module
from typing_extensions import Literal

from src.lib.configuration.validate import StrictNonEmptyStr, RELEASE_DATE_REGEX, HASH_REGEX


class Model(BaseModel):
    @classmethod
    def load(cls, data: dict, **kwargs):
        init = {}
        for k, v in data.items():
            if k in cls.schema()["properties"]:
                init[k] = v

        if init:
            return cls(**init, **kwargs)  # type: ignore

        raise ValueError(init)


class Song(Model):
    artist: Optional[StrictNonEmptyStr] = None
    title: Optional[StrictNonEmptyStr] = None
    difficulty: confloat(ge=1) = 1
    level: conint(ge=1) = 1
    rating: List[conint(ge=1, le=5)] = []
    # FIXME: possible bug, repeated entry with no request date provided initially
    released: Optional[constr(regex=RELEASE_DATE_REGEX)] = None
    version: int = 0

    @property
    def hash(self) -> constr(regex=HASH_REGEX):
        return get_hash(self.artist, self.title, self.difficulty, self.level, self.released)


class SongDbRecord(Song):
    song_id: int
    created_at: str
    last_modified_at: str


class ErrorPointer(Model):
    pointer: Optional[str] = None


class Error(Model):
    status: int
    title: StrictNonEmptyStr
    detail: Optional[str] = None
    source: Optional[ErrorPointer] = None


class ApiError(Model):
    errors: List[Error]


def get_hash(*args, **kwargs) -> constr(regex=HASH_REGEX):
    sha3 = hashlib.sha3_224()

    for each in list(args) + list(kwargs.values()):
        # FIXME: This may fail when there args are some objects
        sha3.update(bytes(str(each).lower(), 'UTF-8'))

    return sha3.hexdigest()


class Status(Model):
    message: str
    status: str
    statusCode: Literal[200, 503]

    def get_status_data(self):
        fields: dict = self.dict()
        del fields['statusCode']

        return fields
