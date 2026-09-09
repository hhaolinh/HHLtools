"""Small helpers for functions, vectors, and lines."""

from .error import raise_error, DimensionError
from .utils import get_type_name


class Function:
    """Represent a real-valued function of one variable.

    :param expression: Python expression used to evaluate the function.
    :param variable: Variable name to substitute in ``expression``.

    .. warning::
       Expressions are evaluated with :func:`eval`. Do not use untrusted input.
    """

    def __init__(self, expression: str, variable: str):
        if type(expression) is not str:
            raise_error(TypeError, f"the expression must be a string, not {get_type_name(expression)}")
        if type(variable) is not str:
            raise_error(TypeError, f"the variable must be a string, not {get_type_name(expression)}")
        self.__expression = expression
        self.__var = variable

    def evaluate(self, value: int | float) -> int | float:
        """Evaluate the function at a given value.

        :param value: Value to substitute for the function's variable.
        :return: The evaluated result.
        """
        if type(value) not in (int, float):
            raise_error(TypeError, f"the value must be an integer, or a real number, not {get_type_name(value)}")
        expression = self.__expression.replace(self.__var, str(value))
        return eval(expression)

    def gradient(self, accuracy: float, value: int | float) -> float:
        """Approximate the function's gradient at a point.

        The implementation uses a forward finite difference with a step of
        ``10 ** -accuracy``.

        :param accuracy: Exponent controlling the finite-difference step.
        :param value: Point at which to approximate the gradient.
        :return: The approximated gradient, rounded to one or three decimal
            places.
        """
        if type(value) not in (int, float):
            raise_error(TypeError, f"the value must be an integer, or a real number, not {get_type_name(value)}")
        if type(accuracy) is not float:
            raise_error(TypeError, f"the acuuracy must be a real number, not {get_type_name(value)}")
        x1 = value
        x2 = value + 10 ** -accuracy
        y1 = self.evaluate(x1)
        y2 = self.evaluate(x2)
        res = (y2 - y1) / (x2 - x1)
        return round(res, 1) if res - int(res) > 0.999 or res - int(res) < 0.001 else round(res, 3)


class Vector:
    """Represent a two- or three-dimensional vector.

    :param dimensions: Components in the ``i``, ``j``, and optional ``k``
        directions.
    """

    def __init__(self, dimensions: list):
        if len(dimensions) != 2 and len(dimensions) != 3:
            raise_error(DimensionError, f'expected 2 or 3 dimensions, got {len(dimensions)}')
        self.dimensions = dimensions

    def __repr__(self):
        return f'Vector({self.dimensions})'

    def __len__(self):
        return len(self.dimensions)

    def __eq__(self, other: "Vector"):
        if not isinstance(other, Vector):
            raise_error(TypeError, f"unsupported operand type(s) for =: 'Vector' and {get_type_name(other)}")
        return self.dimensions == other.dimensions

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise_error(TypeError, f"unsupported operand type(s) for +: 'Vector' and {get_type_name(other)}")
        if len(self) is not len(other):
            raise_error(DimensionError, f'unsupported operand dimension(s) for +: Vectors of different dimensions')
        res = [self.dimensions[i] + other.dimensions[i] for i in range(len(self))]
        return Vector(res)

    def __sub__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise_error(TypeError, f"unsupported operand type(s) for -: 'Vector' and {get_type_name(other)}")
        if len(self) != len(other):
            raise_error(DimensionError, f"unsupported operand dimension(s) for -: Vectors of different dimensions")
        res = [self.dimensions[i] - other.dimensions[i] for i in range(len(self))]
        return Vector(res)

    def __mul__(self, other: "Vector" | int) -> "Vector" | int:
        if isinstance(other, int):
            return Vector([other * i for i in self.dimensions])
        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise_error(DimensionError, f"unsupported operand dimension(s) for *: Vectors of different dimensions")
            return sum([self.dimensions[i] * other.dimensions[i] for i in range(len(self))])
        else:
            raise_error(TypeError, f"unsupported operand type(s) for *: 'Vector' and {get_type_name(other)}")

    def __rmul__(self, other: "Vector" | int) -> "Vector" | int:
        if isinstance(other, int):
            return Vector([other * i for i in self.dimensions])
        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise_error(DimensionError, f"unsupported operand dimension(s) for *: Vectors of different dimensions")
            return sum([self.dimensions[i] * other.dimensions[i] for i in range(len(self))])
        else:
            raise_error(TypeError, f"unsupported operand type(s) for *: {get_type_name(other)} and 'Vector'")

    def __abs__(self) -> int:
        return sum([i ** 2 for i in self.dimensions]) ** (1 / 2)

    def __matmul__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            raise_error(TypeError, f"unsupported operand type(s) for @: 'Vector' and {get_type_name(other)}")
        if len(self.dimensions) != 3 or len(other.dimensions) != 3:
            raise_error(DimensionError, f"unsupported operand dimension(s) for @: Not 3 dimension Vector(s)")
        x = self.dimensions[1] * other.dimensions[2] - self.dimensions[2] * other.dimensions[1]
        y = self.dimensions[2] * other.dimensions[0] - self.dimensions[0] * other.dimensions[2]
        z = self.dimensions[0] * other.dimensions[1] - self.dimensions[1] * other.dimensions[0]
        return Vector([x, y, z])


class Line:
    """Represent a three-dimensional line in vector form.

    :param position: Position vector of a point on the line.
    :param direction: Direction vector of the line.
    :param scalar: Unique symbol used for the line's scalar parameter.
    """

    _chars = []

    def __init__(self, position: Vector, direction: Vector, scalar: str):
        if len(position) != 3:
            raise_error(DimensionError, f'expected 3 dimensions, got {len(position)}')
        if len(direction) != 3:
            raise_error(DimensionError, f'expected 3 dimensions, got {len(direction)}')
        chars = self.__class__._chars
        if scalar in chars:
            raise_error(NameError, f"duplicated scalar symbol {scalar}")
        chars.append(scalar)
        self.position = position
        self.direction = direction
        self.scalar = scalar

    def __repr__(self) -> str:
        pos = self.position.dimensions
        di = self.direction.dimensions
        return f'({pos[0] if pos[0] != 1 else ""}i+' \
               f'{pos[1] if pos[1] != 1 else ""}j+' \
               f'{pos[2] if pos[2] != 1 else ""}k) + ' \
               f'{self.scalar}' \
               f'({di[0] if di[0] != 1 else ""}i+' \
               f'{di[1] if di[1] != 1 else ""}j+' \
               f'{di[2] if di[2] != 1 else ""}k)'
