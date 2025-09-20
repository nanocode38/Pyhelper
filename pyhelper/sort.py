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
# modify it under the terms of the GNU Library Public
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# DON'T EVEN HAVE A PERMIT TOO!
#
# Gao Yuhan(高宇涵)
# nanocode24@outlook.com
# nanocode38
"""
A Python function library containing various sorting algorithms
Copyright (C)
"""
from typing import Iterable, Callable, Sized, Protocol
from abc import ABCMeta

__all__ = [
    'sorted_algorithms',
    'sort_algorithms',
    'select_sort',
]

class SizedIterable(Protocol, Iterable, Sized, metaclass=ABCMeta):
    pass

def _timsort_sort(list, *args, **kwargs):
    list.sort(*args, **kwargs)

sorted_algorithms = {'TimSort': sorted}
sort_algorithms = {'TimSort': _timsort_sort}


def _sort_algorithm(func):
    sort_algorithms[func.__name__] = func
    return func

def _sorted_algorithm(func):
    sorted_algorithms[func.__name__] = func
    return func


@_sort_algorithm
def select_sort(seq: SizedIterable, key: Callable = None, reverse: bool = False) -> None:
    """
    Sort in-place with Select Sort

    ===========================
    Select Sort Algorithm
    Time complexity: O(n ^ 2)
    Space complexity: O(1)
    Stable: No
    ===========================

    - Bubble sort, TimSort all options exceed this sort, so this sort will only be used in specific cases,
        and generally do not need to be used.

    Args:
        seq: The iterable to be sorted.
        key: The function to extract a comparison key from each element.
        reverse: Whether to sort in descending order.
    """
    length: int = len(seq)
    k: int = 0
    for i in range(length):
        k = i
        for j in range(i + 1, length):
            if key(seq[j]) < key(seq[k]):
                k = j
        seq[i], seq[k] = seq[k], seq[i]
    return seq if not reverse else seq[::-1]

def select_sorted(seq: SizedIterable, key: Callable = None, reverse: bool = False) -> SizedIterable:
    """
    Sort with Select Sort

    ===========================
    Select Sort Algorithm
    Time complexity: O(n ^ 2)
    Space complexity: O(1)
    Stable: No
    ===========================

    - Bubble sort, TimSort all options exceed this sort, so this sort will only be used in specific cases,
        and generally do not need to be used.

    Args:
        seq: The iterable to be sorted.
        key: The function to extract a comparison key from each element.
        reverse: Whether to sort in descending order.
    """
    return select_sort(seq[:], key=key, reverse=reverse)
