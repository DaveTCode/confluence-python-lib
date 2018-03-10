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

`0.10.0`_ - 2017-03-10
----------------------

.. _added-1:

Added
~~~~~

-  Added support for all endpoints relating to space properties

.. _changed-1:

Changed
~~~~~~~

-  Complete overhaul of the way that failed responses are handled, all
   of them now raise custom exceptions.

.. _section-1:

`0.9.0`_ - 2017-03-09
---------------------

.. _added-2:

Added
~~~~~

-  Added partial support for space properties

.. _changed-2:

Changed
~~~~~~~

-  Nothing

.. _section-2:

`0.8.0`_ - 2017-03-09
---------------------

.. _added-3:

Added
~~~~~

-  Added full support for manipulating watches on space and content

.. _changed-3:

Changed
~~~~~~~

-  Nothing

.. _section-3:

`0.7.0`_ - 2017-01-30
---------------------

.. _added-4:

Added
~~~~~

-  Added basic support for updating content
-  Many more of the fields on content objects are now stored when
   they’re expanded

.. _changed-4:

Changed
~~~~~~~

-  Major overhaul of the content based objects to better match the API
   provided

.. _section-4:

`0.6.0`_ - 2017-01-26
---------------------

.. _added-5:

Added
~~~~~

-  Added longtask endpoints
-  A markdown file containing all endpoints with their current state

.. _changed-5:

Changed
~~~~~~~

-  client.spaces is renamed to client.get_spaces in keeping with other
   endpoints

.. _section-5:

`0.5.0`_ - 2017-01-26
---------------------

.. _added-6:

Added
~~~~~

-  Added support for python 2.7 & 3.5
-  Added unit tests to verify the models are basically created how you’d
   expect

.. _changed-6:

Changed
~~~~~~~

-  Nothing

.. _section-6:

`0.3.0`_ - 2017-01-18
---------------------

.. _added-7:

Added
~~~~~

-  Can now be treated as a context manager holding a single session for
   the duration of the class.
-  README converted to RST for pypi

.. _changed-7:

Changed
~~~~~~~

-  Nothing

.. _section-7:

`0.2.2`_ - 2017-01-18
---------------------

.. _added-8:

Added
~~~~~

-  Nothing

.. _changed-8:

Changed
~~~~~~~

-  requests.get isn’t a context manager…

.. _section-8:

`0.2.1`_ - 2017-01-18
---------------------

.. _added-9:

Added
~~~~~

-  Nothing

.. _changed-9:

Changed
~~~~~~~

-  Bug fix so we don’t hold a session for quite so long when running
   large queries

First public release of the library ## `0.2.0`_ - 2017-01-15

.. _added-10:

Added
~~~~~

-  API call /content/search
-  API call /content

.. _changed-10:

Changed
~~~~~~~

-  Nothing

.. _Keep a Changelog: http://keepachangelog.com/
.. _Semantic Versioning: http://semver.org/
.. _Unreleased: https://github.com/DaveTCode/confluence-python-lib/compare/0.10.0...HEAD
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