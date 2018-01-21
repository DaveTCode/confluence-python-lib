from confluence.models.page import Page
from confluence.models.space import Space, SpaceType, SpaceStatus
from datetime import date
import logging
import requests
from typing import Callable, Dict, Iterable, List, Optional, Tuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Confluence:
    """
    External interface into this library, all calls should be made through
    an instance of this class.

    Note: This class should be used in a context manager (e.g.
    ```with Confluence(...) as c:```
    """

    def __init__(self, base_url: str, basic_auth: Tuple[str, str]) -> None:
        """
        :param base_url: The URL where the confluence web app is located. e.g. https://mysite.mydomain/confluence
        :param basic_auth: A tuple containing a username/password pair that
        can log into confluence.
        """
        self._base_url = base_url
        self._basic_auth = basic_auth
        self._api_base = f'{self._base_url}/rest/api'
        self._client: requests.Session = None

    def __enter__(self):
        self._client = requests.session()
        self._client.auth = self._basic_auth

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._client.close()

    def _get_single_result(self, item_type: Callable, url: str, params: Dict[str, str]):
        # Allow the class to be used without being inside a with block if
        # required.
        if self._client:
            result = self._client.get(url, params=params).json()
        else:
            result = requests.get(url, params=params, auth=self._basic_auth).json()

        return item_type(result)

    def _get_paged_results(self, item_type: Callable, url: str, params: Dict[str, str]):
        while url is not None:
            # Allow the class to be used without being inside a with block if
            # required.
            if self._client:
                search_results = self._client.get(url, params=params).json()
            else:
                search_results = requests.get(url, params=params, auth=self._basic_auth).json()

            if 'next' in search_results['_links']:
                # We have another page of results
                url = f"{self._base_url}{search_results['_links']['next']}"
                params.clear()
            else:
                # No more pages of results
                url = None

            for result in search_results['results']:
                yield item_type(result)

    def get_content(self, content_type: str = 'page', space_key: Optional[str] = None,
                    title: Optional[str] = None, status: Optional[str] = None, posting_day: Optional[date] = None,
                    expand: Optional[List[str]] = None) -> Iterable[Page]:
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
        content_url = f'{self._api_base}/content'
        params = {}
        if content_type and content_type in ('page', 'blogpost'):
            params['type'] = content_type
        if space_key:
            params['spaceKey'] = space_key
        if title:
            params['title'] = title
        if status:
            params['status'] = status
        if posting_day and content_type == 'blogpost':
            params['postingDay'] = posting_day.strftime('%Y-%m-%d')
        if expand:
            params['expand'] = ','.join(expand)

        return self._get_paged_results(Page, content_url, params)

    def search(self, cql: str, cql_context: Optional[str] = None, expand: Optional[List[str]] = None) -> Iterable[Page]:
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
        search_url = f'{self._api_base}/content/search'
        params = {'cql': cql}
        if cql_context:
            params['cqlcontext'] = cql_context
        if expand:
            params['expand'] = ','.join(expand)

        return self._get_paged_results(Page, search_url, params)

    def spaces(self, space_keys: Optional[List[str]] = None, space_type: Optional[SpaceType] = None,
               status: Optional[SpaceStatus] = None, label: Optional[str] = None, favourite: Optional[bool] = None,
               expand: Optional[List[str]] = None) -> Iterable[Space]:
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
        url = f'{self._api_base}/space'
        params = {}
        if space_keys:
            params['spaceKey'] = ','.join(space_keys)
        if space_type:
            params['type'] = space_type.value()
        if status:
            params['status'] = status.value()
        if label:
            params['label'] = label
        if favourite:
            params['favourite'] = str(favourite)  # TODO - Can't figure out if this really works. The REST API docs don't explain it and no queries re: favourite seem to make any difference
        if expand:
            params['expand'] = ','.join(expand)

        return self._get_paged_results(Space, url, params)

    def get_space(self, space_key: str, expand: Optional[List[str]] = None) -> Space:
        """
        Retrieve information on a single space.

        :param space_key: Required parameter which identifies the space.
        :param expand: Optional list of things to expand. Some of icon,
        description, metadata & homepage.

        :return: The space matching the given key.
        """
        url = f'{self._api_base}/space/{space_key}'
        params = {}

        if expand:
            params['expand'] = ','.join(expand)

        return self._get_single_result(Space, url, params)

    def get_space_content(self, space_key: str, just_root: bool = False,
                          expand: Optional[List[str]] = None) -> Iterable[Page]:
        """
        Get all of the content underneath a particular space.

        TODO - Does this handle blogs ok? Returning everything as pages.

        :param space_key: The unique identifier for the space.
        :param just_root: Set to true if you only want the top level pages.
        :param expand: A list of page properties which can be expanded.

        :return: A generator containing all pages matching the search criteria.
        """
        url = f'{self._api_base}/space/{space_key}/content'
        params = {}

        if just_root:
            params['depth'] = 'root'

        if expand:
            params['expand'] = ','.join(expand)

        return self._get_paged_results(Page, url, params)

    def get_space_content_with_type(self, space_key, space_type: SpaceType, just_root: bool = False,
                                    expand: Optional[List[str]] = None) -> Iterable[Page]:
        """
        Get all of the content underneath a particular space of a given type

        TODO - Does this handle blogs ok? Returning everything as pages.

        :param space_key: The unique identifier for the space.
        :param just_root: Set to true if you only want the top level pages.
        :param expand: A list of page properties which can be expanded.

        :return: A generator containing all pages matching the search criteria.
        """
        url = f'{self._api_base}/space/{space_key}/content/{space_type}'
        params = {}

        if just_root:
            params['depth'] = 'root'

        if expand:
            params['expand'] = ','.join(expand)

        return self._get_paged_results(Page, url, params)

    def __str__(self):
        return self._api_base
