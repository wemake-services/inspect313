# Originally copied from
# https://github.com/python/cpython/blob/main/Lib/inspect.py
#
# Modified to be able to backport to earlier versions.

from __future__ import annotations

import inspect
import types
from typing import Any, Callable, Final, Mapping, TypeVar

_Sig = TypeVar("_Sig", bound=inspect.Signature)

_POSITIONAL_ONLY: Final = inspect._POSITIONAL_ONLY  # type: ignore[attr-defined]
_POSITIONAL_OR_KEYWORD: Final = inspect._POSITIONAL_OR_KEYWORD  # type: ignore[attr-defined]
_KEYWORD_ONLY: Final = inspect._KEYWORD_ONLY  # type: ignore[attr-defined]
_VAR_POSITIONAL: Final = inspect._VAR_POSITIONAL  # type: ignore[attr-defined]
_VAR_KEYWORD: Final = inspect._VAR_KEYWORD  # type: ignore[attr-defined]


def signature_from_code(
    cls: type[_Sig],
    func_code: types.CodeType,
    *,
    globals: Mapping[str, Any] | None = None,
    locals: Mapping[str, Any] | None = None,
    eval_str: bool = False,
    is_duck_function: bool = False,
    func: Callable[..., Any] | None = None,
    compute_defaults: bool = False,
) -> _Sig:
    """Private helper: function to get signature from code objects."""
    Parameter = cls._parameter_cls  # type: ignore[attr-defined]

    # Parameter information.
    pos_count = func_code.co_argcount
    arg_names = func_code.co_varnames
    posonly_count = func_code.co_posonlyargcount
    positional = arg_names[:pos_count]
    keyword_only_count = func_code.co_kwonlyargcount
    keyword_only = arg_names[pos_count : pos_count + keyword_only_count]
    if func is not None:
        annotations = inspect.get_annotations(
            func, globals=globals, locals=locals, eval_str=eval_str
        )
        defaults = func.__defaults__
        kwdefaults = func.__kwdefaults__
    else:
        annotations = {}
        if compute_defaults:
            temp_defaults: list[Any] = []
            for name in positional:
                if locals and name in locals:
                    temp_defaults.append(locals[name])
            defaults = tuple(temp_defaults)

            kwdefaults = {}
            for name in keyword_only:
                if locals and name in locals:
                    kwdefaults.update({name: locals[name]})
        else:
            defaults = None
            kwdefaults = None

    if defaults:
        pos_default_count = len(defaults)
    else:
        pos_default_count = 0

    parameters = []

    non_default_count = pos_count - pos_default_count
    posonly_left = posonly_count

    # Non-keyword-only parameters w/o defaults.
    for name in positional[:non_default_count]:
        kind = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
        annotation = annotations.get(name, inspect._empty)
        parameters.append(Parameter(name, annotation=annotation, kind=kind))
        if posonly_left:
            posonly_left -= 1

    # ... w/ defaults.
    for offset, name in enumerate(positional[non_default_count:]):
        assert defaults  # mypy needs this
        kind = _POSITIONAL_ONLY if posonly_left else _POSITIONAL_OR_KEYWORD
        annotation = annotations.get(name, inspect._empty)
        parameters.append(
            Parameter(
                name, annotation=annotation, kind=kind, default=defaults[offset]
            )
        )
        if posonly_left:
            posonly_left -= 1

    # *args
    if func_code.co_flags & inspect.CO_VARARGS:
        name = arg_names[pos_count + keyword_only_count]
        annotation = annotations.get(name, inspect._empty)
        parameters.append(
            Parameter(name, annotation=annotation, kind=_VAR_POSITIONAL)
        )

    # Keyword-only parameters.
    for name in keyword_only:
        default = inspect._empty
        if kwdefaults is not None:
            default = kwdefaults.get(name, inspect._empty)

        annotation = annotations.get(name, inspect._empty)
        parameters.append(
            Parameter(
                name,
                annotation=annotation,
                kind=_KEYWORD_ONLY,
                default=default,
            )
        )
    # **kwargs
    if func_code.co_flags & inspect.CO_VARKEYWORDS:
        index = pos_count + keyword_only_count
        if func_code.co_flags & inspect.CO_VARARGS:
            index += 1

        name = arg_names[index]
        annotation = annotations.get(name, inspect._empty)
        parameters.append(
            Parameter(name, annotation=annotation, kind=_VAR_KEYWORD)
        )

    # Is 'func' is a pure Python function - don't validate the
    # parameters list (for correct order and defaults), it should be OK.
    return cls(
        parameters,
        return_annotation=annotations.get("return", inspect._empty),
        __validate_parameters__=is_duck_function,
    )
