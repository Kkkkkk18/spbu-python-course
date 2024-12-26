import pytest
from project.generators.RGBA import (
    get_rgba_element,
    rgba_generator,
)


@pytest.mark.parametrize(
    "index, expected",
    [
        (1, (0, 0, 0, 0)),
        (2, (0, 0, 0, 2)),
        (51, (0, 0, 0, 100)),
        (52, (0, 0, 1, 0)),
        (256 * 51 + 1, (0, 1, 0, 0)),
        (256 * 256 * 51 + 1, (1, 0, 0, 0)),
    ],
)
def test_get_rgba_element(index, expected):

    """
    Tests the `get_rgba_element` function to ensure it returns the expected RGBA tuple for given indices.

    """

    assert get_rgba_element(index) == expected


def test_rgba_generator():

    """
    Tests the `rgba_generator` function to ensure it generates the expected sequence of RGBA tuples.

    """

    generator = rgba_generator()
    assert next(generator) == (0, 0, 0, 0)
    assert next(generator) == (0, 0, 0, 2)
    assert next(generator) == (0, 0, 0, 4)
    assert next(generator) == (0, 0, 0, 6)
    assert next(generator) == (0, 0, 0, 8)
    assert next(generator) == (0, 0, 0, 10)


def test_get_rgba_element_error():

    """
    Tests the `get_rgba_element` function to ensure it raises an AssertionError for invalid indices.

    """

    with pytest.raises(AssertionError):
        get_rgba_element(0)
    with pytest.raises(AssertionError):
        get_rgba_element(-1)
