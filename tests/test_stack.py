"""Verify the public stack contract without depending on its storage."""

import pytest

from src.structures.stack import Stack


def test_stack_follows_lifo_and_preserves_state_during_reads():
    stack = Stack[int]()
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert stack.search(10) is False

    for count, value in enumerate([10, 20, 10, 30], start=1):
        assert stack.push(value) is None
        assert stack.size() == count
        assert stack.is_empty() is False

    assert stack.peek() == 30
    assert stack.search(20) is True
    assert stack.search(99) is False
    assert stack.size() == 4
    for remaining, expected in zip([3, 2, 1, 0], [30, 10, 20, 10]):
        assert stack.pop() == expected
        assert stack.size() == remaining
        assert stack.is_empty() is (remaining == 0)


@pytest.mark.parametrize("operation", ["pop", "peek"])
def test_empty_operations_raise_clear_errors_and_allow_reuse(operation):
    stack = Stack[int]()
    with pytest.raises(IndexError, match="empty stack"):
        getattr(stack, operation)()
    assert stack.size() == 0
    assert stack.is_empty() is True
    stack.push(42)
    assert stack.peek() == 42
    assert stack.pop() == 42
    with pytest.raises(IndexError, match="empty stack"):
        getattr(stack, operation)()


def test_stacks_are_independent_and_accept_non_hashable_values():
    first = Stack[object]()
    second = Stack[object]()
    first.push([1, 2])
    first.push(None)
    assert first.search([1, 2]) is True
    assert first.search(None) is True
    assert first.pop() is None
    assert first.pop() == [1, 2]
    assert second.is_empty() is True
    second.push("independent")
    assert first.is_empty() is True


def test_interleaved_operations_follow_lifo_over_repeated_cycles():
    stack = Stack[int]()
    for cycle in range(100):
        stack.push(cycle)
        stack.push(cycle + 1)
        assert stack.pop() == cycle + 1
        stack.push(cycle + 2)
        assert stack.pop() == cycle + 2
        assert stack.pop() == cycle
        assert stack.size() == 0
        assert stack.is_empty() is True
