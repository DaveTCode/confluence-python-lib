from confluence.models.contentbody import ContentBody
from confluence.models.contenthistory import ContentHistory
from confluence.models.version import Version
from confluence.models.space import Space
from enum import Enum
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ContentType(Enum):
    """
    The set of valid content types in confluence along with their representation on the API

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
    INLINE = 'inline'
    FOOTER = 'footer'
    RESOLVED = 'resolved'


class CommentDepth(Enum):
    ROOT = ''
    ALL = 'all'


class Content:
    """
    Main content class for all the different content types. This includes
    pages, blogs, comments and attachments.

    The type field will allow the end user to distinguish between the types
    from calling code.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: str
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

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)
