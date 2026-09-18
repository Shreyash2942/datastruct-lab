"""Verify theoretical bounds independently for every public operation."""

from dataclasses import FrozenInstanceError

import pytest

from src.analysis import analyze_complexity, supported_operations, supported_structures
from src.structures import LinkedList, Queue, Stack


CASES = [
    ("Stack", "push", "O(1) amortized", "O(n)", "O(1)"),
    ("Stack", "pop", "O(1) amortized", "O(n)", "O(1)"),
    ("Stack", "peek", "O(1)", "O(1)", "O(1)"),
    ("Stack", "search", "O(n)", "O(n)", "O(1)"),
    ("Stack", "is_empty", "O(1)", "O(1)", "O(1)"),
    ("Stack", "size", "O(1)", "O(1)", "O(1)"),
    ("Stack", "to_list", "O(n)", "O(n)", "O(n)"),
    ("Queue", "enqueue", "O(1)", "O(1)", "O(1)"),
    ("Queue", "dequeue", "O(1)", "O(1)", "O(1)"),
    ("Queue", "peek", "O(1)", "O(1)", "O(1)"),
    ("Queue", "search", "O(n)", "O(n)", "O(1)"),
    ("Queue", "is_empty", "O(1)", "O(1)", "O(1)"),
    ("Queue", "size", "O(1)", "O(1)", "O(1)"),
    ("Queue", "to_list", "O(n)", "O(n)", "O(n)"),
    ("Linked List", "insert", "O(1)", "O(1)", "O(1)"),
    ("Linked List", "delete", "O(n)", "O(n)", "O(1)"),
    ("Linked List", "search", "O(n)", "O(n)", "O(1)"),
    ("Linked List", "traverse", "O(n)", "O(n)", "O(n)"),
    ("Linked List", "is_empty", "O(1)", "O(1)", "O(1)"),
    ("Linked List", "size", "O(1)", "O(1)", "O(1)"),
]


@pytest.mark.parametrize("structure,operation,time,worst,result_space", CASES)
def test_every_operation_has_correct_time_space_and_explanation(structure, operation, time, worst, result_space):
    prediction = analyze_complexity(structure, operation, 10_000)
    assert (prediction.structure, prediction.operation, prediction.input_size) == (structure, operation, 10_000)
    assert prediction.rule.time == time
    assert prediction.rule.worst_time == worst
    assert prediction.rule.result_space == result_space
    assert prediction.storage_space == "O(n)"
    assert prediction.rule.best_time == ("O(n)" if result_space == "O(n)" else "O(1)")
    resizing = structure == "Stack" and operation in {"push", "pop"}
    assert prediction.rule.auxiliary_space == ("O(n) during resize" if resizing else "O(1)")
    assert prediction.rule.explanation
    assert "10,000" in prediction.growth_explanation
    assert "not exact runtime" in prediction.growth_explanation


def test_supported_operations_cover_all_public_structure_methods():
    classes = {"Stack": Stack, "Queue": Queue, "Linked List": LinkedList}
    assert supported_structures() == tuple(classes)
    assert {(s, o) for s, o, *_ in CASES} == {(s, o) for s in classes for o in supported_operations(s)}
    for name, cls in classes.items():
        public = {method for method in vars(cls) if not method.startswith("_") and callable(getattr(cls, method))}
        assert set(supported_operations(name)) == public


@pytest.mark.parametrize("structure,operation,factors", [
    ("Stack", "push", [1, 1, 1]),
    ("Queue", "enqueue", [1, 1, 1]),
    ("Linked List", "insert", [1, 1, 1]),
    ("Linked List", "delete", [1, 2, 4]),
    ("Linked List", "traverse", [1, 2, 4]),
    ("Stack", "search", [1, 2, 4]),
])
def test_growth_scales_input_sizes_without_changing_bounds(structure, operation, factors):
    for size in [1, 100, 10**12]:
        prediction = analyze_complexity(structure, operation, size)
        assert [n for n, _ in prediction.growth_points] == [size, 2 * size, 4 * size]
        assert [work for _, work in prediction.growth_points] == factors
        assert len(prediction.growth_points) == 3
        assert prediction.rule == analyze_complexity(structure, operation, 1).rule


@pytest.mark.parametrize("size", [0, -1, 1.0, 1.5, True, False, None, "100", [], float("nan"), float("inf")])
def test_invalid_sizes_are_rejected(size):
    with pytest.raises(ValueError, match="positive integer"):
        analyze_complexity("Stack", "search", size)


@pytest.mark.parametrize("structure,operation", [("Tree", "search"), (None, "search"), ([], "search"), ("Stack", "enqueue"), ("Queue", "pop"), ("Linked List", "append"), ("Stack", None), ("Stack", [])])
def test_invalid_selections_are_rejected(structure, operation):
    with pytest.raises(ValueError):
        analyze_complexity(structure, operation, 10)


def test_explanations_state_implementation_assumptions():
    assert "at the head" in analyze_complexity("Linked List", "insert", 10).rule.explanation
    assert "first matching" in analyze_complexity("Linked List", "delete", 10).rule.explanation
    assert "resiz" in analyze_complexity("Stack", "push", 10).rule.explanation
    assert "amortized" in analyze_complexity("Stack", "pop", 10).growth_explanation
    assert "deque" in analyze_complexity("Queue", "dequeue", 10).rule.explanation


def test_results_cannot_mutate_shared_complexity_rules():
    prediction = analyze_complexity("Stack", "peek", 10)
    with pytest.raises(FrozenInstanceError):
        prediction.rule.time = "O(n)"
    with pytest.raises(FrozenInstanceError):
        prediction.input_size = 0
    assert analyze_complexity("Stack", "peek", 20).rule.time == "O(1)"
