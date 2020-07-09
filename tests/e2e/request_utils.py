from typing import Optional, Dict, Any

# pylint: disable=no-name-in-module, C0326
from pydantic import constr

from src.lib.http_utils.api_request import E2EApiRequest
from src.lib.http_utils.request_utils import handle_api_request
from src.lib.requestid.validator import REQUEST_ID_PATTERN
from tests.e2e.common import ENDPOINT_BASE_URL
from tests.e2e.e2e_response import E2EServiceResponse
from tests.fixtures.common import TEST_USER_AGENT
from tests.fixtures.songs_data import TEST_SONG_DATA, DEFAULT_INITIAL_VERSION


def get_service_status_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT
):
    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/status'
    )


def create_song_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        song_data: Optional[dict] = None
):
    if song_data is None:
        song_data = TEST_SONG_DATA

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='POST',
        path='/api/v1/songs/',
        json=song_data
    )


def get_song_request(
        song_id: int,
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        if_match_header: Optional[str] = DEFAULT_INITIAL_VERSION,
        if_none_match_header: Optional[str] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/v1/songs/{}'.format(song_id),
        if_match_header=if_match_header,
        if_none_match_header=if_none_match_header
    )


def get_average_song_rating_request(
        song_id: int,
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        if_match_header: Optional[str] = DEFAULT_INITIAL_VERSION,
        if_none_match_header: Optional[str] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/v1/songs/avg/rating/{}'.format(song_id),
        if_match_header=if_match_header,
        if_none_match_header=if_none_match_header
    )


def get_average_difficulty_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        params: Optional[Dict[str, Any]] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/v1/songs/avg/difficulty',
        params=params
    )


def songs_search_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        params: Optional[Dict[str, Any]] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/v1/songs/search',
        params=params
    )


def get_all_songs_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        params: Optional[Dict[str, Any]] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='GET',
        path='/api/v1/songs',
        params=params
    )


def post_song_rating_request(
        base_url: str = ENDPOINT_BASE_URL,
        request_id: Optional[constr(regex=REQUEST_ID_PATTERN)] = None,
        user_agent: Optional[str] = TEST_USER_AGENT,
        params: Optional[Dict[str, Any]] = None
):

    requester = E2EApiRequest(
        base_url=base_url,
        user_agent=user_agent,
        request_handler=handle_api_request,
        expected_response=E2EServiceResponse,
        request_id=request_id
    )

    return requester.make_request(
        method='POST',
        path='/api/v1/songs/rating',
        params=params
    )
