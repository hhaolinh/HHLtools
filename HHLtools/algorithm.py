from typing import TypeVar, Sequence
from .error import raise_error
from .utils import get_type_name

T = TypeVar("T")


def binary_search(seq: Sequence[T], target: T) -> int:
    """
    Find an occurrence of a target in a sorted sequence using binary search.
    The sequence must be sorted in ascending order, and its elements must be mutually comparable with the target.

    :param seq: The sorted sequence to search
    :param target: The value to search for
    :return: The index of the target, or -1 if target is not Found
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
