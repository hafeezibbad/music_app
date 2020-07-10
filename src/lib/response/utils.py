import json

from flask import request, Response

from src.lib.helpers import CustomJSONEncoder
from src.lib.logging.utils import LOGGING


def create_response(message=None, status_code=200, data=None, extra_headers: dict = None):
    data = data or dict()
    if message:
        data['message'] = message

    js = json.dumps(data, cls=CustomJSONEncoder)

    response = Response(
        js,
        status=status_code,
        mimetype='application/json'
    )
    if extra_headers:
        for k, v in extra_headers.items():
            response.headers[k] = v

    return response


def create_response_and_log(
        log_message,
        message=None,
        status_code=200,
        data=None,
        log_data=False,
        extra_headers: dict = None
):
    data = data or dict()
    response_data = None

    if log_data is True:
        response_data = data

    LOGGING.info(
        'HTTP_RESPONSE',
        message=log_message,
        request_method=request.method,
        request_path=request.path,
        response_status_code=status_code,
        response_data=response_data,
        response_extra_headers=extra_headers
    )

    return create_response(message=message, status_code=status_code, data=data, extra_headers=extra_headers)
