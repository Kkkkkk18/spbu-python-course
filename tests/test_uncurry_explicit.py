import pytest
from project.uncurry_explicit import uncurry_explicit
from project.curry_explicit import curry_explicit


def test_uncurry_basic_sum():

    """
    Test the basic functionality of uncurrying a sum function.

    """

    f1 = curry_explicit(lambda x, y: x + y, 2)
    f2 = uncurry_explicit(f1, 2)
    assert f2(3, 4) == 7


def test_uncurry_basic_mul():

    """
    Test the basic functionality of uncurrying a multiplication function.

    """

    f1 = curry_explicit(lambda x, y, z: x * y * z, 3)
    f2 = uncurry_explicit(f1, 2)
    assert f2(3, 2, 1) == 6


def test_uncurry_0_arity():

    """
    Test uncurrying a function with zero argument.

    """

    f1 = curry_explicit(lambda: ":(", 0)
    f2 = uncurry_explicit(f1, 0)
    assert f2() == ":("


def test_uncurry_1_arity():

    """
    Test uncurrying a function with one argument.

    """

    f1 = curry_explicit(lambda x: x * 2, 1)
    f2 = uncurry_explicit(f1, 1)
    assert f2(3) == 6


def test_uncurry_negative_arity():

    """
    Test the behavior when uncurrying a function with negative arity.

    """

    with pytest.raises(ValueError):
        uncurry_explicit(lambda x: x, -1)


def test_uncurry_error():

    """
    Test the behavior when providing the wrong number of arguments to an uncurried function.

    """
    with pytest.raises(TypeError):
        f1 = curry_explicit(lambda x, y: x * y, 2)
        f2 = uncurry_explicit(f1, 1)
        f2(1, 2, 3)


def test_uncurry_exercise():

    """
    Test uncurrying built-in functions min and max.

    """
    f_min_curry = curry_explicit(min, 3)
    f_min_uncurry = uncurry_explicit(f_min_curry, 3)
    assert f_min_uncurry(1, 2, 3) == 1
    f_max_curry = curry_explicit(max, 2)
    f_max_uncurry = uncurry_explicit(f_max_curry, 2)
    assert f_max_uncurry(12, 34) == 34
