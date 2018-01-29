from enum import Enum
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CommentLocation(Enum):
    INLINE = 'inline'
    FOOTER = 'footer'
    RESOLVED = 'resolved'


class CommentDepth(Enum):
    ROOT = ''
    ALL = 'all'


class Comment:
    """
    Represents a single comment in confluence.

    TODO - None of the expandable content is covered yet.
    TODO - This is a complete duplicate of attachment, shall we merge them?
    """

    def __init__(self, json):
        # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: str
        self.type = json['type']  # type: str
        self.status = json['status']  # type : str
        self.title = json['title']  # type: str
        self.extensions = json['extensions']  # type: Dict[str, Any]

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)
