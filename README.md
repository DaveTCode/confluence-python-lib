[![Build Status](https://travis-ci.org/DaveTCode/confluence-python-lib.svg?branch=master)](https://travis-ci.org/DaveTCode/confluence-python-lib)

# Comala Workflow Python Library

This is a simple wrapper around the REST API which the Confluence provides.

## Installation

~~~~
pip install confluence-rest
~~~~

## Usage

```python
from confluence.client import Confluence
c = Confluence('https://site:8080/confluence', ('user', 'pass'))
pages = c.search('ID=1')
```

## Development and Deployment

See the [Contribution guidelines for this project](CONTRIBUTING.md) for details on how to make changes to this library.