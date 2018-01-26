import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Icon:
    """
    Represents a single user or space icon in confluence.
    """
    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.path = json['path']
        self.width = json['width']
        self.height = json['height']
        self.is_default = json['is_default']

    def __str__(self):
        return '{} [{}x{}]'.format(self.path, self.width, self.height)
