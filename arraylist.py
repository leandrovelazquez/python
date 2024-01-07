# SYSC 2100 Summer 2022 Lab 4
# Last edited: July 13, 2022

"""Class ArrayList implements the List interface from 'Open Data Structures
(in pseudocode)', plus a subset of the operations provided by Python's
built-in list type. The data is stored in a backing array.

Parts of this module were adapted from code from the Open Data Structures
project, opendatastructures.org.

This code (and the code from which it was derived) is released under a
Creative Commons Attribution (CC BY) license. The full text of the license is
available here:

http://creativecommons.org/licenses/by/2.5/ca/
"""
from typing import Any
import ctypes  # To create the backing array.

__author__ = 'Leandro Velazquez'
__student_number__ = '101094885'


class ArrayList:

    def __init__(self, iterable=[]) -> None:
        """Initialize this ArrayList.

        If no argument is given, the ArrayList is empty, with a capacity of 1.
        Otherwise, initialize the ArrayList by adding the values provided by
        the iterable, at the end of the list.

        >>> lst = ArrayList()
        >>> lst
        ArrayList([])
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst
        ArrayList([1, 4, 3, 6])
        """
        self._n = 0  # of elements stored in the ArrayList
        self._elems = _new_array(1)  # backing array

        # Note: len(self._elems) is the capacity of the backing array,
        # which will usually be greater than self._n.

        for elem in iterable:
            self.add(self._n, elem)
            # add() updates self._n and increases the capacity of the
            # backing array, as required.

    def __str__(self) -> str:
        """Return a string representation of this ArrayList.

        >>> lst = ArrayList()
        >>> str(lst)
        '[]'
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> str(lst)
        '[1, 4, 3, 6]'
        """
        # Use repr(x) instead of str(x) in the list comprehension so that
        # elements of type str are enclosed in quotes.
        return "[{0}]".format(", ".join([repr(x) for x in self]))

    def __repr__(self) -> str:
        """Return the canonical string representation of this ArrayList.

        >>> lst = ArrayList()
        >>> repr(lst)
        'ArrayList([])'
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> repr(lst)
        'ArrayList([1, 4, 3, 6])'
        """
        # For an ArrayList object, obj, the expression eval(repr(obj))
        # returns a new ArrayList that is identical to obj.
        return "{0}({1})".format(self.__class__.__name__, str(self))

    def __len__(self) -> int:
        """Return the number of elements in this ArrayList.

        >>> lst = ArrayList()
        >>> len(lst)
        0
        >>> lst = ArrayList([1, 4, 3, 6])
        >>> len(lst)
        4
        """
        return self._n

    def __iter__(self):
        """Return an iterator for this ArrayList.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> for x in lst:
        ...     print(x)
        ...
        1
        4
        3
        6
        """
        for i in range(len(self)):
            yield(self.get(i))

    # The next 6 methods implement the size, get, set, add and remove operations
    # in the ODS List interface, plus the resize backing array operation.
    # These methods implement the pseudocode algorithms presented Section 2.1
    # of the book.
    # DO NOT MODIFY THESE METHODS.

    # size isn't required, given that ArrayList defines __len__, but it's
    # defined here because it's in the List interface.

    def size(self) -> int:
        """Return the number of elements in this ArrayList."""
        return self._n

    def get(self, i: int) -> Any:
        """Return the element at index i in this ArrayList.

        Raise IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list[i] operation, get() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.get(0)
        1
        >>> lst.get(3)
        6
        """
        if i < 0 or i >= self._n:
            raise IndexError('get(i): index out of range')
        return self._elems[i]

    def set(self, i: int, x: Any) -> Any:
        """Replace the element at index i in this ArrayList with x,
        and return the element x replaced.

        Raise IndexError if the index is out of range
        (i < 0 or i >= len(self)).

        Note: Unlike Python's built-in list[i] operation, set() doesn't
        support negative indices.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.set(0, 10)
        1
        >>> lst
        ArrayList([10, 4, 3, 6])
        >>> lst.set(2, 7)
        3
        >>> lst
        ArrayList([10, 4, 7, 6])
        """
        if i < 0 or i >= self._n:
            raise IndexError('set(i, x): index out of range')

        previous = self._elems[i]
        self._elems[i] = x
        return previous

    def add(self, i: int, x: Any) -> None:
        """Insert x at index i in this ArrayList.

        Raise IndexError if the index is out of range
        (i < 0 or i > len(self)).

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.add(0, 10)
        1
        >>> lst
        ArrayList([10, 1, 4, 3, 6])
        >>> len(lst)
        5
        >>> lst.add(2, 7)
        3
        >>> lst
        ArrayList([10, 1, 7, 4, 3, 6])
        >>> len(lst)
        6
        """
        if i < 0 or i > self._n:
            raise IndexError('add(i, x): index out of range')

        if self._n == len(self._elems):
            # The ArrayList is full; double it's capacity.
            self._resize()

        # Shift the element currently at index i (if any) and any subsequent
        # elements, one position to the right, to make room for x.
        self._elems[i + 1:self._n + 1] = self._elems[i:self._n]
        self._elems[i] = x
        self._n += 1

    def remove(self, i: int) -> Any:
        """Remove and return the element at index i in this ArrayList.

        Raise IndexError if the index is out of range.
        (i < 0 or i >= len(self)).

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.remove(0)
        1
        >>> lst
        ArrayList([4, 3, 6])
        >>> len(lst)
        3
        >>> lst.remove(2)
        6
        >>> lst
        ArrayList([4, 3])
        >>> len(lst)
        2
        """
        if i < 0 or i >= self._n:
            raise IndexError('remove(i): index out of range')
        x = self._elems[i]

        # Shift any subsequent elements one position to the left, to close
        # the gap let when x is removed.
        self._elems[i:self._n - 1] = self._elems[i + 1:self._n]
        self._n -= 1

        # Reduce the ArrayList's capacity when two-thirds or more of the
        # backing array is unused.
        if len(self._elems) >= 3 * self._n:
            self._resize()
        return x

    def _resize(self) -> None:
        """Change this ArrayList's capacity to 2 * n, where n is the number of
        elements in the list. If the list is empty, change its capacity to 1.
        """
        # Allocate a new backing array with the required capacity.
        b = _new_array(max(1, 2 * self._n))
        # Initialize the new array with the first n elements of the old one.
        b[0:self._n] = self._elems[0:self._n]
        # Replace the old backing array.
        self._elems = b

    # The next seven methods implement operations that are provided by Python's
    # built-in list type, but aren't part of the ODS List interface.

    def append(self, x: Any) -> None:
        """Append x to the end of this ArrayList.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.append(2)
        >>> lst
        ArrayList([1, 4, 3, 6, 2])
        >>> len(lst)
        5
        """
        self.add(self._n, x)

    def index(self, x: Any) -> int:
        """Return the index of the first occurrence of x in this ArrayList.

        Raise ValueError if x is not in the list.

        >>> lst = ArrayList([10, 20, 30])
        >>> lst.index(10)
        0
        >>> lst.index(20)
        1
        >>> lst.index(40)
        ...
        builtins.ValueError: index(x): 40 is not in the list
        """
        i = 0
        while i != self._n:
            if self._elems[i] == x:
                return i
            else:
                i += 1
        raise ValueError('index(x): ' + str(x) + ' is not in the list')

    def count(self, x: Any) -> int:
        """Return the number of occurrences of x in this ArrayList.

        >>> lst = ArrayList([10, 20, 30, 20])
        >>> lst.count(10)
        1
        >>> lst.count(20)
        2
        >>> lst.count(40)
        0
        """
        i = 0
        c = 0
        while i != self._n:
            if self._elems[i] == x:
                c += 1

            i += 1
        return c

    def __contains__(self, x: Any) -> bool:
        """Return True if x is in this ArrayList; otherwise False.

        >>> lst = ArrayList([10, 20, 30, 20])
        >>> 10 in lst
        True
        >>> 40 in lst
        False
        """
        i = 0
        while i != self._n:
            if self._elems[i] == x:
                return True
            else:
                i += 1

        return False

    def __eq__(self, lst: 'ArrayList') -> bool:
        """Return True if lst equals this ArrayList.

        lst and self are equal iff:
        (1) lst is an ArrayList;
        (2) lst and self contain the same number of items;
        (3) lst[i] == self[i], for all i, 0 <= i < len(lst)

        >>> lst1 = ArrayList([10, 20, 30])
        >>> lst2 = ArrayList([10, 20, 30])
        >>> lst1 == lst2
        True
        >>> tup = (10, 20, 30)  # compare to a tuple with the same elements
        >>> lst1 == tup
        False
        >>> lst2 = ArrayList([10, 20, 30, 20])
        >>> lst1 == lst2
        False
        """
        i = 0
        while i != self._n:
            if self._elems[i] == lst._elems[i]:
                x = 1
            else:
                x = 0
            i += 1

        if (type(self) == type(self)) and (len(self) == len(lst)):
            y = 1
        else:
            y = 2

        return x == y

    def __ne__(self, lst: 'ArrayList') -> bool:
        """Return True if lst is not equal to this ArrayList.
        (List equality is defined by __eq__.)

        >>> lst1 = ArrayList([10, 20, 30])
        >>> lst2 = ArrayList([10, 20, 30])
        >>> lst1 != lst2
        False
        >>> tup = (10, 20, 30)  # compare to a tuple with the same elements
        >>> lst1 != tup
        True
        >>> lst2 = ArrayList([10, 20, 30, 20])
        >>> lst1 != lst2
        True
        """
        if lst == self:
            return False
        else:
            return True

    def clear(self) -> None:
        """Remove all elements from this ArrayList, leaving it empty, with
        capacity 1.

        >>> lst = ArrayList([1, 4, 3, 6])
        >>> lst.clear()
        >>> len(lst)
        0
        >> lst
        ArrayList([])
        """
        self._n = 0  # of elements stored in the ArrayList
        self._elems = _new_array(1)  # backing array


# Pat's new_array function uses numpy. We're using Python's ctypes module,
# so that students don't have to install numpy.

def _new_array(capacity: int) -> 'py_object_Array_<capacity>':
    """Return a new array with the specified capacity that stores
    references to Python objects.
    """
    if capacity <= 0:
        raise ValueError('new_array: capacity must be > 0')
    PyCArrayType = ctypes.py_object * capacity
    a = PyCArrayType()
    for i in range(len(a)):
        a[i] = None
    return a
