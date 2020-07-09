from flask import Blueprint, request

from src.lib.errors.exceptions import handle_and_log_service_exception, handle_and_log_unknown_exception
from src.lib.response.utils import create_response_and_log
from src.music_app.errors import MusicAppError
from src.music_app.models import Status
from src.routes.common import create_music_app_manager

# pylint: disable=invalid-name
status_api = Blueprint('status', __name__)
STATUS_API_PREFIX = '/api'


@status_api.route('/status', methods=['GET'])
def get_status():
    try:
        manager = create_music_app_manager(incoming_request=request)
        status: Status = manager.status()

        return create_response_and_log(
            log_message=status.message,
            message=status.message,
            log_data=True,
            data=status.get_status_data(),
            status_code=status.statusCode
        )

    except MusicAppError as ex:
        return handle_and_log_service_exception(ex, service_name='MusicApp', message='Status failed')

    except BaseException as ex:
        return handle_and_log_unknown_exception(ex, message='Unknown exception')
