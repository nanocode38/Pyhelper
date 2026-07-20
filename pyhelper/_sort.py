# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Callable, List, MutableSequence, Optional, Sequence, Any, Iterable
import math

__all__ = [
    "insertion_sort",
    "shell_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "bucket_sort",
    "radix_sort",
    "tim_sort",
]

# ----------------------------------------------------------------------
#  1. Insertion Sort
# ----------------------------------------------------------------------
def insertion_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using a straight insertion sort.

    Insertion sort builds the final sorted array one element at a time.
    It is efficient for small sequences or nearly sorted data.

    ==============================================
    Insertion Sort
    Best Time complexity: O(n)
    Avg Time complexity: O(n²)
    Worst Time complexity: O(n²)
    Space complexity: O(1)   (in‑place)
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
        >>> insertion_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> insertion_sort(words, key=len)
        >>> words
        ['date', 'apple', 'banana', 'cherry']

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> insertion_sort(nums, reverse=True)
        >>> nums
        [9, 5, 4, 3, 1, 1]
    """
    # Define a local key function (identity if none provided)
    kf = key if key is not None else (lambda x: x)

    n = len(seq)
    # Outer loop: take each element as the "current" one to insert
    for i in range(1, n):
        current = seq[i]          # element to be placed correctly
        cur_key = kf(current)
        j = i - 1

        # Shift elements to the right while they are greater than current
        # (or smaller if reverse is True)
        while j >= 0:
            cmp = kf(seq[j]) > cur_key if not reverse else kf(seq[j]) < cur_key
            if not cmp:
                break
            seq[j + 1] = seq[j]
            j -= 1

        seq[j + 1] = current      # insert current at its correct position


# ----------------------------------------------------------------------
#  2. Shell Sort
# ----------------------------------------------------------------------
def shell_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using Shell's method (diminishing increment sort).

    Shell sort is a generalisation of insertion sort that allows the
    exchange of far‑apart items. It uses a gap sequence (here the
    classic Ciura gaps) to pre‑sort the list, making later insertion
    sorts more efficient.

    ==============================================
    Shell Sort (Ciura gaps)
    Best Time complexity: O(n log n)
    Avg Time complexity: depends on gap sequence – roughly O(n^{1.25})
    Worst Time complexity: O(n^{3/2}) for Ciura gaps
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
        >>> shell_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> shell_sort(nums, reverse=True)
        >>> nums
        [9, 5, 4, 3, 1, 1]
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)

    # Precomputed Ciura gaps (good practical performance)
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:
        if gap >= n:
            continue
        # Perform a gapped insertion sort for this gap size
        for i in range(gap, n):
            temp = seq[i]
            temp_key = kf(temp)
            j = i
            # Compare elements that are 'gap' apart
            while j >= gap:
                cmp = kf(seq[j - gap]) > temp_key if not reverse else kf(seq[j - gap]) < temp_key
                if not cmp:
                    break
                seq[j] = seq[j - gap]
                j -= gap
            seq[j] = temp


# ----------------------------------------------------------------------
#  3. Merge Sort (bottom‑up, in‑place with auxiliary buffer)
# ----------------------------------------------------------------------
def merge_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using a bottom‑up iterative merge sort.

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
        >>> merge_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> words = ['banana', 'apple', 'cherry', 'date']
        >>> merge_sort(words, key=len)
        >>> words
        ['date', 'apple', 'banana', 'cherry']
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)
    # Temporary buffer for merging – reuse it across all merges
    aux = [None] * n

    width = 1
    while width < n:
        left = 0
        while left < n:
            mid = left + width
            if mid >= n:
                break          # no right half to merge
            right = min(left + 2 * width, n)
            # Merge seq[left:mid] and seq[mid:right] into aux[left:right]
            i, j, k = left, mid, left
            while i < mid and j < right:
                # Determine which element should come first
                if not reverse:
                    take_left = kf(seq[i]) <= kf(seq[j])
                else:
                    take_left = kf(seq[i]) >= kf(seq[j])
                if take_left:
                    aux[k] = seq[i]
                    i += 1
                else:
                    aux[k] = seq[j]
                    j += 1
                k += 1
            # Copy remaining elements from left half (if any)
            while i < mid:
                aux[k] = seq[i]
                i += 1
                k += 1
            # Copy remaining elements from right half (if any)
            while j < right:
                aux[k] = seq[j]
                j += 1
                k += 1
            # Copy merged segment back to original sequence
            for p in range(left, right):
                seq[p] = aux[p]
            left = right
        width *= 2


# ----------------------------------------------------------------------
#  4. Quick Sort (Lomuto partition, in‑place, tail‑recursive)
# ----------------------------------------------------------------------
def quick_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using the Quicksort algorithm (Lomuto partition).

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
        >>> quick_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> quick_sort(nums, reverse=True)
        >>> nums
        [9, 5, 4, 3, 1, 1]
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)
    if n <= 1:
        return

    # Use a stack of (low, high) ranges to process
    stack = [(0, n - 1)]

    while stack:
        low, high = stack.pop()
        if low >= high:
            continue

        # Median-of-three pivot selection
        mid = (low + high) // 2
        # Sort the three candidates: seq[low], seq[mid], seq[high]
        # Ascending:  seq[low] <= seq[mid] <= seq[high]
        # Descending: seq[low] >= seq[mid] >= seq[high]
        if not reverse:
            if kf(seq[low]) > kf(seq[mid]):
                seq[low], seq[mid] = seq[mid], seq[low]
            if kf(seq[low]) > kf(seq[high]):
                seq[low], seq[high] = seq[high], seq[low]
            if kf(seq[mid]) > kf(seq[high]):
                seq[mid], seq[high] = seq[high], seq[mid]
        else:
            if kf(seq[low]) < kf(seq[mid]):
                seq[low], seq[mid] = seq[mid], seq[low]
            if kf(seq[low]) < kf(seq[high]):
                seq[low], seq[high] = seq[high], seq[low]
            if kf(seq[mid]) < kf(seq[high]):
                seq[mid], seq[high] = seq[high], seq[mid]
        # Place pivot at end (high) after median-of-three
        pivot_val = seq[mid]
        pivot_key = kf(pivot_val)
        # Swap pivot with the last element (we already know high is >= pivot)
        seq[mid], seq[high] = seq[high], seq[mid]

        # Lomuto partition: rearrange around pivot
        i = low - 1
        for j in range(low, high):
            # Decide if seq[j] belongs to the left side
            if not reverse:
                cond = kf(seq[j]) <= pivot_key
            else:
                cond = kf(seq[j]) >= pivot_key
            if cond:
                i += 1
                seq[i], seq[j] = seq[j], seq[i]
        # Place pivot in its final position
        seq[i + 1], seq[high] = seq[high], seq[i + 1]
        pivot_pos = i + 1

        # Push sub‑ranges onto stack (larger range first to limit stack depth)
        if pivot_pos - 1 - low > high - pivot_pos - 1:
            stack.append((low, pivot_pos - 1))
            stack.append((pivot_pos + 1, high))
        else:
            stack.append((pivot_pos + 1, high))
            stack.append((low, pivot_pos - 1))


# ----------------------------------------------------------------------
#  5. Heap Sort
# ----------------------------------------------------------------------
def heap_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using the Heapsort algorithm.

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
        >>> heap_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> nums = [3, 1, 4, 1, 5, 9]
        >>> heap_sort(nums, reverse=True)
        >>> nums
        [9, 5, 4, 3, 1, 1]
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)

    # Build heap (max‑heap for ascending, min‑heap for descending)
    # Sift down operation for node i
    def sift_down(start: int, end: int) -> None:
        """Restore heap property for subtree rooted at *start*, up to *end*."""
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            # Choose the child that should be swapped with parent
            if not reverse:
                # For max‑heap: pick larger child
                if child + 1 <= end and kf(seq[child]) < kf(seq[child + 1]):
                    child += 1
                swap_cond = kf(seq[root]) < kf(seq[child])
            else:
                # For min‑heap: pick smaller child
                if child + 1 <= end and kf(seq[child]) > kf(seq[child + 1]):
                    child += 1
                swap_cond = kf(seq[root]) > kf(seq[child])

            if not swap_cond:
                break
            seq[root], seq[child] = seq[child], seq[root]
            root = child

    # Phase 1: build heap (start from last internal node)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n - 1)

    # Phase 2: extract elements one by one
    for i in range(n - 1, 0, -1):
        seq[0], seq[i] = seq[i], seq[0]   # move current root to end
        sift_down(0, i - 1)               # restore heap on reduced range


# ----------------------------------------------------------------------
#  6. Counting Sort
# ----------------------------------------------------------------------
def counting_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], int]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using the Counting Sort algorithm.

    **Important:** This algorithm requires that every element's key
    (as returned by *key*) is a **non‑negative integer**. If *key* is
    ``None``, the elements themselves must be non‑negative integers.

    The sort is stable and runs in linear time when the key range is
    small relative to the sequence length.

    ==============================================
    Counting Sort
    Best Time complexity: O(n + k)   where k = max key value
    Avg Time complexity: O(n + k)
    Worst Time complexity: O(n + k)
    Space complexity: O(n + k)
    Stable: Yes
    ==============================================

    Args:
        seq: The sequence to be sorted in place.
        key: A function returning a non‑negative integer key.
             Default is the identity (elements must be ints).
        reverse: Whether to sort in descending order.

    Raises:
        TypeError: If *key* does not return an integer.
        ValueError: If any key is negative.

    Examples:
        >>> data = [5, 2, 8, 1, 9, 3]
        >>> counting_sort(data)
        >>> data
        [1, 2, 3, 5, 8, 9]

        >>> ages = [25, 30, 18, 22, 35]
        >>> counting_sort(ages, key=lambda x: x % 10)  # sort by last digit
        >>> ages
        [30, 22, 25, 35, 18]
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)
    if n <= 1:
        return

    # Compute keys for all elements
    keys = [kf(e) for e in seq]
    # Validate keys are non‑negative integers
    for k in keys:
        if not isinstance(k, int) or k < 0:
            raise ValueError("Counting sort requires non‑negative integer keys.")

    max_key = max(keys) if keys else 0

    # Count occurrences of each key
    count = [0] * (max_key + 1)
    for k in keys:
        count[k] += 1

    # Transform counts to cumulative positions (for stable placement)
    if not reverse:
        for i in range(1, len(count)):
            count[i] += count[i - 1]
    else:
        # For reverse, we compute cumulative from the end
        for i in range(len(count) - 2, -1, -1):
            count[i] += count[i + 1]

    # Build output array (stable placement from right to left)
    output = [None] * n
    if not reverse:
        # Forward cumulative → place from end for stability
        for i in range(n - 1, -1, -1):
            k = keys[i]
            count[k] -= 1
            pos = count[k]
            output[pos] = seq[i]
    else:
        # Reverse cumulative → place from beginning for stability
        for i in range(n - 1, -1, -1):
            k = keys[i]
            count[k] -= 1
            pos = count[k]
            output[pos] = seq[i]

    # Copy back to original sequence
    for i in range(n):
        seq[i] = output[i]


# ----------------------------------------------------------------------
#  7. Radix Sort (LSD, base 10)
# ----------------------------------------------------------------------
def radix_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], int]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using LSD (Least Significant Digit) Radix Sort.

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
        >>> radix_sort(data)
        >>> data
        [2, 24, 45, 66, 75, 90, 170, 802]

        >>> nums = [329, 457, 657, 839, 436, 720, 355]
        >>> radix_sort(nums, reverse=True)
        >>> nums
        [839, 720, 657, 457, 436, 355, 329]
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)
    if n <= 1:
        return

    # Compute keys and find maximum to determine number of digits
    keys = [kf(e) for e in seq]
    for k in keys:
        if not isinstance(k, int) or k < 0:
            raise ValueError("Radix sort requires non‑negative integer keys.")
    if not keys:
        return
    max_key = max(keys)

    # Number of digits in base 10
    num_digits = len(str(max_key))

    # LSD radix sort: iterate over each digit position
    for digit_pos in range(num_digits):
        divisor = 10 ** digit_pos
        # Counting sort on the current digit (0..9)
        count = [0] * 10
        for k in keys:
            digit = (k // divisor) % 10
            count[digit] += 1

        # Convert counts to cumulative positions (stable)
        if not reverse:
            for i in range(1, 10):
                count[i] += count[i - 1]
        else:
            for i in range(8, -1, -1):
                count[i] += count[i + 1]

        # Build output for this digit pass
        output = [None] * n
        if not reverse:
            for i in range(n - 1, -1, -1):
                digit = (keys[i] // divisor) % 10
                count[digit] -= 1
                output[count[digit]] = seq[i]
        else:
            for i in range(n - 1, -1, -1):
                digit = (keys[i] // divisor) % 10
                count[digit] -= 1
                output[count[digit]] = seq[i]

        # Update seq and keys for next digit
        for i in range(n):
            seq[i] = output[i]
        # Recompute keys because seq changed? Actually keys remain the same
        # because they depend on the original elements, not on order.
        # But we need to keep keys aligned with the new order.
        # Since we didn't change elements, only permuted them, we can rebuild keys:
        keys = [kf(e) for e in seq]


# ----------------------------------------------------------------------
#  8. Bucket Sort
# ----------------------------------------------------------------------
def bucket_sort(
        seq: MutableSequence,
        key: Optional[Callable[[Any], float]] = None,
        reverse: bool = False,
) -> None:
    """
    Sort *seq* in place using the Bucket Sort algorithm.

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
        >>> bucket_sort(data)
        >>> data
        [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]

        >>> nums = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
        >>> bucket_sort(nums, reverse=True)
        >>> nums
        [0.52, 0.51, 0.47, 0.42, 0.37, 0.33, 0.32]

        >>> words = ['apple', 'bananas', 'cherry', 'date']
        >>> bucket_sort(words, reverse=True, key=len)
        >>> words
        ['bananas', 'cherry', 'apple', 'date']
    """
    kf = key if key is not None else (lambda x: x)
    n = len(seq)
    if n <= 1:
        return

    # Collect raw keys
    raw_keys = [kf(e) for e in seq]

    # Determine whether keys are already in [0, 1); if not, normalize
    min_k = min(raw_keys)
    max_k = max(raw_keys)
    if min_k >= 0.0 and max_k < 1.0:
        keys = raw_keys
    else:
        # Min-max scale to [0, 1). If all keys are equal, use 0.0.
        range_k = max_k - min_k
        if range_k == 0:
            keys = [0.0] * n
        else:
            keys = [(k - min_k) / range_k for k in raw_keys]

    # Number of buckets: typically sqrt(n) or n itself
    num_buckets = int(math.sqrt(n)) + 1
    buckets = [[] for _ in range(num_buckets)]

    # Distribute elements into buckets according to their key
    for elem, k in zip(seq, keys):
        idx = int(k * num_buckets)   # map key to bucket index
        # Ensure index stays within bounds (edge case: k == 1.0 is excluded)
        if idx == num_buckets:
            idx = num_buckets - 1
        buckets[idx].append(elem)

    # Sort each bucket individually (use insertion sort for small buckets)
    for bucket in buckets:
        # We reuse insertion_sort with the same key and reverse
        insertion_sort(bucket, key=key, reverse=reverse)

    # Concatenate buckets back into seq
    pos = 0
    if not reverse:
        # Ascending: concatenate buckets in order 0 .. num_buckets-1
        for bucket in buckets:
            for elem in bucket:
                seq[pos] = elem
                pos += 1
    else:
        # Descending: concatenate buckets in reverse order
        for bucket in reversed(buckets):
            for elem in bucket:
                seq[pos] = elem
                pos += 1

# ----------------------------------------------------------------------
#  9. Tim Sort
# ----------------------------------------------------------------------
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