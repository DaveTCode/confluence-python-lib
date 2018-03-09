from confluence.models.version import Version
from confluence.models.user import User
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ContentHistory:
    """
    Represents the history of a piece of content(blog|page|comment|attachment)
    in confluence.
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.latest = json['latest']
        self.author = User(json['createdBy'])
        self.created_date = json['createdDate']

        # Fields only returned if the history.lastUpdated is expanded
        if 'lastUpdated' in json:
            self.last_updated = Version(json['lastUpdated'])

        if 'previousVersion' in json:
            self.previous_version = Version(json['previousVersion'])

        if 'nextVersion' in json:
            self.next_version = Version(json['nextVersion'])

        if 'contributors' in json:
            # Note: this is not properly implemented yet, we don't turn this
            # into objects with known properties.
            self.contributors = json['contributors']
