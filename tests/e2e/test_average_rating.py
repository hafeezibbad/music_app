# pylint: disable=unused-import
from tests.e2e.common import fixture_temporary_song_record, fixture_request_id, \
    fixture_temporary_song_record_without_rating
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import get_average_song_rating_request
from tests.fixtures.songs_data import TEST_SONG_RATING_STATS


# pylint: disable=redefined-outer-name
class TestGetRatingForSong:
    def test_get_song_rating_returns_200(self, fixture_request_id, fixture_temporary_song_record):
        response: E2EServiceResponse = get_average_song_rating_request(
            request_id=fixture_request_id,
            song_id=fixture_temporary_song_record
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.body_contains_field(field='average', expected_value=TEST_SONG_RATING_STATS.average)
        response.body_contains_field(field='lowest', expected_value=TEST_SONG_RATING_STATS.lowest)
        response.body_contains_field(field='highest', expected_value=TEST_SONG_RATING_STATS.highest)

    def test_not_existing_record_returns_404(self, fixture_request_id):
        response: E2EServiceResponse = get_average_song_rating_request(request_id=fixture_request_id, song_id=123)

        response.contains_request_id(fixture_request_id)
        response.status_code_is_404_not_found()

    def test_get_song_rating_returns_200_and_null_values_if_there_are_no_ratings(
            self,
            fixture_request_id,
            fixture_temporary_song_record_without_rating
    ):
        response: E2EServiceResponse = get_average_song_rating_request(
            request_id=fixture_request_id,
            song_id=fixture_temporary_song_record_without_rating
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.body_contains_field(field='average', expected_value=None)
        response.body_contains_field(field='lowest', expected_value=None)
        response.body_contains_field(field='highest', expected_value=None)
