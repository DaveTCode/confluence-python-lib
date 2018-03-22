from confluence.exceptions.generalerror import ConfluenceError
from confluence.models.content import ContentType, ContentStatus
from integration_tests.config import get_confluence_instance
import logging
import pytest

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'PSA'


def setup_module():
    c.create_space(space_key, 'Page Space')


def teardown_module():
    c.delete_space(space_key)


def test_create_orphaned_page():
    page = c.create_content(ContentType.PAGE, 'Test orphaned page', space_key, '<h1>Test</h1>')
    assert page.title == 'Test orphaned page'

    c.delete_content(page.id, ContentStatus.CURRENT)


def test_create_page_with_ancestor():
    parent = c.create_content(ContentType.PAGE, 'Parent page', space_key, 'Parent')

    try:
        child = c.create_content(ContentType.PAGE, 'Child page', space_key, 'Child', parent_content_id=parent.id)
        assert child.title == 'Child page'
        c.delete_content(child.id, ContentStatus.CURRENT)
    finally:
        c.delete_content(parent.id, ContentStatus.CURRENT)


def test_create_duplicate_page():
    c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')

    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')


def test_create_page_in_nonexistent_space():
    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Bad page', 'NONSENSE', 'Test')
