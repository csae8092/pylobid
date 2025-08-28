# pylobid

[![Build the docs](https://github.com/csae8092/pylobid/actions/workflows/docs.yml/badge.svg)](https://github.com/csae8092/pylobid/actions/workflows/docs.yml)
[![flake8 Lint](https://github.com/csae8092/pylobid/actions/workflows/lint.yml/badge.svg)](https://github.com/csae8092/pylobid/actions/workflows/lint.yml)
[![Test](https://github.com/csae8092/pylobid/actions/workflows/test.yml/badge.svg)](https://github.com/csae8092/pylobid/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/csae8092/pylobid/graph/badge.svg?token=52C1Z6KJHM)](https://codecov.io/gh/csae8092/pylobid)
[![PyPI version](https://badge.fury.io/py/pylobid.svg)](https://badge.fury.io/py/pylobid)

`pylobid` is a Python LOBID-REST-API client. [Lobid](https://lobid.org) is a web service providing data from the [GND](https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html) - Gemeinsame Normdatei of the German National Library.

- **Free software**: MIT license
- **Documentation**: [https://csae8092.github.io/pylobid/](https://csae8092.github.io/pylobid/)

## Features

- Harmonize GND-URIs and URLs
- Wrap up several LOBID-API requests in single methods
- Validate inputs from WTForms against the LOBID-API

## Development

### run tests
```shell
uv run coverage run -m pytest
uv run coverage report
```

## Credits


* Peter Andorfer <p.andorfer@gmail.com>
* Christian Lölkes <christian.loelkes@gmail.com>

