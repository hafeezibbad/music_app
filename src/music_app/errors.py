from src.music_app.models import ApiError


class MusicAppErrorType:
    # internal error code, HTTP status code, log event name
    NO_ERROR = (0, 200, 'OK')
    INTERNAL_SERVER_ERROR = (1, 500, 'INTERNAL_SERVER_ERROR')
    SONG_NOT_FOUND = (2, 404, 'SONG_NOT_FOUND')
    SONG_ALREADY_EXISTS = (3, 409, 'SONG_ALREADY_EXISTS')
    SONG_DATA_INVALID = (4, 400, 'INVALID_SONG_DATA')
    SERVICE_UNAVAILABLE_ERROR = (5, 503, 'SERVICE_UNAVAILABLE_ERROR')
    REQUEST_BODY_EMPTY = (6, 400, 'REQUEST_BODY_EMPTY')
    REQUEST_BODY_INVALID_JSON = (7, 400, 'REQUEST_BODY_INVALID_JSON')
    DATA_RETRIEVAL_FAILED = (8, 503, 'DATA_RETRIEVAL_FAILED')
    INVALID_REQUEST_DATA = (9, 400, 'INVALID_REQUEST_DATA')
    UPDATE_FAILED_VERSION_MISMATCH = (10, 412, 'UPDATE_FAILED_MISMATCH_VERSION')
    DB_PERSISTENCE_ERROR = (11, 503, 'DB_PERSISTENCE_ERROR')
    READ_FAILED_VERSION_MISMATCH = (12, 412, 'READ_FAILED_MISMATCH_VERSION')


class MusicAppError(Exception):
    code = None
    http_status = None
    event_name = None

    def __init__(self, code):
        self.code, self.http_status, self.event_name = code


class MusicAppSimpleError(MusicAppError):
    """For simple errors where message and status code is enough"""
    message = None

    def __init__(self, code, message):
        super(MusicAppSimpleError, self).__init__(code)
        self.message = message


class MusicAppApiError(MusicAppError):
    """For more complex API errors raised from validation failures"""
    api_error = None

    def __init__(self, code, api_error: ApiError):
        super(MusicAppApiError, self).__init__(code)
        self.api_error = api_error
