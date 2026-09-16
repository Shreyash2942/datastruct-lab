"""A singly linked list with constant-time insertion at the head."""

from __future__ import annotations

from typing import Generic, TypeVar


T = TypeVar("T")


class Node(Generic[T]):
    """Store one value in data and a reference to the next node in next."""

    def __init__(self, data: T, next: Node[T] | None = None) -> None:
        """Store data and the optional next node (default None) in O(1) time."""
        self.data = data
        self.next = next


class LinkedList(Generic[T]):
    """Store values in linked nodes using O(n) storage.

    Insertions occur at the head; deletion removes the first equal value from
    the head. Duplicates are allowed and each instance owns its node chain.
    Time bounds assume constant-cost equality comparisons.
    """

    def __init__(self) -> None:
        """Create an empty list with no arguments in O(1) time."""
        self._head: Node[T] | None = None
        self._size = 0

    def insert(self, value: T) -> None:
        """Insert value at the head and return None. Time: O(1)."""
        self._head = Node(value, self._head)
        self._size += 1

    def delete(self, value: T) -> bool:
        """Remove the first value equal to value; return whether one was removed.

        An empty list or missing value returns False without changing state.
        Time: O(n) worst case; auxiliary space: O(1). Exceptions raised by
        value equality comparisons propagate before any mutation occurs.
        """
        previous: Node[T] | None = None
        current = self._head
        while current is not None:
            if current.data == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def search(self, value: T) -> bool:
        """Return whether an equal value occurs, searching from head to tail.

        Does not change the list. Time: O(n) worst case, O(1) best case;
        auxiliary space: O(1). Exceptions from value equality propagate.
        """
        current = self._head
        while current is not None:
            if current.data == value:
                return True
            current = current.next
        return False

    def traverse(self) -> list[T]:
        """Return a new list of values from head to tail; takes no arguments.

        Return [] if empty. The result is a shallow copy: values are shared,
        but adding/removing entries in the result does not alter the nodes.
        Time and result space: O(n).
        """
        values: list[T] = []
        current = self._head
        while current is not None:
            values.append(current.data)
            current = current.next
        return values

    def is_empty(self) -> bool:
        """Return True if no nodes remain; no arguments. Time: O(1)."""
        return self._head is None

    def size(self) -> int:
        """Return the maintained element count; no arguments. Time: O(1)."""
        return self._size
