from tests.e2e.common import fixture_temporary_song_record, fixture_request_id  # pylint: disable=unused-import
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import get_song_request
from tests.fixtures.songs_data import TEST_SONG_DATA, DEFAULT_INITIAL_VERSION, INVALID_VERSION, NON_EXISTING_SONG_ID


# pylint: disable=redefined-outer-name
class TestGetSongRecord:
    def test_get_song_successful_returns_200(self, fixture_request_id, fixture_temporary_song_record):
        # Song entry created using fixture_temporary_song_record
        response: E2EServiceResponse = get_song_request(
            request_id=fixture_request_id,
            song_id=fixture_temporary_song_record
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.is_valid_song(expected_song=TEST_SONG_DATA)

    def test_not_existing_record_returns_404(self, fixture_request_id):
        response: E2EServiceResponse = get_song_request(request_id=fixture_request_id, song_id=NON_EXISTING_SONG_ID)

        response.contains_request_id(fixture_request_id)
        response.status_code_is_404_not_found()

    def test_get_song_returns_304_for_matching_version(self, fixture_request_id, fixture_temporary_song_record):
        # Song entry created using fixture_temporary_song_record
        response: E2EServiceResponse = get_song_request(
            request_id=fixture_request_id,
            song_id=fixture_temporary_song_record,
            if_none_match_header=DEFAULT_INITIAL_VERSION
        )

        response.contains_request_id(fixture_request_id)
        response.status_code_is_304_not_modified()
        response.etag_is(DEFAULT_INITIAL_VERSION)
        response.body_is_empty()

    def test_get_song_contains_returns_400_for_non_numeric_version(
            self,
            fixture_request_id,
            fixture_temporary_song_record
    ):
        # Song entry created using fixture_temporary_song_record
        response: E2EServiceResponse = get_song_request(
            request_id=fixture_request_id,
            song_id=fixture_temporary_song_record,
            if_none_match_header=INVALID_VERSION
        )

        response.contains_request_id(fixture_request_id)
        response.status_code_is_400_bad_request()
        response.does_not_have_etag()
        response.message_is("Invalid value for If-None-Match header, <int> expected")
