def rgba_generator():

    """
    Generates a sequence of RGBA (Red, Green, Blue, Alpha) tuples.

    Returns:
        A generator that yields tuples of the form `(r, g, b, a)`, where:
        - `r`, `g`, `b` are integers in the range `[0, 255]` representing the red, green, and blue components of the color, respectively.
        - `a` is an integer in the range `[0, 100]` representing the alpha transparency component, but only even values are included.

    """

    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(101)
        if a % 2 == 0
    )


def get_rgba_element(i):

    """
    Retrieves the `i`-th RGBA tuple from the sequence generated by `rgba_generator`.

    Args:
        i (int): The index of the RGBA tuple to retrieve. Must be greater than 0.

    Returns:
        tuple: The `i`-th RGBA tuple from the generated sequence.

    Raises:
        AssertionError: If `i` is not greater than 0.

    """

    assert i > 0
    generator = rgba_generator()
    s = 0
    for _ in range(i):
        s = next(generator)
    return s
