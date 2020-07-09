import copy
import pytest

# pylint: disable=unused-import
from tests.e2e.common import fixture_temporary_song_record_without_rating, fixture_request_id
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import post_song_rating_request
from tests.fixtures.songs_data import TEST_SONG_DATA_WITHOUT_RATING, TEST_SONG_RATINGS, INVALID_SONG_RATINGS


# pylint: disable=redefined-outer-name
class TestPostSongRating:
    @pytest.mark.parametrize("rating", TEST_SONG_RATINGS)
    def test_post_song_rating_returns_200(
            self,
            rating,
            fixture_request_id,
            fixture_temporary_song_record_without_rating
    ):
        # Temp router created using fixture_temporary_song_record_without_rating
        expected_song = copy.deepcopy(TEST_SONG_DATA_WITHOUT_RATING)
        expected_song['rating'] = [rating]
        response: E2EServiceResponse = post_song_rating_request(
            request_id=fixture_request_id,
            params=dict(song_id=fixture_temporary_song_record_without_rating, rating=rating)
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.body_contains_field(field='rating', expected_value=expected_song['rating'])
        response.is_valid_song(expected_song=expected_song)

    def test_multiple_post_rating_requests_return_200(
            self,
            fixture_request_id,
            fixture_temporary_song_record_without_rating
    ):
        # Temp router created using fixture_temporary_song_record_without_rating
        expected_song = copy.deepcopy(TEST_SONG_DATA_WITHOUT_RATING)
        for i, rating in enumerate(TEST_SONG_RATINGS):
            expected_song['rating'] = TEST_SONG_RATINGS[:i+1]
            response: E2EServiceResponse = post_song_rating_request(
                request_id=fixture_request_id,
                params=dict(song_id=fixture_temporary_song_record_without_rating, rating=rating)
            )
            response.status_code_is_200_ok()
            response.contains_request_id(fixture_request_id)
            response.body_contains_field(field='rating', expected_value=TEST_SONG_RATINGS[:i+1])
            response.is_valid_song(expected_song=expected_song)

    @pytest.mark.parametrize("invalid_rating", INVALID_SONG_RATINGS)
    def test_post_song_rating_returns_400_for_invalid_rating(
            self,
            invalid_rating,
            fixture_request_id,
            fixture_temporary_song_record_without_rating
    ):
        # Temp router created using fixture_temporary_song_record_without_rating
        response: E2EServiceResponse = post_song_rating_request(
            request_id=fixture_request_id,
            params=dict(song_id=fixture_temporary_song_record_without_rating, rating=invalid_rating)
        )
        response.status_code_is_400_bad_request()
        response.contains_request_id(fixture_request_id)
