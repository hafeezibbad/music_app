import pytest

from tests.e2e.common import fixture_populate_db, fixture_request_id  # pylint: disable=unused-import
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import songs_search_request
from tests.fixtures.songs_data import TEST_DATASET_SONGS, TEST_SEARCH_RESULTS, TEST_SEARCH_RESULTS_WITH_PAGESIZE


# pylint: disable=redefined-outer-name
class TestSongsSearchWithMessage:
    def test_search_song_with_no_search_text_return_all_items_with_200(
            self,
            fixture_request_id,
            fixture_populate_db
    ):
        # Database populated using fixture_populate_db
        response: E2EServiceResponse = songs_search_request(request_id=fixture_request_id)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        assert len(response.get_field('songs')) == len(TEST_DATASET_SONGS)

    @pytest.mark.parametrize("search_term,expected_item_count", TEST_SEARCH_RESULTS)
    def test_search_songs_return_200(
            self,
            search_term,
            expected_item_count,
            fixture_request_id,
            fixture_populate_db
    ):
        # Database populated using fixture_populate_db
        response: E2EServiceResponse = songs_search_request(
            request_id=fixture_request_id,
            params={'message': search_term}
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        assert len(response.get_field('songs')) == expected_item_count

    @pytest.mark.parametrize(
        "search_term,page_size,expected_item_count,next_anchor_present",
        TEST_SEARCH_RESULTS_WITH_PAGESIZE
    )
    def test_search_songs_return_200_with_pagination(
            self,
            search_term,
            page_size,
            expected_item_count,
            next_anchor_present,
            fixture_request_id,
            fixture_populate_db
    ):
        # Database populated using fixture_populate_db
        response: E2EServiceResponse = songs_search_request(
            request_id=fixture_request_id,
            params={'message': search_term, 'pageSize': page_size}
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        assert len(response.get_field('songs')) == expected_item_count
        if next_anchor_present is False:
            response.body_does_not_contain_field('links')
        else:
            response.body_contains_field('links')
