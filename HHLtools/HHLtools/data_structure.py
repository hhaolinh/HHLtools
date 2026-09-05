from typing import Any, Generic, TypeVar, cast, Self
from math import prod
from .error import raise_error, DimensionError, UninitializedError
from .utils import get_type_name

T = TypeVar("T")


class Queue:
    """
    A LIFO data structure
    """

    def __init__(self, size: int = -1):
        """
        :param size: the fixed size of the queue, infinite length if not set
        """
        if size > 0:
            self.__size = size
            self.__queue = [None] * size
            self.__head = 0
            self.__tail = 0
            self.__count = 0
        else:
            self.__size = -1
            self.__queue = []

    def __repr__(self):
        if self.__size != -1:
            return f'Queue({str(self.__queue)}, ' \
                   f'headPointer = {self.__head if self.__size != -1 else len(self.__queue) - 1}, ' \
                   f'tailPointer = {self.__tail if self.__size != -1 else 0}, Fixedlength = True)'
        else:
            return f'Queue({str(self.__queue)})'

    def __len__(self):
        return self.__count if self.__size != -1 else len(self.__queue)

    def __eq__(self, other: "Queue"):
        if not isinstance(other, Queue):
            raise_error(TypeError, f"Unsupported operand type(s) for =: Queue and {get_type_name(other)}")
        return self.toList() == other.toList()

    def toList(self) -> list[Any]:
        """
        Convert the queue to a ``list``
        :return: the list
        """
        contents = []
        if self.__size == -1:
            contents = self.__queue[:]
        else:
            head = self.__head
            while 1:
                contents.append(self.__queue[head])
                head += 1
                head = head % self.__size
                if head == self.__tail:
                    break
        return contents

    def show(self) -> None:
        """
        Show the queue
        :return:
        """
        contents = self.__queue
        maxlen = 0
        for c in contents:
            if len(str(c)) > maxlen:
                maxlen = len(str(c))
        print('=' * (15 + maxlen + 15))
        for c in range(len(contents)):
            front = ' ' * 15
            end = ' '
            if c == self.__head:
                front = 'headPointer    '
            if c == self.__tail:
                end = (maxlen + 4) * ' ' + 'tailPointer'
            print(front + str(contents[c]) + ' ' * (maxlen - len(str(contents[c]))) + end)
        print('=' * (15 + maxlen + 15))

    def push(self, content: Any) -> None:
        """
        Push an element to the tail of the queue, raise ``IndexError`` if the queue is full
        :param content: The element to be pushed
        :return:
        """
        if self.__size > 0:
            if self.__count == self.__size:
                raise_error(IndexError, 'the queue is full, try pop()')
            self.__queue[self.__tail] = content
            self.__tail = (self.__tail + 1) % self.__size
            self.__count += 1
        else:
            self.__queue.append(content)

    def pop(self) -> Any:
        """
        Get and remove the element from the head of the queue, raise ``IndexError`` if the queue is empty
        :return: The element being popped
        """
        if self.__size > 0:
            if self.__count == 0:
                return None
            tmp = self.__head
            self.__head = (self.__head + 1) % self.__size
            self.__count -= 1
            return self.__queue[tmp]
        else:
            try:
                res = self.__queue[0]
                del self.__queue[0]
                return res
            except IndexError:
                return None


class Stack:
    def __init__(self, size: int = -1):
        """
        A LIFO data structure
        :param size: the fixed size of the stack, if not set, infinite length
        """
        self.a = 0
        if size > 0:
            self.__stack = [None] * size
            self.__size = size
        else:
            self.__stack = []
            self.__size = -1
        self.__top = -1

    def __repr__(self):
        if self.__size != -1:
            return f'Stack({str(self.__stack)}, topPointer = {self.__top})'
        else:
            return f'Stack({str(self.__stack)})'

    def __len__(self):
        return self.__top if self.__size != -1 else len(self.__stack)

    def __eq__(self, other: "Stack"):
        if not isinstance(other, Stack):
            raise_error(TypeError, f"Unsupported operand type(s) for =: Stack and {get_type_name(other)}")
        return self.toList() == other.toList()

    def toList(self) -> list[Any]:
        """
        Convert the stack to a ``list``
        :return: the list
        """
        contents = []
        if self.__size == -1:
            contents = self.__stack[:]
        else:
            for i in range(0, self.__top):
                contents.append(self.__stack[i])
        return contents

    def push(self, content: Any) -> None:
        """
        Push an element to the top of the stack, raise ``IndexError`` if the queue is full
        :param content: The element to be pushed
        :return:
        """
        if self.__size > 0:
            if self.__top < self.__size - 1:
                self.__top += 1
                self.__stack[self.__top] = content
            else:
                raise_error(IndexError, 'the stack is full, try pop()')
        else:
            self.__stack.insert(0, content)

    def pop(self) -> Any:
        """
        Get and remove an element from the top of the stack, raise ``IndexError`` if the queue is full
        :return: The element being popped
        """
        if self.__size > 0:
            if self.__top > -1:
                self.__top -= 1
                return self.__stack[self.__top + 1]
            else:
                return None
        else:
            try:
                res = self.__stack[0]
                del self.__stack[0]
                return res
            except IndexError:
                return None


class LinkedListNode:
    def __init__(self, val):
        """
        A node of a Linked list
        :param val: the value inside the node
        """
        self.val = val
        self.next = None

    def __repr__(self):
        content = []
        temp = self
        while temp.next is not None:
            content.append(temp.val)
            temp = temp.next
        content.append(temp.val)
        return f'LinkedList({content})'

    def __iter__(self):
        cur = self
        while cur.next:
            yield cur.val
            cur = cur.next
        yield cur.val

    def __eq__(self, other: "LinkedListNode"):
        if not isinstance(other, LinkedListNode):
            raise_error(TypeError, f"Unsupported operand type(s) for =: LinkedListNode and {get_type_name(other)}")
        return self.toList() == other.toList()

    def __add__(self, other: "LinkedListNode"):
        """
        Concatenate two Linked lists Together
        :param other:
        :return:
        """
        if not isinstance(other, LinkedListNode):
            raise_error(TypeError, f"unsupported operand type(s) for +: 'LinkedListNode' and {get_type_name(other)}")
        temp = self
        result = LinkedListNode(self.val)
        cur = result
        while temp.next is not None:
            temp = temp.next
            cur.next = LinkedListNode(temp.val)
            cur = cur.next
        temp = other
        while temp is not None:
            cur.next = LinkedListNode(temp.val)
            cur = cur.next
            temp = temp.next
        return result

    def toList(self) -> list[Any]:
        """
        Convert the linked list into a ``list``
        :return: the list
        """
        content = []
        temp = self
        while temp is not None:
            content.append(temp.val)
            temp = temp.next
        return content


class ArrayMeta(type):
    def __call__(cls, *args, **kwargs):
        raise_error(TypeError, "use Array[<lower1>:<upper1>, <lower2>:<upper2>, ...] @ type to create an array")

    def __matmul__(cls, data_type: type[T]) -> "Array[T]":
        array_cls = cast("type[Array[T]]", cls)
        # noinspection PyProtectedMember
        return array_cls._create(data_type)


class Array(Generic[T], metaclass=ArrayMeta):
    __UNSET = object()
    _dimensions: list[tuple[int, int]] | None = None
    __type: type
    __array: list[T]
    __dimensions: list[tuple[int, int]]

    @classmethod
    def _create(cls, data_type: type[T]) -> "Array[T]":
        """
        create an array of type ``data_type`` with given dimensions
        :param data_type: The type of elements in the array
        """
        if cls._dimensions is None:
            raise_error(UninitializedError, "Array must be initialized with its upper bounds and lower bounds", level=1)
        if not isinstance(data_type, type):
            raise_error(ValueError, f"element_type expects a type, got {get_type_name(data_type)} instead", level=1)
        obj = object.__new__(cls)
        obj.__type = data_type
        obj.__array = [cls.__UNSET] * prod([d[1] - d[0] + 1 for d in cls._dimensions])
        obj.__dimensions = cls._dimensions

        return obj

    def __getitem__(self, indices: int | tuple[int, ...]) -> T:
        if not isinstance(indices, tuple):
            indices = (indices,)
        exact_index = self.__get_exact_index(indices)
        if self.__array[exact_index] is self.__UNSET:
            raise_error(UninitializedError, f"Array element at index {list(indices)} is not initialized")
        return self.__array[exact_index]

    def __setitem__(self, indices: int | tuple[int, ...], value: T):
        if not isinstance(indices, tuple):
            indices = (indices,)
        exact_index = self.__get_exact_index(indices)
        if not isinstance(value, self.__type):
            raise_error(TypeError, f"Value of type {self.__type.__name__} expected, got {get_type_name(value)} instead")
        self.__array[exact_index] = value

    def __get_exact_index(self, indices: tuple[int, ...]) -> int:
        if len(indices) != len(self.__dimensions):
            raise_error(DimensionError, f"{len(self.__dimensions)} indices expected, got {len(indices)} instead",
                        level=1)
        exact_index = 0
        for i, index in enumerate(list(indices)):
            cur_dim = self.__dimensions[i]
            if not isinstance(index, int):
                raise_error(TypeError, f"Integer indices expected, got {get_type_name(index)} instead", level=1)
            if not cur_dim[0] <= index <= cur_dim[1]:
                raise_error(IndexError, f"Invalid index, an integer between {cur_dim[0]} and {cur_dim[1]} expected",
                            level=1)
            exact_index = exact_index * (cur_dim[1] - cur_dim[0] + 1) + (index - cur_dim[0])
        return exact_index

    def __class_getitem__(cls, indices: slice | tuple[slice, ...]) -> type[Self]:
        if not isinstance(indices, tuple):
            indices = (indices,)
        if any(not isinstance(index, slice) for index in indices):
            raise_error(TypeError, "Expected form [<lower1>:<upper1>, <lower2>:<upper2>, ...] with <lower i> and "
                                   "<upper i> are integers")
        dimensions = [(index.start, index.stop) for index in indices]
        if len(dimensions) == 0:
            raise_error(DimensionError, "No Dimensions given")
        if any(not isinstance(d, tuple) or len(d) != 2 or not isinstance(d[0], int) or not isinstance(d[1], int)
               or d[0] >= d[1] for d in dimensions):
            raise_error(DimensionError, "Dimensions must be in the form (a, b) with a, b are integers and a < b")
        dimensions_str_list = list(map(lambda index: f"{index[0]}:{index[1]}", dimensions))
        dimensions_str = f"[{', '.join(dimensions_str_list)}]"
        return type(
            f"{cls.__name__}{dimensions_str}",
            (cls,),
            {f"_dimensions": dimensions, "__module__": cls.__module__}
        )

    @property
    def dimensions(self):
        return self.__dimensions


def create_linkedlist_from_list(lst: list[Any]) -> LinkedListNode:
    """
    create a linked list from a non-empty ``list``
    :param lst: The list
    :return: The linked list
    """
    if not isinstance(lst, list):
        raise_error(TypeError, f"{get_type_name(lst)} object is not a list")
    if len(lst) == 0:
        raise_error(IndexError, f"Creating an empty linked list is unsupported now")
    node = LinkedListNode(lst[0])
    temp = node
    for i in lst[1:]:
        temp.next = LinkedListNode(i)
        temp = temp.next
    return node


def create_stack_from_list(lst: list[Any], Fixedlength: bool = True) -> Stack:
    """
    create a stack from a ``list``
    :param Fixedlength: Indicate if the stack has a fixed length
    :param lst: The list
    :return: The stack
    """
    if not isinstance(lst, list):
        raise_error(TypeError, f"{get_type_name(lst)} object is not a list")

    if Fixedlength:
        stack = Stack(len(lst))
    else:
        stack = Stack()
    for i in lst:
        stack.push(i)
    return stack


def create_queue_from_list(lst: list[Any], Fixedlength: bool = True):
    """
    create a queue from a ``list``
    :param Fixedlength: Indicate if the queue has a fixed length
    :param lst: The list
    :return: The queue
    """
    if not isinstance(lst, list):
        raise_error(TypeError, f"{get_type_name(lst)} object is not a list")

    if Fixedlength:
        queue = Queue(len(lst))
    else:
        queue = Queue()
    for i in lst:
        queue.push(i)
    return queue
