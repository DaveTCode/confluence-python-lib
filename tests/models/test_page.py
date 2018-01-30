from confluence.models.content import Content
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_with_minimal_json():
    p = Content({
        'id': 1,
        'title': 'Hello',
        'status': 'current',
        'type': 'page'
    })

    assert str(p) == '1 - Hello'


def test_create_complete():
    p = Content({
        "id": "65577",
        "type": "page",
        "status": "current",
        "title": "SandBox",
        "space": {
            "id": 98306,
            "key": "SAN",
            "name": "SandBox",
            "type": "global"
        },
        "history": {
            "latest": True,
            "createdBy": {
                "type": "anonymous",
                "profilePicture": {
                    "path": "anonymous.png",
                    "width": 48,
                    "height": 48,
                    "isDefault": True
                },
                "displayName": "Anonymous"
            },
            "createdDate": "2017-09-22T11:03:07.420+01:00"
        },
        "version": {
            "by": {
                "type": "known",
                "username": "user",
                "userKey": "12345",
                "profilePicture": {
                    "path": "default.png",
                    "width": 48,
                    "height": 48,
                    "isDefault": True
                },
                "displayName": "user"
            },
            "when": "2017-10-28T17:05:56.026+01:00",
            "message": "",
            "number": 8,
            "minorEdit": False,
            "hidden": False
        },
        "body": {
            "storage": {
                "value": "",
                "representation": "storage",
                "_expandable": {
                    "content": "/rest/api/content/65577"
                }
            }
        },
        "metadata": {
        },
        "extensions": {
            "position": "none"
        }
    })

    assert p.body.storage == ''
    assert p.body.storage_representation == 'storage'
    assert not hasattr(p.body, 'edit')

    assert p.history.latest

    assert p.space.id == 98306
