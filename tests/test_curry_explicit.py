import pytest
from project.curry_explicit import curry_explicit


def test_curry_basic_sum():
    f = curry_explicit(lambda x, y: x + y, 2)
    assert f(5)(2) == 7


def test_curry_basic_mul():
    f = curry_explicit(lambda x, y, z: x * y * z, 3)
    assert f(1)(2)(3) == 6


def test_curry_0_arity():
    f = curry_explicit(lambda: ":(", 0)
    assert f() == ":("


def test_curry_1_arity():
    f = curry_explicit(lambda x: x * 2, 1)
    assert f(3) == 6


def test_curry_negative_arity():
    with pytest.raises(ValueError):
        curry_explicit(lambda x: x, -1)


def test_curry_error():
    with pytest.raises(TypeError):
        f = curry_explicit(lambda x, y: x * y, 2)
        f(3)(2)(2)


def test_curry_exercise():
    f_min = curry_explicit(min, 3)
    assert f_min(1)(2)(3) == 1
    f_max = curry_explicit(max, 2)
    assert f_max(12)(34) == 34
