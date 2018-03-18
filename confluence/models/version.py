from confluence.models.user import User
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Version:
    """
    Represents a version of an object in Confluence.

    Corresponds to https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/Version.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.number = json['number']  # type: int
        self.minor_edit = json['minorEdit']  # type: bool

        if 'hidden' in json:
            self.hidden = json['hidden']  # type: bool

        if 'by' in json:
            self.by = User(json['by'])

        if 'when' in json:
            self.when = json['when']  # type: str

        if 'message' in json:
            self.message = json['message']  # type: str

    def __str__(self):
        return '{}'.format(self.number)
