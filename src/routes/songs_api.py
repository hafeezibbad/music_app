import json
import os

from flask import Blueprint, request
from src.lib.configuration.utils import load_configuration_from_yaml_file
from src.lib.errors.exceptions import handle_and_log_service_exception, handle_and_log_unknown_exception

from src.lib.logging.utils import log_request
from src.lib.response.utils import create_response_and_log, create_response
from src.music_app.errors import MusicAppError
from src.music_app.manager import MusicAppManager
from src.music_app.models import SongDbRecord


# pylint: disable=invalid-name
from src.routes.common import create_music_app_manager

songs_api = Blueprint('songs', __name__)
SONGS_API_PREFIX = '/api/v1/songs/'
app_config = load_configuration_from_yaml_file(os.environ['APP_CONFIG_FILE'])


@songs_api.route('/uploads', methods=['POST'])
def batch_upload():
    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        request_data: dict = manager.parse_request_data_as_json(request.get_data())
        log_request(log_message='Request started to batch upload songs data', log_data=True, request_data=request_data)

        created_ids, existing_ids = manager.batch_create_songs(request_data=request_data)

        return create_response_and_log(
            log_message='Batch create song successful',
            status_code=201,
            data=dict(
                newly_created_songs=len(created_ids),
                new_song_ids=created_ids,
                existing_song_ids=existing_ids
            ),
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song rating retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/uploadfile', methods=['POST'])
def batch_upload_file():
    try:
        f = request.files['file']
        request_data = {'songs': []}
        for line in f.readlines():
            request_data['songs'].append(json.loads(line.decode('utf-8').strip()))
        f.close()

        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Request started to batch upload songs data', log_data=True, request_data=request_data)

        created_ids, existing_ids = manager.batch_create_songs(request_data=request_data)

        return create_response_and_log(
            log_message='Batch create song successful',
            status_code=201,
            data=dict(
                newly_created_songs=len(created_ids),
                new_song_ids=created_ids,
                existing_song_ids=existing_ids
            ),
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song rating retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/avg/difficulty', methods=['GET'])
def get_average_song_difficulty():
    # FIXME: This will break if there are too many songs
    try:
        level = int(request.args.get('level', -1))
    except ValueError:
        return create_response(
            message='Invalid parameter value for `rating`, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Request started to get average difficulty', log_data=True, request_args=request.args)

        difficulty: float = manager.get_average_difficulty(level=level)

        # TODO: Average difficulty will be zero if there are no records found
        return create_response_and_log(
            log_message='Average difficulty retrieved successfully',
            status_code=200,
            data=dict(average_difficulty=round(difficulty, 1)),
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song rating retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/search', methods=['GET'])
def search_songs_with_title_and_artist():
    try:
        start = int(request.args.get('nextId', 0))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return create_response(
            message='Invalid parameter value, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        search_text: str = request.args.get('message', '')
        log_request(
            log_message='Request started to search songs using text `{}`'.format(search_text),
            log_data=True,
            request_args=request.args
        )

        songs, anchor = manager.search_songs(search_text=search_text, start=start, page_size=page_size)

        data = dict()
        if songs:
            data['songs'] = [vars(song) for song in songs]
        if anchor:
            data['links'] = dict(next_anchor=anchor)

        return create_response_and_log(
            log_message='Song record retrieved successfully',
            status_code=200,
            data=data,
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Songs retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/avg/rating/<int:song_id>', methods=['GET'])
def get_average_rating_for_song(song_id: int):
    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Request started to retrieve song rating', log_data=True)

        rating_stats: dict = manager.get_average_rating(song_id=song_id)

        return create_response_and_log(
            log_message='Song rating retrieved successfully',
            status_code=200,
            data=rating_stats,
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song rating retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/rating', methods=['POST'])
def add_song_rating():
    try:
        rating = int(request.args.get('rating'))
        song_id = int(request.args.get('song_id'))
    except ValueError:
        return create_response(
            message='Invalid parameter value, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Request started to update song rating', log_data=True, request_args=request.args)

        song: SongDbRecord = manager.update_song(song_id=song_id, request_data={'rating': rating})
        extra_headers = {'etag': song.version}

        return create_response_and_log(
            log_message='Song record updated successfully',
            status_code=200,
            data=vars(song),
            log_data=True,
            extra_headers=extra_headers
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song update failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('', methods=['GET'])
def get_all_songs_paginated():
    try:
        start = int(request.args.get('nextId', 0))
        page_size = int(request.args.get('pageSize', 20))

    except ValueError:
        return create_response(
            message='Invalid parameter value, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Request started to retrieve all songs', log_data=True, request_args=request.args)

        songs, anchor = manager.get_all_songs(start=start, page_size=page_size)

        data = dict()
        if songs:
            data['songs'] = [vars(song) for song in songs]
        if anchor:
            data['links'] = dict(next_anchor=anchor)

        return create_response_and_log(
            log_message='Song record retrieved successfully',
            status_code=200,
            data=data,
            log_data=True
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Songs retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/', methods=['POST'])
def create_song_record():
    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        request_data: dict = manager.parse_request_data_as_json(request.get_data())
        log_request(log_message='Song record creation request started', log_data=True, request_data=request_data)

        new_song: SongDbRecord = manager.create_song(request_data=request_data)
        extra_headers = {'etag': new_song.version}

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song creation failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')

    return create_response_and_log(
        log_message='Song record created successfully',
        status_code=201,
        data=vars(new_song),
        log_data=True,
        extra_headers=extra_headers
    )


@songs_api.route('/<int:song_id>', methods=['GET'])
def get_song_record(song_id: int):
    version = None
    try:
        if request.headers.get('if-none-match') is not None:
            version = int(request.headers.get('if-none-match'))

    except ValueError:
        return create_response(
            message='Invalid value for If-None-Match header, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Song record creation request started', log_data=True)

        song: SongDbRecord = manager.get_song(song_id=song_id, version=version)
        extra_headers = {'etag': song.version}

        if version is not None and version == song.version:
            return create_response(message='Not Modified', status_code=304, extra_headers=extra_headers)

        return create_response_and_log(
            log_message='Song record retrieved successfully',
            status_code=200,
            data=vars(song),
            log_data=True,
            extra_headers=extra_headers
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song retrieval failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/<int:song_id>', methods=['PATCH'])
def update_song_record(song_id: int):
    version = None
    try:
        if request.headers.get('if-none-match') is not None:
            version = int(request.headers.get('if-none-match'))

    except ValueError:
        return create_response(
            message='Invalid value for If-None-Match header, <int> expected',
            status_code=400
        )

    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        request_data: dict = manager.parse_request_data_as_json(request.get_data())
        log_request(log_message='Song record update request started', log_data=True, request_data=request_data)

        updated_song: SongDbRecord = manager.update_song(song_id=song_id, request_data=request_data, version=version)
        extra_headers = {'etag': updated_song.version}

        return create_response_and_log(
            log_message='Song record retrieved successfully',
            status_code=200,
            data=vars(updated_song),
            log_data=True,
            extra_headers=extra_headers
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song update failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')


@songs_api.route('/<int:song_id>', methods=['DELETE'])
def delete_song_record(song_id: int):
    # TODO: Requires version support
    # TODO: Additional authorization
    try:
        manager: MusicAppManager = create_music_app_manager(incoming_request=request)
        log_request(log_message='Song record delete request started', log_data=True)

        _ = manager.delete_song(song_id=song_id)

        return create_response_and_log(
            log_message='Song deleted successfully',
            status_code=204
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Song deletion failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')
