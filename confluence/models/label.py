import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Label:
    """
    Represents a label on a piece of confluence content.

    c.f. https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/labels/Label.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: str
        self.name = json['name']  # type: str
        self.prefix = json['prefix']  # type: str

    def __str__(self):
        return self.name
