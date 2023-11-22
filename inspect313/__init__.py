from __future__ import annotations

import inspect
import sys
from typing import Any, Callable, Mapping

from typing_extensions import Self, TypeAlias

_IntrospectableCallable: TypeAlias = Callable[..., Any]

if sys.version_info >= (3, 13):
    Signature = inspect.Signature

elif sys.version_info >= (3, 10):

    class Signature(inspect.Signature):
        __doc__ = inspect.Signature.__doc__

        @classmethod
        def from_callable(
            cls,
            obj: _IntrospectableCallable,
            *,
            follow_wrapped: bool = True,
            skip_bound_arg: bool = True,
            globals: Mapping[str, Any] | None = None,
            locals: Mapping[str, Any] | None = None,
            eval_str: bool = False,
        ) -> Self:
            """Constructs Signature for the given callable object."""
            return inspect._signature_from_callable(  # type: ignore[attr-defined]
                obj,
                sigcls=cls,
                follow_wrapper_chains=follow_wrapped,
                skip_bound_arg=skip_bound_arg,
                globals=globals,
                locals=locals,
                eval_str=eval_str,
            )
elif sys.version_info >= (3, 9):

    class Signature(inspect.Signature):
        __doc__ = inspect.Signature.__doc__

        @classmethod
        def from_callable(
            cls,
            obj: _IntrospectableCallable,
            *,
            follow_wrapped: bool = True,
            skip_bound_arg: bool = True,
        ) -> Self:
            """Constructs Signature for the given callable object."""
            return inspect._signature_from_callable(  # type: ignore[attr-defined]
                obj,
                sigcls=cls,
                follow_wrapper_chains=follow_wrapped,
                skip_bound_arg=skip_bound_arg,
            )
else:
    raise RuntimeError(
        "Python version {0}.{1} is not supported".format(*sys.version_info[2:]),
    )


if sys.version_info >= (3, 13):
    signature = inspect.signature

elif sys.version_info >= (3, 10):

    def signature(
        obj: _IntrospectableCallable,
        *,
        follow_wrapped: bool = True,
        skip_bound_arg: bool = True,
        globals: Mapping[str, Any] | None = None,
        locals: Mapping[str, Any] | None = None,
        eval_str: bool = False,
    ) -> Signature:
        """Get a signature object for the passed callable."""
        return Signature.from_callable(
            obj,
            follow_wrapped=follow_wrapped,
            skip_bound_arg=skip_bound_arg,
            globals=globals,
            locals=locals,
            eval_str=eval_str,
        )
elif sys.version_info >= (3, 9):

    def signature(
        obj: _IntrospectableCallable,
        *,
        follow_wrapped: bool = True,
        skip_bound_arg: bool = True,
    ) -> Signature:
        """Get a signature object for the passed callable."""
        return Signature.from_callable(
            obj,
            follow_wrapped=follow_wrapped,
            skip_bound_arg=skip_bound_arg,
        )
