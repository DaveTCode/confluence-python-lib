from confluence.models.pageupdate import PageUpdate
from confluence.models.user import User
from enum import Enum
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ContentType(Enum):
    PAGE = "page"
    BLOG = "blog"


class Page:
    """
    Represents a single page in Confluence. Note that fields are only
    populated if the corresponding area was expanded in the HTTP request.
    c.f. https://developer.atlassian.com/server/confluence/expansions-in-the-rest-api/
    for more details.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        # Fields that must exist on the json object
        self.id = json['id']
        self.title = json['title']
        self.status = json['status']

        # Fields that only exist if the space is expanded
        if 'space' in json:
            from confluence.models.space import Space  # Avoid circular dependency caused by space having a page
            self.space = Space(json['space'])

        # Fields that only exist if a part of the body is expanded
        if 'body' in json:
            if 'storage' in json['body']:
                self.body_storage = json['body']['storage']
            if 'editor' in json['body']:
                self.body_storage = json['body']['editor']
            if 'view' in json['body']:
                self.body_storage = json['body']['view']
            if 'export_view' in json['body']:
                self.body_storage = json['body']['export_view']
            if 'styled_view' in json['body']:
                self.body_storage = json['body']['styled_view']
            if 'anonymous_export_view' in json['body']:
                self.body_storage = json['body']['anonymous_export_view']

        # Fields that only exist if the history is expanded
        if 'history' in json:
            self.latest = json['history']['latest']
            self.created_date = json['history']['createdDate']
            self.author = User(json['history']['createdBy'])

            # Fields only returned if the history.lastUpdated is expanded
            if 'lastUpdated' in json['history']:
                self.last_updated = PageUpdate(json['history']['lastUpdated'])

        if 'version' in json:
            if 'number' in json['version']:
                self.version_number = json['version']['number']

    def for_page_update(self) -> Dict[str, Any]:
        json = {'id': self.id, 'title': self.title, 'type': 'page',
                'body': {'storage': self.body_storage},
                'version': {'number': self.version_number + 1}}
        return json

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)
