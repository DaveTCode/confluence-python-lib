from confluence.models.page import Page
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_with_minimal_json():
    p = Page({
        'id': 1,
        'title': 'Hello',
        'status': 'Archived'
    })

    assert str(p) == '1 - Hello'


def test_create_with_space():
    p = Page({
        'id': 1,
        'title': 'Hello',
        'status': 'Archived',
        'space': {
            'id': 1,
            'key': 'TEST',
            'name': 'Test',
            'type': 'personal'
        }
    })

    assert str(p.space) == '1 - TEST | Test'


def test_create_with_body():
    p = Page({
        'id': 1,
        'title': 'Hello',
        'status': 'Archived',
        'body': {
            'storage': 1,
            'editor': 'TEST',
            'view': 'Test',
            'export_view': 'personal',
            'styled_view': 'personal',
            'anonymous_export_view': 'body storage'
        }
    })

    assert str(p.body_storage) == 'body storage'  # TODO - Needs fixing when we better implement the storage element on a page


def test_create_with_history():
    p = Page({
        'id': 1,
        'title': 'Hello',
        'status': 'Archived',
        'history': {
            'latest': 1,
            'createdDate': '2017-01-01',
            'createdBy': {
                'username': '1',
                'displayName': '2',
                'userKey': '3',
                'type': '4'
            },
            'lastUpdated': {
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
            }
        }
    })

    assert p.latest == 1
    assert p.created_date == '2017-01-01'
    assert str(p.author) == '1'
    assert str(p.last_updated) == '1 - 2017-02-01'
