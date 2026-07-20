# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#   ___      _  _     _
#  | _ \_  _| || |___| |_ __  ___ _ _
#  |  _/ || | __ / -_) | '_ \/ -_) '_|
#  |_|  \_, |_||_\___|_| .__/\___|_|
#       |__/           |_|

#
# PyHelper - Packages that provide more helper tools for Python
# Copyright (C) 2026-2030  Weixu Zheng(郑维序)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library Public
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# DON'T EVEN HAVE A PERMIT TOO!
#
# Weixu Zheng(郑维序)
# nanocode38@88.com
# nanocode38
"""
A random function library for generating truly random numbers
Copyright (C)
"""

import os
from typing import *

__all__ = ["randint", "choice", "randrange", "shuffle", "sample"]


def random():
    # Use os.urandom to generate 7 bytes of random data
    byte_data = os.urandom(7)
    # Convert byte data to a 53-bit integer
    int_data = int.from_bytes(byte_data, byteorder="big") & ((1 << 53) - 1)
    # Convert to floating point numbers in the range [0.0, 1.0)
    return int_data / (1 << 53)


def randint(min_: int, max_: int | None = None, random: Callable = random):
    """
    Generates a random integer within the inclusive range [min, max].

    This function generates a random integer in the range [min, max] using a
    more secure randomization method based on os.urandom for generating the
    base random seed. It ensures that the generated number is uniformly
    distributed across the specified range.

    Args:
        min_: The lower limit of the range (inclusive).
        max_: The upper limit of the range (inclusive). Must be greater than or equal to min.
        random: Optional parameters for generating random dependency functions, default to random() functions generated using os.urandom()

    Returns:
        int: A random integer within the inclusive range [min, max].

    Raises:
        ValueError: If the min parameter is greater than the max parameter.

    Examples:
        >>> randint(1, 10, random=lambda: 0.0)
        10
        >>> randint(1, 10, random=lambda: 0.5)
        6
        >>> randint(1, 10, random=lambda: 0.99)
        3
        >>> randint(5, 5, random=lambda: 0.5)
        5
        >>> randint(3)  # doctest: +SKIP
    """
    if max_ is None:
        max_ = min_
        min_ = 1

    if min_ > max_:
        raise ValueError("The lower limit should be less than or equal to the upper limit")

    return int(random() * (min_ - max_ + 1)) + max_


def choice(seq: Sequence, random: Callable = random) -> Iterable:
    """
    Select a random element from a non-empty sequence.

    This function selects a random element from the given non-empty sequence.
    It uses the randint function to generate a random index within the range
    of the sequence length.

    Args:
        seq: The non-empty sequence from which to select a random element.
        random: Optional parameters for generating random dependency functions, default to random() functions generated using os.urandom()

    Returns:
        Sized: The randomly selected element from the sequence.

    Raises:
        IndexError: When the sequence provided is empty

    Examples:
        >>> choice([10, 20, 30], random=lambda: 0.0)
        10
        >>> choice([10, 20, 30], random=lambda: 0.5)
        20
        >>> choice([10, 20, 30], random=lambda: 0.99)
        30
        >>> choice("abc", random=lambda: 0.5)
        'b'
        >>> choice([], random=lambda: 0.5)
        Traceback (most recent call last):
            ...
        IndexError: Cannot choose from an empty sequence
    """
    if len(seq) <= 0:
        raise IndexError("Cannot choose from an empty sequence")
    return seq[int(random() * len(seq))]


def randrange(start: int, stop: int = None, step: int = 1, random: Callable = random):
    """
    Return a randomly selected element from the range(start, stop, step).

    This function returns a randomly selected element from the range specified by
    the start, stop, and step parameters. If only one argument is provided, it
    treats it as the stop value and starts from 1 with a step of 1. If no arguments
    are provided, it returns a random integer from the range 0-9.

    Args:
        start: The start of the range. Default is 1.
        stop: The end of the range. Default is the start value.
        step: The step value for the range. Default is 1.
        random: Optional parameters for generating random dependency functions, default to random() functions generated using os.urandom()

    Returns:
        int: A randomly selected element from the specified range.

    Raises:
        ValueError: If the range is empty or step is zero
        ValueError: If the stop value is less than the start value

    Examples:
        >>> randrange(1, 10, random=lambda: 0.0)
        1
        >>> randrange(1, 10, random=lambda: 0.5)
        6
        >>> randrange(1, 10, random=lambda: 0.99)
        10
        >>> randrange(5, random=lambda: 0.0)
        1
        >>> randrange(1, 10, step=2, random=lambda: 0.5)
        5
        >>> randrange(10, 1)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        ValueError: Stop value cannot be less than start value
    """
    if stop is None:
        stop, start, step = start, 1, 1
    elif step == 0:
        raise ValueError("Step cannot be zero")
    if stop < start:
        raise ValueError("Stop value cannot be less than start value")
    start = int(start)
    step = int(step)
    stop = int(stop)
    return choice(range(start, stop + 1, step), random=random)


def shuffle(seq: Sequence, random: Callable = random):
    """
    Shuffles the elements of a sequence in-place.

    This function takes a sequence (such as a list or tuple) as input and
    shuffles its elements in-place using the Fisher-Yates algorithm. The original
    sequence is modified, and no new sequence is created.

    Args:
        seq: The sequence to be shuffled.
        random: Optional parameters for generating random dependency functions, default to random() functions generated using os.urandom()

    Returns:
        None: The original sequence is modified in-place.

    Examples:
        >>> lst = [1, 2, 3, 4, 5]
        >>> _r = iter([0.0, 0.5, 0.0, 0.5])
        >>> shuffle(lst, random=lambda: next(_r, 0.0))
        >>> lst
        [4, 2, 5, 3, 1]
        >>> lst = [10, 20]
        >>> shuffle(lst, random=lambda: 0.0)
        >>> lst
        [20, 10]
        >>> lst = [10, 20]
        >>> shuffle(lst, random=lambda: 0.5)
        >>> lst
        [10, 20]
        >>> lst = []
        >>> shuffle(lst, random=lambda: 0.5)
        >>> lst
        []
    """
    # Copy the original sequence to avoid modifying it directly
    for i in reversed(range(1, len(seq))):
        j = int(random() * (i + 1))
        seq[i], seq[j] = seq[j], seq[i]


def sample(population, k, random: Callable = random) -> list:
    """
    Randomly selects k unique elements from a population sequence.

    This function takes a population sequence (such as a list or tuple) and a
    number k as input, and returns a new list containing k unique elements chosen
    randomly from the population. The original population sequence is not modified.

    Args:
        population: The sequence from which to select elements.
        k: The number of elements to select. Must be less than or equal to the
           length of the population.
        random: Optional parameters for generating random dependency functions, default to random() functions generated using os.urandom()

    Returns:
        list: A new list containing k unique elements randomly selected from the population.

    Raises:
        TypeError: If population is not a Sequence
        ValueError: If k is greater than the length of the population.

    Examples:
        >>> _r = iter([0.0, 0.5, 0.0])
        >>> sample([1, 2, 3], 2, random=lambda: next(_r, 0.0))
        [1, 2]
        >>> _r = iter([0.0, 0.5, 0.0])
        >>> sample([1, 2, 3], 3, random=lambda: next(_r, 0.0))
        [1, 2, 3]
        >>> sample([42], 1, random=lambda: 0.0)
        [42]
        >>> sample([1, 2], 3, random=lambda: 0.0)
        Traceback (most recent call last):
            ...
        ValueError: Sample size larger than population
        >>> sample(42, 1)  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        TypeError: Population must be a sequence
    """
    if not isinstance(population, Sequence):
        raise TypeError("Population must be a sequence")

    n = len(population)
    if k > n:
        raise ValueError("Sample size larger than population")

    result = []
    pool = list(population)
    for i in range(k):
        j = int(random() * (n - i))
        result.append(pool[j])
        pool[j] = pool[n - i - 1]
    return result
