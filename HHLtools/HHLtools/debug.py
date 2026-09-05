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
    """
    Display the calling stack whenever the decorated function is called
    :param depth: Maximum depth of the stack
    :return: The decorated function
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
    """
    Print an object in tree-style
    :param obj: The object to be printed
    :param depth: Maximum depth of expansion
    :return:
    """
    if depth is None:
        depth = getrecursionlimit()
    if depth <= 0:
        print(obj)
        return
    print(_format_obj(obj, depth=depth).removesuffix("\n"))


def _format_obj(obj: object, prefix: str = "", children_prefix: str = "", name: str | None = None,
                depth: int = 0, seen: set[str] = None) -> str:
    if seen is None:
        seen = set()
    res = prefix
    attributes = _getattrs(obj)
    if attributes is None or not attributes:
        res += (repr(obj) if name is None else f"{name} = {obj!r}") + "\n"
        return res

    if id(obj) in seen:
        res += (f"{TreeConnectors.RECURSION}{obj}" if name is None else f"{TreeConnectors.RECURSION}{name}: {obj}") + "\n"
        return res

    if depth == 0:
        res += (f"{obj}..." if name is None else f"{name}: {obj}...") + "\n"
        return res

    res += (get_type_name(obj) if name is None else f"{name}: {get_type_name(obj)}") + "\n"
    depth -= 1
    seen.add(id(obj))
    for i, (varName, val) in enumerate(attributes.items()):
        last = i == len(attributes) - 1
        branch = TreeConnectors.SHORT if last else TreeConnectors.LONG
        continuation = TreeConnectors.CONTINUATION if last else TreeConnectors.STRAIGHT
        res += _format_obj(val, children_prefix + branch, children_prefix + continuation, varName, depth, seen)
    seen.remove(id(obj))
    return res

def _getattrs(obj: object) -> dict[str, Any] | None:
    if hasattr(obj, "__dict__"):
        attributes = vars(obj)
    elif isinstance(obj, list):
        attributes = dict((f"[{i}]", obj[i]) for i in range(len(obj)))
    else:
        attributes = None
    return attributes
