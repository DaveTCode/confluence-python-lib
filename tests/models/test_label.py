from confluence.models.label import Label
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_create_label():
    label = Label({
        "prefix": "global",
        "name": "branding",
        "id": "12345"
    })

    assert str(label) == 'branding'
