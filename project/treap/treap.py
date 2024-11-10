import random
from collections.abc import MutableMapping
from typing import Any, Optional, Tuple, Generator


class Node:
    def __init__(self, key: int, value: Any, priority: Optional[int] = None):
        self.key: int = key
        self.value: Any = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.priority: int = (
            priority if priority is not None else random.randint(1, 100)
        )


class CartesianTree(MutableMapping):
    def __init__(self, root: Optional[Node] = None):
        self.root: Optional[Node] = root

    def _merge(self, left: Optional[Node], right: Optional[Node]) -> Optional[Node]:

        if left is None:
            return right

        if right is None:
            return left

        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def _split(
        self, node: Optional[Node], key: int
    ) -> Tuple[Optional[Node], Optional[Node]]:
        if not node:
            return None, None
        if key < node.key:
            left, right = self._split(node.left, key)
            node.left = right
            return left, node
        else:
            left, right = self._split(node.right, key)
            node.right = left
            return node, right

    def _rotate_left(self, node: Node) -> Node:

        if not node.right:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _rotate_right(self, node: Node) -> Node:

        if not node.left:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _insert(self, node: Optional[Node], key: int, value: Any) -> Node:

        if not node:
            return Node(key, value)
        if key == node.key:
            node.value = value
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
            if node.left and node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, key, value)
            if node.right and node.right.priority > node.priority:
                node = self._rotate_left(node)
        return node

    def __setitem__(self, key: int, value: Any) -> None:

        self.root = self._insert(self.root, key, value)

    def _find(self, node: Optional[Node], key: int) -> Any:
        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def __getitem__(self, key: int) -> Any:
        value = self._find(self.root, key)
        if value is None:
            raise KeyError(f"!key {key} not found!")
        return value

    def __delitem__(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[Node], key: int) -> Optional[Node]:

        if not node:
            raise KeyError(f"!key {key} not found!")
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            return self._merge(node.left, node.right)
        return node

    def __iter__(self) -> Generator[int, Any, None]:

        yield from self._in_order_traversal(self.root)

    def _in_order_traversal(self, node: Optional[Node]) -> Generator[int, Any, None]:

        if node:
            yield from self._in_order_traversal(node.left)
            yield node.key
            yield from self._in_order_traversal(node.right)

    def __reversed__(self) -> Generator[int, Any, None]:

        yield from self._reverse_in_order_traversal(self.root)

    def _reverse_in_order_traversal(
        self, node: Optional[Node]
    ) -> Generator[int, Any, None]:

        if node:
            yield from self._reverse_in_order_traversal(node.right)
            yield node.key
            yield from self._reverse_in_order_traversal(node.left)

    def __len__(self) -> int:
        return self._count(self.root)

    def _count(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)

    def __contains__(self, key: Any) -> bool:
        return self._find(self.root, key)

    def __treap_str__(self) -> str:

        return f"Treap({list(self)})"
