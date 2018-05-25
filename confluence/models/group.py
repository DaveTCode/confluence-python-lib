import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Group:
    """Represents a group object in confluence."""

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.type = json['type']
        self.name = json['name']

    def __str__(self):
        return self.name
