from typing import List, Iterable, Any
from .error import *
from .utils import getType


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
            raise_error(TypeError, f"Unsupported operand type(s) for =: Queue and {getType(other)}")
        return self.toList() == other.toList()

    def toList(self) -> List[Any]:
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
            raise_error(TypeError, f"Unsupported operand type(s) for =: Stack and {getType(other)}")
        return self.toList() == other.toList()

    def toList(self) -> List[Any]:
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
            raise_error(TypeError, f"Unsupported operand type(s) for =: LinkedListNode and {getType(other)}")
        return self.toList() == other.toList()

    def __add__(self, other: "LinkedListNode"):
        """
        Concatenate two Linked lists Together
        :param other:
        :return:
        """
        if not isinstance(other, LinkedListNode):
            raise_error(TypeError, f"unsupported operand type(s) for +: 'LinkedListNode' and {getType(other)}")
        temp = self
        while temp.next is not None:
            temp = temp.next
        temp.next = other
        return self

    def toList(self) -> List[Any]:
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


def create_linkedlist_from_list(lst: List[Any]) -> LinkedListNode:
    """
    create a linked list from a non-empty ``list``
    :param lst: The list
    :return: The linked list
    """
    if not isinstance(lst, Iterable):
        raise_error(TypeError, f"{getType(lst)} object is not iterable")
    if len(lst) == 0:
        raise_error(IndexError, f"Creating an empty linked list is unsupported now")
    node = LinkedListNode(lst[0])
    temp = node
    for i in lst[1:]:
        temp.next = LinkedListNode(i)
        temp = temp.next
    return node


def create_stack_from_list(lst: list, Fixedlength: bool = True) -> Stack:
    """
    create a stack from a ``list``
    :param Fixedlength: Indicate if the stack has a fixed length
    :param lst: The list
    :return: The stack
    """
    if not isinstance(lst, Iterable):
        raise_error(TypeError, f"{getType(lst)} object is not iterable")

    if Fixedlength:
        stack = Stack(len(lst))
    else:
        stack = Stack()
    for i in lst:
        stack.push(i)
    return stack


def create_queue_from_list(lst: list, Fixedlength: bool = True):
    """
    create a queue from a ``list``
    :param Fixedlength: Indicate if the queue has a fixed length
    :param lst: The list
    :return: The queue
    """
    if not isinstance(lst, Iterable):
        raise_error(TypeError, f"{getType(lst)} object is not iterable")

    if Fixedlength:
        queue = Queue(len(lst))
    else:
        queue = Queue()
    for i in lst:
        queue.push(i)
    return queue
