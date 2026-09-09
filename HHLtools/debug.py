"""Utilities for inspecting calls and object state."""

import inspect
import traceback
from functools import wraps
from sys import getrecursionlimit
from typing import ParamSpec, TypeVar, Callable, Any
from .error import raise_error
from .prettyprint import prints, FontColor, FontStyle, TreeConnectors
from .utils import get_type_name

P = ParamSpec("P")
R = TypeVar("R")


def calling_stack(depth: int = None):
    """Print the call stack after each successful call to a function.

    This decorator can be used either as ``@calling_stack`` or as
    ``@calling_stack(depth)``. A negative depth is treated as unlimited.

    :param depth: Maximum number of stack frames to print. If omitted, print
        all available frames.
    :return: A decorator, or the decorated function when used without
        parentheses.
    """
    if isinstance(depth, Callable):
        return calling_stack()(depth)

    if depth is not None and type(depth) is not int:
        raise_error(TypeError, f"callingStack() takes integer argument(s) but {get_type_name(depth)} was given")

    if depth is None or depth < 0:
        depth = float("inf")

    def inner(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            ret = None
            try:
                ret = f(*args, **kwargs)
            except Exception as e:
                if e.__traceback__ is not None:
                    e.__traceback__ = e.__traceback__.tb_next
                    raise
            frame = inspect.currentframe()
            d = depth
            _print_debug_message("HHLtools.debug:")
            _print_debug_message("Calling stack (most recent call last):")
            while frame.f_back and d > 0:
                frame = frame.f_back
                info = traceback.extract_stack(frame, 1)[0]
                _print_debug_message(f"  File \"{info.filename}\", line {info.lineno}, in {info.name}")
                _print_debug_message(f"    {info.line}")
                d -= 1
            _print_debug_message(f"Return value: {ret}")
            return ret

        return wrapper

    return inner


def _print_debug_message(message: str) -> None:
    prints(message, fontColor=FontColor.YELLOW, fontStyle=FontStyle.BOLD)


def print_obj(obj: object, depth: int | None = None) -> None:
    """Print an object's attributes as a tree.

    Recursive references are marked rather than expanded again.

    :param obj: The object to print.
    :param depth: Maximum expansion depth. If omitted, use Python's recursion
        limit.
    """
    if depth is None:
        depth = getrecursionlimit()
    if depth <= 0:
        print(obj)
        return
    print("\n".join(_format_obj(obj, depth=depth)))


def _format_obj(obj: object, prefix: str = "", children_prefix: str = "", name: str | None = None,
                depth: int = 0, seen: set[str] = None) -> list[str]:
    if seen is None:
        seen = set()
    res = [prefix]
    attributes = _get_attrs(obj)
    if not attributes:
        res[0] += repr(obj) if name is None else f"{name} = {obj!r}"
        return res

    if id(obj) in seen:
        res[0] += f"{TreeConnectors.RECURSION}{obj}" if name is None else f"{TreeConnectors.RECURSION}{name}: {obj}"
        return res

    if depth == 0:
        res[0] += f"{obj}..." if name is None else f"{name}: {obj}..."
        return res

    res[0] += get_type_name(obj) if name is None else f"{name}: {get_type_name(obj)}"
    depth -= 1
    seen.add(id(obj))
    for i, (varName, val) in enumerate(attributes.items()):
        last = i == len(attributes) - 1
        branch = TreeConnectors.SHORT if last else TreeConnectors.LONG
        continuation = TreeConnectors.CONTINUATION if last else TreeConnectors.STRAIGHT
        res += _format_obj(val, children_prefix + branch, children_prefix + continuation, varName, depth, seen)
    seen.remove(id(obj))
    return res


def _get_attrs(obj: object) -> dict[str, Any]:
    attributes = {}
    mro = type(obj).__mro__
    for cls in mro[:-1]:
        if hasattr(cls, "__slots__"):
            slots = cls.__slots__
            if not isinstance(slots, tuple):
                slots = (slots,)
            for key in slots:
                try:
                    attributes[key] = getattr(obj, key)
                except AttributeError:
                    pass
    if hasattr(obj, "__dict__"):
        for key, val in obj.__dict__.items():
            attributes[key] = val
    if isinstance(obj, list):
        attributes = dict((f"[{i}]", obj[i]) for i in range(len(obj)))

    return attributes
