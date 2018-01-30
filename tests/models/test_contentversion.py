from confluence.models.contentversion import ContentVersion
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_page_update_creation():
    cv = ContentVersion({
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

    assert str(cv) == '1 - 2017-02-01'
