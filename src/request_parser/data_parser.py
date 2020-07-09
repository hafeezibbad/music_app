import json
from abc import ABC, abstractmethod
from typing import Type

from pydantic import ValidationError

from src.music_app.models import ApiError, Model


class RequestDataParserABC(ABC):
    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def get_api_error(self) -> ApiError:
        pass

    @abstractmethod
    def get_model(self) -> Type[Model]:
        pass


class RequestDataParser(RequestDataParserABC):
    def __init__(self, request_data: dict) -> None:
        self.errors = []
        self.model = None
        self.api_error = None
        self.request_data = request_data

    def get_api_error(self) -> ApiError:
        return self.api_error

    def is_valid(self):
        return not self.errors

    def get_model(self) -> Type[Model]:
        raise NotImplementedError

    def _handle_pydantic_validation_error(self, validation_error: ValidationError):
        errors = []
        errors_dict = json.loads(validation_error.json())
        for error in errors_dict:
            status = 400  # Data validation failure: 400 Bad Request
            field_name = error['loc'][0]
            error_title = 'Input validation failed'
            error_detail = 'Invalid data for {field_name}'.format(field_name=field_name)
            api_error_dict = {
                'status': status,
                'source': {
                    'pointer': field_name
                },
                'title': error_title,
                'detail': error_detail
            }

            errors.append(api_error_dict)
        self.errors = errors

        return ApiError(**{'errors': errors})
