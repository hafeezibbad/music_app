import logging
from typing import Optional

from flask import request
import structlog
from structlog.stdlib import filter_by_level

from src.lib.logging.helpers import logprocessor_add_timestamp

LOGGING = structlog.get_logger(__name__)


def log_request(
        log_message: str = '',
        log_data: bool = False,
        request_data: Optional[dict] = None,
        request_args: Optional[dict] = None
):
    if request_data is None:
        request_data = request.get_data()

    if log_data is False:
        request_data = None

    LOGGING.info(
        'HTTP_REQUEST',
        message=log_message,
        request_method=request.method,
        request_path=request.path,
        request_data=request_data,
        request_args=request_args
    )


def setup_logging():
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    logging.basicConfig(
        format="%(message)s", level=logging.INFO
    )

    # Default log processors for structlog
    struct_log_processors = [
        filter_by_level,
        logprocessor_add_timestamp,
        structlog.processors.JSONRenderer()
    ]
    structlog.configure(
        processors=struct_log_processors,
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )


def get_flask_details_for_log():
    data = {}
    if "HTTP_USER_AGENT" in request.environ:
        data['user_agent'] = request.environ['HTTP_USER_AGENT']

    if 'context' in request.environ:
        context = request.environ['context']
        aws_details = {
            'function_name': context.function_name,
            'function_version': context.function_version,
            'invoked_function_arn': context.invoked_function_arn,
            'request_id': context.aws_request_id
        }
        data['aws_details'] = aws_details
    return data
