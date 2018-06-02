import logging

from confluence.models.content import ContentType, ContentStatus
from confluence.models.label import LabelPrefix
from integration_tests.config import get_confluence_instance

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'LO'


def setup_module():
    c.create_space(space_key, 'Label Operations Space')


def teardown_module():
    c.delete_space(space_key)


def test_add_get_delete_label():
    page = c.create_content(ContentType.PAGE, content='A', space_key=space_key, title='A')
    try:
        c.create_labels(page.id, [(LabelPrefix.GLOBAL, 'b'), (LabelPrefix.MY, 'd')])

        labels = list(c.get_labels(page.id))
        prefixed_labels = list(c.get_labels(page.id, LabelPrefix.GLOBAL))
        assert len(labels) == 2
        assert len(prefixed_labels) == 1

        c.delete_label(page.id, labels[0].name)
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)
