import inspect
import sys
import traceback
import types
from typing import NoReturn, Any


def raise_error(err: type[Exception], *args: Any, level: int = 0, exit_code: int = 1) -> NoReturn:
    """
    Raise an exception while hiding the raising function from the traceback.
    :param err: The exception type to raise
    :param args: Arguments passed to the exception constructor
    :param level: The number of extra frames to be removed in the calling stack
    :param exit_code: The exit code of the program
    """
    try:
        raise err(*args)
    except Exception as e:
        frame = inspect.currentframe()
        frame = frame.f_back if frame is not None else None
        frame = frame.f_back if frame is not None else None
        for _ in range(level):
            if frame is None:
                break
            frame = frame.f_back

        tb = None
        while frame is not None:
            tb = types.TracebackType(
                tb_next=tb,
                tb_frame=frame,
                tb_lasti=frame.f_lasti,
                tb_lineno=frame.f_lineno
            )
            frame = frame.f_back

        traceback.print_exception(type(e), e, tb)
        sys.exit(exit_code)


class DimensionError(Exception):
    """
    Error caused by unaccepted dimensions for objects with dimensions
    """
    __module__ = "builtins"


class UninitializedError(ValueError):
    """
    Error caused by accessing an uninitialized item
    """
    __module__ = "builtins"
