"""A deque-backed queue that adds at the rear and removes from the front."""

from collections import deque
from typing import Generic, TypeVar


T = TypeVar("T")


class Queue(Generic[T]):
    """Store values in first-in, first-out (FIFO) order using O(n) storage.

    Values may be duplicated. Each queue owns its own deque. Using both ends
    avoids shifting all remaining values on removal. Time bounds assume
    constant-cost equality comparisons.
    """

    def __init__(self) -> None:
        """Create an empty queue in O(1) time; takes no arguments."""
        self._items: deque[T] = deque()

    def enqueue(self, value: T) -> None:
        """Add value at the rear and return None. Time: O(1)."""
        self._items.append(value)

    def dequeue(self) -> T:
        """Remove and return the front value; takes no arguments.

        Raises IndexError if empty, leaving the queue unchanged. Time: O(1).
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue.")
        return self._items.popleft()

    def peek(self) -> T:
        """Return the front value without removing it; takes no arguments.

        Raises IndexError if empty. Time: O(1).
        """
        if self.is_empty():
            raise IndexError("Cannot peek at an empty queue.")
        return self._items[0]

    def search(self, value: T) -> bool:
        """Return whether value occurs, searching from front to rear.

        Does not change the queue. Time: O(n) worst case, O(1) best case.
        Exceptions raised by a value's equality comparison propagate.
        """
        return value in self._items

    def is_empty(self) -> bool:
        """Return True if no values remain; no arguments. Time: O(1)."""
        return not self._items

    def size(self) -> int:
        """Return the number of stored values; no arguments. Time: O(1)."""
        return len(self._items)
