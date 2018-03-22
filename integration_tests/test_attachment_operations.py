from confluence.exceptions.resourcenotfound import ConfluenceResourceNotFound
from confluence.models.content import ContentType, ContentStatus
from integration_tests.config import get_confluence_instance
import logging
import py
import pytest

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

c = get_confluence_instance()
space_key = 'ATTSP'
page_id = 0


def setup_module():
    c.create_space(space_key, 'Page Space')
    global page_id
    page_id = c.create_content(ContentType.PAGE, space_key=space_key, content='', title='Test Attachment Page').id


def teardown_module():
    c.delete_content(content_id=page_id, content_status=ContentStatus.CURRENT)
    c.delete_space(space_key)


def test_add_attachment(tmpdir):  # type: (py.path.local) -> None
    p = tmpdir.mkdir("attachments").join("test.txt")
    p.write("test")
    c.add_attachment(page_id, p.realpath())
    attachments = list(c.get_attachments(page_id, filename=None, media_type=None))
    assert len(attachments) == 1


def test_add_attachment_to_missing_page(tmpdir):  # type: (py.path.local) -> None
    p = tmpdir.mkdir("attachments").join("bad.txt")
    p.write("bad")
    with pytest.raises(ConfluenceResourceNotFound):
        c.add_attachment(-1, file_path=p.realpath())
