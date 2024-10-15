import pytest
import random
from project.smart_args import (
    smart_args,
    Evaluated,
    Isolated,
)


def test_evaluated():
    def get_random_number():
        return random.randint(1, 10)

    def evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
        return x, y

    res_1 = evaluation()
    res_2 = evaluation()

    assert res_1[0] == res_2[0]
    assert res_1[1] != res_2[1]


def test_isolated():
    def isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    res = isolation(d={"a": 10})
    assert res == {"a": 0}
