# inspect313

[![test](https://github.com/wemake-services/inspect313/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/wemake-services/inspect313/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/inspect313.svg)](https://pypi.org/project/inspect313/)

Backport of `inspect` module from Python3.13, supports Python 3.8+

## Features

- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)
- Has backported `bound_arg` parameter of `signature` and `Signature.from_callable` [gh-116559](https://github.com/python/cpython/pull/116559)
- Has backported `Signature.from_frame` method

## Installation

```bash
pip install inspect313
```

## Examples

### Replace `inspect.getfullargspec` with `inspect.signature`

`getfullargspec` is an old way of getting the function signature.
It is [deprecated](https://github.com/python/cpython/issues/108901) since Python 3.13,
and new `bound_arg: bool = False` argument was introduced in the same version.

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
...    bound_arg=True,
...    follow_wrapped=False,
... )
<Signature (self, arg: int) -> None>

>>> inspect313.signature(
...    func,
...    bound_arg=True,
...    follow_wrapped=False,
... )
<Signature (*args, **kwargs) -> None>

```

However, consider migrating to just using `inspect.signature`,
since it produces more correct results in a general case.

### Replace `inspect.getargvalues` with `inspect.Signature.from_frame`

`getargvalues` was used to create signature-like objects from frame objects.
But, it didn't really support all features of modern functions.

This is why Python 3.13 introduced `inspect.Signature.from_frame`
public constructor and `getargvalues` and `formatargvalues` were deprecated.

Here's how it worked before:

```python
>>> import inspect

>>> def func(a: int = 0, /, b: int = 1, *, c: int = 2):
...     return inspect.currentframe()

>>> frame = func()
>>> # notice that pos-only and kw-only args are not supported properly:
>>> inspect.formatargvalues(*inspect.getargvalues(frame))
'(a=0, b=1, c=2)'

```

Here's how to replace it with modern API:

```python
>>> from inspect313 import Signature

>>> str(Signature.from_frame(frame))
'(a=0, /, b=1, *, c=2)'

```

## License

[MIT](https://github.com/wemake-services/inspect313/blob/master/LICENSE)
