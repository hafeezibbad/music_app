import re
import uuid


REQUEST_ID_PATTERN = r'0000-[a-f0-9]{32}'


class RequestIdValidator:
    @staticmethod
    def generate(request_id=None) -> str:
        """
        Validates and returns request ID if one was given.
        If no request ID or invalid one was given, generates new.
        """
        if request_id:
            if RequestIdValidator.validate(request_id) is False:
                request_id = None

        if not request_id:
            request_id = "0000-{}".format(str(uuid.uuid4()).replace('-', '')[:32])

        return request_id

    @staticmethod
    def validate(request_id: str) -> bool:
        if re.compile('^0000-[a-z0-9]{32}(-[A-Za-z0-9]+)*$').match(request_id):
            return True

        return False
