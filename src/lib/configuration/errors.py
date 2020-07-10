from src.lib.errors.exceptions import GenericError


class ConfigurationErrorType:
    # internal error code, HTTP status code, log event name
    FILE_NOT_FOUND = (1, 500, 'CONFIG_FILE_NOT_FOUND')
    BAD_CONFIG_FILE = (2, 500, 'BAD_CONFIGURATION_FILE')
    INVALID_CONFIG = (3, 500, 'INVALID_CONFIGURATION_FILE')
    BAD_FILE_PERMISSIONS = (4, 500, 'BAD_FILE_PERMISSIONS')
    CONFIG_PARSING_ERROR = (5, 500, 'CONFIG_PARSING_ERROR')
    EMPTY_CONFIG_FILE = (6, 500, 'EMPTY_CONFIG_FILE')
    INVALID_FILE_PATH = (7, 404, 'INVALID_FILE_PATH')
    INVALID_FILE_TYPE = (8, 400, 'INVALID_FILE_TYPE')
    UNSUPPORTED_FILE_TYPE = (9, 500, 'UNSUPPORTED_FILE_TYPE')


class ConfigurationError(GenericError):
    pass
