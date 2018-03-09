from confluence.models.space import Space, SpaceProperty
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


def test_create_space_property_minimal():
    s = SpaceProperty({
        'space': {
            'key': 'TST',
            'name': 'Example space',
            'description': {
                'plain': {
                    'value': 'This is an example space',
                    'representation': 'plain'
                }
            },
            'metadata': {},
            '_links': {
                'self': 'http://myhost:8080/confluence/rest/api/space/TST'
            }
        },
        'key': 'example-property-key',
        'value': {
            'anything': 'goes'
        },
        'version': {
            'number': 2,
            'minorEdit': False,
            'hidden': False
        }
    })

    assert str(s) == 'example-property-key'
    assert s.version.number == 2
    assert s.space.key == 'TST'
