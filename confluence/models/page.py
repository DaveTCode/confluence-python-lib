from confluence.models.pageupdate import PageUpdate
from confluence.models.space import Space
from confluence.models.user import User
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Page:
    """
    Represents a single page in Confluence. Note that fields are only
    populated if the corresponding area was expanded in the HTTP request.
    c.f. https://developer.atlassian.com/server/confluence/expansions-in-the-rest-api/
    for more details.
    """

    def __init__(self, json: Dict[str, Any]) -> None:
        # Fields that must exist on the json object
        self.id = json['id']
        self.title = json['title']
        self.status = json['status']

        # Fields that only exist if the space is expanded
        if 'space' in json:
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
            self.last_updated = PageUpdate(json['history']['lastUpdated'])

    def __str__(self):
        return f'{self.id} - {self.title}'
