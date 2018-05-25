import logging
import os
from datetime import date
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import requests

from confluence.exceptions.generalerror import ConfluenceError
from confluence.exceptions.permissionerror import ConfluencePermissionError
from confluence.exceptions.resourcenotfound import ConfluenceResourceNotFound
from confluence.exceptions.valuetoolong import ConfluenceValueTooLong
from confluence.exceptions.versionconflict import ConfluenceVersionConflict
from confluence.models.auditrecord import AuditRecord
from confluence.models.content import CommentDepth, CommentLocation, Content, ContentStatus, ContentType, \
    ContentProperty
from confluence.models.contenthistory import ContentHistory
from confluence.models.group import Group
from confluence.models.label import Label
from confluence.models.longtask import LongTask
from confluence.models.space import Space, SpaceProperty, SpaceStatus, SpaceType
from confluence.models.user import User

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Confluence:
    """
    External interface into this library, all calls should be made through an instance of this class.

    Note: This class should be used in a context manager. e.g.
    ```with Confluence(...) as c:```
    """

    def __init__(self, base_url, basic_auth):  # type: (str, Tuple[str, str]) -> None
        """
        :param base_url: The URL where the confluence web app is located. e.g. https://mysite.mydomain/confluence
        :param basic_auth: A tuple containing a username/password pair that
            can log into confluence.
        """
        self._base_url = base_url
        self._basic_auth = basic_auth
        self._api_base = '{}/rest/api'.format(self._base_url)
        self._client = None  # type: requests.Session

    def __enter__(self):  # type: () -> Confluence
        self._client = requests.session()
        self._client.auth = self._basic_auth
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._client.close()
            self._client = None

    @property
    def client(self):
        # type: () -> Union[requests.Session, Any]
        # Allow the class to be used without being inside a with block if
        # required.
        return self._client if self._client else requests

    @staticmethod
    def _handle_response_errors(path, params, response):
        # type: (str, Dict[str, str], requests.Response) -> None
        if response.status_code == 400:
            raise ConfluenceError(path, params, response)
        elif response.status_code == 403:
            raise ConfluencePermissionError(path, params, response)
        elif response.status_code == 404:
            raise ConfluenceResourceNotFound(path, params, response)
        elif response.status_code == 409:
            raise ConfluenceVersionConflict(path, params, response)
        elif response.status_code == 413:
            raise ConfluenceValueTooLong(path, params, response)

    def _get(self, path, params, expand):
        # type: (str, Dict[str, str], Optional[List[str]]) -> requests.Response
        url = '{}/{}'.format(self._api_base, path)

        if expand:
            params['expand'] = ','.join(expand)

        response = self.client.get(url, params=params, auth=self._basic_auth)

        Confluence._handle_response_errors(path, params, response)

        return response

    def _get_single_result(self, item_type, path, params, expand):
        # type: (Callable, str, Dict[str, str], Optional[List[str]]) -> Any
        return item_type(self._get(path, params, expand).json())

    # TODO - Need to refactor this to make use of _get function.
    def _get_paged_results(self, item_type, path, params, expand):
        # type: (Callable, str, Dict[str, str], Optional[List[str]]) -> Iterable[Any]
        url = '{}/{}'.format(self._api_base, path)

        if expand:
            params['expand'] = ','.join(expand)

        while url is not None:
            response = self.client.get(url, params=params, auth=self._basic_auth)
            Confluence._handle_response_errors(path, params, response)
            search_results = response.json()

            if 'next' in search_results['_links']:
                # We have another page of results
                url = '{}{}'.format(self._base_url, search_results['_links']['next'])
                params.clear()
            else:
                # No more pages of results
                url = None

            for result in search_results['results']:
                yield item_type(result)

    def _post(self, path, params, data, files=None, expand=None):
        # type: (str, Dict[str, str], Any, Optional[Any], Optional[List[str]]) -> requests.Response
        url = '{}/{}'.format(self._api_base, path)
        headers = {"X-Atlassian-Token": "nocheck"}

        if expand:
            params['expand'] = ','.join(expand)

        response = self.client.post(url, params=params, json=data, headers=headers, files=files, auth=self._basic_auth)

        Confluence._handle_response_errors(path, params, response)

        return response

    def _post_return_single(self, item_type, path, params, data, expand=None):
        # type: (Callable, str, Dict[str, str], Any, Optional[List[str]]) -> Any
        return item_type(self._post(path, params, data, files=None, expand=expand).json())

    def _post_return_multiple(self, item_type, path, params, data, files, expand=None):
        # type: (Callable, str, Dict[str, str], Any, Dict[str, Any], Optional[List[str]]) -> Any
        response = self._post(path, params, data, files=files, expand=expand)

        return [item_type(r) for r in response.json()['results']]

    def _put(self, path, params, data, expand):
        # type: (str, Dict[str, str], Any, Optional[List[str]]) -> requests.Response
        url = '{}/{}'.format(self._api_base, path)
        headers = {"X-Atlassian-Token": "nocheck"}

        if expand:
            params['expand'] = ','.join(expand)

        response = self.client.put(url, json=data, params=params, headers=headers, auth=self._basic_auth)

        Confluence._handle_response_errors(path, params, response)

        return response

    def _put_return_single(self, item_type, path, params, data, expand=None):
        # type: (Callable, str, Dict[str, str], Any, Optional[List[str]]) -> Any
        return item_type(self._put(path, params, data, expand).json())

    def _delete(self, path, params):
        # type: (str, Dict[str, str]) -> requests.Response
        url = '{}/{}'.format(self._api_base, path)
        headers = {"X-Atlassian-Token": "nocheck"}

        response = self.client.delete(url, params=params, headers=headers, auth=self._basic_auth)

        Confluence._handle_response_errors(path, params, response)

        return response

    def create_content(self, content_type, title, space_key, content, parent_content_id=None, expand=None):
        # type: (ContentType, str, str, str, Optional[int], Optional[List[str]]) -> Content
        """
        Create a new piece of content, used for creating blog entries & pages.

        :param content_type: Currently only works for ContentType.PAGE and
            BLOG_POST. Attachments and comments are handled through other
            routes.
        :param title: The title of the content.
        :param space_key: The space to put the content in.
        :param content: The storage format of the new piece of content.
        :param parent_content_id: An optional parent page id to put as the
            ancestor for this piece of content.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter
            allows the user to select which fields that they want to expand on
            the returning piece of content.

        :return: A fully populated content object.
        """
        if content_type not in (ContentType.BLOG_POST, ContentType.PAGE):
            raise ValueError('Only blog posts and pages can be added through this function')

        data = {
            'type': content_type.value,
            'title': title,
            'space': {
                'key': space_key
            },
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }

        if parent_content_id:
            data['ancestors'] = [{
                'id': parent_content_id
            }]

        return self._post_return_single(Content, 'content', {}, data, expand)

    def update_content(self, content_id, content_type, new_version,
                       new_content, new_title, status=None, new_parent=None, new_status=None,
                       minor_edit=False, edit_message=None):
        # type: (int, ContentType, int, str, str, Optional[ContentStatus], Optional[int], Optional[ContentStatus], Optional[bool], Optional[str]) -> Content
        """
        Replace a piece of content in confluence. This can be used to update
        title, content, parent or status.

        :param content_id: The confluence unique ID .
        :param content_type: The type of content to be updated.
        :param new_version: This should be the current version + 1.
        :param status: The current status of the object.
        :param new_content: The new content to store.
        :param new_title: The new title.
        :param new_parent: The new parent content id, optional.
        :param new_status: The new content status, optional.
        :param minor_edit: Defaults to False. Set to true to make this update
            a minor edit.
        :param edit_message: Edit message, optional.

        :return: The updated content object.
        """
        content = {
            'title': new_title,
            'version': {
                'number': new_version,
                'minorEdit': minor_edit
            },
            'type': content_type.value,
            'body': {
                'storage': {
                    'value': new_content,
                    'representation': 'storage'
                }
            }
        }

        if edit_message:
            content['version']['message'] = edit_message

        if new_parent:
            content['ancestors'] = [{
              'id': new_parent
            }]

        if new_status:
            content['status'] = new_status.value

        params = {}
        if status:
            params['status'] = status.value

        return self._put_return_single(Content, 'content/{}'.format(content_id), params=params, data=content)

    def get_content(self, content_type=ContentType.PAGE, space_key=None,
                    title=None, status=None, posting_day=None, expand=None):
        # type: (ContentType, Optional[str], Optional[str], Optional[str], Optional[date], Optional[List[str]]) -> Iterable[Content]
        """
        Matches the REST API call https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/#content-getContent
        which returns an iterable of either pages or blogposts depending on
        the value of the content_type parameter. The default is to return documents.

        Note that this function handles pagination automatically and returns
        an iterable containing all content. Therefore any attempt to
        materialise the results will result in potentially large numbers of
        HTTP requests.

        :param content_type: Determines whether we want to return blog posts
            of pages, defaults to page. Valid values are page|blogpost.
        :param space_key: The string space key of a space on the confluence
            server. Defaults to None which results in this field being ignored.
        :param title: The title of the page we're looking for. Defaults to
            None which results in this field being ignored.
        :param status: Only return documents in a given status.
            Defaults to None which results in this field being ignored.
        :param posting_day: Only valid for blogpost content_type and returns
            blogs posted on the given day.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a comma
            separated list.

        :return: An iterable of pages/blogposts which match the parameters.
        """
        params = {}

        if content_type and content_type not in (ContentType.PAGE, ContentType.BLOG_POST):
            raise ValueError('Cannot GET comments/attachments, only blogposts available on this API call')
        elif content_type:
            params['type'] = content_type.value

        if space_key:
            params['spaceKey'] = space_key
        if title:
            params['title'] = title
        if status:
            params['status'] = status
        if posting_day and content_type == ContentType.BLOG_POST:
            params['postingDay'] = posting_day.strftime('%Y-%m-%d')

        return self._get_paged_results(Content, 'content', params, expand)

    def get_content_by_id(self, content_id, expand=None):
        # type: (int, Optional[List[str]]) -> Content
        """
        Matches the REST API call https://docs.atlassian.com/atlassian-confluence/REST/6.6.0/#content-getContentById
        which returns the document based on the id.

        :param content_id: The unique identifier in confluence for the piece
            of content.

        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a comma
            separated list.

        :return: An iterable of pages/blogposts which match the parameters.
        """
        return self._get_single_result(Content, 'content/{}'.format(content_id), {}, expand)

    def delete_content(self, content_id, content_status):  # type: (int, ContentStatus) -> None
        """
        Deletes a piece of content according to a set of rules based on it's status.

        c.f. https://docs.atlassian.com/ConfluenceServer/rest/6.6.0/#content-delete
        for more details.

        :param content_id: The ID of the content in confluence.
        :param content_status: Required on this call to determine how to
            delete (whether to trash or permanently delete).
        """
        self._delete('content/{}'.format(content_id), params={'status': content_status.value})

    def get_content_history(self, content_id, expand=None):  # type: (int, Optional[List[str]]) -> ContentHistory
        """
        Get the full history of a confluence object. Note that in general you
        can retrieve this by using get_content with history expanded so this
        function is only useful when you don't need the content object as well.

        :param content_id: The ID of the content in confluence.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a list.

        :return: A content history object.
        """
        return self._get_single_result(ContentHistory, 'content/{}/history'.format(content_id), {}, expand)

    def get_child_pages(self, content_id, parent_version=None, expand=None):
        # type: (int, Optional[int], Optional[List[str]]) -> Iterable[Content]
        """
        Get the child pages of a piece of content. Doesn't recurse through
        their children.

        :param content_id: Must be the confluence ID of a page.
        :param parent_version: Optionally pass the version of the page to look
            for children on. Defaults to 0.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a list.

        :return: An iterable containing 0-n pages that are children of this page.
        """
        params = {}
        if parent_version:
            params['parentVersion'] = str(parent_version)

        return self._get_paged_results(Content, 'content/{}/child/page'.format(content_id), params, expand)

    def get_comments(self, content_id, depth=None, parent_version=None, location=None, expand=None):
        # type: (int, Optional[CommentDepth], Optional[int], Optional[List[CommentLocation]], Optional[List[str]]) -> Iterable[Content]
        """
        Retrieve comments on a piece of content.

        :param content_id: The ID of the content in confluence.
        :param depth: Either ROOT or ALL to indicate whether to see all
            comments at all depths.
        :param parent_version: The version of the content which we want
            comments on. Default is to use current version.
        :param location: List of inline, resolved and footer.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a list.

        :return: A list of 0-n comments from the document.
        """
        params = {}

        if depth:
            params['depth'] = depth.value

        if parent_version:
            params['parent_version'] = parent_version

        if location:
            # Note, this is really correct. The confluence API wants to have location=A&location=B not location=A,B
            params['location'] = [l.value for l in location]

        return self._get_paged_results(Content,
                                       'content/{}/child/comment'.format(content_id),
                                       params=params,
                                       expand=expand)

    def get_attachments(self, content_id, filename=None, media_type=None, expand=None):
        # type: (int, Optional[str], Optional[str], Optional[List[str]]) -> Iterable[Content]
        """
        Retrieve attachments on a piece of content.

        :param content_id: The ID of the content in confluence.
        :param filename: Optionally the filename to search by exact filename.
        :param media_type: Optionally the media type of attachments to search
            for.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a list.

        :return: A list of 0-n attachments from the document.
        """
        params = {}

        if filename:
            params['filename'] = filename

        if media_type:
            params['media_type'] = media_type

        return self._get_paged_results(Content,
                                       'content/{}/child/attachment'.format(content_id),
                                       params=params,
                                       expand=expand)

    def add_attachment(self, content_id, file_path, file_name=None, status=None):
        # type: (int, str, Optional[str], Optional[ContentStatus]) -> Iterable[Content]
        """
        Add a single attachment to an existing piece of content.

        :param content_id: the confluence content to add the attachment to.
        :param file_path: The full location of the file on the local system.
        :param file_name: Optionally the name to give the attachment in
            confluence.
        :param status: Optionally the status of the attachment after upload.
            Must be one of current or draft, defaults to current.

        :return: A list containing 0-1 attachments depending on whether this
            succeeded or not.
        """
        params = {}
        if status:
            if status in (ContentStatus.HISTORICAL, ContentStatus.TRASHED):
                raise ValueError('Only draft or current are valid states for a new attachment')
            params['status'] = status.value

        if not file_name:
            file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            return self._post_return_multiple(Content,
                                              'content/{}/child/attachment'.format(content_id),
                                              params=params,
                                              files={'file': (file_name, f)},
                                              data={})

    def get_labels(self, content_id, prefix):  # type: (int, Optional[str]) -> Iterable[Label]
        """
        Retrieve the set of labels on a piece of content.

        :param content_id: The confluence unique id for this content.
        :param prefix: Optionally specify the label prefix.

        :return: A list of the labels on that document.
        """
        params = {}

        if prefix:
            params['prefix'] = prefix

        return self._get_paged_results(Label, 'content/{}/label'.format(content_id), params, None)

    def create_labels(self, content_id, new_labels):  # type: (int, Iterable[Tuple[str, str]]) -> Iterable[Label]
        """
        Create 1-n labels on a piece of content.

        :param content_id: The unique identifier for the content object.
        :param new_labels: An array of tuples where item 1 is the label prefix
            and item 2 is the label name.

        :return: The set of labels as Label objects.
        """
        data = [{
            'prefix': label[0],
            'name': label[1]
        } for label in new_labels]

        return self._post_return_multiple(Label, 'content/{}/label'.format(content_id),
                                          files={}, data=data, params={})

    def delete_label(self, content_id, label_name):  # type: (int, str) -> None
        """
        Remove a label from a piece of content by label name.

        Note that we use the query parameter form of the delete to allow for
        deleting labels with a / in the name.

        :param content_id: The unique identifier for the content object.
        :param label_name: The name of the label to remove.
        """
        self._delete('content/{}/label'.format(content_id), params={'name': label_name})

    def get_content_properties(self, content_id, expand=None):
        # type: (int, Optional[List[str]]) -> Iterable[ContentProperty]
        """

        :param content_id: Required to identify which piece of content we want
            to get properties from.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a comma
            separated list.

        :return: The full list of properties defined on that piece of content.
        """
        return self._get_paged_results(ContentProperty, 'content/{}/property'.format(content_id), {}, expand)

    def create_content_property(self, content_id, property_key, property_value):
        # type: (int, str, Dict[str, Any]) -> ContentProperty
        """
        Create a property on a specific piece of content.

        :param content_id: Required to identify which piece of content we want
            to store the property on.
        :param property_key: The new key, will raise a GeneralError if this
            clashes with an existing property.
        :param property_value: An arbitrary piece of json serializable data.

        :return: The fully populated ContentProperty object.
        """
        data = {
            'key': property_key,
            'value': property_value
        }

        return self._post_return_single(ContentProperty, 'content/{}/property'.format(content_id), {}, data)

    def get_content_property(self, content_id, property_key, expand=None):
        # type: (int, str, Optional[List[str]]) -> ContentProperty
        """
        Retrieve a single property by key from a particular piece of content.

        :param content_id: Required to identify the content we're looking for a
            property on.
        :param property_key: The specific property to search for. If this
            doesn't exist then we raise a ResourceNotFound error.
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a comma
            separated list.

        :return: The fully populated ContentProperty object.
        """
        return self._get_single_result(ContentProperty, 'content/{}/property/{}'.format(content_id, property_key), {},
                                       expand)

    def update_content_property(self, content_id, property_key, new_value, new_version,
                                is_minor_edit=False, is_hidden_edit=False):
        # type: (int, str, Dict[str, Any], int, bool, bool) -> ContentProperty
        """
        Create a new version of a property on a piece of content.

        :param content_id: Required to identify the piece of content.
        :param property_key: The specific property to update. If this doesn't
            exist then we raise a ResourceNotFound error.
        :param new_value: Any arbitrary JSON serializable value.
        :param new_version: If this is 1 and the key doesn't already exist then
            create a new property. Otherwise it must be 1 more than the
            previous version number for this property.
        :param is_minor_edit: Whether this should count as a minor update.
            Defaults to False.
        :param is_hidden_edit: Whether this should count as a hidden edit.
            Defaults to False.

        :return: The new ContentProperty object.
        """
        data = {
            'key': property_key,
            'value': new_value,
            'version': {
                'number': new_version,
                'minorEdit': is_minor_edit,
                'hidden': is_hidden_edit
            }
        }

        return self._put_return_single(ContentProperty, 'content/{}/property/{}'.format(content_id, property_key),
                                       {}, data)

    def delete_content_property(self, content_id, property_key):
        # type: (int, str) -> None
        """
        Remove a property from a piece of content.

        :param content_id: Required to identify the piece of content.
        :param property_key: Required to identify the property uniquely.
        """
        self._delete('content/{}/property/{}'.format(content_id, property_key), {})

    def search(self, cql, cql_context=None, expand=None):
        # type: (str, Optional[str], Optional[List[str]]) -> Iterable[Content]
        """
        Perform a CQL search on the confluence instance and return an iterable
        of the pages which match the query.

        :param cql: A CQL query. See https://developer.atlassian.com/server/confluence/advanced-searching-using-cql/
            for reference.
        :param cql_context: "the context to execute a cql search in, this is
            the json serialized form of SearchContext".
        :param expand: The confluence REST API utilised expansion to avoid
            returning all fields on all requests. This optional parameter allows
            the user to select which fields that they want to expand as a comma
            separated list.

        :return: An iterable of pages which match the parameters.
        """
        params = {'cql': cql}
        if cql_context:
            params['cqlcontext'] = cql_context

        return self._get_paged_results(Content, 'content/search', params, expand)

    def get_spaces(self, space_keys=None, space_type=None, status=None, label=None, favourite=None, expand=None):
        # type: (Optional[List[str]], Optional[SpaceType], Optional[SpaceStatus], Optional[str], Optional[bool], Optional[List[str]]) -> Iterable[Space]
        """
        Queries the list of spaces, providing several ways to further filter
        that query.

        :param space_keys: A list of space keys, only these spaces will be
            returned and invalid values will be ignored.
        :param space_type: Filter on the type of space, all space types
            returned by default.
        :param status: Filter on the status of space, all statuses returned by
            default.
        :param label: Filter on space label, no filter by default.
        :param favourite: Filter on whether the space is favourited by the
            user running the query. Ignored by default.
        :param expand: Optional list of things to expand. Some of icon,
            description, metadata & homepage.
        :return:
        """
        params = {}
        if space_keys:
            params['spaceKey'] = ','.join(space_keys)
        if space_type:
            params['type'] = space_type.value
        if status:
            params['status'] = status.value
        if label:
            params['label'] = label
        if favourite:
            # TODO - Can't figure out if this really works. The REST API docs don't explain it and no
            # queries re: favourite seem to make any difference
            params['favourite'] = str(favourite)

        return self._get_paged_results(Space, 'space', params, expand)

    def create_space(self, space_key, space_name, space_description=None, is_private=False):
        # type: (str, str, Optional[str], bool) -> Space
        """
        Create a space with the specified key, name and (optional) description.

        :param space_key: The new space key. Causes exception if this is not
            unique.
        :param space_name: The new name for the space.
        :param space_description: Optional. A description of the space.
        :param is_private: Set to true to make this space only visible by the
            creator.

        :return: The full space object including it's id.
        """
        path = 'space/_private' if is_private else 'space'

        data = {
            'key': space_key,
            'name': space_name
        }  # type: Dict[str, Any]

        if space_description:
            data['description'] = {
                'plain': {
                    'value': space_description,
                    'representation': 'plain'
                }
            }

        return self._post_return_single(Space, path, data=data, params={})

    def get_space(self, space_key, expand=None):  # type: (str, Optional[List[str]]) -> Space
        """
        Retrieve information on a single space.

        :param space_key: Required parameter which identifies the space.
        :param expand: Optional list of things to expand. Some of icon,
            description, metadata & homepage.

        :return: The space matching the given key.
        """
        return self._get_single_result(Space, 'space/{}'.format(space_key), {}, expand)

    def update_space(self, space_key, new_name, new_description):
        # type: (str, Optional[str], Optional[str]) -> Space
        """
        Update the name, description or both for a given space.

        :param space_key: The unique key for the space.
        :param new_name: The new name, if None then don't update.
        :param new_description: The new description, if None then don't update.

        :return: The full new space object including id.
        """
        data = {}  # type: Dict[str, Any]

        if new_name:
            data['name'] = new_name

        if new_description:
            data['description'] = {
                'plain': {
                    'value': new_description,
                    'representation': 'plain'
                }
            }

        return self._put_return_single(Space, 'space/{}'.format(space_key), data=data, params={})

    def delete_space(self, space_key):  # type: (str) -> None
        """
        Delete a space inside of a long running task.

        # TODO - This should really return the longtask that can be used to poll for when it completes.
        :param space_key: The spaces unique identifier.
        """
        self._delete('space/{}'.format(space_key), params={})

    def get_space_content(self, space_key, just_root=False, expand=None):
        # type: (str, bool, Optional[List[str]]) -> Iterable[Content]
        """
        Get all of the content underneath a particular space.

        :param space_key: The unique identifier for the space.
        :param just_root: Set to true if you only want the top level pages.
        :param expand: A list of page properties which can be expanded.

        :return: A generator containing all pages matching the search criteria.
        """
        params = {}

        if just_root:
            params['depth'] = 'root'

        return self._get_paged_results(Content, 'space/{}/content'.format(space_key), params, expand)

    def get_space_content_with_type(self, space_key, content_type, just_root=False, expand=None):
        # type: (str, ContentType, bool, Optional[List[str]]) -> Iterable[Content]
        """
        Get all of the content underneath a particular space of a given type

        :param space_key: The unique identifier for the space.
        :param content_type: What sort of content to return. Blogs or pages.
        :param just_root: Set to true if you only want the top level pages.
        :param expand: A list of page properties which can be expanded.

        :return: A generator containing all pages matching the search criteria.
        """
        path = 'space/{}/content/{}'.format(space_key, content_type.value)
        params = {}

        if just_root:
            params['depth'] = 'root'

        return self._get_paged_results(Content, path, params, expand)

    def get_space_properties(self, space_key, expand=None):
        # type: (str, Optional[List[str]]) -> Iterable[SpaceProperty]
        """
        Get all of the properties attached to a given space.

        :param space_key: The key of the space.
        :param expand: A list of properties which can be expanded.

        :return: A generator containing all of the properties attached to the
            space.
        """
        return self._get_paged_results(SpaceProperty, 'space/{}/property'.format(space_key), {}, expand)

    def create_space_property(self, space_key, property_key, property_value):
        # type: (str, str, Dict[str, Any]) -> SpaceProperty
        """
        Create a property attached to a space.

        :param space_key: The space to which we're adding a property.
        :param property_key: The key for the new property.
        :param property_value: An arbitrary JSON serializable object which
            will become the property value.

        :return: The space property that was created.
        """
        data = {
            'key': property_key,
            'value': property_value
        }
        return self._post_return_single(SpaceProperty, 'space/{}/property'.format(space_key), params={}, data=data)

    def get_space_property(self, space_key, property_key, expand=None):
        # type: (str, str, Optional[List[str]]) -> Iterable[SpaceProperty]
        """
        Get all of the properties attached to a given space which match a
        property key.

        :param space_key: The key of the space.
        :param property_key: The key of the property.
        :param expand: A list of properties which can be expanded.

        :return: A generator containing all of the properties attached to the
            space.
        """
        path = 'space/{}/property/{}'.format(space_key, property_key)

        return self._get_paged_results(SpaceProperty, path, {}, expand)

    def update_space_property(self, space_key, property_key, property_value, new_version,
                              minor_edit=False, hidden_version=False):
        # type: (str, str, Dict[str, Any], int, Optional[bool], Optional[bool]) -> SpaceProperty
        """
        Create a new version of a space property.

        :param space_key: The space to create the property in.
        :param property_key: The key of the property to create.
        :param property_value: The new value of the property.
        :param new_version: The version number of the property. If this is 1
            then a new property is created, otherwise it must be current_version+1
            or this function will raise an exception.
        :param minor_edit: Defaults to False. Set to true to make this update
            a minor edit.
        :param hidden_version: Defaults to False. Set to true to make this
            version hidden.

        :return: The created property (including version).
        """
        path = 'space/{}/property/{}'.format(space_key, property_key)
        data = {
            'key': property_key,
            'value': property_value,
            'version': {
                'number': new_version,
                'minorEdit': minor_edit,
                'hidden': hidden_version
            }
        }
        return self._put_return_single(SpaceProperty, path, params={}, data=data)

    def delete_space_property(self, space_key, property_key):
        # type: (str, str) -> None
        """

        :param space_key: The space in which we're removing a property.
        :param property_key: The property to remove.
        """
        self._delete('space/{}/property/{}'.format(space_key, property_key), {})

    def get_user(self, username=None, user_key=None, expand=None):
        # type: (Optional[str], Optional[str], Optional[List[str]]) -> User
        """
        Return a single user object matching either the username of the key
        passed in.

        Note: You must pass exactly one of username or user_key to this
        function.

        :param username: The username as seen in Confluence.
        :param user_key: The unique user id.
        :param expand: A list of sections of the user object to expand.

        :return: A full user object.
        """
        if (not username and not user_key) or (username and user_key):
            raise ValueError('Exactly one of username or user_key must be set')

        params = {}
        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        return self._get_single_result(User, 'user', params, expand)

    def get_anonymous_user(self):  # type: () -> User
        """
        Returns the user object which represents anonymous users on Confluence.

        :return: A full user object.
        """
        return self._get_single_result(User, 'user/anonymous', {}, None)

    def get_current_user(self):  # type: () -> User
        """
        Returns the user object for the current logged in user.

        :return: A full user object.
        """
        return self._get_single_result(User, 'user/current', {}, None)

    def get_user_groups(self, username=None, user_key=None, expand=None):
        # type: (Optional[str], Optional[str], Optional[List[str]]) -> Iterable[Group]
        """
        Get a list of the groups that a user is a member of. Either the
        username or key must be set and not both.

        :param username: The username as seen in confluence.
        :param user_key: The users unique key in confluence.
        :param expand: An optional list of fields to expand on the returned
            group objects. None currently known.

        :return: The list of groups as an iterator.
        """
        if (not username and not user_key) or (username and user_key):
            raise ValueError('Exactly one of username or user_key must be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        return self._get_paged_results(Group, 'user/memberof', params, expand)

    def get_groups(self, expand):
        # type: (Optional[List[str]]) -> Iterable[Group]
        """
        Get the entire collection of groups on this instance.

        :param expand: An optional list of fields to expand on the returned
            group objects. None currently known.

        :return: The list of groups as an iterator.
        """
        return self._get_paged_results(Group, 'group', {}, expand)

    def get_group(self, name, expand):
        # type: (str, Optional[List[str]]) -> Group
        """
        Get a single group instance.

        :param name: The name of the group to search for.
        :param expand: An optional list of fields to expand on the returned
            group objects. None currently known.

        :return: The group object.
        """
        return self._get_single_result(Group, 'group/{}'.format(name), {}, expand)

    def get_group_members(self, name, expand):
        # type: (str, Optional[List[str]]) -> Iterable[User]
        """
        Get the entire collection of users in this group.

        :param name: The name of the group to search for.
        :param expand: An optional list of fields to expand on the returned
            user objects. None currently known.

        :return: The list of groups as an iterator.
        """
        return self._get_paged_results(User, 'group/{}/member'.format(name), {}, expand)

    def get_long_tasks(self, expand):
        # type: (Optional[List[str]]) -> Iterable[LongTask]
        """
        Get the full list of long running tasks from the confluence instance.

        :param expand: An optional list of fields to expand on the returned
            user objects. None currently known.

        :return: The list of long running tasks including recently completed
            ones.
        """
        return self._get_paged_results(LongTask, 'longtask', {}, expand)

    def get_long_task(self, task_id, expand):
        # type: (str, Optional[List[str]]) -> Iterable[LongTask]
        """
        Get the details about a single long running task.

        :param task_id: The task id as a GUID.
        :param expand: An optional list of fields to expand on the returned
            user objects. None currently known.

        :return: The full task information.
        """
        return self._get_paged_results(LongTask, 'longtask/{}'.format(task_id), {}, expand)

    def get_audit_records(self, start_date, end_date, search_string):
        # type: (Optional[date], Optional[date], Optional[str]) -> Iterable[AuditRecord]
        """
        Retrieve audit records between two dates with the given search
        parameters.

        :param start_date: Optional date to start searching.
        :param end_date: Optional date to end searching.
        :param search_string: Optional string which will be included in all
            returned audit records.

        :return: A list of all audit records matching the given criteria.
        """
        params = {}
        if start_date:
            params['startDate'] = start_date.strftime('%Y-%m-%d')

        if end_date:
            params['endDate'] = end_date.strftime('%Y-%m-%d')

        if search_string:
            params['searchString'] = search_string

        return self._get_paged_results(AuditRecord, 'audit', params, None)

    def add_content_watch(self, content_id, user_key=None, username=None):
        # type: (int, Optional[str], Optional[str]) -> None
        """
        Add a watch for a given user & piece of content.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param content_id: The unique content id.
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        self._post('user/watch/content/{}'.format(content_id), params=params, data={})

    def remove_content_watch(self, content_id, user_key=None, username=None):
        # type: (int, Optional[str], Optional[str]) -> None
        """
        Stop a user watching a piece of content.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param content_id: The unique content id.
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        self._delete('user/watch/content/{}'.format(content_id), params)

    def is_user_watching_content(self, content_id, user_key=None, username=None):
        # type: (int, Optional[str], Optional[str]) -> bool
        """
        Get information about whether a user is watching specific content.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param content_id: The content id to check
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.

        :return: True/False depending on whether the user is watching the
            specified content.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        return self._get('user/watch/content/{}'.format(content_id), params, None).json()['watching']

    def add_space_watch(self, space_key, user_key=None, username=None):
        # type: (str, Optional[str], Optional[str]) -> None
        """
        Add a watch for a given user & space.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param space_key: The key of the space to add the watch on.
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        self._post('user/watch/space/{}'.format(space_key), params, data={})

    def remove_space_watch(self, space_key, user_key=None, username=None):
        # type: (str, Optional[str], Optional[str]) -> None
        """
        Stop a user watching a space.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param space_key: The key of the space to remove the watch on.
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        self._delete('user/watch/space/{}'.format(space_key), params)

    def is_user_watching_space(self, space_key, user_key=None, username=None):
        # type: (str, Optional[str], Optional[str]) -> bool
        """
        Get information about whether a user is watching a specific space.

        User is optional. If not specified, currently logged-in user will be
        used. Otherwise, it can be specified by either user key or username.
        When a user is specified and is different from the logged-in user,
        the logged-in user needs to be a Confluence administrator.

        :param space_key: The key of the space to check.
        :param user_key: The users unique key. If this is set then username
            must not be.
        :param username: The username to check for watches. If this is set
            then user_key must not be.

        :return: True/False depending on whether the user is watching the
            specified space.
        """
        if username and user_key:
            raise ValueError('Only one of username or user_key may be set')

        params = {}

        if username:
            params['username'] = username
        if user_key:
            params['key'] = user_key

        return self._get('user/watch/space/{}'.format(space_key), params, None).json()['watching']

    def __str__(self):
        return self._api_base
