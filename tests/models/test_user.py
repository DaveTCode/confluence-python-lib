from confluence.models.user import User
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_creation_valid_json():
    u = User({
        'username': '1',
        'displayName': '2',
        'userKey': '3',
        'type': '4',
        'profilePicture': {
            'path': 'https://a.com',
            'width': 200,
            'height': 201,
            'is_default': False
        }
    })
    assert u.username == '1'
    assert u.display_name == '2'
    assert u.user_key == '3'
    assert u.type == '4'

    assert str(u) == '1'


def test_creation_minimal_json():
    u = User({})
    assert u.username is None
    assert not hasattr(u, 'display_name')
    assert not hasattr(u, 'user_key')
    assert not hasattr(u, 'type')

    assert str(u) == 'None'
