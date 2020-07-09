import pytest

from tests.e2e.common import fixture_request_id, fixture_populate_db  # pylint: disable=unused-import
from tests.e2e.e2e_response import E2EServiceResponse
from tests.e2e.request_utils import get_average_difficulty_request
from tests.fixtures.songs_data import DATASET_AVERAGE_DIFFICULTY, TEST_DATASET_DIFFICULTY_WITH_LEVEL


# pylint: disable=redefined-outer-name
class TestGetAverageDifficulty:
    def test_get_average_difficulty_returns_200(self, fixture_request_id, fixture_populate_db):
        # Database entries created using fixture_populate_db
        response: E2EServiceResponse = get_average_difficulty_request(request_id=fixture_request_id)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.body_contains_field(field='average_difficulty', expected_value=DATASET_AVERAGE_DIFFICULTY)

    @pytest.mark.parametrize("level,expected_difficulty", TEST_DATASET_DIFFICULTY_WITH_LEVEL)
    def test_get_average_difficulty_with_level_returns_200(
            self,
            level,
            expected_difficulty,
            fixture_request_id,
            fixture_populate_db
    ):
        # Database entries created using fixture_populate_db
        response: E2EServiceResponse = get_average_difficulty_request(
            request_id=fixture_request_id,
            params={'level': level}
        )

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.body_contains_field(field='average_difficulty', expected_value=expected_difficulty)
