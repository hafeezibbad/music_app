from pydantic import constr  # pylint: disable=no-name-in-module

from src.lib.requestid.validator import RequestIdValidator, REQUEST_ID_PATTERN


def generate_request_id() -> constr(regex=REQUEST_ID_PATTERN, min_length=35, max_length=35):
    request_id = RequestIdValidator.generate()
    request_msg = "Generated request_id: {request_id}"
    print(request_msg.format(request_id=request_id))
    return request_id
