import pytest

from tests.e2e.common import fixture_temporary_song_record, fixture_request_id  # pylint: disable=unused-import
from tests.e2e.common import delete_test_song_from_db, invalidate_song_data
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import create_song_request
from tests.fixtures.songs_data import TEST_SONG_DATA, INVALID_SONG_DATA


# pylint: disable=redefined-outer-name
class TestCreateSongRecord:
    def test_create_song_successful_returns_201(self, fixture_request_id):
        response: E2EServiceResponse = create_song_request(request_id=fixture_request_id)
        delete_test_song_from_db(song_id=response.get_song_id())

        response.status_code_is_201_created()
        response.contains_request_id(fixture_request_id)
        response.is_valid_song(expected_song=TEST_SONG_DATA)

    def test_already_existing_song_returns_409(self, fixture_request_id, fixture_temporary_song_record):
        # First router with similar data created using fixture_temporary_song_record
        response: E2EServiceResponse = create_song_request(
            request_id=fixture_request_id,
            song_data=TEST_SONG_DATA
        )

        response.contains_request_id(fixture_request_id)
        response.status_code_is_409_conflict()
        response.message_is('Song already exists')

    @pytest.mark.parametrize("song_data,field_name,invalid_data", INVALID_SONG_DATA)
    def test_invalid_song_data_returns_400(
            self,
            song_data: dict,
            field_name,
            invalid_data,
            fixture_request_id
    ):
        invalid_song_data = invalidate_song_data(song_data, [field_name], [invalid_data])
        response = create_song_request(request_id=fixture_request_id, song_data=invalid_song_data)

        response.contains_request_id(fixture_request_id)
        response.status_code_is_400_bad_request()
