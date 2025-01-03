import pytest
import random
from project.smart_args import (
    smart_args,
    Evaluated,
    Isolated,
)


def test_evaluated():

    """
    Test the Evaluated class functionality.

    """

    def get_random_number():

        """
        Returns a random integer between 1 and 10.

        """

        return random.randint(1, 10)

    @smart_args
    def evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
        return x, y

    res_1 = evaluation()
    res_2 = evaluation()
    assert res_1[0] == res_2[0]


def test_isolated():

    """
    Test the Isolated class functionality.

    """

    @smart_args
    def isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}
    res = isolation(d=no_mutable)
    assert res == {"a": 0}
    assert no_mutable == {"a": 10}


def test_isolated_error():

    """
    Test the error handling of the Isolated class.

    """

    @smart_args
    def isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    with pytest.raises(ValueError):
        isolation()


def test_evaluated_isolated():

    """
    Test the error handling of the Isolated class.

    """

    def get_random_number():
        return random.randint(1, 10)

    @smart_args
    def evaluated_isolated(*, x=Isolated(), y=Evaluated(get_random_number)):
        x["a"] = 0
        return (x, y)

    no_mutable = {"a": 10}
    with pytest.raises(AssertionError):
        evaluated_isolated(x=no_mutable)
