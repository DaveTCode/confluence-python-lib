from confluence.models.user import User
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PageUpdate:
    """
    Represents the information stored in confluence about a single page update.
    """
    def __init__(self, json: Dict[str, Any]):
        self.updater = User(json['by'])
        self.when = json['when']
        self.message = json['message']
        self.number = json['number']
        self.minor_edit = json['minorEdit']
        self.hidden = json['hidden']

    def __str__(self):
        return f'{self.updater} - {self.when}'
