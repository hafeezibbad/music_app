import pytest


class ApiErrorAssertions:
    def __init__(self, api_error_dict: dict):
        self.api_error_dict = api_error_dict

    def error_count_is(self, count: int):
        actual_count = len(self.api_error_dict['errors'])
        if actual_count != count:
            error_msg = 'Validation error count should have been {expected}, but is actually {actual}'
            pytest.fail(error_msg.format(expected=count, actual=actual_count))

    def has_validation_error_with_title_and_detail(self, title: str, detail: str):
        for error in self.api_error_dict['errors']:
            if error['title'] == title and error['detail'] == detail:
                return

        error_msg = 'Could not find error with following title: {title} and detail: {detail}'
        pytest.fail(error_msg.format(title=title, detail=detail))

    def has_validation_error_with_title(self, title: str):
        for error in self.api_error_dict['errors']:
            if error['title'] == title:
                return

        error_msg = 'Could not find error with following title: {title}'
        pytest.fail(error_msg.format(title=title))
