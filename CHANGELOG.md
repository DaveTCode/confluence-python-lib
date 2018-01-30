# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added
- Nothing

### Changed
- Nothing

## [0.7.0] - 2017-01-30

### Added
- Added basic support for updating content
- Many more of the fields on content objects are now stored when they're expanded

### Changed
- Major overhaul of the content based objects to better match the API provided

## [0.6.0] - 2017-01-26

### Added
- Added longtask endpoints
- A markdown file containing all endpoints with their current state

### Changed
- client.spaces is renamed to client.get_spaces in keeping with other endpoints

## [0.5.0] - 2017-01-26

### Added
- Added support for python 2.7 & 3.5
- Added unit tests to verify the models are basically created how you'd expect 

### Changed
- Nothing

## [0.3.0] - 2017-01-18

### Added
- Can now be treated as a context manager holding a single session for the duration
 of the class.
- README converted to RST for pypi

### Changed
- Nothing

## [0.2.2] - 2017-01-18

### Added
- Nothing

### Changed
- requests.get isn't a context manager...

## [0.2.1] - 2017-01-18

### Added
- Nothing

### Changed
- Bug fix so we don't hold a session for quite so long when running large queries

First public release of the library
## [0.2.0] - 2017-01-15

### Added
- API call /content/search
- API call /content

### Changed
- Nothing

[Unreleased]: https://github.com/DaveTCode/confluence-python-lib/compare/0.7.0...HEAD
[0.7.0]: https://github.com/DaveTCode/confluence-python-lib/compare/0.6.0...0.7.0
[0.6.0]: https://github.com/DaveTCode/confluence-python-lib/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/DaveTCode/confluence-python-lib/compare/0.3.0...0.5.0
[0.3.0]: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.2...0.3.0
[0.2.1]: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/DaveTCode/confluence-python-lib/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/DaveTCode/confluence-python-lib/compare/0.0.1...0.2.0