"""Exception-reporting helpers and package-specific exception types."""

import inspect
import sys
import traceback
import types
from typing import NoReturn


def raise_error(err: type[Exception] | Exception, *args, level: int = 0, exit_code: int = 1) -> NoReturn:
    """Print an exception with a shortened traceback, then exit the program.

    :param err: An exception instance or exception class to report.
    :param args: Arguments passed to ``err`` when it is an exception class.
    :param level: Number of additional caller frames to omit.
    :param exit_code: Process exit code passed to :func:`sys.exit`.
    """
    print_error(err, *args, level)
    sys.exit(exit_code)


def print_error(err: type[Exception] | Exception, *args, level: int = 0) -> None:
    """Print an exception with internal frames omitted from its traceback.

    :param err: An exception instance or exception class to report.
    :param args: Arguments passed to ``err`` when it is an exception class.
    :param level: Number of additional caller frames to omit.
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
    """Indicate that an object has invalid or incompatible dimensions."""
    __module__ = "builtins"


class UninitializedError(ValueError):
    """Indicate an attempt to access an uninitialized value."""
    __module__ = "builtins"


class __UNSET:
    __module__ = "builtins"

    def __repr__(self):
        return "UNSET"


UNSET = __UNSET()
