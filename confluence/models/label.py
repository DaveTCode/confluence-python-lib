import logging
from enum import Enum
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LabelPrefix(Enum):
    """
    Represents the valid prefix values for a Label.

    c.f. https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/Label.Prefix.html
    """

    GLOBAL = 'global'
    MY = 'my'
    SYSTEM = 'system'
    TEAM = 'team'


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
