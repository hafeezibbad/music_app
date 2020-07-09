from contextlib import suppress

from src.database.errors import RecordAlreadyExists
from src.music_app.models import Song
from src.service.songs import SongsService


HEALTH_CHECK_SONG_DATA = dict(
    artist="Health checker",
    title="Health check song",
    difficulty=1.1,
    level=1,
    released="2020-07-06"
)


class HealthService:
    HEALTH_CHECK_SONG_TITLE = 'Health check song'
    HEALTH_CHECK_SONG_ = 'Health check song'

    def __init__(self, service: SongsService):
        self.service = service

    def __create_test_song_record(self) -> Song:
        return Song(**HEALTH_CHECK_SONG_DATA)

    def check_db_operations(self) -> bool:
        try:
            with suppress(RecordAlreadyExists):
                song = self.service.create_record(record=self.__create_test_song_record())

            read_song = self.service.get_record(record_id=song.song_id)
            if song.hash != read_song.hash:
                raise Exception

            _ = self.service.delete_record(record_id=song.song_id)

        except Exception:
            return False

        return True

    def check_all(self) -> bool:
        service_status = True
        service_status = service_status and self.check_db_operations()

        return service_status
