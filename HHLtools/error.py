import inspect
import sys
import traceback
import types
from typing import NoReturn


def raise_error(err: type[Exception] | Exception, *args, level: int = 0, exit_code: int = 1) -> NoReturn:
    """
    Raise an exception while hiding the raising function from the traceback.
    :param err: The exception type to raise
    :param args: Arguments passed to the exception constructor
    :param level: The number of extra frames to be removed in the calling stack
    :param exit_code: The exit code of the program
    """
    print_error(err, *args, level)
    sys.exit(exit_code)


def print_error(err: type[Exception] | Exception, *args, level: int = 0) -> None:
    """
    print an exception while hiding the raising function from the traceback.
    :param err: The exception type to raise
    :param args: Arguments passed to the exception constructor
    :param level: The number of extra frames to be removed in the calling stack
    """
    try:
        if isinstance(err, Exception):
            raise err from None
        raise err(*args) from None
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


class __UNSET:
    __module__ = "builtins"

    def __repr__(self):
        return "UNSET"


UNSET = __UNSET()
