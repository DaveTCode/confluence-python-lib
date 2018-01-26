from confluence.models.icon import Icon
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_with_valid_json():
    i = Icon({
        'path': 'https://a.com',
        'width': 200,
        'height': 201,
        'is_default': False
    })

    assert str(i) == 'https://a.com [200x201]'
