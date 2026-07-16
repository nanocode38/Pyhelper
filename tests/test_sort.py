from random import randint, choice
import pytest
from pyhelper.sort import sort_algorithms, sorted_algorithms


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

    def test_sorted_algorithms_basic(self, random_list):
        for name, sort_func in sorted_algorithms.items():
            seq = random_list[:]
            result = sort_func(seq)
            assert result == sorted(random_list), f"{name} failed basic sorting"

    def test_sorted_algorithms_reverse(self, random_list):
        for name, sort_func in sorted_algorithms.items():
            seq = random_list[:]
            result = sort_func(seq, reverse=True)
            assert result == sorted(random_list, reverse=True), f"{name} failed reverse sorting"

    def test_sorted_algorithms_key(self, random_float_list):
        for name, sort_func in sorted_algorithms.items():
            seq = random_float_list[:]
            result = sort_func(seq, key=lambda x: abs(x))
            assert result == sorted(random_float_list, key=lambda x: abs(x)), f"{name} failed key sorting"

    def test_sort_algorithms_basic(self, random_list):
        for name, sort_func in sort_algorithms.items():
            seq = random_list[:]
            sort_func(seq)
            assert seq == sorted(random_list), f"{name} failed basic sorting"

    def test_sort_algorithms_reverse(self, random_list):
        for name, sort_func in sort_algorithms.items():
            seq = random_list[:]
            sort_func(seq, reverse=True)
            assert seq == sorted(random_list, reverse=True), f"{name} failed reverse sorting"

    def test_sort_algorithms_key(self, random_float_list):
        for name, sort_func in sort_algorithms.items():
            seq = random_float_list[:]
            sort_func(seq, key=lambda x: abs(x))
            assert seq == sorted(random_float_list, key=lambda x: abs(x)), f"{name} failed key sorting"

    def test_empty_list(self):
        for name, sort_func in sorted_algorithms.items():
            assert sort_func([]) == [], f"{name} failed empty list"
        for name, sort_func in sort_algorithms.items():
            seq = []
            sort_func(seq)
            assert seq == [], f"{name} failed empty list"

    def test_single_element(self):
        for name, sort_func in sorted_algorithms.items():
            assert sort_func([1]) == [1], f"{name} failed single element"
        for name, sort_func in sort_algorithms.items():
            seq = [1]
            sort_func(seq)
            assert seq == [1], f"{name} failed single element"

    def test_already_sorted(self, random_list):
        sorted_list = sorted(random_list)
        for name, sort_func in sorted_algorithms.items():
            result = sort_func(sorted_list[:])
            assert result == sorted_list, f"{name} failed already sorted list"
        for name, sort_func in sort_algorithms.items():
            seq = sorted_list[:]
            sort_func(seq)
            assert seq == sorted_list, f"{name} failed already sorted list"

    def test_reverse_sorted(self, random_list):
        reverse_sorted_list = sorted(random_list, reverse=True)
        for name, sort_func in sorted_algorithms.items():
            result = sort_func(reverse_sorted_list[:], reverse=True)
            assert result == reverse_sorted_list, f"{name} failed reverse sorted list"
        for name, sort_func in sort_algorithms.items():
            seq = reverse_sorted_list[:]
            sort_func(seq, reverse=True)
            assert seq == reverse_sorted_list, f"{name} failed reverse sorted list"

    def test_all_same_elements(self):
        same_list = [5] * 100
        for name, sort_func in sorted_algorithms.items():
            assert sort_func(same_list[:]) == same_list, f"{name} failed all same elements"
        for name, sort_func in sort_algorithms.items():
            seq = same_list[:]
            sort_func(seq)
            assert seq == same_list, f"{name} failed all same elements"

    def test_string_sorting(self, random_string_list):
        for name, sort_func in sorted_algorithms.items():
            seq = random_string_list[:]
            result = sort_func(seq)
            assert result == sorted(random_string_list), f"{name} failed string sorting"
        for name, sort_func in sort_algorithms.items():
            seq = random_string_list[:]
            sort_func(seq)
            assert seq == sorted(random_string_list), f"{name} failed string sorting"