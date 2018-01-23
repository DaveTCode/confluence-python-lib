[![Build Status](https://travis-ci.org/DaveTCode/confluence-python-lib.svg?branch=master)](https://travis-ci.org/DaveTCode/confluence-python-lib)
[![PyPI version](https://badge.fury.io/py/confluence-rest-library.svg)](https://badge.fury.io/py/confluence-rest-library)

# Confluence Python Library

This is a simple wrapper around the REST API which the Confluence provides.

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