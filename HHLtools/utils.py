"""Internal helpers shared by the package's public modules."""

from typing import Any
from .error import raise_error, UNSET


def get_type_name(obj: object) -> str:
    """Return the name of an object's concrete type.

    :param obj: The object to inspect.
    :return: The unqualified name of ``type(obj)``.
    """
    return f"{type(obj).__name__}"


def get_type_name_from_annotation(annotation: Any) -> str:
    """Return the name exposed by a type annotation.

    :param annotation: An annotation with a ``__name__`` attribute.
    :return: The annotation's name.
    """
    return annotation.__name__


def check_type_from_annotation(annotation: Any, obj: object) -> bool | None:
    """Check whether an object satisfies a supported type annotation.

    ``typing.Any`` accepts every value. The ``UNSET`` sentinel is also accepted
    for every annotation. Parameterized annotations are not yet supported.

    :param annotation: The annotation against which to check the object.
    :param obj: The object to check.
    :return: ``True`` if the object matches, otherwise ``False``.
    :raises NotImplementedError: If the annotation is unsupported.
    """
    if annotation is Any or obj is UNSET:
        return True

    if isinstance(annotation, type):
        return isinstance(obj, annotation)

    error = NotImplementedError(f"Type {annotation} has not been supported yet")
    raise error
