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


def test_get_page_content():
    title = 'Full page'
    content = 'This is a full piece of content'
    c.create_content(ContentType.PAGE, title, space_key, content=content)
    result = c.get_content(ContentType.PAGE, space_key=space_key, title=title,
                           expand=['body.storage', 'body.editor', 'body.view', 'body.export_view', 'body.styled_view',
                                   'body.anonymous_export_view'])
    page = list(result)[0]  # TODO - Replace with call to get content by ID when implemented
    assert page.body.anonymous_export_view == content
    assert hasattr(page.body, 'anonymous_export_view_representation')
    assert page.body.editor == content
    assert hasattr(page.body, 'editor_representation')
    assert page.body.export_view == content
    assert hasattr(page.body, 'export_view_representation')
    assert page.body.storage == content
    assert hasattr(page.body, 'storage_representation')
    assert content in page.body.styled_view
    assert hasattr(page.body, 'styled_view_representation')
    assert page.body.view == content
    assert hasattr(page.body, 'view_representation')


def test_create_duplicate_page():
    c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')

    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')


def test_create_page_in_nonexistent_space():
    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Bad page', 'NONSENSE', 'Test')
