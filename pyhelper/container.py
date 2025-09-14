# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#   ___      _  _     _
#  | _ \_  _| || |___| |_ __  ___ _ _
#  |  _/ || | __ / -_) | '_ \/ -_) '_|
#  |_|  \_, |_||_\___|_| .__/\___|_|
#       |__/           |_|

#
# Pyhelper - Packages that provide more helper tools for Python
# Copyright (C) 2023-2024   Gao Yuhan(高宇涵)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation;
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# DON'T EVEN HAVE A PERMIT TOO!
#
# Gao Yuhan(高宇涵)
# anocode38@88.com
# nanocode38

"""
A Python module for supplementing the collections module
Copyright (C)
"""
from collections import UserList
from collections.abc import Iterable
import bisect
from typing import Any

__all__ = [
    'SortedList'
]

class SortedList(UserList):
    """
    A sorted list class that inherits from UserList.

    Args:
        data: An optional iterable of elements to initialize the list with.
        key: An optional function that takes an element as input and returns a value to sort by. Defaults to lambda x: x.

    Examples:
        >>> sorted_list = SortedList([3, 1, 2])
        >>> sorted_list
        SortedList([1, 2, 3])
        >>> str(sorted_list)
        'SortedList([1, 2, 3])'
        >>> 1 in sorted_list
        True
        >>> 4 in sorted_list
        False
        >>> sorted_list[0]
        1
        >>> sorted_list[1]
        2
        >>> sorted_list[2]
        3
        >>> sorted_list[3]
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        >>> sorted_list[::-1]
        SortedList([1, 2, 3])
        >>> sorted_list[0] = 9
        >>> sorted_list
        SortedList([2, 3, 9])
        >>> list(sorted_list)[::-1]
        [9, 3, 2]
        >>> sorted_list += [4, 5, 6]
        >>> sorted_list
        SortedList([2, 3, 4, 5, 6, 9])
        >>> sorted_list + [7, 8, 9]
        SortedList([2, 3, 4, 5, 6, 7, 8, 9, 9])
        >>> sorted_list + 1
        SortedList([1, 2, 3, 4, 5, 6, 9])
        >>> sorted_list += 1
        >>> sorted_list
        SortedList([1, 2, 3, 4, 5, 6, 9])
        >>> sorted_list * 2
        SortedList([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 9, 9])
        >>> sorted_list *= 2
        >>> sorted_list
        SortedList([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 9, 9])
    """
    def __init__(self, data=None, *, key=lambda x: x):
        super().__init__(data)
        self.key = key
        self._sort(key=self.key)

    def __repr__(self):
        return f"SortedList({self.data!r})"

    def __str__(self):
        return f"SortedList({self.data})"

    def __contains__(self, item):
        key_value = self.key(item)
        index = bisect.bisect_left([self.key(elem) for elem in self.data], key_value)
        return index < len(self.data) and self.key(self.data[index]) == key_value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._sort(key=self.key)

    def __add__(self, other: Any):
        copy = self[:]   # Copy the original list
        if isinstance(other, Iterable):
            for item in other:
                copy.add(item)
        else:
            copy.add(other)
        return copy

    def __iadd__(self, other):
        copy = self   # Copy the original list
        if isinstance(other, Iterable):
            for item in other:
                copy.add(item)
        else:
            copy.add(other)
        return copy

    def __mul__(self, other):
        ret = []
        for val in self.data:
            for i in range(other):
                ret.append(val)
        return type(self)(ret)

    __rmul__ = __mul__

    def __imul__(self, other):
        ret = []
        for val in self.data:
            for i in range(other):
                ret.append(val)
        self.data = ret
        return self

    def __copy__(self):
        return self.__class__(self)

    def add(self, item: Any) -> None:
        """
        Insert elements into an ordered list to keep the list organized        Args:

        Args:
            item: Elements that need to be inserted

        Examples:
            >>> sorted_list = SortedList([1, 2, 4])
            >>> sorted_list.add(5)
            >>> sorted_list.add(3)
            >>> sorted_list
            SortedList([1, 2, 3, 4, 5])

        """
        bisect.insort(self.data, item, key=self.key)

    def append(self, item) -> None:
        """
        The secondary method is equivalent to the add() method, just to maintain consistency with the list class, please avoid using it.
        For detailed documentation, see the add() method.

        Args:
            item: Elements that need to be inserted
        """
        self.add(item)

    def _sort(self, key=lambda x: x):
        self.data.sort(key=key)

    def sort(self, /, *args, **kwargs):
        raise NotImplementedError("You Can't Call SortedList.sort()!! This Class didn't has sort() method!")

    def insert(self, index, item) -> None:
        """
        A method that remains forward compatible should use the add() method.
        The index parameter of this method is useless and only takes up place.

        Args:
            index: Useless, to maintain forward compatible placeholder parameters
            item: Data to be inserted

        Examples:
            >>> sorted_list = SortedList([1, 2, 4])
            >>> sorted_list.insert(None, 5)
            >>> sorted_list.insert(None, 3)
            >>> sorted_list
            SortedList([1, 2, 3, 4, 5])

        """
        self.add(item)

    def pop(self, i:None=None) -> Any:
        """
        Remove and return the element at the given index.

        Args:
            i: Useless, used to placeholder to keep it consistent with the list, use the default value.

        Returns:
            Elements that are popped up

        Examples:
            >>> sorted_list = SortedList([1, 2, 3])
            >>> sorted_list.pop()
            3
            >>> sorted_list
            SortedList([1, 2])
        """

        return self.data.pop()

    def clear(self) -> None:
        """
        Clear all element in the list.

        Examples:
            >>> sorted_list = SortedList([1, 2, 3])
            >>> sorted_list.clear()
            >>> sorted_list
            SortedList([])
        """
        self.data.clear()

    def copy(self) -> 'SortedList':
        """
        Return a shallow copy of the list.

        Returns:
            A shallow copy of the list.
        """
        return self.__class__(self)

    def reverse(self):
        raise NotImplementedError("You Can't Call SortedList.reverse()!! This Class didn't has reverse() method!")

    def extend(self, other) -> None:
       """
        The secondary method is equivalent to the add() method, just to maintain consistency with the list class, please avoid using it.
        For detailed documentation, see the add() method.

        Args:
            other: Elements that need to be inserted
       """
       self.add(other)



if __name__ == '__main__':
    # Run the test
    import doctest
    doctest.testmod(verbose=True)
