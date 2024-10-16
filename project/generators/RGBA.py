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

    assert i > 0
    generator = rgba_generator()
    s = 0
    for index in range(i):
        s = next(generator)
    return s
