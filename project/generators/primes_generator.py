from typing import Generator, Callable


def prime_generator() -> Generator[int, None, None]:

    """
    Generates an infinite sequence of prime numbers.

    Returns:
        generator: A generator that yields prime numbers in ascending order.

    """

    num = 2
    while True:
        prime_num = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                prime_num = False
                break
        if prime_num:
            yield num
        num += 1


def kth_prime_generator(
    generator: Callable[[], Generator[int, None, None]]
) -> Callable:

    """
    Retrieve the k-th prime number.

    Parameters:
        gen: Generator[Any, None, None]
            Generator for our prime sequence

    Returns:
        Callable: the function which gives the k-th prime number.

    Raises:
        AssertionError: If `k` is not greater than 0.

    """
    gen = generator()
    index = 0

    def inner(k: int) -> int | None:
        assert k > 0
        nonlocal gen
        nonlocal index

        if k <= index:
            gen = generator()
            index = 0

        result = None
        while index != k:
            result = next(gen)
            index += 1
        return result

    return inner
