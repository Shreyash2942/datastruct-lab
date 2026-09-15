"""Verify the public queue contract without depending on its storage."""

import pytest

from src.structures.queue import Queue


def test_queue_follows_fifo_and_preserves_state_during_reads():
    queue = Queue[int]()
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert queue.search(10) is False

    for count, value in enumerate([10, 20, 10, 30], start=1):
        assert queue.enqueue(value) is None
        assert queue.size() == count
        assert queue.is_empty() is False

    assert queue.peek() == 10
    assert queue.search(20) is True
    assert queue.search(99) is False
    assert queue.size() == 4
    for remaining, expected in zip([3, 2, 1, 0], [10, 20, 10, 30]):
        assert queue.dequeue() == expected
        assert queue.size() == remaining
        assert queue.is_empty() is (remaining == 0)


@pytest.mark.parametrize("operation", ["dequeue", "peek"])
def test_empty_operations_raise_clear_errors_and_allow_reuse(operation):
    queue = Queue[int]()
    with pytest.raises(IndexError, match="empty queue"):
        getattr(queue, operation)()
    assert queue.size() == 0
    assert queue.is_empty() is True
    queue.enqueue(42)
    assert queue.peek() == 42
    assert queue.dequeue() == 42
    with pytest.raises(IndexError, match="empty queue"):
        getattr(queue, operation)()


def test_queues_are_independent_and_accept_non_hashable_values():
    first = Queue[object]()
    second = Queue[object]()
    first.enqueue([1, 2])
    first.enqueue(None)
    assert first.search([1, 2]) is True
    assert first.search(None) is True
    assert first.dequeue() == [1, 2]
    assert first.dequeue() is None
    assert second.is_empty() is True
    second.enqueue("independent")
    assert first.is_empty() is True


def test_interleaved_operations_follow_fifo_over_repeated_cycles():
    queue = Queue[int]()
    for cycle in range(100):
        queue.enqueue(cycle)
        queue.enqueue(cycle + 1)
        assert queue.dequeue() == cycle
        queue.enqueue(cycle + 2)
        assert queue.peek() == cycle + 1
        assert queue.dequeue() == cycle + 1
        assert queue.dequeue() == cycle + 2
        assert queue.size() == 0
        assert queue.is_empty() is True
