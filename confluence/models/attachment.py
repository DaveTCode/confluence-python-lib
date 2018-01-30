import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Attachment:
    """
    Represents a single attachement on any piece of content in confluence.

    TODO - None of the expandable content is covered yet.
    """

    def __init__(self, json):
        # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: str
        self.type = json['type']  # type: str
        self.status = json['status']  # type: str
        self.title = json['title']  # type: str
        self.metadata = json['metadata']  # type: Dict[str, Any]
        self.extensions = json['extensions']  # type: Dict[str, Any]

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)
