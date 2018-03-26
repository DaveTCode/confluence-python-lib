from confluence.exceptions.generalerror import ConfluenceError
from confluence.exceptions.resourcenotfound import ConfluenceResourceNotFound
from confluence.models.content import ContentType, ContentStatus
from integration_tests.config import get_confluence_instance
import logging
import pytest

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'CPS'
page_id = 0  # type: int


def setup_module():
    c.create_space(space_key, 'Page Space')
    global page_id
    page = c.create_content(ContentType.PAGE, 'Test page', space_key, '<h1>Test</h1>')
    page_id = page.id


def teardown_module():
    c.delete_content(page_id, ContentStatus.CURRENT)
    c.delete_space(space_key)


def test_crud_property():
    prop = c.create_content_property(page_id, 'KEY', {'test': 'value'})
    assert prop.key == 'KEY'
    assert prop.value['test'] == 'value'

    props = list(c.get_content_properties(page_id))
    assert len(props) == 1

    prop = c.get_content_property(page_id, 'KEY')
    assert prop.value['test'] == 'value'

    prop = c.update_content_property(page_id, prop.key, {'test': 'new_value'}, 2)
    assert prop.value['test'] == 'new_value'
    assert prop.version.number == 2

    c.delete_content_property(page_id, prop.key)


def test_duplicate_property_creation():
    c.create_content_property(page_id, 'DK', {'test': 'value'})
    with pytest.raises(ConfluenceError):
        c.create_content_property(page_id, 'DK', {'test': 'value'})


def test_update_non_existent_property():
    with pytest.raises(ConfluenceResourceNotFound):
        c.update_content_property(page_id, 'NE', {}, 2)


def test_update_with_wrong_version():
    c.create_content_property(page_id, 'WV', {})
    with pytest.raises(ConfluenceError):
        c.update_content_property(page_id, 'WV', {}, 10)
