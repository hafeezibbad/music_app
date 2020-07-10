from abc import ABC, abstractmethod
from typing import Optional, Callable, Dict, Type, Any

from urllib.parse import urljoin

# pylint: disable=no-name-in-module, C0326
from pydantic import constr
from typing_extensions import Literal

from src.lib.http_utils.http_response import HttpResponse
from src.lib.requestid.validator import REQUEST_ID_PATTERN


class ApiRequest(ABC):
    headers: Dict[str, str]

    @abstractmethod
    def make_request(
            self,
            method: Literal['POST', 'GET', 'PUT', 'DELETE', 'PATCH'],
            path: str,
            json: Optional[dict],
            data: Optional[dict],
            user_agent: str,
            if_match_header: str,
            if_none_match_header: str,
            params: Optional[Dict[str, Any]]
    ):
        raise NotImplementedError('Implementation needed')

    def update_headers(
            self,
            request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
            additional_headers: Optional[Dict[str, str]] = None,
            if_match_header: Optional[str] = None,
            if_none_match_header: Optional[str] = None,
            user_agent: Optional[str] = None
    ) -> Dict[str, str]:
        if not self.headers:
            self.headers = {'Content-Type': 'application/json'}

        if request_id:
            self.headers['X-Request-Id'] = request_id

        if additional_headers is not None:
            for header_name, header_value in additional_headers.items():
                self.headers[header_name] = header_value

        if if_match_header is not None:
            self.headers['If-Match'] = str(if_match_header)

        if if_none_match_header is not None:
            self.headers['If-None-Match'] = str(if_none_match_header)

        if user_agent is not None:
            self.headers['User-Agent'] = user_agent

        return self.headers


class E2EApiRequest(ApiRequest):
    def __init__(
            self,
            base_url: str,
            request_handler: Type[Callable] = None,
            expected_response: Type[HttpResponse] = None,
            request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
            additional_headers: Optional[Dict[str, str]] = None,
            user_agent: Optional[str] = None
    ):
        assert request_handler is not None
        assert expected_response is not None
        self.base_url = base_url
        self.request_handler = request_handler
        self.expected_response = expected_response
        self.headers = dict()

        self.update_headers(
            request_id=request_id,
            additional_headers=additional_headers,
            user_agent=user_agent
        )

    def make_request(
            self,
            method: Literal['POST', 'GET', 'PUT', 'DELETE', 'PATCH'],
            path: str,
            json: Optional[dict] = None,
            data: Optional[dict] = None,
            user_agent: str = None,
            if_match_header: str = None,
            if_none_match_header: str = None,
            params: Optional[Dict[str, Any]] = None
    ):
        full_url = urljoin(self.base_url, path)
        self.update_headers(
            user_agent=user_agent,
            if_match_header=if_match_header,
            if_none_match_header=if_none_match_header
        )
        response_dict = self.request_handler(
            url=full_url,
            method=method,
            headers=self.headers,
            body=json,
            params=params
        )

        return self.expected_response(response_dict)
