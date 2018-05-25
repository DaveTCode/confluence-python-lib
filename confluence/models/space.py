from enum import Enum
import logging
from confluence.models.icon import Icon
from typing import Any, Dict

from confluence.models.version import Version

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SpaceType(Enum):
    """
    By default only a specified set of types are valid.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/SpaceType.html
    """

    GLOBAL = "global"
    PERSONAL = "personal"


class SpaceStatus(Enum):
    """
    By default only a specific set of statuses are valid.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/SpaceStatus.html
    """

    CURRENT = "current"
    ARCHIVED = "archived"


class Space:
    """Represents a single space in Confluence."""

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        # All fields always exist on the json object
        self.id = json['id']  # type: int
        self.key = json['key']  # type: str
        self.name = json['name']  # type: str
        self.type = SpaceType(json['type'])  # type: SpaceType

        # Description is expandable
        if 'description' in json:
            pass  # TODO - Description comes back with `view` & `plain` expandable, not clear whether that's a common object so not handling for now

        # Homepage is an expandable full page object
        if 'homepage' in json:
            from confluence.models.content import Content
            self.homepage = Content(json['homepage'])

        # icon is expandable
        if 'icon' in json:
            self.icon = Icon(json['icon'])

        # metadata (inc labels) is expandable
        if 'metadata' in json:
            self.metadata = json['metadata']  # type: Dict[str, Any]

    def __str__(self):
        return '{} - {} | {}'.format(self.id, self.key, self.name)


class SpaceProperty:
    """
    Represents a single property attached to a space.

    Corresponds to https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/JsonSpaceProperty.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.key = json['key']  # type: str
        self.value = json['value']  # type: Dict[str, Any]
        if 'version' in json:
            self.version = Version(json['version'])
        if 'space' in json:
            self.space = Space(json['space'])

    def __str__(self):
        return str(self.key)
