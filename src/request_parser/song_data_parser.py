from pydantic import ValidationError

from src.music_app.models import Song
from src.request_parser.data_parser import RequestDataParser


class SongRequestDataParser(RequestDataParser):
    def __init__(self, request_data: dict) -> None:
        super(SongRequestDataParser, self).__init__(request_data)
        self.__validate(data=request_data)

    def get_model(self) -> Song:
        return self.model

    def __validate(self, data: dict):
        try:
            self.model = Song(**data)

        except ValidationError as ex:
            self.api_error = self._handle_pydantic_validation_error(ex)
