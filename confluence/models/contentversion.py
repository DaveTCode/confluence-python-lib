from confluence.models.user import User
from datetime import datetime
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ContentVersion:
    """
    Represents a single page in Confluence. Note that fields are only
    populated if the corresponding area was expanded in the HTTP request.
    c.f. https://developer.atlassian.com/server/confluence/expansions-in-the-rest-api/
    for more details.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.by = User(json['by'])
        self.when = json['when']  # type: str
        self.message = json['message']  # type: str
        self.number = json['number']  # type: int
        self.minor_edit = json['minorEdit']  # type: bool
        self.hidden = json['hidden']  # type: bool

    def __str__(self):
        return '{} - {}'.format(str(self.by), self.when)
