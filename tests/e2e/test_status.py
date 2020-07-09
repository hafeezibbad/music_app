from tests.e2e.common import fixture_request_id  # pylint: disable=unused-import
from tests.e2e.request_utils import get_service_status_request


# pylint: disable=redefined-outer-name
class TestStatus:
    def test_service_status_is_ok(self, fixture_request_id):
        response = get_service_status_request(request_id=fixture_request_id)

        response.status_code_is_200_ok()
        response.contains_request_id(fixture_request_id)
        response.health_check_status_is_up()
