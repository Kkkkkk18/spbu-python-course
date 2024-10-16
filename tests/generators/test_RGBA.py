import pytest
from project.generators.RGBA import get_rgba_element


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (50, (0, 0, 0, 100)),
        (51, (0, 0, 1, 0)),
        (256 * 51, (0, 1, 0, 0)),
        (256 * 256 * 51, (1, 0, 0, 0)),
    ],
)
def test_get_rgba_element(index, expected):
    assert get_rgba_element(index) == expected


@pytest.mark.parametrize("index_error", [-1, 256 * 256 * 256 * 51])
def test_get_rgba_element_error(index_error):

    with pytest.raises(IndexError):
        get_rgba_element(index_error)
