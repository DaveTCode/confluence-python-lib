import logging

from confluence.models.content import ContentProperty

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def create_with_minimal_json():
    p = ContentProperty({
        'key': 'KEY',
        'value': {}
    })

    assert str(p) == 'KEY'
    assert not hasattr(p, 'content')
    assert not hasattr(p, 'version')


def create_with_full_json():
    p = ContentProperty({
        'key': 'KEY',
        'value': {
            'anything': 1
        },
        'version': {
            'number': 2,
            'minorEdit': False,
            'hidden': False
        },
        'content': {
            'id': 1,
            'title': 'Hello',
            'status': 'current',
            'type': 'page'
        }
    })

    assert str(p) == 'KEY'
    assert p.version.number == 2
    assert p.content.id == 1
