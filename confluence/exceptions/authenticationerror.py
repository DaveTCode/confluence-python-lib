import logging
import requests
from typing import Dict

from confluence.exceptions.generalerror import ConfluenceError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluenceAuthenticationError(ConfluenceError):
    """This exception corresponds to 401 errors on the REST API."""

    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'Authentication failure. This is most likely due to incorrect username/password'.format(path)
        super(ConfluenceAuthenticationError, self).__init__(path, params, response, msg)
