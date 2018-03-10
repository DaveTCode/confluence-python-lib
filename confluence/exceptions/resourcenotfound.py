import logging
import requests
from typing import Dict

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResourceNotFound(Exception):
    """
    This exception corresponds to 404 errors on the REST API
    """
    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'Resource was not found at path {} or the user has insufficient permissions'
        self.path = path
        self.params = params
        self.response = response
        super(ResourceNotFound, self).__init__(msg, format(path))
