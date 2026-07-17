# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive pytest tests for custom_random and gamehelpers (Timer classes).

These tests complement the doctests already embedded in the source modules.
They cover edge cases, error conditions, and behavior that is difficult or
impractical to express in a doctest (time-dependent behavior, statistical
properties, etc.).

Modules covered:
  - pyhelper.custom_random   (random, randint, choice, randrange, shuffle, sample)
  - pyhelper.gamehelpers      (Timer, CountUpTimer, CountDownTimer)
"""

import time

import pytest

from pyhelper.custom_random import choice, randint, randrange, random, sample, shuffle
from pyhelper.gamehelpers import CountDownTimer, CountUpTimer, Timer


# ===========================================================================
#  custom_random.random
# ===========================================================================
class TestRandom:
    """Tests for the base random() function."""

    def test_returns_float(self):
        result = random()
        assert isinstance(result, float)

    def test_range_zero_to_one(self):
        for _ in range(100):
            r = random()
            assert 0.0 <= r < 1.0

    def test_different_values(self):
        # Very unlikely to get 100 identical values from os.urandom
        values = {random() for _ in range(100)}
        assert len(values) > 1


# ===========================================================================
#  custom_random.randint
# ===========================================================================
class TestRandint:
    """Tests for randint()."""

    def test_single_value_range(self):
        result = randint(5, 5, random=lambda: 0.5)
        assert result == 5

    def test_min_equals_max(self):
        result = randint(3, 3, random=lambda: 0.99)
        assert result == 3

    def test_single_arg(self):
        # randint(n) is equivalent to randint(1, n)
        result = randint(1, random=lambda: 0.0)
        assert result == 1

    def test_single_arg_max(self):
        result = randint(1, random=lambda: 0.99)
        assert result == 1

    def test_range_inclusive(self):
        # Formula: int(random() * (min_ - max_ + 1)) + max_
        # For randint(1, 10): factor = 1 - 10 + 1 = -8
        # random=0.0 -> int(0) + 10 = 10 (max)
        # random=0.5 -> int(-4.0) + 10 = 6
        # random=0.99 -> int(-7.92) + 10 = 3
        assert randint(1, 10, random=lambda: 0.0) == 10
        assert randint(1, 10, random=lambda: 0.5) == 6
        assert randint(1, 10, random=lambda: 0.99) == 3

    def test_negative_range(self):
        # For randint(-5, -1): factor = -5 - (-1) + 1 = -3
        # random=0.0 -> int(0) + (-1) = -1 (max)
        # random=0.99 -> int(-2.97) + (-1) = -2 + (-1) = -3
        assert randint(-5, -1, random=lambda: 0.0) == -1
        assert randint(-5, -1, random=lambda: 0.99) == -3

    def test_value_in_range(self):
        for _ in range(200):
            val = randint(1, 100)
            assert 1 <= val <= 100

    def test_value_in_range_negative(self):
        for _ in range(200):
            val = randint(-50, -1)
            assert -50 <= val <= -1

    def test_raises_value_error(self):
        with pytest.raises(ValueError, match="lower limit"):
            randint(10, 1, random=lambda: 0.5)

    def test_default_random_callable(self):
        # Without injecting random, should use os.urandom
        val = randint(1, 10)
        assert 1 <= val <= 10


# ===========================================================================
#  custom_random.choice
# ===========================================================================
class TestChoice:
    """Tests for choice()."""

    def test_returns_element_from_list(self):
        seq = [10, 20, 30]
        result = choice(seq, random=lambda: 0.0)
        assert result in seq

    def test_first_element(self):
        assert choice([10, 20, 30], random=lambda: 0.0) == 10

    def test_last_element(self):
        assert choice([10, 20, 30], random=lambda: 0.99) == 30

    def test_with_string(self):
        assert choice("abc", random=lambda: 0.0) == "a"
        assert choice("abc", random=lambda: 0.5) == "b"
        assert choice("abc", random=lambda: 0.99) == "c"

    def test_with_tuple(self):
        assert choice((1, 2, 3), random=lambda: 0.5) == 2

    def test_single_element(self):
        assert choice([42], random=lambda: 0.0) == 42
        assert choice([42], random=lambda: 0.99) == 42

    def test_empty_list_raises(self):
        with pytest.raises(IndexError, match="empty sequence"):
            choice([], random=lambda: 0.5)

    def test_empty_string_raises(self):
        with pytest.raises(IndexError, match="empty sequence"):
            choice("", random=lambda: 0.5)

    def test_random_selection_distribution(self):
        seq = list(range(10))
        counts = {i: 0 for i in seq}
        for _ in range(1000):
            val = choice(seq)
            counts[val] += 1
        # Every element should be chosen at least once in 1000 trials
        assert all(c > 0 for c in counts.values())


# ===========================================================================
#  custom_random.randrange
# ===========================================================================
class TestRandrange:
    """Tests for randrange()."""

    def test_basic(self):
        assert randrange(1, 10, random=lambda: 0.0) == 1
        assert randrange(1, 10, random=lambda: 0.99) == 10

    def test_single_arg(self):
        # randrange(n) is equivalent to randrange(1, n)
        result = randrange(5, random=lambda: 0.0)
        assert result == 1

    def test_with_step(self):
        # range(1, 11, 2) = [1, 3, 5, 7, 9, 10] — wait, stop is inclusive
        # Actually: range(start, stop+1, step) = range(1, 11, 2) = [1, 3, 5, 7, 9]
        # With random=0.0 → first element = 1
        assert randrange(1, 10, step=2, random=lambda: 0.0) == 1
        # With random=0.99 → last element
        result = randrange(1, 10, step=2, random=lambda: 0.99)
        assert result in [1, 3, 5, 7, 9, 10]

    def test_value_in_range(self):
        for _ in range(200):
            val = randrange(1, 100)
            assert 1 <= val <= 100

    def test_raises_on_stop_less_than_start(self):
        with pytest.raises(ValueError, match="Stop value"):
            randrange(10, 1, random=lambda: 0.5)

    def test_raises_on_zero_step(self):
        with pytest.raises(ValueError, match="Step cannot be zero"):
            randrange(1, 10, step=0, random=lambda: 0.5)


# ===========================================================================
#  custom_random.shuffle
# ===========================================================================
class TestShuffle:
    """Tests for shuffle()."""

    def test_preserves_elements(self):
        original = [1, 2, 3, 4, 5]
        shuffle(original, random=lambda: 0.5)
        assert sorted(original) == [1, 2, 3, 4, 5]

    def test_empty_list(self):
        lst = []
        shuffle(lst, random=lambda: 0.5)
        assert lst == []

    def test_single_element(self):
        lst = [42]
        shuffle(lst, random=lambda: 0.5)
        assert lst == [42]

    def test_two_elements_swap(self):
        # Fisher-Yates: i=1, j=int(random()*2)
        # random=0.0 -> j=0 -> swap seq[1] with seq[0]
        lst = [10, 20]
        shuffle(lst, random=lambda: 0.0)
        assert lst == [20, 10]

    def test_two_elements_no_swap(self):
        # random=0.5 -> j=int(1.0)=1 -> swap seq[1] with seq[1] (no-op)
        lst = [10, 20]
        shuffle(lst, random=lambda: 0.5)
        assert lst == [10, 20]

    def test_in_place_modification(self):
        original = [1, 2, 3, 4, 5]
        original_id = id(original)
        shuffle(original, random=lambda: 0.5)
        assert id(original) == original_id  # same object, modified in place

    def test_random_shuffle_preserves_multiset(self):
        original = list(range(20))
        shuffle(original)
        assert sorted(original) == list(range(20))

    def test_deterministic_with_fixed_random(self):
        """Same random sequence → same shuffle result."""
        r1 = iter([0.3, 0.7, 0.1, 0.9])
        lst1 = [1, 2, 3, 4, 5]
        shuffle(lst1, random=lambda: next(r1, 0.0))

        r2 = iter([0.3, 0.7, 0.1, 0.9])
        lst2 = [1, 2, 3, 4, 5]
        shuffle(lst2, random=lambda: next(r2, 0.0))

        assert lst1 == lst2


# ===========================================================================
#  custom_random.sample
# ===========================================================================
class TestSample:
    """Tests for sample()."""

    def test_basic(self):
        result = sample([1, 2, 3], 2, random=lambda: 0.0)
        assert len(result) == 2
        assert all(r in [1, 2, 3] for r in result)

    def test_unique_elements(self):
        result = sample(range(100), 10)
        assert len(result) == 10
        assert len(set(result)) == 10  # all unique

    def test_k_equals_len(self):
        result = sample([1, 2, 3], 3, random=lambda: 0.0)
        assert sorted(result) == [1, 2, 3]

    def test_k_zero(self):
        result = sample([1, 2, 3], 0, random=lambda: 0.0)
        assert result == []

    def test_k_one(self):
        result = sample([1, 2, 3], 1, random=lambda: 0.5)
        assert result == [2]

    def test_does_not_modify_population(self):
        pop = [1, 2, 3, 4, 5]
        pop_copy = pop[:]
        sample(pop, 3, random=lambda: 0.0)
        assert pop == pop_copy

    def test_raises_k_too_large(self):
        with pytest.raises(ValueError, match="Sample size larger"):
            sample([1, 2], 3, random=lambda: 0.0)

    def test_raises_type_error(self):
        with pytest.raises(TypeError, match="Population must be a sequence"):
            sample(42, 1, random=lambda: 0.0)

    def test_returns_list(self):
        result = sample((1, 2, 3), 2, random=lambda: 0.0)
        assert isinstance(result, list)

    def test_random_sample_unique(self):
        result = sample(range(50), 20)
        assert len(result) == 20
        assert len(set(result)) == 20


# ===========================================================================
#  Timer
# ===========================================================================
class TestTimer:
    """Tests for the Timer class."""

    def test_init_defaults(self):
        t = Timer()
        assert t.time_in_seconds == -1
        assert t.is_running is False

    def test_init_with_time(self):
        t = Timer(5)
        assert t.time_in_seconds == 5
        assert t.is_running is False

    def test_init_with_command(self):
        t = Timer(5, command=lambda: None)
        assert t.time_in_seconds == 5

    def test_start(self):
        t = Timer(5)
        t.start()
        assert t.is_running is True

    def test_start_with_new_time(self):
        t = Timer(5)
        t.start(10)
        assert t.time_in_seconds == 10
        assert t.is_running is True

    def test_start_default_uses_original_time(self):
        t = Timer(7)
        t.start()
        assert t.time_in_seconds == 7

    def test_pause(self):
        t = Timer(5)
        t.start()
        t.pause()
        assert t.is_running is False

    def test_go_on(self):
        t = Timer(5)
        t.start()
        t.pause()
        t.go_on()
        assert t.is_running is True

    def test_stop_not_running(self):
        t = Timer(5)
        t.stop()
        assert t.is_running is False

    def test_stop_running(self):
        t = Timer(5)
        t.start()
        t.stop()
        assert t.is_running is False

    def test_stop_executes_command(self):
        results = []
        t = Timer(5, command=lambda: results.append("done"))
        t.start()
        t.stop()
        assert results == ["done"]

    def test_stop_without_command(self):
        t = Timer(5)
        t.start()
        t.stop()  # should not raise

    def test_update_not_running(self):
        t = Timer(5)
        t.update()  # should not raise
        assert t.is_running is False

    def test_update_running_not_finished(self):
        t = Timer(100)
        t.start()
        t.update()
        assert t.is_running is True

    def test_update_finished(self):
        t = Timer(0)
        t.start()
        time.sleep(0.01)
        t.update()
        assert t.is_running is False

    def test_get_time_not_running(self):
        t = Timer(5)
        assert t.get_time() == 0.0

    def test_get_time_running(self):
        t = Timer(100)
        t.start()
        time.sleep(0.05)
        elapsed = t.get_time()
        assert 0.0 < elapsed < 1.0

    def test_get_time_with_precision(self):
        t = Timer(100)
        t.start()
        time.sleep(0.05)
        t.pause()
        elapsed = t.get_time(number_of_reserved_bits=0)
        assert isinstance(elapsed, (int, float))

    def test_start_time_property(self):
        t = Timer(5)
        t.start()
        assert t.start_time > 0

    def test_infinite_timer_never_finishes(self):
        t = Timer(-1)
        t.start()
        time.sleep(0.01)
        t.update()
        assert t.is_running is True

    def test_command_on_timer_expiry(self):
        results = []
        t = Timer(0, command=lambda: results.append("expired"))
        t.start()
        time.sleep(0.01)
        t.update()
        assert results == ["expired"]
        assert t.is_running is False

    def test_restart_timer(self):
        t = Timer(5)
        t.start()
        t.stop()
        t.start(3)
        assert t.is_running is True
        assert t.time_in_seconds == 3


# ===========================================================================
#  CountUpTimer
# ===========================================================================
class TestCountUpTimer:
    """Tests for the CountUpTimer class."""

    def test_init_defaults(self):
        t = CountUpTimer()
        assert t.is_running is False
        assert t.is_pause is False

    def test_init_with_start_time(self):
        t = CountUpTimer(10.0)
        assert t.start_time > 10.0  # start_time = start_time + time.time()

    def test_start(self):
        t = CountUpTimer()
        t.start()
        assert t.is_running is True
        assert t.is_pause is True

    def test_start_sets_is_pause(self):
        t = CountUpTimer()
        assert t.is_pause is False
        t.start()
        assert t.is_pause is True

    def test_get_time_not_started(self):
        t = CountUpTimer()
        assert t.get_time() == 0.0

    def test_get_time_after_start(self):
        t = CountUpTimer()
        t.start()
        time.sleep(0.05)
        elapsed = t.get_time()
        assert elapsed > 0.0

    def test_get_time_seconds_mode(self):
        t = CountUpTimer()
        t.start()
        time.sleep(0.05)
        elapsed = t.get_time(mode="Seconds")
        assert isinstance(elapsed, float)
        assert elapsed > 0.0

    def test_get_time_hhmmss_mode(self):
        t = CountUpTimer()
        t.start()
        time.sleep(0.05)
        result = t.get_time(mode="HHMMSS")
        assert isinstance(result, str)
        assert ":" in result
        # Format should be HH:MM:SS.s
        parts = result.split(":")
        assert len(parts) == 3

    def test_stop(self):
        t = CountUpTimer()
        t.start()
        t.stop()
        assert t.is_running is False

    def test_stop_preserves_time(self):
        t = CountUpTimer()
        t.start()
        time.sleep(0.05)
        t.stop()
        elapsed = t.get_time()
        assert elapsed > 0.0

    def test_get_time_after_stop(self):
        t = CountUpTimer()
        t.start()
        time.sleep(0.05)
        t.stop()
        time.sleep(0.05)
        # Time should not advance after stop
        elapsed1 = t.get_time()
        time.sleep(0.05)
        elapsed2 = t.get_time()
        assert elapsed1 == elapsed2

    def test_is_running_property(self):
        t = CountUpTimer()
        assert t.is_running is False
        t.start()
        assert t.is_running is True
        t.stop()
        assert t.is_running is False


# ===========================================================================
#  CountDownTimer
# ===========================================================================
class TestCountDownTimer:
    """Tests for the CountDownTimer class."""

    def test_init_seconds(self):
        t = CountDownTimer("00:01:00.0")
        assert t.seconds == 60.0

    def test_init_complex(self):
        t = CountDownTimer("01:30:20.5")
        assert t.seconds == 5420.5

    def test_init_with_command(self):
        t = CountDownTimer("00:00:05.0", command=lambda: None)
        assert t.seconds == 5.0

    def test_start(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        assert t.timer.is_running is True

    def test_pause(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        t.pause()
        assert t.timer.is_running is False

    def test_go_on(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        t.pause()
        t.go_on()
        assert t.timer.is_running is True

    def test_get_time_initial(self):
        t = CountDownTimer("00:00:10.0")
        assert t.get_time() == 10.0

    def test_get_time_after_start(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        time.sleep(0.05)
        t.update()  # update() refreshes _saved_time
        remaining = t.get_time()
        assert 9.0 < remaining < 10.0

    def test_get_time_hhmmss(self):
        t = CountDownTimer("00:01:00.0")
        result = t.get_time(mode="HHMMSS")
        assert isinstance(result, str)
        assert ":" in result

    def test_get_time_hhmmss_complex(self):
        t = CountDownTimer("01:30:20.5")
        result = t.get_time(mode="HHMMSS")
        assert isinstance(result, str)
        parts = result.split(":")
        assert len(parts) == 3

    def test_stop(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        t.stop()
        assert t.timer.is_running is False

    def test_update_decrements(self):
        t = CountDownTimer("00:00:10.0")
        t.start()
        time.sleep(0.05)
        t.update()
        remaining = t.get_time()
        assert remaining < 10.0

    def test_countdown_expiry(self):
        results = []
        t = CountDownTimer("00:00:00.0", command=lambda: results.append("done"))
        t.start()
        time.sleep(0.01)
        t.update()
        assert results == ["done"]

    def test_zero_seconds(self):
        t = CountDownTimer("00:00:00.0")
        assert t.seconds == 0.0

    def test_large_time(self):
        t = CountDownTimer("99:59:59.9")
        expected = 99 * 3600 + 59 * 60 + 59.9
        assert abs(t.seconds - expected) < 0.001
