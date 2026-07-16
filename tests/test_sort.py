from random import randint, choice
import pytest
from pyhelper.sort import sort_algorithms, sorted_algorithms

# Algorithms with special input constraints that cannot be tested
# with arbitrary comparable data:
#   - bucket_sort / bucket_sorted : require float keys in [0, 1)
#   - radix_sort / radix_sorted   : require non-negative integer keys
_CONSTRAINED_FUNCS = {
    "bucket_sort", "bucket_sorted",
    "radix_sort", "radix_sorted",
}


def _skip_constrained(name, sort_func):
    """Return True if sort_func has input constraints not met by the test data."""
    return sort_func.__name__ in _CONSTRAINED_FUNCS


class TestSortAlgorithms:
    @pytest.fixture
    def random_list(self):
        return [randint(-1000, 1000) for _ in range(randint(50, 200))]

    @pytest.fixture
    def random_float_list(self):
        return [randint(-1000, 1000) / 100 for _ in range(randint(50, 200))]

    @pytest.fixture
    def random_string_list(self):
        chars = "abcdefghijklmnopqrstuvwxyz"
        return ["".join(choice(chars) for _ in range(randint(3, 10)))
                for _ in range(randint(50, 200))]

    # ── sorted_algorithms (return a new sorted copy) ──────────────────────

    def test_sorted_algorithms_basic(self, random_list):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_list[:]
            result = sort_func(seq)
            assert result == sorted(random_list), f"{name} failed basic sorting"

    def test_sorted_algorithms_reverse(self, random_list):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_list[:]
            result = sort_func(seq, reverse=True)
            assert result == sorted(random_list, reverse=True), \
                f"{name} failed reverse sorting"

    def test_sorted_algorithms_key(self, random_float_list):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_float_list[:]
            result = sort_func(seq, key=lambda x: abs(x))
            # Compare key sequences to avoid tie-breaking differences
            # between stable sorted() and unstable sorts
            assert [abs(x) for x in result] == \
                sorted(abs(x) for x in random_float_list), \
                f"{name} failed key sorting"

    # ── sort_algorithms (in-place sort) ───────────────────────────────────

    def test_sort_algorithms_basic(self, random_list):
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_list[:]
            sort_func(seq)
            assert seq == sorted(random_list), f"{name} failed basic sorting"

    def test_sort_algorithms_reverse(self, random_list):
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_list[:]
            sort_func(seq, reverse=True)
            assert seq == sorted(random_list, reverse=True), \
                f"{name} failed reverse sorting"

    def test_sort_algorithms_key(self, random_float_list):
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_float_list[:]
            sort_func(seq, key=lambda x: abs(x))
            assert [abs(x) for x in seq] == \
                sorted(abs(x) for x in random_float_list), \
                f"{name} failed key sorting"

    # ── Edge cases ────────────────────────────────────────────────────────

    def test_empty_list(self):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            assert sort_func([]) == [], f"{name} failed empty list"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = []
            sort_func(seq)
            assert seq == [], f"{name} failed empty list"

    def test_single_element(self):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            assert sort_func([1]) == [1], f"{name} failed single element"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = [1]
            sort_func(seq)
            assert seq == [1], f"{name} failed single element"

    def test_already_sorted(self, random_list):
        sorted_list = sorted(random_list)
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            result = sort_func(sorted_list[:])
            assert result == sorted_list, f"{name} failed already sorted list"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = sorted_list[:]
            sort_func(seq)
            assert seq == sorted_list, f"{name} failed already sorted list"

    def test_reverse_sorted(self, random_list):
        reverse_sorted_list = sorted(random_list, reverse=True)
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            result = sort_func(reverse_sorted_list[:], reverse=True)
            assert result == reverse_sorted_list, \
                f"{name} failed reverse sorted list"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = reverse_sorted_list[:]
            sort_func(seq, reverse=True)
            assert seq == reverse_sorted_list, \
                f"{name} failed reverse sorted list"

    def test_all_same_elements(self):
        same_list = [5] * 100
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            assert sort_func(same_list[:]) == same_list, \
                f"{name} failed all same elements"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = same_list[:]
            sort_func(seq)
            assert seq == same_list, f"{name} failed all same elements"

    def test_string_sorting(self, random_string_list):
        for name, sort_func in sorted_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_string_list[:]
            result = sort_func(seq)
            assert result == sorted(random_string_list), \
                f"{name} failed string sorting"
        for name, sort_func in sort_algorithms.items():
            if _skip_constrained(name, sort_func):
                continue
            seq = random_string_list[:]
            sort_func(seq)
            assert seq == sorted(random_string_list), \
                f"{name} failed string sorting"
