from typing import Tuple


def get_rgba_element(i: int) -> Tuple[int, int, int, int]:

    generator = (
        (r, g, b, a)
        for b in range(256)
        for g in range(256)
        for r in range(256)
        for a in range(0, 101, 2)
    )

    for index, rgba in range(generator):
        if index == i:
            return rgba

    raise ValueError("!does not find the index!")
