from confluence.client import Confluence
from confluence.exceptions.generalerror import ConfluenceError
from confluence.exceptions.resourcenotfound import ConfluenceResourceNotFound
from integration_tests.config import local_url, local_admin
import logging
import pytest

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = Confluence(local_url, local_admin)


def test_create_space():
    s = c.create_space('TEST', 'Test space', 'Test space description')
    assert s.key == 'TEST'
    assert s.name == 'Test space'


def test_create_duplicate_space():
    with pytest.raises(ConfluenceError):
        c.create_space('TEST', '')


def test_get_all_spaces():
    spaces = c.get_spaces()
    assert len(list(spaces)) == 2

    spaces = c.get_spaces(space_keys=['TEST'])
    assert len(list(spaces)) == 1


def test_get_space_no_expands():
    s = c.get_space('TEST')
    assert s.name == 'Test space'
    assert s.key == 'TEST'


def test_update_existing_space():
    s = c.update_space('TEST', new_name='Test space updated', new_description='Test space description 2')
    assert s.key == 'TEST'
    assert s.name == 'Test space updated'


def test_delete_space():
    c.delete_space('TEST')


def test_create_space_without_description():
    try:
        s = c.create_space('TNOD', 'Test space without desc')
        assert s.key == 'TNOD'
        assert s.name == 'Test space without desc'
    finally:
        c.delete_space('TNOD')


def test_update_nonexistent_space():
    with pytest.raises(ConfluenceError):
        c.update_space('NONSENSE', '', '')


def test_delete_nonexistent_space():
    with pytest.raises(ConfluenceResourceNotFound):
        c.delete_space('NONSENSE')


def test_create_private_space():
    s = c.create_space('PRIVATE', 'Private space', is_private=True)
    assert s.key == 'PRIVATE'
    assert s.name == 'Private space'

    c.delete_space('PRIVATE')
