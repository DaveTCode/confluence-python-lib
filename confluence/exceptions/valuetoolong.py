import logging
import requests
from typing import Dict

from confluence.exceptions.generalerror import ConfluenceError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluenceValueTooLong(ConfluenceError):
    """This exception corresponds to 413 errors on the REST API."""

    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'Resource post to path {} was too large'.format(path)
        super(ConfluenceValueTooLong, self).__init__(path, params, response, msg)
