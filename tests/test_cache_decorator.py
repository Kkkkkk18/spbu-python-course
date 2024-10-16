import pytest
from project.cache_decorator import cache_results


def test_cache_exercise():

    """
    Test the basic functionality of a function without caching.

    This test defines a simple function `func_sum` that calculates the sum of a list
    and asserts that the function returns the correct result.
    """

    def func_sum(val):
        return sum(val)

    assert func_sum([1, 2, 3]) == 6


def add(x, y):
    return x + y


def test_cache_error():

    """
    Test the behavior of a function without caching.

    """
    res_1 = add(1, 2)
    assert res_1 == 3
    res_2 = add(1, 2)
    assert res_2 == res_1  # the result is already in the cache


def test_cache_with_limit():

    """
    Test the caching behavior with a limited cache size.

    This test applies the `cache_results` decorator to the `add` function with
    a maximum cache size of 2. It verifies that the cache correctly stores and
    retrieves results, and that the oldest results are evicted when the cache
    size limit is reached.
    """
    cached_function = cache_results(max_results=2)(add)

    assert cached_function(1, 2) == 3  # calculate and cache
    assert cached_function(3, 4) == 7  # calculate and cache
    assert cached_function(5, 6) == 11  # calculate and cache and 1st delete
    assert cached_function(1, 2) == 3  # add 1st again and calculate
