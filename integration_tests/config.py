from confluence.client import Confluence
import os

local_url = 'http://localhost:1990/confluence'
local_admin = ('admin', 'admin')


def get_confluence_instance():
    # type: () -> Confluence
    user = os.environ.get('ATLASSIAN_CLOUD_USER')
    password = os.environ.get('ATLASSIAN_CLOUD_PASSWORD')
    url = os.environ.get('ATLASSIAN_CLOUD_URL')

    return Confluence(url, (user, password)) if user and password and url else Confluence(local_url, local_admin)
