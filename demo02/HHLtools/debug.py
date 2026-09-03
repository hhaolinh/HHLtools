import inspect
import traceback
from sys import getrecursionlimit
from typing import ParamSpec, TypeVar, Callable, Any
from .error import raise_error
from .prettyprint import prints, FontColor, FontStyle, TreeConnectors
from .utils import getType

P = ParamSpec("P")
R = TypeVar("R")


def callingStack(depth: int = None):
    """
    Display the calling stack whenever the decorated function is called
    :param depth: Maximum depth of the stack
    :return: The decorated function
    """
    if isinstance(depth, Callable):
        return callingStack()(depth)

    if depth is not None and type(depth) is not int:
        raise_error(TypeError, f"callingStack() takes integer argument(s) but {getType(depth)} was given")

    if depth is None or depth < 0:
        depth = float("inf")

    def inner(f: Callable[P, R]) -> Callable[P, R]:

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
            _printDebugMessage("HHLtools.debug:")
            _printDebugMessage("Calling stack (most recent call last):")
            while frame.f_back and d > 0:
                frame = frame.f_back
                info = traceback.extract_stack(frame, 1)[0]
                _printDebugMessage(f"  File \"{info.filename}\", line {info.lineno}, in {info.name}")
                _printDebugMessage(f"    {info.line}")
                d -= 1
            _printDebugMessage(f"Return value: {ret}")
            return ret

        return wrapper

    return inner


def _printDebugMessage(message: str) -> None:
    prints(message, fontColor=FontColor.YELLOW, fontStyle=FontStyle.BOLD)


def printObj(obj: object, depth: int | None = None) -> None:
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
    _printObj(obj, depth=depth)


def _printObj(obj: object, prefix: str = "", children_prefix: str = "", name: str | None = None,
              depth: int = 0) -> None:
    print(prefix, end="")
    attributes = _getattrs(obj)
    if attributes is None:
        print(repr(obj) if name is None else f"{name} = {obj!r}")
        return

    if depth == 0:
        print(f"{obj}..." if name is None else f"{name}: {obj}...")
        return

    print(getType(obj) if name is None else f"{name}: {getType(obj)}")
    depth -= 1

    for i, (varName, val) in enumerate(attributes.items()):
        last = i == len(attributes) - 1
        branch = TreeConnectors.SHORT if last else TreeConnectors.LONG
        continuation = TreeConnectors.CONTINUATION if last else TreeConnectors.STRAIGHT
        _printObj(val, children_prefix + branch, children_prefix + continuation, varName, depth)


def _getattrs(obj: object) -> dict[str, Any] | None:
    if hasattr(obj, "__dict__"):
        attributes = vars(obj)
    elif isinstance(obj, list):
        attributes = dict((f"[{i}]", obj[i]) for i in range(len(obj)))
    else:
        attributes = None
    return attributes
