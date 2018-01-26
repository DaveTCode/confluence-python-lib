from confluence.models.user import User
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PageUpdate:
    """
    Represents the information stored in confluence about a single page update.
    """
    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.updater = User(json['by'])
        self.when = json['when']
        self.message = json['message']
        self.number = json['number']
        self.minor_edit = json['minorEdit']
        self.hidden = json['hidden']

    def __str__(self):
        return '{} - {}'.format(self.updater, self.when)
