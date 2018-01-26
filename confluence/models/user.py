from confluence.models.icon import Icon
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class User:
    """
    Represents a single user object in confluence either as attached to a page
    or as requested directly over the API.

    Note that all fields here are optional as the user attached to pages might
    not contain standard fields (e.g. when it's anonymous)
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        # Fields are not always present when requesting a user.
        self.username = json['username'] if 'username' in json else None
        if 'displayName' in json:
            self.display_name = json['displayName']
        if 'userKey' in json:
            self.user_key = json['userKey']
        if 'type' in json:
            self.type = json['type']
        if 'profilePicture' in json:
            self.profile_picture = Icon(json['profilePicture'])

    def __str__(self):
        return str(self.username)
