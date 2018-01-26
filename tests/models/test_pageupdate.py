from confluence.models.pageupdate import PageUpdate
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_page_update_creation():
    p = PageUpdate({
        'by': {
            'username': '1',
            'displayName': '2',
            'userKey': '3',
            'type': '4'
        },
        'when': '2017-02-01',
        'message': 'Hello',
        'number': 1,
        'minorEdit': False,
        'hidden': False
    })

    assert str(p) == '1 - 2017-02-01'
