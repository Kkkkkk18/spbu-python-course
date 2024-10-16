import itertools


def rgba_generator():
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(101)
        if a % 2 == 0
    )


def get_rgba_element(i):

    generator = rgba_generator()

    for index, rgba in range(generator):
        if index == i:
            return rgba

    raise ValueError("!does not find the index!")
