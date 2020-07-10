RELEASE_DATE_REGEX = r"^[\d]{4}-[\d]{2}-[\d]{2}$"
RELEASE_DATE_FORMAT = "%Y-%m-%d"
HASH_REGEX = r"^[a-f0-9]{32,128}"
URL_REGEX = r"https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"


class StrictNonEmptyStr(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise ValueError('Strict string: str expected, {} provided'.format(type(value)))

        if not value.strip():
            raise ValueError('Strict string: empty string provided')

        return value
