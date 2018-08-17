import logging

from confluence.models.content import ContentType, ContentStatus

from integration_tests.config import get_confluence_instance

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'CH'


def setup_module():
    c.create_space(space_key, 'Content History Space')


def teardown_module():
    c.delete_space(space_key)


def test_get_page_history_with_no_expansion():
    page = c.create_content(ContentType.PAGE, content='A', space_key=space_key, title='A')
    try:
        c.update_content(page.id, ContentType.PAGE, new_version=page.version.number + 1, new_content='AA',
                         new_title=page.title)
        history = c.get_content_history(page.id)
        assert history.author.username == 'admin'
        assert history.last_updated.number == 2
        assert history.previous_version.number == 1
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)


def test_get_page_history_with_all_expansions():
    page = c.create_content(ContentType.PAGE, content='A', space_key=space_key, title='A')
    try:
        c.update_content(page.id, ContentType.PAGE, new_version=page.version.number + 1, new_content='AA',
                         new_title=page.title)
        history = c.get_content_history(page.id, expand=['previousVersion', 'nextVersion', 'lastUpdated',
                                                         'contributors.publishers'])
        assert history.author.username == 'admin'
        assert history.last_updated.number == 2
        assert history.previous_version.number == 1
        assert history.contributors is not None
    finally:
        c.delete_content(page.id, ContentStatus.CURRENT)
