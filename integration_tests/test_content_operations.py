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
        children = c.get_child_pages(parent.id)
        assert len(list(children)) == 1

        c.delete_content(child.id, ContentStatus.CURRENT)
    finally:
        c.delete_content(parent.id, ContentStatus.CURRENT)


def test_get_page_content():
    title = 'Full page'
    content = 'This is a full piece of content'
    page = c.create_content(ContentType.PAGE, title, space_key, content=content)
    page = c.get_content_by_id(page.id,
                               expand=['body.storage', 'body.editor', 'body.view', 'body.export_view',
                                       'body.styled_view', 'body.anonymous_export_view'])
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

    c.delete_content(page.id, ContentStatus.CURRENT)


def test_update_page_content():
    # Create test page
    title = 'Full page updated'
    content = 'This is a full piece of content'
    result = c.create_content(ContentType.PAGE, title, space_key, content=content, expand=['body.storage', 'version'])
    assert result.body.storage == content

    # Update test page
    new_content = 'This is updated content'
    new_title = 'Updated title'
    result = c.update_content(result.id, result.type, result.version.number + 1, new_content, new_title)
    assert result.title == new_title
    assert result.body.storage == new_content

    # Read updated page
    result = c.get_content_by_id(result.id, expand=['body.storage'])
    assert result.title == new_title
    assert result.body.storage == new_content

    c.delete_content(result.id, ContentStatus.CURRENT)


def test_get_content_no_results():
    result = list(c.get_content(ContentType.PAGE, space_key=space_key, title='Nothing here'))
    assert len(result) == 0


def test_create_duplicate_page():
    page = c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')

    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Duplicate Page', space_key, '1')

    c.delete_content(page.id, ContentStatus.CURRENT)


def test_create_page_in_nonexistent_space():
    with pytest.raises(ConfluenceError):
        c.create_content(ContentType.PAGE, 'Bad page', 'NONSENSE', 'Test')


def test_get_content_with_bad_content_type():
    with pytest.raises(ValueError):
        c.get_content(ContentType.ATTACHMENT)
