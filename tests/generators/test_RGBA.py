import pytest
from project.generators.RGBA import get_rgba_element


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
    assert get_rgba_element(index) == expected
