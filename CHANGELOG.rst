Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_ and this project adheres to
`Semantic Versioning`_.

`Unreleased`_
-------------

Added
~~~~~

-  Nothing

Changed
~~~~~~~

-  Nothing

`1.0.0`_ - 2018-06-02
----------------------

Added
~~~~~

-  Additional functional tests to bring coverage up to ~90%

Changed
~~~~~~~

-  The API for getting labels has been changed so that the prefix is now an enum as the HTTP API expects.

`0.15.0`_ - 2018-05-25
----------------------

Added
~~~~~

-  Option to update content without sending notifications

Changed
~~~~~~~

-  Added lots of extra docstrings

`0.14.0`_ - 2018-04-06
----------------------

Added
~~~~~

-  Get content by identifier

Changed
~~~~~~~

-  Fixed update_content and added integration tests for it

`0.13.2`_ - 2018-04-04
----------------------

Added
~~~~~

-  Nothing

Changed
~~~~~~~

-  Fixed content body implementation to contain the correct data and added integration tests to verify it

`0.13.1`_ - 2018-04-04
----------------------

Added
~~~~~

-  Nothing

Changed
~~~~~~~

-  Fixed context managed client to return itself

`0.13.0`_ - 2018-03-26
----------------------

Added
~~~~~

-  Added functionality for handling content properties

Changed
~~~~~~~

-  Nothing

`0.12.0`_ - 2018-03-18
----------------------

Added
~~~~~

-  Added support for creating new content (blogs & pages)
-  Added functional tests for creating new content and various space functions

Changed
~~~~~~~

-  hidden is now optional when viewing a Version object

`0.11.0`_ - 2018-03-11
----------------------

Added
~~~~~

-  Added support for deleting content
-  Added support for creating, updating and deleting labels

Changed
~~~~~~~

-  Nothing

`0.10.0`_ - 2018-03-10
----------------------

Added
~~~~~

-  Added support for all endpoints relating to space properties

Changed
~~~~~~~

-  Complete overhaul of the way that failed responses are handled, all
   of them now raise custom exceptions.

`0.9.0`_ - 2018-03-09
---------------------

Added
~~~~~

-  Added partial support for space properties

Changed
~~~~~~~

-  Nothing

`0.8.0`_ - 2018-03-09
---------------------

Added
~~~~~

-  Added full support for manipulating watches on space and content

Changed
~~~~~~~

-  Nothing

`0.7.0`_ - 2018-01-30
---------------------

Added
~~~~~

-  Added basic support for updating content
-  Many more of the fields on content objects are now stored when
   they’re expanded

Changed
~~~~~~~

-  Major overhaul of the content based objects to better match the API
   provided

`0.6.0`_ - 2018-01-26
---------------------

Added
~~~~~

-  Added longtask endpoints
-  A markdown file containing all endpoints with their current state

Changed
~~~~~~~

-  client.spaces is renamed to client.get_spaces in keeping with other
   endpoints

`0.5.0`_ - 2018-01-26
---------------------

Added
~~~~~

-  Added support for python 2.7 & 3.5
-  Added unit tests to verify the models are basically created how you’d
   expect

Changed
~~~~~~~

-  Nothing

`0.3.0`_ - 2018-01-18
---------------------

Added
~~~~~

-  Can now be treated as a context manager holding a single session for
   the duration of the class.
-  README converted to RST for pypi

Changed
~~~~~~~

-  Nothing

`0.2.2`_ - 2018-01-18
---------------------

Added
~~~~~

-  Nothing

Changed
~~~~~~~

-  requests.get isn’t a context manager…

`0.2.1`_ - 2018-01-18
---------------------

Added
~~~~~

-  Nothing

Changed
~~~~~~~

-  Bug fix so we don’t hold a session for quite so long when running
   large queries

`0.2.0`_ - 2018-01-15
---------------------

Added
~~~~~

-  API call /content/search
-  API call /content

Changed
~~~~~~~

-  Nothing

.. _Keep a Changelog: http://keepachangelog.com/
.. _Semantic Versioning: http://semver.org/
.. _Unreleased: https://github.com/DaveTCode/confluence-python-lib/compare/1.0.0...HEAD
.. _1.0.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.15.0...1.0.0
.. _0.15.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.14.0...0.15.0
.. _0.14.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.13.1...0.14.0
.. _0.13.1: https://github.com/DaveTCode/confluence-python-lib/compare/0.13.0...0.13.1
.. _0.13.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.12.0...0.13.0
.. _0.12.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.11.1...0.12.0
.. _0.11.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.10.1...0.11.0
.. _0.10.1: https://github.com/DaveTCode/confluence-python-lib/compare/0.9.0...0.10.1
.. _0.10.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.9.0...0.10.0
.. _0.9.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.8.0...0.9.0
.. _0.8.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.7.0...0.8.0
.. _0.7.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.6.0...0.7.0
.. _0.6.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.5.0...0.6.0
.. _0.5.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.3.0...0.5.0
.. _0.3.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.2...0.3.0
.. _0.2.2: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.1...0.2.2
.. _0.2.1: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.0...0.2.1
.. _0.2.0: https://github.com/DaveTCode/confluence-python-lib/compare/0.0.1...0.2.0