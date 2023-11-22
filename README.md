# inspect313

[![test](https://github.com/wemake-services/inspect313/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/wemake-services/inspect313/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/inspect313.svg)](https://pypi.org/project/inspect313/)

Backport of `inspect` module from Python3.13, supports Python 3.8+

## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)
- Has backported `skip_bound_arg` argument to `signature` and `Signature.from_callable`

## Installation

```bash
pip install inspect313
```

## Examples

### Replace `inspect.getfullargspec` with `inspect.Signature`

`getfullargspec` is an old way of getting the function signature.
It is [deprecated](https://github.com/python/cpython/issues/108901) since Python 3.13,
and new `skip_bound_arg: bool = True` argument was introduced in the same version.

However, this change was not backported, so users of older Python versions
need this package to have the same functionality.

Here's how `getfullargspec` is different from regular `signature` call:

- the `self` / `cls` parameter is always reported, even for bound methods

```python
>>> import inspect

>>> class A:
...    def method(self, arg: int) -> None: ...

>>> inspect.getfullargspec(A().method)
FullArgSpec(args=['self', 'arg'], varargs=None, varkw=None, defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={'return': None, 'arg': <class 'int'>})

>>> # signature() produces a different result:
>>> inspect.signature(A().method)
<Signature (arg: int) -> None>

```

- wrapper chains defined by `__wrapped__` *not* unwrapped automatically

```python
>>> import functools

>>> def some_decorator(f):
...     @functools.wraps(f)
...     def wrapper(*args, **kwargs):
...         return f(*args, **kwargs)
...     return wrapper

>>> @some_decorator
... def func(a: int, /, b: str) -> None: ...

>>> inspect.getfullargspec(func)
FullArgSpec(args=[], varargs='args', varkw='kwargs', defaults=None, kwonlyargs=[], kwonlydefaults=None, annotations={'return': None})

>>> # signature() produces a different result:
>>> inspect.signature(func)
<Signature (a: int, /, b: str) -> None>

```

Here's how you can migrate, these results will be in line with `getfullargspec`:

```python
>>> import inspect313

>>> inspect313.signature(
...    A().method, 
...    skip_bound_arg=False, 
...    follow_wrapped=False,
... )
<Signature (self, arg: int) -> None>

>>> inspect313.signature(
...    func, 
...    skip_bound_arg=False, 
...    follow_wrapped=False,
... )
<Signature (*args, **kwargs) -> None>

```

## License

[MIT](https://github.com/wemake-services/inspect313/blob/master/LICENSE)
