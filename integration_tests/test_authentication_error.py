import pytest

from confluence.client import Confluence
from confluence.exceptions.authenticationerror import ConfluenceAuthenticationError
from integration_tests.config import local_url


def test_bad_username_password():  # type: () -> None
    c = Confluence(local_url, ('bad', 'bad'))
    with pytest.raises(ConfluenceAuthenticationError):
        c.create_space('OK', 'ok')
