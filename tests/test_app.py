"""Exercise real Streamlit widgets, reruns, and independent session state."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def open_page(name):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.radio("page").set_value(name).run()
    assert not app.exception
    return app


def click(app, page, action, value=None):
    if value is not None:
        app.text_input(f"value_{page}").set_value(value)
    app.button(f"{page}_{action}").click().run()
    assert not app.exception


@pytest.mark.parametrize("page", ["Home", "Stack", "Queue", "Linked List", "Complexity Analyzer", "Performance", "About"])
def test_every_page_renders(page):
    app = open_page(page)
    assert len(app.title) >= 1
    if page in {"Complexity Analyzer", "Performance"}:
        assert "Coming on Day" in app.info[0].value


@pytest.mark.parametrize("page,add,remove,next_value,remaining", [
    ("Stack", "Push", "Pop", 20, [10]),
    ("Queue", "Enqueue", "Dequeue", 10, [20]),
])
def test_stack_queue_controls_and_diagrams(page, add, remove, next_value, remaining):
    app = open_page(page)
    click(app, page, remove)
    assert "empty" in app.warning[0].value
    click(app, page, "Peek")
    assert "empty" in app.warning[0].value
    click(app, page, add, "10")
    click(app, page, add, "20")
    assert app.metric[0].value == "2"
    click(app, page, "Peek")
    assert f"Next value: {next_value}" in app.success[0].value
    click(app, page, "Search", "10")
    assert "10 was found" in app.success[0].value
    click(app, page, "Search", "99")
    assert "99 was not found" in app.success[0].value
    assert app.metric[0].value == "2"
    click(app, page, remove)
    assert f"Removed {next_value}" in app.success[0].value
    assert app.session_state["structures"][page].to_list() == remaining
    assert app.metric[0].value == "1"
    html = next(item.value for item in app.markdown if 'role="img"' in item.value)
    assert f': {remaining}' in html


def test_linked_list_controls_first_match_and_empty_traversal():
    app = open_page("Linked List")
    click(app, "Linked List", "Traverse")
    assert "Head to tail: []" in app.success[0].value
    for value in ["10", "20", "10"]:
        click(app, "Linked List", "Insert", value)
    click(app, "Linked List", "Delete", "10")
    assert app.session_state["structures"]["Linked List"].traverse() == [20, 10]
    click(app, "Linked List", "Delete", "99")
    assert "Nothing was deleted" in app.success[0].value
    click(app, "Linked List", "Search", "20")
    assert "20 was found" in app.success[0].value
    click(app, "Linked List", "Traverse")
    assert "[20, 10]" in app.success[0].value
    assert app.metric[0].value == "2"
    html = next(item.value for item in app.markdown if 'role="img"' in item.value)
    assert "HEAD" in html and "None" in html and "[20, 10]" in html


@pytest.mark.parametrize("page,add", [("Stack", "Push"), ("Queue", "Enqueue"), ("Linked List", "Insert")])
def test_invalid_input_never_mutates_structure(page, add):
    app = open_page(page)
    click(app, page, add, "-5")
    for value in ["", " ", "1.5", "hello", "<script>", "1_000"]:
        click(app, page, add, value)
        assert "whole number" in app.warning[0].value
        assert app.metric[0].value == "1"
    click(app, page, "Search", "abc")
    assert "whole number" in app.warning[0].value
    if page == "Linked List":
        click(app, page, "Delete", "abc")
        assert app.session_state["structures"][page].traverse() == [-5]


def test_navigation_reruns_resets_and_sessions_are_independent():
    app = open_page("Stack")
    click(app, "Stack", "Push", "10")
    app.radio("page").set_value("Queue").run()
    click(app, "Queue", "Enqueue", "20")
    app.radio("page").set_value("Linked List").run()
    click(app, "Linked List", "Insert", "30")
    app.radio("page").set_value("Home").run()
    app.run()
    for page in ["Stack", "Queue", "Linked List"]:
        app.radio("page").set_value(page).run()
        assert app.metric[0].value == "1"
        click(app, page, "Reset")
        assert app.metric[0].value == "0"
        assert "reset to empty" in app.success[0].value
        if page == "Stack":
            assert app.session_state["structures"]["Queue"].size() == 1
            assert app.session_state["structures"]["Linked List"].size() == 1
    click(app, "Linked List", "Insert", "40")
    fresh = open_page("Linked List")
    assert fresh.metric[0].value == "0"
    assert app.session_state["structures"]["Linked List"].traverse() == [40]
