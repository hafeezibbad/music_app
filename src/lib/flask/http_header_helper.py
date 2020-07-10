from abc import ABC, abstractmethod
from src.lib.requestid.validator import RequestIdValidator


class HttpHeaderHelper(ABC):
    @abstractmethod
    def get_request_id(self, request_object) -> str:
        pass

    @abstractmethod
    def is_test_request(self, request_object) -> bool:
        pass

    def _get_request_id(self, request_id=None) -> str:
        """HTTP framework agnostic function to get/generate request ID"""
        return RequestIdValidator.generate(request_id)

    def _is_test_request(self, test_request_header) -> bool:
        """HTTP framework agnostic function to define whether current request is test request or not"""
        return test_request_header == '1'


class FlaskHttpHeaderHelper(HttpHeaderHelper):
    """Flask implementation of HTTP header helper functions"""
    def get_request_id(self, request_object) -> str:
        request_id = request_object.headers.get('X-Request-Id')
        return self._get_request_id(request_id)

    def is_test_request(self, request_object) -> bool:
        test_request_header = request_object.headers.get('X-Test-Request')
        return self._is_test_request(test_request_header)
