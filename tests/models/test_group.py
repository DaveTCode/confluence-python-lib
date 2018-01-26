from confluence.models.group import Group
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_group_with_valid_json():
    g = Group({
        'type': 'Type',
        'name': 'Name'
    })
    assert str(g) == 'Name'
