# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from typing import Callable, Optional, Any, MutableSequence, Sequence

from ._sort import (
    insertion_sort,
    shell_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    bucket_sort,
    radix_sort,
    tim_sort,
)

__all__ = [
    "insertion_sorted",
    "shell_sorted",
    "merge_sorted",
    "quick_sorted",
    "heap_sorted",
    "bucket_sorted",
    "radix_sorted",
    "tim_sorted",
]

def _sorted_helper(seq, key, reverse, sort_func):
    if not isinstance(seq, Sequence):
        raise TypeError("seq must be a sequence")
    if isinstance(seq, MutableSequence):
        seq = copy.deepcopy(seq)
    else:
        seq = list(seq)
    sort_func(seq, key, reverse)
    return seq


def insertion_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using a straight insertion sort.

    Insertion sort builds the final sorted array one element at a time.
    It is efficient for small sequences or nearly sorted data.

    ==============================================
    Insertion Sort
    Best Time complexity: O(n)
    Avg Time complexity: O(n²)
    Worst Time complexity: O(n²)
    Space complexity: O(n)
    Stable: Yes
    ==============================================

    Args:
    seq: The sequence to be sorted in place.
    key: A function that extracts a comparison key from each element.
    Default is the identity function.
    reverse: Whether to sort in descending order (default ``False``).

    Raises:
    TypeError: If elements (after applying *key*) are not comparable.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> insertion_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> insertion_sorted(words, key=len)
        ['date', 'apple', 'banana', 'cherry']

        >>> data = [3, 1, 4, 1, 5, 9]
        >>> insertion_sorted(data, reverse=True)
        [9, 5, 4, 3, 1, 1]
    """
    return _sorted_helper(seq, key, reverse, insertion_sort)

def shell_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using Shell's method (diminishing increment sort).

    Shell sort is a generalisation of insertion sort that allows the
    exchange of far‑apart items. It uses a gap sequence (here the
    classic Ciura gaps) to pre‑sort the list, making later insertion
    sorts more efficient.

    ==============================================
    Shell Sort (Ciura gaps)
    Best Time complexity: O(n log n)
    Avg Time complexity: depends on gap sequence – roughly O(n^{1.25})
    Worst Time complexity: O(n^{3/2}) for Ciura gaps
    Space complexity: O(n)
    Stable: No
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function that extracts a comparison key from each element.
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If elements (after *key*) are not comparable.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> shell_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]
        >>> data = ['apple', 'banana', 'cherry', 'date']
        >>> shell_sorted(data, reverse=True, key=len)
        ['banana', 'cherry', 'apple', 'date']
    """
    return _sorted_helper(seq, key, reverse, shell_sort)

def merge_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using a bottom‑up iterative merge sort.

    This implementation uses a temporary buffer of the same length as
    *seq* to avoid recursive overhead and to guarantee stability.
    The merge step compares elements using the supplied *key*.

    ==============================================
    Merge Sort (iterative, bottom‑up)
    Best Time complexity: O(n log n)
    Avg Time complexity: O(n log n)
    Worst Time complexity: O(n log n)
    Space complexity: O(n)   (auxiliary buffer)
    Stable: Yes
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function that extracts a comparison key from each element.
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If elements (after *key*) are not comparable.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> merge_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> merge_sorted(words, key=len)
        ['date', 'apple', 'banana', 'cherry']
    """
    return _sorted_helper(seq, key, reverse, merge_sort)

def quick_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using the Quicksort algorithm (Lomuto partition).

    This implementation uses an explicit stack to avoid recursion depth
    issues. The pivot is chosen as the median of three (first, middle,
    last). The algorithm is NOT stable.

    ==============================================
    Quick Sort (Lomuto partition, iterative)
    Best Time complexity: O(n log n)
    Avg Time complexity: O(n log n)
    Worst Time complexity: O(n²)   (rare with median‑of‑three)
    Space complexity: O(log n)     (stack for sub‑arrays)
    Stable: No
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function that extracts a comparison key from each element.
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If elements (after *key*) are not comparable.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> quick_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> quick_sorted(nums, reverse=True)
        [9, 5, 4, 3, 1, 1]

        >>> data = ['apple', 'bananas', 'cherry', 'date']
        >>> quick_sorted(data, reverse=True, key=len)
        ['bananas', 'cherry', 'apple', 'date']
    """
    return _sorted_helper(seq, key, reverse, quick_sort)

def heap_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using the Heapsort algorithm.

    Heapsort first builds a max‑heap (or min‑heap if *reverse* is True)
    from the sequence, then repeatedly extracts the root to obtain a
    sorted order. The algorithm is NOT stable.

    ==============================================
    Heap Sort
    Best Time complexity: O(n log n)
    Avg Time complexity: O(n log n)
    Worst Time complexity: O(n log n)
    Space complexity: O(1)   (in‑place)
    Stable: No
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function that extracts a comparison key from each element.
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If elements (after *key*) are not comparable.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> heap_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> heap_sorted(nums, reverse=True)
        [9, 5, 4, 3, 1, 1]
    """
    return _sorted_helper(seq, key, reverse, heap_sort)

def bucket_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using the Bucket Sort algorithm.

    **Important:** This algorithm distributes elements into buckets based on
    their keys. By default it expects floating‑point numbers in **[0, 1)**.
    If the keys fall outside this range, they are automatically normalized to
    [0, 1) using min-max scaling — this means you can also use arbitrary
    numeric keys (e.g. ``key=len`` for string length).

    The algorithm distributes elements into buckets, sorts each bucket
    individually (using insertion sort here), and then concatenates them.
    It is stable only if the bucket sort used inside is stable (insertion
    sort is stable).

    ==============================================
    Bucket Sort
    Best Time complexity: O(n + k)   (uniform distribution)
    Avg Time complexity: O(n + n²/k + k)   ≈ O(n) when k ~ n
    Worst Time complexity: O(n²)   (all elements in one bucket)
    Space complexity: O(n + k)
    Stable: Yes (when inner sort is stable)
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function returning a comparable numeric value. Values are
            automatically normalized to [0, 1) if necessary. Default is
            identity.
        reverse: Whether to sort in descending order.

    Examples:
        >>> data = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
        >>> bucket_sorted(data)
        [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
        >>> data
        [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]

        >>> data = ['apple', 'bananas', 'cherry', 'date']
        >>> bucket_sorted(data, reverse=True, key=len)
        ['bananas', 'cherry', 'apple', 'date']
    """
    return _sorted_helper(seq, key, reverse, bucket_sort)

def radix_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """
    Sort *seq* using LSD (Least Significant Digit) Radix Sort.

    **Important:** This algorithm requires that every element's key
    (as returned by *key*) is a **non‑negative integer**. If *key* is
    ``None``, the elements themselves must be non‑negative integers.

    Radix sort processes digits from least significant to most,
    using a stable counting sort per digit. The overall sort is stable.

    ==============================================
    Radix Sort (LSD, base 10)
    Best Time complexity: O(d·(n + k))   d = number of digits, k = base (10)
    Avg Time complexity: O(d·(n + k))
    Worst Time complexity: O(d·(n + k))
    Space complexity: O(n + k)
    Stable: Yes
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function returning a non‑negative integer key.
        Default is the identity.
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If *key* does not return an integer.
        ValueError: If any key is negative.

    Examples:
        >>> data = [170, 45, 75, 90, 802, 24, 2, 66]
        >>> radix_sorted(data)
        [2, 24, 45, 66, 75, 90, 170, 802]
        >>> data
        [170, 45, 75, 90, 802, 24, 2, 66]

        >>> data = ['apple', 'banana', 'cherry', 'date']
        >>> radix_sorted(data, reverse=True, key=len)
        ['banana', 'cherry', 'apple', 'date']
    """
    return _sorted_helper(seq, key, reverse, radix_sort)

def tim_sorted(
        seq: Sequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> MutableSequence:
    """Sort *seq* using a pure‑Python Timsort algorithm.

    This function mimics the behaviour of the built‐in ``sorted()`` but
    modifies the input sequence directly. It is a faithful re‑implementation
    of the Timsort algorithm as used by CPython, including:

    - Adaptive identification of natural runs (ascending or descending).
    - Binary insertion sort for short runs.
    - Merge policy that maintains a stack of runs with decreasing lengths
      (the same invariants as CPython's listobject.c).
    - Stable sorting (equal elements retain their original relative order).

    The implementation works with any :class:`Sequence` type, even
    those that do not support slice operations (e.g. :class:`collections.deque`),

    ===========================
    TimSort Algorithm
    Best Time complexity: O(n)
    Avg Time complexity: O(n log n)
    Worst Time complexity: O(n log n)
    Space complexity: O(n)
    Stable: Yes
    ===========================

    Args:
        seq : The sequence to be sorted in place.
        key : A function that extracts a comparison key from each element. Default is lambda x: x.
        reverse : Whether to sort in reverse order

    Raises:
        TypeError
            If the elements cannot be compared with the given *key* (or without one).
        IndexError
            If the sequence is mutated during sorting (should never happen).

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> tim_sorted(data)
        [1, 2, 3, 5, 8, 9]
        >>> data
        [5, 2, 8, 1, 9, 3]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> tim_sorted(words, key=len)
        ['date', 'apple', 'banana', 'cherry']

    Notes
    -----
    Because this is written entirely in Python, it is significantly slower
    than the C implementation of ``list.sort()`` or ``sorted()``.
    and to serve as a drop‑in for environments where only pure Python is
    allowed (e.g. restricted execution contexts).
    """
    return _sorted_helper(seq, key, reverse, tim_sort)

if __name__ == "__main__":
    import doctest
    doctest.testmod()