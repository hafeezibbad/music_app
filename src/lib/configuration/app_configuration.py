from typing import Optional

from pydantic import conint, constr, Extra  # pylint: disable=no-name-in-module
from typing_extensions import Literal

from src.lib.configuration.validate import StrictNonEmptyStr, URL_REGEX
from src.music_app.models import Model


class AppConfiguration(Model):
    DbName: StrictNonEmptyStr
    DbHost: StrictNonEmptyStr
    DbPort: conint(gt=0)
    ItemsPerPage: conint(gt=0)
    DbUsername: Optional[StrictNonEmptyStr]
    DbPassword: Optional[StrictNonEmptyStr]
    Stage: Literal["dev", "test"]
    EndpointBaseUrl: constr(regex=URL_REGEX)
    MailUsername: str = ''
    MailPassword: str = ''
    ServerPort: conint(ge=1024, le=65535)
    Debug: bool = False

    class Config:
        extra = Extra.allow     # allow extra fields (not specific in schema) in configuration object.
