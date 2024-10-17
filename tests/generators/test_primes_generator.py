import pytest
from project.generators.primes_generator import (
    prime_generator,
    kth_prime_generator,
)


@pytest.mark.parametrize(
    "num_prime, expected_prime",
    [
        (5, [2, 3, 5, 7, 11]),
        (2, [2, 3]),
    ],
)
def test_prime_generator(num_prime, expected_prime):

    prime_gen = prime_generator()
    primes = [next(prime_gen) for _ in range(num_prime)]
    assert primes == expected_prime


@pytest.mark.parametrize(
    "k, expected_prime",
    [
        (1, 2),
        (2, 3),
        (3, 5),
        (4, 7),
        (5, 11),
    ],
)
def test_get_kth_prime(k, expected_prime):

    assert kth_prime_generator(k) == expected_prime


def test_get_kth_prime_error():
    with pytest.raises(AssertionError):
        kth_prime_generator(0)
    with pytest.raises(AssertionError):
        kth_prime_generator(-1)
