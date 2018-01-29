from confluence.models.comment import Comment
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_group_with_valid_json():
    c = Comment({
        "id": "39128239",
        "type": "comment",
        "status": "current",
        "title": "Re: Puppet: Architecture Overview",
        "extensions": {
            "location": "inline",
            "_expandable": {
                "inlineProperties": "",
                "resolution": ""
            }
        }
    })
    assert str(c) == '39128239 - Re: Puppet: Architecture Overview'
