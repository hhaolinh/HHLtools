import inspect
import sys
import traceback
import types
from typing import Never


def raise_error(err: type[Exception], *args: object) -> Never:
    """
    Raise an exception while hiding the raising function from the traceback.
    :param err: The exception type to raise
    :param args: Arguments passed to the exception constructor
    """
    try:
        raise err(*args)
    except Exception as e:
        currentframe = inspect.currentframe()
        frame = currentframe.f_back
        tb = None
        if frame.f_back is None:
            tb = types.TracebackType(
                tb_next=None,
                tb_frame=frame,
                tb_lasti=frame.f_lasti,
                tb_lineno=frame.f_lineno
            )
        frame = frame.f_back
        while frame is not None:
            tb = types.TracebackType(
                tb_next=tb,
                tb_frame=frame,
                tb_lasti=frame.f_lasti,
                tb_lineno=frame.f_lineno
            )
            frame = frame.f_back
        traceback.print_exception(type(e), e, tb)
        sys.exit(1)


class DimensionError(Exception):
    """
    Dimension mismatch for matrix or vector operation
    """
    pass
