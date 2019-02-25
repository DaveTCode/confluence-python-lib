from confluence.models.content import Content
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_group_with_valid_json():
    a = Content({
        "id": "att35459744",
        "type": "attachment",
        "status": "current",
        "title": "Puppet Architecture.png",
        "metadata": {
            "comment": "Added by UWC, the Universal Wiki Converter",
            "mediaType": "image/png",
            "labels": {
                "results": [],
                "start": 0,
                "limit": 200,
                "size": 0,
            }
        },
        "extensions": {
            "mediaType": "image/png",
            "fileSize": 61601,
            "comment": "Added by UWC, the Universal Wiki Converter"
        },
        "_links": {
            "download": "/download/attachment/123454/Puppet%20Architecture.png"
        }
    })
    assert str(a) == '35459744 - Puppet Architecture.png'
