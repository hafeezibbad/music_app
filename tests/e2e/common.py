import json
import os
import copy
from typing import List
from urllib.parse import urljoin
import pytest

# pylint: disable=no-name-in-module, C0326
from pydantic import constr

from src.lib.configuration.validate import URL_REGEX
from src.lib.http_utils.request_utils import handle_api_request
from src.lib.requestid.utils import generate_request_id
from src.lib.requestid.validator import RequestIdValidator
from src.music_app.models import SongDbRecord
from tests.fixtures.common import TEST_USER_AGENT
from tests.fixtures.songs_data import TEST_SONG_DATA, TEST_DATASET_SONGS, TEST_SONG_DATA_WITHOUT_RATING

ENDPOINT_BASE_URL = os.environ["ENDPOINT_BASE_URL"]


@pytest.fixture
def fixture_request_id():
    return generate_request_id()


@pytest.fixture()
def fixture_temporary_song_record() -> int:
    temp_song_id = create_test_song_in_db(song_data=TEST_SONG_DATA).song_id
    yield temp_song_id
    delete_test_song_from_db(song_id=temp_song_id)


@pytest.fixture()
def fixture_temporary_song_record_without_rating() -> int:
    temp_song_id = create_test_song_in_db(song_data=TEST_SONG_DATA_WITHOUT_RATING).song_id
    yield temp_song_id
    delete_test_song_from_db(song_id=temp_song_id)


@pytest.fixture()
def fixture_populate_db() -> int:
    song_ids = populate_db_with_dataset()
    yield song_ids
    delete_multiple_records(song_ids=song_ids)


def invalidate_song_data(song_data: dict, invalid_field_names: List[str], invalid_values: List[str]) -> dict:
    invalid_song_data = copy.deepcopy(song_data)
    for i, _ in enumerate(invalid_field_names):
        invalid_song_data[invalid_field_names[i]] = invalid_values[i]

    return invalid_song_data


def create_test_song_in_db(
        song_data: dict = None,
        endpoint_base_url: constr(regex=URL_REGEX) = ENDPOINT_BASE_URL,
        path: str = '/api/v1/songs/'
):
    if song_data is None:
        song_data = TEST_SONG_DATA

    response = handle_api_request(
        method="POST",
        url=urljoin(endpoint_base_url, path),
        headers={
            "Content-Type": "application/json",
            "User-Agent": TEST_USER_AGENT,
            "X-Request-Id": RequestIdValidator.generate()
        },
        body=song_data
    )

    song_record_data = json.loads(response['body'])

    return SongDbRecord(**song_record_data)


def delete_test_song_from_db(
        song_id: int,
        endpoint_base_url: constr(regex=URL_REGEX) = ENDPOINT_BASE_URL,
        path: str = '/api/v1/songs/{song_id}'
):
    path = path.format(song_id=song_id)
    response = handle_api_request(
        method='DELETE',
        url=urljoin(endpoint_base_url, path),
        headers={
            "Content-Type": "application/json",
            "User-Agent": TEST_USER_AGENT,
            "X-Request-Id": RequestIdValidator.generate()
        }
    )

    assert response['statusCode'] == 204


def populate_db_with_dataset(
        endpoint_base_url: constr(regex=URL_REGEX) = ENDPOINT_BASE_URL,
        path: str = '/api/v1/songs/uploads'
) -> List[int]:

    response = handle_api_request(
        method="POST",
        url=urljoin(endpoint_base_url, path),
        headers={
            "Content-Type": "application/json",
            "User-Agent": TEST_USER_AGENT,
            "X-Request-Id": RequestIdValidator.generate()
        },
        body={'songs': TEST_DATASET_SONGS}
    )

    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    return body['new_song_ids'] + body['existing_song_ids']


def delete_multiple_records(song_ids: List[int]):
    for song_id in song_ids:
        delete_test_song_from_db(song_id=song_id)
