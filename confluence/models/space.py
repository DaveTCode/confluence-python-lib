import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Space:
    """
    Represents a single space in Confluence. Spaces have no optional/
    expandable content.
    """

    def __init__(self, json: Dict[str, Any]) -> None:
        # All fields always exist on the json object
        self.id = json['id']
        self.key = json['key']
        self.name = json['name']
        self.type = json['type']

    def __str__(self):
        return f'{self.id} - {self.key} | {self.name}'
