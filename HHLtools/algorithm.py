"""General-purpose algorithms."""

from typing import TypeVar, Sequence
from .error import raise_error
from .utils import get_type_name

T = TypeVar("T")


def binary_search(seq: Sequence[T], target: T) -> int:
    """Find ``target`` in an ascending, sorted sequence.

    The sequence's elements must be comparable with ``target``. If the target
    occurs more than once, the index of any matching element may be returned.

    :param seq: The sorted sequence to search.
    :param target: The value to search for.
    :return: The target's index, or ``-1`` if it is not present.
    """
    if not isinstance(seq, Sequence):
        raise_error(TypeError, f"{get_type_name(seq)} object is not a Sequence")
    highIndex = len(seq) - 1
    lowIndex = 0
    while lowIndex <= highIndex:
        mid = (highIndex + lowIndex) // 2
        if seq[mid] == target:
            return mid
        elif seq[mid] > target:
            highIndex = mid - 1
        else:
            lowIndex = mid + 1
    return -1
