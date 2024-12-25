import pytest
from project.generators.primes_generator import (
    prime_generator,
    kth_prime_generator,
)


def test_prime_generator_first_primes():
    gen = prime_generator()
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 5
    assert next(gen) == 7
    assert next(gen) == 11
    assert next(gen) == 13


@pytest.mark.parametrize(
    "k, expected",
    [(1, [2, 3]), (3, [5, 7]), (8, [19, 23])],
)
def test_get_kth_prime(k, expected):

    decorated_gen = kth_prime_generator(prime_generator)
    for exp in expected:
        assert decorated_gen(k) == exp
        k += 1


@pytest.mark.parametrize("k", [-1, 0])
def test_get_k_prime_invalid_k(k):
    decorated_gen = kth_prime_generator(prime_generator)
    with pytest.raises(AssertionError):
        decorated_gen(k)
