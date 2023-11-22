import inspect
import types

from inspect313 import Signature


def test_signature_from_frame() -> None:
    """Test that `.from_frame` works."""

    def with_defaults(a=1, /, b=2, *e, c: int = 3, d, **f) -> types.FrameType:
        fr = inspect.currentframe()
        assert fr
        return fr

    fr = with_defaults(d=4)
    assert str(Signature.from_frame(fr)) == "(a=1, /, b=2, *e, c=3, d=4, **f)"

    def less_defaults(a, /, b, *e, c: int = 3, d, **f) -> types.FrameType:
        fr = inspect.currentframe()
        assert fr
        return fr

    fr = less_defaults(1, 2, d=4)
    assert str(Signature.from_frame(fr)) == "(a=1, /, b=2, *e, c=3, d=4, **f)"


def test_signature_from_frame_defaults_change() -> None:
    """Test that default are not really defaults."""

    def inner(a=1, /, c=5, *, b=2) -> types.FrameType:
        a = 3  # noqa: F841
        fr = inspect.currentframe()
        b = 4  # noqa: F841
        assert fr
        return fr

    fr = inner()
    assert str(Signature.from_frame(fr)) == "(a=3, /, c=5, *, b=4)"
