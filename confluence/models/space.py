from enum import Enum
import logging
from confluence.models.icon import Icon
#from confluence.models.page import Page
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SpaceType(Enum):
    """
    By default only a specified set of types are valid.
    """
    GLOBAL = "global"
    PERSONAL = "personal"


class SpaceStatus(Enum):
    """
    By default only a specific set of statuses are valid.
    """
    CURRENT = "current"
    ARCHIVED = "archived"


class Space:
    """
    Represents a single space in Confluence.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        # All fields always exist on the json object
        self.id = json['id']
        self.key = json['key']
        self.name = json['name']
        self.type = json['type']

        # Description is expandable
        if 'description' in json:
            pass  # TODO - Description comes back with `view` & `plain` expandable, not clear whether that's a common object so not handling for now

        # Homepage is an expandable full page object
        #if 'homepage' in json:
        #    self.homepage = Page(json['homepage'])

        # icon is expandable
        if 'icon' in json:
            self.icon = Icon(json['icon'])

        # metadata (inc labels) is expandable
        if 'metadata' in json:
            pass  # TODO - Labels not implemented

    def __str__(self):
        return '{} - {} | {}'.format(self.id, self.key, self.name)
