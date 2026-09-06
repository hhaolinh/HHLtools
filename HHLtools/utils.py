from typing import Any
from .error import raise_error, UNSET


def get_type_name(obj: object) -> str:
    """
    Get the name of the type of the given object
    :param obj:
    :return:
    """
    return f"{type(obj).__name__}"


def get_type_name_from_annotation(annotation: Any) -> str:
    """
    Get the type name from annotation
    :param annotation:
    :return:
    """
    return annotation.__name__


def check_type_from_annotation(annotation: Any, obj: object) -> bool | None:
    """
    Check the given object has the specified type
    :param annotation: The annotation
    :param obj: The object to be checked
    :return: ``True`` if it passes the type check, ``False`` otherwise
    """
    if annotation is Any or obj is UNSET:
        return True

    if isinstance(annotation, type):
        return isinstance(obj, annotation)

    error = NotImplementedError(f"Type {annotation} has not been supported yet")
    raise error
