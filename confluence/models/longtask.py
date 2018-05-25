import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TaskName:
    """Represents the name of a long running task."""

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.key = json['key']  # type: str
        self.args = json['args']  # type: List[str]

    def __str__(self):
        return self.key


class TaskMessage:
    """Represents a message about a long running task."""

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.translation = json['translation']  # type: str
        self.args = json['args']  # type: List[str]

    def __str__(self):
        return self.translation


class LongTask:
    """Represents a single long running task in confluence (e.g. PDF space export)."""

    def __init__(self, json):  # type: (Dict[str, Any]) -> None
        self.id = json['id']  # type: str
        self.name = TaskName(json['name'])  # type: TaskName
        self.elapsed_time = json['elapsedTime']  # type: int
        self.percentage_complete = json['percentageComplete']  # type: int
        self.successful = json['successful']  # type: bool
        self.messages = [TaskMessage(m) for m in json['messages']]  # type: List[TaskMessage]

    def __str__(self):
        return str(self.name)
