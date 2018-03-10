|Build Status| |PyPI version| |codecov| |Requirements Status| |Docs|

Confluence Python Library
=========================

This is a simple wrapper around the REST API which the Confluence
provides.

Note that the library is undergoing major work so don’t expect the API
to be stable until this notice is removed!

c.f. `endpoints.md`_ for a list of endpoints and whether this library
supports them yet. Please do send pull requests if you want an endpoint
that isn’t covered!

Installation
------------

::

    pip install confluence-rest-library

Usage
-----

.. code:: python

    from confluence.client import Confluence
    with Confluence('https://site:8080/confluence', ('user', 'pass')) as c:
        pages = c.search('ID=1')

Development and Deployment
--------------------------

See the `Contribution guidelines for this project`_ for details on how
to make changes to this library.

Testing Locally
~~~~~~~~~~~~~~~

For now there are only some basic unit tests included. These can be run
using

::

    python setup.py test

.. _endpoints.md: endpoints.md
.. _Contribution guidelines for this project: CONTRIBUTING.md

.. |Build Status| image:: https://travis-ci.org/DaveTCode/confluence-python-lib.svg?branch=master
   :target: https://travis-ci.org/DaveTCode/confluence-python-lib
.. |PyPI version| image:: https://badge.fury.io/py/confluence-rest-library.svg
   :target: https://badge.fury.io/py/confluence-rest-library
.. |codecov| image:: https://codecov.io/gh/DaveTCode/confluence-python-lib/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/DaveTCode/confluence-python-lib
.. |Requirements Status| image:: https://requires.io/github/DaveTCode/confluence-python-lib/requirements.svg?branch=develop
   :target: https://requires.io/github/DaveTCode/confluence-python-lib/requirements/?branch=develop
.. |Docs| image:: https://readthedocs.org/projects/confluence-python-lib/badge/?version=latest
   :target: http://confluence-python-lib.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status