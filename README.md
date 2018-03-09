[![Build Status](https://travis-ci.org/DaveTCode/confluence-python-lib.svg?branch=master)](https://travis-ci.org/DaveTCode/confluence-python-lib)
[![PyPI version](https://badge.fury.io/py/confluence-rest-library.svg)](https://badge.fury.io/py/confluence-rest-library)
[![codecov](https://codecov.io/gh/DaveTCode/confluence-python-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/DaveTCode/confluence-python-lib)

# Confluence Python Library

This is a simple wrapper around the REST API which the Confluence provides.

Note that the library is undergoing major work so don't expect the API to 
be stable until this notice is removed!

c.f. [endpoints.md](endpoints.md) for a list of endpoints and whether this library 
supports them yet. Please do send pull requests if you want an endpoint that isn't covered!

## Installation

~~~~
pip install confluence-rest-library
~~~~

## Usage

```python
from confluence.client import Confluence
with Confluence('https://site:8080/confluence', ('user', 'pass')) as c:
    pages = c.search('ID=1')
```

## Development and Deployment

See the [Contribution guidelines for this project](CONTRIBUTING.md) for details on how to make changes to this library.

### Testing Locally

For now there are only some basic unit tests included. These can be run using
```
python setup.py test
```