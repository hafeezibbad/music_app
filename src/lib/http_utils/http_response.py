from abc import ABC, abstractmethod
from typing import Optional, Union, Any
import re

import pytest

from .fixtures import STATUS_DATA_UP_RESPONSE


class HttpResponse(ABC):
    status_code: Optional[int]
    body: dict
    raw_body: str
    headers: dict
    body_parsed: bool = False

    HEALTH_CHECK_UP_RESPONSE = STATUS_DATA_UP_RESPONSE

    @abstractmethod
    def _parse_body(self):
        pass

    def status_code_is(self, expected_status_code):
        msg = "HTTP response status code was expected to be {expected}, but is actually {actual}. Response body: {body}"
        if self.status_code != expected_status_code:
            pytest.fail(msg.format(expected=expected_status_code, actual=self.status_code, body=self.body))

    def message_is(self, message: str):
        self._parse_body()
        if self.body['message'] != message:
            msg = "Message was expected to be '{expected}', but is actually '{actual}'"
            pytest.fail(msg.format(expected=message, actual=self.body['message']))

    def body_does_not_contain(self, string: str):
        if string in self.raw_body:
            pytest.fail("Body should NOT contain string '{string}' but it actually does".format(string=string))

    def status_code_is_200_ok(self):
        self.status_code_is(200)

    def status_code_is_201_created(self):
        self.status_code_is(201)

    def status_code_is_204_no_content(self):
        self.status_code_is(204)

    def status_code_is_304_not_modified(self):
        self.status_code_is(304)

    def status_code_is_400_bad_request(self):
        self.status_code_is(400)

    def status_code_is_401_unauthorized(self):
        self.status_code_is(401)

    def status_code_is_403_forbidden(self):
        self.status_code_is(403)

    def status_code_is_404_not_found(self):
        self.status_code_is(404)

    def status_code_is_409_conflict(self):
        self.status_code_is(409)

    def status_code_is_412_precondition_failed(self):
        self.status_code_is(412)

    def status_code_is_500_internal_server_error(self):
        self.status_code_is(500)

    def status_code_is_503_service_unavailable(self):
        self.status_code_is(503)

    def etag_is(self, etag: Union[int, str]):
        assert 'etag' in self.headers
        assert self.headers.get('etag') == str(etag)

    def does_not_have_etag(self):
        assert 'etag' not in self.headers

    def health_check_status_is_up(self):
        self._parse_body()
        if self.body != self.HEALTH_CHECK_UP_RESPONSE:
            pytest.fail('Health check response invalid.')  # TODO: print the response difference here

    def body_contains_field(self, field: str, expected_value: Optional[Any] = None, pattern: Optional[str] = None):
        self._parse_body()
        value_mismatch_err = 'Mismatching value for `{field}` in response. Expected `{expected}`, actual `{actual}`'
        regex_mismatch_err = 'Unexpected value for `{field}` in response. actual `{actual}` does not match regex ' \
                             '`{regex}`'
        missing_field = '`{field}` not found in response body'
        if field in self.body:
            if expected_value and self.body[field] != expected_value:
                pytest.fail(value_mismatch_err.format(field=field, expected=expected_value, actual=self.body[field]))
            if pattern and re.match(pattern, self.body[field]) is None:
                pytest.fail(regex_mismatch_err.format(field=field, actual=self.body[field], regex=pattern))

        else:
            pytest.fail(missing_field.format(field=field))

    def get_field(self, field: str):
        self._parse_body()
        self.body_contains_field(field=field)

        return self.body[field]

    def body_does_not_contain_field(self, field: str):
        self._parse_body()
        value_exists_error = 'Unexpected `{field}` present in response'
        if field in self.body:
            pytest.fail(value_exists_error.format(field=field))

    def contains_request_id(self, expected_req_id: str = None):
        assert 'X-Request-Id' in self.headers
        tx_msg = "Mismatching request ID in response. expected: `{expected}` actual: `{actual}`"
        if expected_req_id and expected_req_id != self.headers["X-Request-Id"]:
            pytest.fail(tx_msg.format(expected=expected_req_id, actual=self.headers["X-Request-Id"]))

    def body_is_empty(self):
        self._parse_body()
        assert len(self.body) == 0
