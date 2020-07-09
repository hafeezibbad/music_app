import pytest

from tests.e2e.common import fixture_request_id, fixture_populate_db  # pylint: disable=unused-import
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import get_all_songs_request
from tests.fixtures.songs_data import TEST_DATASET_SONGS, TEST_GET_ALL_SONGS_WITH_PAGINATION


# pylint: disable=redefined-outer-name
class TestGetAllSongs:
    def test_get_all_song_returns_200(self, fixture_request_id, fixture_populate_db):
        # Database entries created using fixture_populate_db
        response: E2EServiceResponse = get_all_songs_request(request_id=fixture_request_id)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        assert len(response.get_field('songs')) == len(TEST_DATASET_SONGS)

    @pytest.mark.parametrize("page_size,expected_item_count", TEST_GET_ALL_SONGS_WITH_PAGINATION)
    def test_search_songs_return_200_with_pagination(
            self,
            page_size,
            expected_item_count,
            fixture_request_id,
            fixture_populate_db
    ):
        # Database entries created using fixture_populate_db
        response: E2EServiceResponse = get_all_songs_request(
            request_id=fixture_request_id,
            params={'pageSize': page_size}
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        assert len(response.get_field('songs')) == expected_item_count
