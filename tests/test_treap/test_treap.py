from project.treap.treap import CartesianTree, Node
import pytest
from collections.abc import MutableMapping


@pytest.fixture
def sample_treap():

    tree = CartesianTree()
    tree[1] = "a"
    tree[2] = "b"
    tree[3] = "c"
    tree[4] = "d"
    return tree


def test__merge(sample_treap):
    left = CartesianTree()
    right = CartesianTree()

    left[1] = "a"
    left[2] = "b"

    right[3] = "c"
    right[4] = "d"

    root = sample_treap._merge(left.root, right.root)
    merged = CartesianTree(root)

    assert len(merged) == 4
    assert all(k in merged for k in range(1, 5))


@pytest.mark.parametrize(
    "key,value",
    [
        (10, "e"),
        (15, "f"),
        (20, "g"),
    ],
)
def test_insert(sample_treap, key, value):

    sample_treap[key] = value
    assert sample_treap[key] == value


@pytest.mark.parametrize(
    "key,value",
    [
        (1, "a"),
        (2, "b"),
        (3, "c"),
        (4, "d"),
    ],
)
def test__getitem__(sample_treap, key, value):

    assert sample_treap[key] == value


@pytest.mark.parametrize(
    "key",
    [
        -1,
        0,
        -11,
        -2,
    ],
)
def test__getitem__error(sample_treap, key):

    with pytest.raises(KeyError):
        sample_treap[key]


@pytest.mark.parametrize("key", [1, 2, 3, 4])
def test__delitem__(sample_treap, key):

    del sample_treap[key]
    assert key not in sample_treap


def test__delitem__error(sample_treap):
    with pytest.raises(KeyError):

        del sample_treap[5]


@pytest.mark.parametrize("key", [1, 2, 3, 4])
def test_contains(sample_treap, key):

    assert key in sample_treap


@pytest.mark.parametrize("key", [50, 100, -2])
def test_not_contains(sample_treap, key):

    assert key not in sample_treap


def test__iter__(sample_treap):

    assert list(sample_treap) == [1, 2, 3, 4]


def test__reversed__iter__(sample_treap):

    assert list(reversed(sample_treap)) == [4, 3, 2, 1]


def test__len__(sample_treap):

    assert len(sample_treap) == 4
    sample_treap[5] = "e"
    assert len(sample_treap) == 5
    del sample_treap[5]
    assert len(sample_treap) == 4


def test_mutablemapping(sample_treap):

    assert isinstance(sample_treap, MutableMapping)


def test_interaction_brackets(sample_treap):

    assert sample_treap[1] == "a"
    sample_treap[1] = "x"
    assert sample_treap[1] == "x"
    del sample_treap[1]
    with pytest.raises(KeyError):
        _ = sample_treap[1]
