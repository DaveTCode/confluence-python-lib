import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluenceError(Exception):
    """Corresponds to 400 errors on the REST API."""

    def __init__(self, path, params, response, msg=None):
        # type: (str, Dict[str, str], requests.Response, Optional[str]) -> None
        if not msg:
            msg = 'General resource error accessing path {}'.format(path)
        self.path = path
        self.params = params
        self.response = response
        super(ConfluenceError, self).__init__(msg)
