from confluence.client import Confluence
import logging
import os

local_url = 'http://localhost:1990/confluence'
local_admin = ('admin', 'admin')


def get_confluence_instance():
    # type: () -> Confluence
    os.system('curl --fail http://localhost:1990/confluence/rest/api/space')
    user = os.environ.get('ATLASSIAN_CLOUD_USER')
    password = os.environ.get('ATLASSIAN_CLOUD_PASSWORD')
    url = os.environ.get('ATLASSIAN_CLOUD_URL')

    logging.info(url)  # This isn't really secret, just testing env variable retrieval

    return Confluence(url, (user, password)) if user and password and url else Confluence(local_url, local_admin)
