import logging
import requests
from typing import Dict

from confluence.exceptions.generalerror import ConfluenceError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluencePermissionError(ConfluenceError):
    """This exception corresponds to 403 errors on the REST API."""

    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'User has insufficient permissions to perform that operation on the path {}'.format(path)
        super(ConfluencePermissionError, self).__init__(path, params, response, msg)
