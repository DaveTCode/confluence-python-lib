import logging
from enum import Enum
from typing import Any, Dict

from confluence.models.contentbody import ContentBody
from confluence.models.contenthistory import ContentHistory
from confluence.models.space import Space
from confluence.models.version import Version

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ContentType(Enum):
    """
    The set of valid content types in confluence along with their representation on the API.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/ContentType.html
    """

    ATTACHMENT = "attachment"
    BLOG_POST = "blogpost"
    COMMENT = "comment"
    PAGE = "page"


class ContentStatus(Enum):
    """
    The set of valid content statuses in confluence along with their API representation.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/ContentStatus.html
    """

    CURRENT = "current"
    DRAFT = "draft"
    HISTORICAL = "historical"
    TRASHED = "trashed"


class CommentLocation(Enum):
    """The set of valid comment locations as per the Confluence API."""

    INLINE = 'inline'
    FOOTER = 'footer'
    RESOLVED = 'resolved'


class CommentDepth(Enum):
    """The set of depths at which comments can be retrieved over the API."""

    ROOT = ''
    ALL = 'all'


class Content:
    """
    Main content class for all the different content types. This includes pages, blogs, comments and attachments.

    The type field will allow the end user to distinguish between the types from calling code.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: int
        self.title = json['title']  # type: str
        self.status = ContentStatus(json['status'])  # type: ContentStatus
        self.type = ContentType(json['type'])  # type: ContentType

        if 'metadata' in json:
            self.metadata = json['metadata']  # type: Dict[str, Any]

        if 'extensions' in json:
            self.extensions = json['extensions']  # type: Dict[str, Any]

        if 'space' in json:
            self.space = Space(json['space'])

        if 'body' in json:
            self.body = ContentBody(json['body'])

        if 'history' in json:
            self.history = ContentHistory(json['history'])

        if 'version' in json:
            self.version = Version(json['version'])

        if self.type == ContentType.ATTACHMENT:
            self.links = json['_links']  # type: Dict[str, Any]

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)


class ContentProperty:
    """
    Represents a single property attached to a piece of content.

    Corresponds to https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/content/JsonContentProperty.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.key = json['key']  # type: str
        self.value = json['value']  # type: Dict[str, Any]
        if 'version' in json:
            self.version = Version(json['version'])
        if 'content' in json:
            self.content = Content(json['content'])

    def __str__(self):
        return self.key
