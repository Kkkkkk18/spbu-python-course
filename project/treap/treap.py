import random
from collections.abc import MutableMapping
from typing import Any, Optional, Tuple, Generator


class Node:

    """
    A class representing a node in a Cartesian Tree (Treap).

    Attributes:
        key (int): The key of the node.
        value (Any): The value associated with the key.
        left (Optional[Node]): The left child node.
        right (Optional[Node]): The right child node.
        priority (int): The priority of the node, used for balancing the tree.
    """

    def __init__(self, key: int, value: Any, priority: Optional[int] = None):

        """
        Initializes a new instance of the Node class.

        Args:
            key (int): The key of the node.
            value (Any): The value associated with the key.
            priority (Optional[int]): The priority of the node. If not provided, a random priority is assigned.
        """
        self.key: int = key
        self.value: Any = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.priority: int = (
            priority if priority is not None else random.randint(1, 100)
        )


class CartesianTree(MutableMapping):

    """
    A class representing a Cartesian Tree (Treap), which is a type of balanced binary search tree.

    Attributes:
        root (Optional[Node]): The root node of the tree.

    Methods:
    _merge(left, right)
            Merge two treaps into one
    _split(node, key)
        Split treap into two subtrees
    _rotate_left(node)
        Rotate treap to left
    _rotate_right(node)
        Rotate treap to right
    _insert(node, key, value)
        Insert new key and value or change value of existing key
    __setitem__(key, value)
        Add new key and value or change value of existing key to the treap
    _find(node, key)
        Return value of the given key
    __getitem__(key)
        Get value of the given key inn the treap
    __delitem__(key)
        Delete given key and its value from the treap
    _delete(node, key)
        Delete given key and its value
    __iter__()
        Return iterator of keys in the treap
    _inorder_traversal(node)
        Iterate through keys in ascending order
    __reverse__()
        Return reverse iterator of keys in the treap
    _reverse_inorder_traversal(node)
        Iterate through keys in descending order
    __len__()
        Return number of nodes in the treap
    _count(node)
        Return number of nodes
    __contains__(key)
       Return True if the given key is in the treap
    __treap_str__()
       Return keys and values of nodes as a string
    """

    def __init__(self, root: Optional[Node] = None):
        """
        Initializes a new instance of the CartesianTree class.

        Args:
            root (Optional[Node]): The root node of the tree.
        """
        self.root: Optional[Node] = root

    def _merge(self, left: Optional[Node], right: Optional[Node]) -> Optional[Node]:

        """
        Merges two subtrees into a single tree.

        Args:
            left (Optional[Node]): The left subtree.
            right (Optional[Node]): The right subtree.

        Returns:
            Optional[Node]: The merged tree.
        """

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

        """
        Splits the tree into two subtrees based on the given key.

        Args:
            node (Optional[Node]): The root node of the tree to split.
            key (int): The key to split the tree on.

        Returns:
            Tuple[Optional[Node], Optional[Node]]: A tuple containing the left and right subtrees.
        """

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

        """
        Performs a left rotation on the given node.

        Args:
            node (Node): The node to rotate.

        Returns:
            Node: The new root node after rotation.
        """

        if not node.right:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def _rotate_right(self, node: Node) -> Node:

        """
        Performs a right rotation on the given node.

        Args:
            node (Node): The node to rotate.

        Returns:
            Node: The new root node after rotation.
        """

        if not node.left:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _insert(self, node: Optional[Node], key: int, value: Any) -> Node:

        """
        Inserts a new key-value pair into the tree.

        Args:
            node (Optional[Node]): The root node of the tree.
            key (int): The key to insert.
            value (Any): The value associated with the key.

        Returns:
            Node: The new root node after insertion.
        """

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

        """
        Sets the value for the given key in the tree.

        Args:
            key (int): The key to set.
            value (Any): The value to associate with the key.
        """

        self.root = self._insert(self.root, key, value)

    def _find(self, node: Optional[Node], key: int) -> Any:

        """
        Finds the value associated with the given key in the tree.

        Args:
            node (Optional[Node]): The root node of the tree.
            key (int): The key to find.

        Returns:
            Any: The value associated with the key, or None if the key is not found.
        """

        if not node:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def __getitem__(self, key: int) -> Any:

        """
        Gets the value associated with the given key in the tree.

        Args:
            key (int): The key to get.

        Returns:
            Any: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the tree.
        """

        value = self._find(self.root, key)
        if value is None:
            raise KeyError(f"!key {key} not found!")
        return value

    def __delitem__(self, key: int) -> None:

        """
        Deletes the key-value pair with the given key from the tree.

        Args:
            key (int): The key to delete.

        Raises:
            KeyError: If the key is not found in the tree.
        """

        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[Node], key: int) -> Optional[Node]:

        """
        Deletes the key-value pair with the given key from the tree.

        Args:
            node (Optional[Node]): The root node of the tree.
            key (int): The key to delete.

        Returns:
            Optional[Node]: The new root node after deletion.

        Raises:
            KeyError: If the key is not found in the tree.
        """

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

        """
        Returns an iterator over the keys in the tree in ascending order.

        Yields:
            int: The keys in the tree.
        """

        yield from self._in_order_traversal(self.root)

    def _in_order_traversal(self, node: Optional[Node]) -> Generator[int, Any, None]:

        """
        Performs an in-order traversal of the tree.

        Args:
            node (Optional[Node]): The root node of the tree.

        Yields:
            int: The keys in the tree in ascending order.
        """

        if node:
            yield from self._in_order_traversal(node.left)
            yield node.key
            yield from self._in_order_traversal(node.right)

    def __reversed__(self) -> Generator[int, Any, None]:

        """
        Returns an iterator over the keys in the tree in descending order.

        Yields:
            int: The keys in the tree.
        """

        yield from self._reverse_in_order_traversal(self.root)

    def _reverse_in_order_traversal(
        self, node: Optional[Node]
    ) -> Generator[int, Any, None]:

        """
        Performs a reverse in-order traversal of the tree.

        Args:
            node (Optional[Node]): The root node of the tree.

        Yields:
            int: The keys in the tree in descending order.
        """

        if node:
            yield from self._reverse_in_order_traversal(node.right)
            yield node.key
            yield from self._reverse_in_order_traversal(node.left)

    def __len__(self) -> int:

        """
        Returns the number of key-value pairs in the tree.

        Returns:
            int: The number of key-value pairs in the tree.
        """

        return self._count(self.root)

    def _count(self, node: Optional[Node]) -> int:

        """
        Counts the number of nodes in the tree.

        Args:
            node (Optional[Node]): The root node of the tree.

        Returns:
            int: The number of nodes in the tree.
        """

        if not node:
            return 0
        return 1 + self._count(node.left) + self._count(node.right)

    def __contains__(self, key: Any) -> bool:

        """
        Checks if the tree contains the given key.

        Args:
            key (Any): The key to check.

        Returns:
            bool: True if the key is in the tree, False otherwise.
        """
        return self._find(self.root, key)

    def __treap_str__(self) -> str:

        """
        Returns a string representation of the tree.

        Returns:
            str: A string representation of the tree.
        """

        return f"Treap({list(self)})"
