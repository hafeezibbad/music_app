from datetime import datetime, date
import json
from time import time
import random

from bson import ObjectId

DEFAULT_DATETIME_REGEX = '%B %d %Y - %H:%M:%S'


def generate_random_date(date_format: str = '%Y-%M-%D') -> str:
    """
    This function generates a random date between epoch time and current time.
    :param date_format: Format for date expression returned.
    :type date_format: str
    :return random_date: Random date
    :rtype: str
    """

    return datetime.fromtimestamp(random.randrange(int(time()))).strftime(date_format)


class CustomJSONEncoder(json.JSONEncoder):
    # pylint: disable=E0012,E0202,W0221
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
