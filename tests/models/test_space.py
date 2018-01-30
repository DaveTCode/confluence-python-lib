from confluence.models.space import Space
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_minimal_space():
    s = Space({
        'id': 1,
        'key': 'TEST',
        'name': 'Test',
        'type': 'personal'
    })

    assert str(s) == '1 - TEST | Test'


def test_create_space_all():
    s = Space({
        'id': 1,
        'key': 'TEST',
        'name': 'Test',
        'type': 'personal',
        'description': '',
        'homepage': {
            'id': 1,
            'title': 'Hello',
            'status': 'current',
            'type': 'page',
            'space': {
                'id': 1,
                'key': 'TEST',
                'name': 'Test',
                'type': 'personal'
            }
        },
        'icon': {
            'path': 'https://a.com',
            'width': 200,
            'height': 201,
            'isDefault': False
        },
        'metadata': {

        }
    })

    assert str(s) == '1 - TEST | Test'
    assert s.icon is not None
    assert s.homepage is not None
