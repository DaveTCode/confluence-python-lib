from integration_tests.config import get_confluence_instance
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()


def test_context_managed_client():
    """
    This test just verifies that a context managed client can be used to
    perform requests.
    """
    with c:
        c.create_space('TCMC', 'Test context managed space', 'Description')
        c.delete_space('TCMC')
