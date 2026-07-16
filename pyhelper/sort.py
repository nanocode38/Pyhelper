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

from ._sorted import (
    insertion_sorted,
    shell_sorted,
    merge_sorted,
    quick_sorted,
    heap_sorted,
    bucket_sorted,
    radix_sorted,
    tim_sorted,
)


__all__ = [
    "insertion_sort",
    "shell_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "bucket_sort",
    "radix_sort",
    "tim_sort",
    "insertion_sorted",
    "shell_sorted",
    "merge_sorted",
    "quick_sorted",
    "heap_sorted",
    "bucket_sorted",
    "radix_sorted",
    "tim_sorted",
]

# Built sort algorithms
sort_algorithms, sorted_algorithms = {}, {}
for func in __all__:
    if func.endswith("_sort"):
        sort_algorithms[" ".join(word.capitalize() for word in func.split("_"))] = globals()[func]
    elif func.endswith("_sorted"):
        sorted_algorithms[" ".join(word.capitalize() for word in func.split("_"))] = globals()[func]