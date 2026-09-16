"""Verify linked-list behavior and the Node contract."""

from random import Random

import pytest

from src.structures import LinkedList, Node


def test_node_stores_data_and_next_reference():
    tail = Node(10)
    head = Node(20, tail)
    assert tail.data == 10
    assert tail.next is None
    assert head.data == 20
    assert head.next is tail


def test_empty_list_operations_preserve_empty_state():
    linked = LinkedList[int]()
    assert linked.is_empty() is True
    assert linked.size() == 0
    assert linked.traverse() == []
    assert linked.search(10) is False
    assert linked.delete(10) is False
    assert linked.size() == 0
    assert linked.is_empty() is True


def test_insert_at_head_and_read_operations_preserve_order():
    linked = LinkedList[int]()
    for count, value in enumerate([10, 20, 30], start=1):
        assert linked.insert(value) is None
        assert linked.size() == count
        assert linked.is_empty() is False
    for value in [30, 20, 10]:
        assert linked.search(value) is True
    assert linked.search(99) is False
    assert linked.traverse() == [30, 20, 10]
    assert linked.traverse() == [30, 20, 10]
    assert linked.size() == 3


@pytest.mark.parametrize(
    ("value", "removed", "expected"),
    [
        (30, True, [20, 10]),
        (20, True, [30, 10]),
        (10, True, [30, 20]),
        (99, False, [30, 20, 10]),
    ],
    ids=["head", "middle", "tail", "missing"],
)
def test_delete_relinks_neighbors_and_updates_count(value, removed, expected):
    linked = LinkedList[int]()
    for item in [10, 20, 30]:
        linked.insert(item)
    assert linked.delete(value) is removed
    assert linked.traverse() == expected
    assert linked.size() == len(expected)
    assert linked.is_empty() is False


def test_delete_only_first_duplicate_from_head():
    linked = LinkedList[int]()
    for value in [7, 3, 7]:
        linked.insert(value)
    assert linked.delete(7) is True
    assert linked.traverse() == [3, 7]
    assert linked.size() == 2
    assert linked.search(7) is True
    assert linked.delete(7) is True
    assert linked.traverse() == [3]
    assert linked.delete(7) is False
    assert linked.size() == 1


def test_single_element_removal_and_reuse():
    linked = LinkedList[int]()
    for value in range(10):
        linked.insert(value)
        assert linked.traverse() == [value]
        assert linked.size() == 1
        assert linked.search(value) is True
        assert linked.delete(value) is True
        assert linked.is_empty() is True
        assert linked.size() == 0
        assert linked.traverse() == []
        assert linked.search(value) is False
        assert linked.delete(value) is False


def test_traversal_returns_independent_container_with_shared_values():
    linked = LinkedList[list[int]]()
    value = [1, 2]
    linked.insert(value)
    snapshot = linked.traverse()
    assert snapshot[0] is value
    snapshot.clear()
    assert linked.traverse() == [[1, 2]]
    assert linked.size() == 1
    snapshot = linked.traverse()
    linked.insert([3])
    assert snapshot == [[1, 2]]


def test_instances_are_independent_and_support_non_hashable_values():
    first = LinkedList[object]()
    second = LinkedList[object]()
    first.insert([1, 2])
    first.insert(None)
    assert second.is_empty() is True
    second.insert("independent")
    assert first.search([1, 2]) is True
    assert first.search(None) is True
    assert first.delete([1, 2]) is True
    assert first.traverse() == [None]
    assert first.delete(None) is True
    assert first.is_empty() is True
    assert second.traverse() == ["independent"]


def test_mixed_operations_match_reference_sequence():
    linked = LinkedList[int]()
    reference = []
    random = Random(506)
    for _ in range(300):
        value = random.randrange(12)
        operation = random.choice(["insert", "delete", "search"])
        if operation == "insert":
            linked.insert(value)
            reference.insert(0, value)
        elif operation == "delete":
            expected = value in reference
            assert linked.delete(value) is expected
            if expected:
                reference.remove(value)
        else:
            assert linked.search(value) is (value in reference)
        assert linked.traverse() == reference
        assert linked.size() == len(reference)
        assert linked.is_empty() is (len(reference) == 0)


def test_long_chain_operations_are_iterative():
    linked = LinkedList[int]()
    for value in range(3000):
        linked.insert(value)
    assert linked.search(0) is True
    assert linked.search(-1) is False
    assert linked.delete(0) is True
    assert linked.traverse() == list(range(2999, 0, -1))
    assert linked.size() == 2999
