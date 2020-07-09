from typing import Optional


class DbError(RuntimeError):
    def __init__(self, message: Optional[str] = None):
        self.message = message


class RecordNotFound(DbError):
    pass


class RecordAlreadyExists(DbError):
    def __init__(self, message: Optional[str] = None, existing_record_id: Optional[int] = None):
        super(RecordAlreadyExists, self).__init__(message=message)
        self.existing_record_id = existing_record_id


class PreconditionFailed(DbError):
    pass


class SchemaValidationError(DbError):
    pass


class InvalidDataError(DbError):
    pass


class DbGenericError(DbError):
    pass
