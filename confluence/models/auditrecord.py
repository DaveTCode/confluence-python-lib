import logging
from datetime import datetime
from typing import Any, Dict, List

from confluence.models.user import User

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AffectedObject:
    """
    Represents the affected object of an audit record. c.f.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/audit/AffectedObject.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.name = json['name']  # type: str
        self.object_type = json['objectType']  # type: str

    def __str__(self):
        return self.name


class ChangedValue:
    """
    Represents the change in value of an object in an audit record. c.f.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/audit/ChangedValue.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.name = json['name']  # type: str
        self.new_value = json['newValue']  # type: str
        self.old_value = json['oldValue']  # type: str

    def __str__(self):
        return '{} change from {} to {}'.format(self.name, self.old_value, self.new_value)


class AuditRecord:
    """
    Represents a single audit record from Confluence. c.f.

    https://docs.atlassian.com/atlassian-confluence/6.6.0/com/atlassian/confluence/api/model/audit/AuditRecord.html
    """

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.affected_object = AffectedObject(json['affectedObject'])  # type: AffectedObject
        self.associated_objects = [AffectedObject(a) for a in json['associatedObjects']]  # type: List[AffectedObject]
        self.author = User(json['author'])  # type: User
        self.category = json['category']  # type: str
        self.changed_values = [ChangedValue(v) for v in json['changedValues']]  # type: List[ChangedValue]
        self.creation_date = datetime.utcfromtimestamp(json['creationDate'] / 1000)  # type: datetime
        self.description = json['description']  # type: str
        self.remote_address = json['remoteAddress'].split(',')  # type: List[str]
        self.summary = json['summary']  # type: str
        self.is_sys_admin = json['sysAdmin']  # type: bool

    def __str__(self):
        return self.summary
