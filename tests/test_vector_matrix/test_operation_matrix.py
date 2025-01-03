import pytest
from project.operation_matrix_vector.operation_matrix import add, mul, transpose


def test_add():
    A = [[1, 0], [2, 5]]
    B = [[3, 9], [0, 4]]
    assert add(A, B) == [[4, 9], [2, 9]]


def test_add_value_error():
    with pytest.raises(ValueError):
        add([[1]], [[1, 2]])


def test_mul():
    A = [[8, 0], [1, 9], [0, 7]]
    B = [[8, 2, 3], [6, 0, 5]]
    assert mul(A, B) == [[64, 16, 24], [62, 2, 48], [42, 0, 35]]


def test_mul_value_error():
    with pytest.raises(ValueError):
        mul([[1, 2]], [[1], [2], [3]])


def test_mul_square():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[5.0, 6.0], [7.0, 8.0]]
    expected = [[19.0, 22.0], [43.0, 50.0]]
    assert mul(A, B) == expected


def test_transpose():
    A = [[1, 8], [2, 5]]
    assert transpose(A) == [[1, 2], [8, 5]]
