"""Check diagram semantics, escaping, and read-only display snapshots."""

import pytest

from src.structures import Queue, Stack
from src.visualization.visualizer import structure_diagram


@pytest.mark.parametrize("kind,label", [("Stack", "TOP"), ("Queue", "FRONT / REAR"), ("Linked List", "HEAD → None")])
def test_empty_diagrams_have_orientation_labels(kind, label):
    html = structure_diagram(kind, [])
    assert label in html
    assert "Empty" in html and 'role="img"' in html


@pytest.mark.parametrize("kind", ["Stack", "Queue", "Linked List"])
def test_values_are_escaped_and_source_order_is_preserved(kind):
    values = ["<script>alert(1)</script>", 20]
    html = structure_diagram(kind, values)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert html.index("&lt;script&gt;") < html.index("20")
    assert values == ["<script>alert(1)</script>", 20]


def test_queue_singleton_has_both_end_labels_and_list_ends_at_none():
    assert "FRONT / REAR" in structure_diagram("Queue", [10])
    html = structure_diagram("Linked List", [10, 20])
    assert "HEAD" in html and "ds-pointer" in html and "None" in html
    with pytest.raises(ValueError, match="Unsupported"):
        structure_diagram("Tree", [])


@pytest.mark.parametrize("factory,add,expected", [(Stack, "push", [20, 10]), (Queue, "enqueue", [10, 20])])
def test_display_snapshots_preserve_structure_and_copy_container(factory, add, expected):
    structure = factory()
    assert structure.to_list() == []
    for value in [10, 20]:
        getattr(structure, add)(value)
    snapshot = structure.to_list()
    assert snapshot == expected
    snapshot.clear()
    assert structure.to_list() == expected
    assert structure.size() == 2
    assert structure.peek() == expected[0]
