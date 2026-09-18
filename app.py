"""Interactive data structure learning lab. Run with streamlit run app.py."""

import re

import streamlit as st

from src.structures import LinkedList, Queue, Stack
from src.visualization.visualizer import DIAGRAM_CSS, structure_diagram


PAGES = ["Home", "Stack", "Queue", "Linked List", "Complexity Analyzer", "Performance", "About"]
FACTORIES = {"Stack": Stack, "Queue": Queue, "Linked List": LinkedList}
DETAILS = {
    "Stack": {
        "tag": "01 / LAST IN, FIRST OUT",
        "intro": "The newest value leaves first. Push onto the top, then pop to see the order unfold.",
        "add": "Push", "remove": "Pop", "read": "Peek",
        "rule": "Push and pop work at the top. Search looks from top to bottom.",
        "uses": ["Undo history: reverse the latest action first.", "Browser navigation: return through previously visited pages.", "Function calls: finish the most recent call before returning.", "Expression evaluation: track pending operators and operands."],
        "try": "Push 10, 20, and 30. Pop once: 30 leaves first.",
    },
    "Queue": {
        "tag": "02 / FIRST IN, FIRST OUT",
        "intro": "First to arrive, first to leave. Add at the rear and serve values from the front.",
        "add": "Enqueue", "remove": "Dequeue", "read": "Peek",
        "rule": "Enqueue adds at the rear. Dequeue removes from the front.",
        "uses": ["Job scheduling: serve tasks in arrival order.", "Print queues: print the earliest waiting job next.", "Customer requests: handle the longest-waiting request first.", "Message processing: consume messages in arrival order."],
        "try": "Enqueue 10, 20, and 30. Dequeue once: 10 leaves first.",
    },
    "Linked List": {
        "tag": "03 / CONNECTED NODES",
        "intro": "Follow the links. Insert at the head and watch the chain change when a value is deleted.",
        "add": "Insert", "remove": "Delete", "read": "Traverse",
        "rule": "Insert adds at the head. Delete removes the first matching value from the head.",
        "uses": ["Dynamic collections: grow by linking new nodes.", "Frequent updates: insertion or unlinking is efficient when the needed node references are known; locating a value still takes O(n).", "Building other structures: nodes can form stacks and queues.", "Flexible storage: nodes do not need contiguous memory."],
        "try": "Insert 10, 20, and 10. Delete 10: only the first matching node disappears.",
    },
}


def initialize_state() -> None:
    """Create independent structures and feedback once per browser session."""
    if "structures" not in st.session_state:
        st.session_state.structures = {name: factory() for name, factory in FACTORIES.items()}
    if "feedback" not in st.session_state:
        st.session_state.feedback = {}


def perform_operation(kind: str, operation: str, raw_value: str) -> None:
    """Apply one UI action; retain state and show friendly input/empty errors."""
    structure = st.session_state.structures[kind]
    value = None
    if operation in {"Push", "Enqueue", "Insert", "Delete", "Search"}:
        cleaned = raw_value.strip()
        if not re.fullmatch(r"[+-]?[0-9]{1,64}", cleaned):
            st.session_state.feedback[kind] = ("warning", "Enter a whole number, such as 10 or -5. Your structure has not changed.")
            return
        value = int(cleaned)
    try:
        if operation in {"Push", "Enqueue", "Insert"}:
            method = {"Push": "push", "Enqueue": "enqueue", "Insert": "insert"}[operation]
            getattr(structure, method)(value)
            message = f"Added {value}."
        elif operation in {"Pop", "Dequeue"}:
            removed = getattr(structure, operation.lower())()
            message = f"Removed {removed}."
        elif operation == "Delete":
            removed = structure.delete(value)
            message = f"Deleted the first {value}." if removed else f"{value} was not found. Nothing was deleted."
        elif operation == "Peek":
            message = f"Next value: {structure.peek()}. Nothing was removed."
        elif operation == "Search":
            message = f"{value} was found." if structure.search(value) else f"{value} was not found."
        elif operation == "Traverse":
            message = f"Head to tail: {structure.traverse()}"
        elif operation == "Reset":
            st.session_state.structures[kind] = FACTORIES[kind]()
            message = f"{kind} reset to empty."
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        st.session_state.feedback[kind] = ("success", message)
    except IndexError:
        st.session_state.feedback[kind] = ("warning", f"The {kind.lower()} is empty. Add a value before using {operation.lower()}.")


def render_home() -> None:
    """Introduce the lab and explain how to start exploring."""
    st.caption("DATASTRUCT LAB / LEARN BY DOING")
    st.title("Small operations.\nBig ideas.")
    st.write("Build a structure, change one value, and see what happens. Explore three ways to organize data through live, interactive diagrams.")
    for column, (kind, details) in zip(st.columns(3), DETAILS.items()):
        with column, st.container(border=True):
            st.caption(details["tag"])
            st.subheader(kind)
            st.write(details["intro"])
            st.caption(details["try"])
    st.subheader("Your first experiment")
    st.write("Choose **Stack** in the sidebar. Enter **10** and click **Push**. Repeat with **20**, then click **Pop**. Compare the result with the same experiment in **Queue**.")
    st.info("Your structures stay in this browser session when you switch pages. Reset clears only the selected structure. A new or reloaded session starts fresh.")


def render_structure(kind: str) -> None:
    """Render controls, operation feedback, a snapshot, and educational use cases."""
    details = DETAILS[kind]
    st.caption(details["tag"])
    st.title(kind)
    st.write(details["intro"])
    controls, canvas = st.columns([1, 2], gap="large")
    with controls, st.container(border=True):
        st.subheader("Try an operation")
        raw_value = st.text_input("Enter value", placeholder="e.g. 10 or -5", max_chars=65, key=f"value_{kind}", help="Whole numbers only. Add, search, and linked-list delete use this value.")
        st.caption("Negative numbers and duplicate values are welcome.")
        actions = [details["add"], details["remove"], details["read"], "Search", "Reset"]
        for action in actions:
            if st.button(action, key=f"{kind}_{action}", type="primary" if action == details["add"] else "secondary", width="stretch"):
                perform_operation(kind, action, raw_value)
    structure = st.session_state.structures[kind]
    with canvas:
        st.subheader("Live structure")
        st.caption(details["rule"])
        count, state = st.columns(2)
        count.metric("Elements", structure.size())
        state.metric("State", "Empty" if structure.is_empty() else "Ready")
        values = structure.traverse() if kind == "Linked List" else structure.to_list()
        st.markdown(structure_diagram(kind, values), unsafe_allow_html=True)
        order = {"Stack": "Top to bottom", "Queue": "Front to rear", "Linked List": "Head to tail"}[kind]
        with st.expander("Values as text"):
            st.write(f"{order}: {values}")
        if kind in st.session_state.feedback:
            level, message = st.session_state.feedback[kind]
            getattr(st, level)(message)
        else:
            st.info(details["try"])
    st.divider()
    st.subheader("When to use it")
    for use in details["uses"]:
        st.markdown(f"- {use}")


def main() -> None:
    """Launch the seven-page learning interface."""
    st.set_page_config(page_title="DataStruct Lab", page_icon="🧩", layout="wide")
    st.markdown(DIAGRAM_CSS, unsafe_allow_html=True)
    initialize_state()
    with st.sidebar:
        st.title("DataStruct Lab")
        st.caption("A playground for the fundamentals")
        page = st.radio("Explore", PAGES, key="page")
        st.divider()
        st.caption("Stack · Queue · Linked List")
        st.caption("Values are kept in this session only.")
    if page == "Home":
        render_home()
    elif page in FACTORIES:
        render_structure(page)
    elif page == "Complexity Analyzer":
        st.title("Complexity Analyzer")
        st.info("Coming on Day 5: choose a structure, operation, and input size to explore time and space complexity.")
        st.write("For now, explore the structure pages to see how operation order affects their contents.")
    elif page == "Performance":
        st.title("Performance")
        st.info("Coming on Day 6: repeated benchmarks, measured runtimes, CSV results, and growth comparison charts.")
        st.write("Big-O describes how work grows with input size; it does not predict exact runtime. No benchmark measurements have been generated yet.")
    else:
        st.title("About this lab")
        st.write("DataStruct Lab is a Python learning project for CSC506 Design and Analysis of Algorithms. It connects small, documented implementations with hands-on visual demonstrations.")
        st.subheader("What you can explore today")
        st.write("Stack, Queue, and singly Linked List operations, diagrams, and real-world use cases. All three structures keep independent state while you navigate.")
        st.caption("Built with Python and Streamlit. Complexity analysis and measured performance are the next milestones.")


if __name__ == "__main__":
    main()
