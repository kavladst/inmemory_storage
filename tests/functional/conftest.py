from telnetlib import Telnet
from typing import Callable

import pytest

from settings import CLIENT_HOST, CLIENT_PORT


@pytest.fixture(scope='session')
def setup_user_connection() -> Telnet:
    telnet = Telnet(CLIENT_HOST, CLIENT_PORT)
    telnet.write(b'REGISTER test_user test_password')
    assert telnet.read_until(b'\n') == b'OK\n'
    yield telnet
    telnet.close()


@pytest.fixture(scope='function')
def get_response(setup_user_connection: Telnet) -> Callable[[str], str]:
    def _get_response(query: str) -> str:
        setup_user_connection.write(query.encode())
        response = setup_user_connection.read_until(b'\n').decode()
        if response[-1] == '\n':
            response = response[:-1]
        return response
    return _get_response
