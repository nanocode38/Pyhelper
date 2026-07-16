"""
Pure Python implementation of Timsort (in-place sort) compatible with any MutableSequence.
Supports key and reverse parameters like built-in sorted().
"""
import copy
from collections.abc import  MutableSequence, Sequence
from typing import (
    Callable,
    List,
    Any,
    Iterable,
)

# try:
#     from numba import jit
# except ImportError:
jit = lambda func: func

@jit
def _set_slice(seq: MutableSequence, s: slice, values: Iterable) -> None:
    """Assign *values* to ``seq[s]``.

    Tries native slice assignment first; falls back to element‑wise assignment
    if the sequence does not support slice assignment (e.g. ``deque``).
    """
    vals = list(values)
    try:
        seq[s] = vals
    except TypeError:
        indices = range(*s.indices(len(seq)))
        for idx, v in zip(indices, vals):
            seq[idx] = v

@jit
def _get_slice(seq: MutableSequence, s: slice) -> List[Any]:
    """Return a list copy of ``seq[s]``.

    Tries native slicing first; falls back to element‑wise extraction
    if the sequence does not support slicing.
    """
    try:
        return list(seq[s])
    except TypeError:
        indices = range(*s.indices(len(seq)))
        return [seq[i] for i in indices]

@jit
def tim_sort(
    seq: MutableSequence,
    key: Callable | None = None,
    reverse: bool = False,
) -> None:
    """Sort *seq* in place using a pure‑Python Timsort algorithm.

    This function mimics the behaviour of the built‐in ``sorted()`` but
    modifies the input sequence directly. It is a faithful re‑implementation
    of the Timsort algorithm as used by CPython, including:

    - Adaptive identification of natural runs (ascending or descending).
    - Binary insertion sort for short runs.
    - Merge policy that maintains a stack of runs with decreasing lengths
      (the same invariants as CPython's listobject.c).
    - Stable sorting (equal elements retain their original relative order).

    The implementation works with any :class:`MutableSequence` type, even
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
        >>> tim_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> tim_sort(words, key=len)
        >>> words
        ['date', 'apple', 'banana', 'cherry']

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> tim_sort(nums, reverse=True)
        >>> nums
        [9, 5, 4, 3, 1, 1]

    Notes
    -----
    Because this is written entirely in Python, it is significantly slower
    than the C implementation of ``list.sort()`` or ``sorted()``.
    and to serve as a drop‑in for environments where only pure Python is
    allowed (e.g. restricted execution contexts).
    """
    n = len(seq)
    if n <= 1:
        return

    # ---- key and comparator setup ----
    if key is None:
        kfunc = lambda x: x
    else:
        kfunc = key

    def natural_lt(a: Any, b: Any) -> bool:
        return kfunc(a) < kfunc(b)

    if reverse:
        def lt(a: Any, b: Any) -> bool:
            return kfunc(b) < kfunc(a)
    else:
        def lt(a: Any, b: Any) -> bool:
            return kfunc(a) < kfunc(b)

    # ---- internal helpers ----
    def binary_insertion_sort(start: int, end: int) -> None:
        """Stable binary insertion sort on seq[start:end]."""
        for i in range(start + 1, end):
            val = seq[i]
            lo, hi = start, i
            while lo < hi:
                mid = (lo + hi) // 2
                if lt(val, seq[mid]):
                    hi = mid
                else:
                    lo = mid + 1
            # shift [lo, i) one position to the right
            part = _get_slice(seq, slice(lo, i))
            _set_slice(seq, slice(lo + 1, i + 1), part)
            seq[lo] = val

    def merge(lo: int, mid: int, hi: int) -> None:
        """Merge two adjacent sorted subarrays [lo, mid) and [mid, hi)."""
        left_len = mid - lo
        right_len = hi - mid
        if left_len <= right_len:
            left_part = _get_slice(seq, slice(lo, mid))
            i, j, k = 0, mid, lo
            while i < left_len and j < hi:
                if not lt(seq[j], left_part[i]):
                    seq[k] = left_part[i]
                    i += 1
                else:
                    seq[k] = seq[j]
                    j += 1
                k += 1
            if i < left_len:
                _set_slice(seq, slice(k, k + left_len - i), left_part[i:])
        else:
            right_part = _get_slice(seq, slice(mid, hi))
            left_part = _get_slice(seq, slice(lo, mid))
            i, j, k = left_len - 1, right_len - 1, hi - 1
            while i >= 0 and j >= 0:
                # right-to-left: prefer right element when keys equal
                # (right element belongs at the more-right position k)
                if lt(right_part[j], left_part[i]):
                    seq[k] = left_part[i]
                    i -= 1
                else:
                    seq[k] = right_part[j]
                    j -= 1
                k -= 1
            if j >= 0:
                _set_slice(seq, slice(lo, lo + j + 1), right_part[:j + 1])

    def calc_min_run() -> int:
        """Compute the minimum run length for the current sequence size."""
        r = 0
        nn = n
        while nn >= 64:
            r |= nn & 1
            nn >>= 1
        return nn + r

    min_run = calc_min_run()

    # ---- main scan: identify runs and merge ----
    runs: List[tuple[int, int]] = []   # stack of (start, length)
    i = 0
    while i < n:
        run_start = i
        i += 1
        if i == n:
            run_len = 1
        else:
            if lt(seq[i - 1], seq[i]):
                while i < n and not lt(seq[i], seq[i - 1]):
                    i += 1
                run_len = i - run_start
            elif lt(seq[i], seq[i - 1]):
                while i < n and not lt(seq[i - 1], seq[i]):
                    i += 1
                run_len = i - run_start
                part = _get_slice(seq, slice(run_start, i))
                part.reverse()
                _set_slice(seq, slice(run_start, i), part)
            else:
                # equal elements — treat as ascending run (stable sort)
                while i < n and not lt(seq[i], seq[i - 1]):
                    i += 1
                run_len = i - run_start

        # extend short runs via insertion sort
        if run_len < min_run:
            extend_to = min(run_start + min_run, n)
            binary_insertion_sort(run_start, extend_to)
            run_len = extend_to - run_start
            i = run_start + run_len

        # push the run onto the stack
        runs.append((run_start, run_len))

        # enforce merge invariants (same as CPython's listobject.c)
        # invariants: runs[-3] > runs[-2] + runs[-1],  runs[-2] > runs[-1]
        while len(runs) > 1:
            a_start, a_len = runs[-2]
            b_start, b_len = runs[-1]
            if len(runs) >= 3:
                c_start, c_len = runs[-3]
                if a_len <= b_len + c_len:
                    if a_len < c_len:
                        # C is smallest: merge C and A
                        merge(c_start, a_start, a_start + a_len)
                        runs.pop(-2)
                        runs[-2] = (c_start, c_len + a_len)
                    else:
                        # A is smallest: merge A and B
                        merge(a_start, b_start, b_start + b_len)
                        runs.pop()
                        runs[-1] = (a_start, a_len + b_len)
                elif b_len <= c_len:
                    # B <= C, merge C and A
                    merge(c_start, a_start, a_start + a_len)
                    runs.pop(-2)
                    runs[-2] = (c_start, c_len + a_len)
                else:
                    break
            else:
                if a_len <= b_len:
                    merge(a_start, b_start, b_start + b_len)
                    runs.pop()
                    runs[-1] = (a_start, a_len + b_len)
                else:
                    break

    # final merging of all remaining runs
    while len(runs) > 1:
        a_start, a_len = runs[-2]
        b_start, b_len = runs[-1]
        merge(a_start, b_start, b_start + b_len)
        runs.pop()
        runs[-1] = (a_start, a_len + b_len)

def tim_sorted(seq: Sequence, key: Callable | None = None, reverse: bool = False) -> MutableSequence:
    """Sort *seq* using a pure‑Python Timsort algorithm.

    This function mimics the behaviour of the built‐in ``sorted()``
    It is a faithful re‑implementation
    of the Timsort algorithm as used by CPython, including:

    - Adaptive identification of natural runs (ascending or descending).
    - Binary insertion sort for short runs.
    - Merge policy that maintains a stack of runs with decreasing lengths
      (the same invariants as CPython's listobject.c).
    - Stable sorting (equal elements retain their original relative order).

    The implementation works with any :class:`Sequence` type, even
    those that do not support slice operations (e.g. :class:`collections.deque`).


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

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> tim_sorted(nums, reverse=True)
        [9, 5, 4, 3, 1, 1]

    Notes
    -----
    Because this is written entirely in Python, it is significantly slower
    than the C implementation of ``list.sort()`` or ``sorted()``.
    and to serve as a drop‑in for environments where only pure Python is
    allowed (e.g. restricted execution contexts).
    """
    if not isinstance(seq, Sequence):
        raise TypeError("seq must be a sequence")
    if isinstance(seq, MutableSequence):
        seq = copy.deepcopy(seq)
    else:
        seq = list(seq)[:]
    tim_sort(seq, key, reverse)
    return seq