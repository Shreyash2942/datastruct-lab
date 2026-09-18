"""A list-backed stack with the most recently added value at the top."""

from typing import Generic, TypeVar


T = TypeVar("T")


class Stack(Generic[T]):
    """Store values in last-in, first-out (LIFO) order using O(n) storage.

    Values may be duplicated. Each stack owns its own list. Time bounds assume
    constant-cost equality comparisons; resizing makes push/pop amortized O(1).
    """

    def __init__(self) -> None:
        """Create an empty stack in O(1) time; takes no arguments."""
        self._items: list[T] = []

    def push(self, value: T) -> None:
        """Add value at the top and return None.

        Time: O(1) amortized, O(n) when the underlying list resizes.
        """
        self._items.append(value)

    def pop(self) -> T:
        """Remove and return the top value; takes no arguments.

        Raises IndexError if empty, leaving the stack unchanged.
        Time: O(1) amortized, O(n) when the underlying list resizes.
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top value without removing it; takes no arguments.

        Raises IndexError if empty. Time: O(1).
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def search(self, value: T) -> bool:
        """Return whether value occurs, searching from top to bottom.

        Does not change the stack. Time: O(n) worst case, O(1) best case.
        Exceptions raised by a value's equality comparison propagate.
        """
        return value in reversed(self._items)

    def is_empty(self) -> bool:
        """Return True if no values remain; no arguments. Time: O(1)."""
        return not self._items

    def size(self) -> int:
        """Return the number of stored values; no arguments. Time: O(1)."""
        return len(self._items)

    def to_list(self) -> list[T]:
        """Return a shallow snapshot from top to bottom in O(n) time/space.

        Takes no arguments. Changing the returned container leaves the stack
        unchanged; mutable values themselves remain shared.
        """
        return list(reversed(self._items))
