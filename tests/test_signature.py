import functools
import inspect
from typing import Any, Callable, TypeVar, cast

import pytest

import inspect313

_Func = TypeVar("_Func", bound=Callable[..., Any])


def _decorator(func: _Func) -> _Func:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return cast(_Func, wrapper)


def _function(
    a: int,
    /,
    b: str,
    c: int = 0,
    *d,
    e: bool,
    f: bool = True,
    **kwargs,
) -> None:
    """Function to test."""


@_decorator  # will have `__wrapped__` set
def _decorated_function(a: int, /, b: str) -> None: ...


class _Class:
    def __init__(self, default: int = 0) -> None: ...

    def __call__(self, c: int, *, d: str) -> None: ...

    def method(self, e, /, *args, **kwargs) -> None: ...

    @staticmethod
    def st(arg1: int, /, arg2: str) -> None: ...

    @classmethod
    def cl(cls, arg3: int, /, *, arg4: str = "a") -> None: ...


@pytest.mark.parametrize(
    "obj",
    [
        _function,
        _decorated_function,
        _Class,
        _Class(),
        _Class.method,
        _Class().method,
        _Class.st,
        _Class().st,
        _Class.cl,
        _Class().cl,
    ],
)
def test_signature_default(obj) -> None:
    """Test default arguments."""
    assert inspect.signature(obj) == inspect313.signature(obj)
    assert inspect.Signature.from_callable(
        obj,
    ) == inspect313.Signature.from_callable(obj)


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        (
            _function,
            "(a: int, /, b: str, c: int = 0, *d, e: bool, f: bool = True, **kwargs) -> None",
        ),
        (_decorated_function, "(*args, **kwargs) -> None"),
        (_Class, "(self, default: int = 0) -> None"),
        (_Class(), "(self, c: int, *, d: str) -> None"),
        (_Class.method, "(self, e, /, *args, **kwargs) -> None"),
        (_Class().method, "(self, e, /, *args, **kwargs) -> None"),
        (_Class.st, "(arg1: int, /, arg2: str) -> None"),
        (_Class().st, "(arg1: int, /, arg2: str) -> None"),
        (_Class.cl, "(cls, arg3: int, /, *, arg4: str = 'a') -> None"),
        (_Class().cl, "(cls, arg3: int, /, *, arg4: str = 'a') -> None"),
    ],
)
def test_signature_to_migrate(obj, expected: str) -> None:
    """Test that you keep bound args."""
    assert (
        str(
            inspect313.signature(
                obj, skip_bound_arg=False, follow_wrapped=False
            )
        )
        == expected
    )
    assert (
        str(
            inspect313.Signature.from_callable(
                obj, skip_bound_arg=False, follow_wrapped=False
            )
        )
        == expected
    )
