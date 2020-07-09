import pytest


def function_was_called_once(function):
    if function.call_count != 1:
        error_msg = 'Function should have been called once, but was actually called {times}'
        pytest.fail(error_msg.format(times=function.call_count))
