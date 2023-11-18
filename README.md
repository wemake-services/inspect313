# inspect313

[![Build Status](https://github.com/wemake-services/inspect313/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/inspect313/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/wemake-services/inspect313/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-services/inspect313)
[![Python Version](https://img.shields.io/pypi/pyversions/inspect313.svg)](https://pypi.org/project/inspect313/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Backport of `insect` module from Python3.13

## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)
- Add yours!

## Installation

```bash
pip install inspect313
```

## Example

Showcase how your project can be used:

```python
from inspect313.example import some_function

print(some_function(3, 4))
# => 7
```

## License

[MIT](https://github.com/wemake-services/inspect313/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [fd12a6bfd37eeb665fd971e7f92bf429b974b8fb](https://github.com/wemake-services/wemake-python-package/tree/fd12a6bfd37eeb665fd971e7f92bf429b974b8fb). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/fd12a6bfd37eeb665fd971e7f92bf429b974b8fb...master) since then.
