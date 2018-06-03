import logging
from typing import Dict

import requests

from confluence.exceptions.generalerror import ConfluenceError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConfluenceVersionConflict(ConfluenceError):
    """Corresponds to 409 errors on the REST API."""

    def __init__(self, path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        msg = 'The given version does not match the expected next version. This is likely because someone else has ' \
              'made a change to the resource at path {}'.format(path)
        super(ConfluenceVersionConflict, self).__init__(path, params, response, msg)
