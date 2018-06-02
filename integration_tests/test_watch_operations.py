import logging

import pytest

from confluence.exceptions.resourcenotfound import ConfluenceResourceNotFound
from confluence.models.content import ContentType, ContentStatus
from integration_tests.config import get_confluence_instance

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'WOS'


def setup_module():
    c.create_space(space_key, 'Watch Space')


def teardown_module():
    c.delete_space(space_key)


def test_user_not_watching_content():
    page = c.create_content(ContentType.PAGE, space_key=space_key, title='Test', content='Test')
    try:
        c.remove_content_watch(page.id)  # Remove the watch because we created the content so it's watched by default!
        assert not c.is_user_watching_content(page.id)
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)


def test_user_watching_content():
    page = c.create_content(ContentType.PAGE, space_key=space_key, title='Test', content='Test')
    try:
        c.add_content_watch(page.id)
        assert c.is_user_watching_content(page.id)
        c.remove_content_watch(page.id)
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)


def test_user_is_watching_content_by_username():
    page = c.create_content(ContentType.PAGE, space_key=space_key, title='Test', content='Test')
    try:
        c.add_content_watch(page.id, username='admin')
        assert c.is_user_watching_content(page.id, username='admin')
        c.remove_content_watch(page.id, username='admin')
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)


def test_user_is_watching_content_by_key():
    page = c.create_content(ContentType.PAGE, space_key=space_key, title='Test', content='Test')
    try:
        user = c.get_user(username='admin')
        c.add_content_watch(page.id, user_key=user.user_key)
        assert c.is_user_watching_content(page.id, user_key=user.user_key)
        c.remove_content_watch(page.id, user_key=user.user_key)
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)


def test_bad_user_of_content_watch_functions():
    with pytest.raises(ValueError):
        c.add_content_watch(1, "a", "a")
    with pytest.raises(ValueError):
        c.is_user_watching_content(1, "a", "a")
    with pytest.raises(ValueError):
        c.remove_content_watch(1, "a", "a")


def test_user_not_watching_space():
    assert not c.is_user_watching_space(space_key, username='admin')


def test_user_is_watching_space():
    c.add_space_watch(space_key, username='admin')
    assert c.is_user_watching_space(space_key, username='admin')
    c.remove_space_watch(space_key, username='admin')


def test_user_is_watching_space_by_key():
    user = c.get_user(username='admin')
    c.add_space_watch(space_key, user_key=user.user_key)
    assert c.is_user_watching_space(space_key, user_key=user.user_key)
    c.remove_space_watch(space_key, user_key=user.user_key)


def test_remove_space_watch_without_one():
    c.remove_space_watch(space_key, username='admin')
    assert True


def test_current_user_watching_space():
    c.add_space_watch(space_key)
    assert c.is_user_watching_space(space_key)
    c.remove_space_watch(space_key)


def test_watching_non_existent_space():
    with pytest.raises(ConfluenceResourceNotFound):
        c.add_space_watch("NONSENSE")
    with pytest.raises(ConfluenceResourceNotFound):
        c.is_user_watching_space("NONSENSE")
    with pytest.raises(ConfluenceResourceNotFound):
        c.remove_space_watch("NONSENSE")


def test_bad_user_of_space_watch_functions():
    with pytest.raises(ValueError):
        c.add_space_watch(space_key, "a", "a")
    with pytest.raises(ValueError):
        c.is_user_watching_space(space_key, "a", "a")
    with pytest.raises(ValueError):
        c.remove_space_watch(space_key, "a", "a")
