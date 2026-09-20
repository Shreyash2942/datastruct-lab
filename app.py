"""Interactive data structure learning lab. Run with streamlit run app.py."""

import re

import streamlit as st

from src.analysis import analyze_complexity, supported_operations, supported_structures
from src.benchmark.performance_tester import DEFAULT_SIZES, run_benchmarks
from src.benchmark.reporting import build_artifacts, zip_artifacts
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


def render_complexity() -> None:
    """Explore predicted time, space, and normalized growth without mutations."""
    st.caption("04 / HOW DOES THE WORK GROW?")
    st.title("Complexity Analyzer")
    st.write("Choose an operation and explore what changes as the input grows. These predictions describe the implementations in this lab.")
    controls, result_area = st.columns([1, 2], gap="large")
    with controls, st.container(border=True):
        st.subheader("Choose a scenario")
        structure = st.selectbox("Data structure", supported_structures(), key="complexity_structure")
        operations = supported_operations(structure)
        if st.session_state.get("complexity_operation") not in operations:
            st.session_state.complexity_operation = operations[0]
        labels = {"insert": "Insert (at head)", "delete": "Delete (first match)", "to_list": "To list (snapshot)", "is_empty": "Is empty"}
        operation = st.selectbox("Operation", operations, format_func=lambda name: labels.get(name, name.capitalize()), key="complexity_operation")
        size = st.number_input("Input size (n)", min_value=1, max_value=1_000_000_000, value=10_000, step=1, key="complexity_size", help="Number of stored values. This scenario does not create or change your structures.")
        st.caption("Change a selection to update the prediction.")
    with result_area:
        try:
            prediction = analyze_complexity(structure, operation, size)
        except ValueError as error:
            st.warning(str(error))
            return
        rule = prediction.rule
        time, storage = st.columns(2)
        time.metric("Predicted time complexity", rule.time)
        storage.metric("Total structure storage", prediction.storage_space)
        st.subheader("Why this bound?")
        st.write(rule.explanation)
        st.write(f"**Best-case time:** {rule.best_time} · **Worst single-operation time:** {rule.worst_time}")
        st.write(f"**Auxiliary space (excluding result):** {rule.auxiliary_space}")
        st.write(f"**Result space:** {rule.result_space}")
        st.caption("Total storage covers the existing structure. Auxiliary space covers temporary work; result space covers the returned value or container. Bounds assume constant-cost equality and fixed-size references.")
    st.divider()
    st.subheader("What happens as n grows?")
    st.write(prediction.growth_explanation)
    st.line_chart(
        {"Input size": [point[0] for point in prediction.growth_points], "Relative work": [point[1] for point in prediction.growth_points]},
        x="Input size", y="Relative work", x_label="Input size (n)", y_label="Relative work (illustrative)", color="#087F72",
    )
    st.caption("Normalized to 1 at your selected n. This is a theoretical growth illustration, not a runtime measurement or a comparison of absolute speed between operations.")


def render_performance() -> None:
    """Run isolated benchmarks on demand and keep downloadable results in session."""
    st.caption("05 / FROM THEORY TO MEASUREMENT")
    st.title("Performance")
    st.write("Measure insertions and missing-value searches for all three structures. Compare growth across input sizes using actual runtimes.")
    sizes = st.multiselect("Input sizes", [100, 1_000, 10_000, 50_000, 100_000], default=list(DEFAULT_SIZES), key="benchmark_sizes")
    trials = st.number_input("Trials per case", min_value=20, max_value=50, value=30, step=1, key="benchmark_trials")
    st.caption("Six operations per size, three untimed warmups, fresh fixtures outside timing, and median nanoseconds. Your live structures stay unchanged.")
    if len(sizes) < 2:
        st.warning("Choose at least two sizes to compare growth.")
    if st.button("Run benchmarks", key="run_benchmarks", type="primary", disabled=len(sizes) < 2):
        progress = st.progress(0, text="Preparing measurements…")
        try:
            with st.spinner("Measuring operations and generating charts…"):
                run = run_benchmarks(sizes, trials, progress=lambda done, total: progress.progress(done / total, text=f"Measured {done} of {total} cases"))
                artifacts = build_artifacts(run)
                bundle = zip_artifacts(artifacts)
            st.session_state.performance_run = run
            st.session_state.performance_artifacts = artifacts
            st.session_state.performance_bundle = bundle
            st.success("Benchmark run complete. Results and downloads are ready.")
        except ValueError as error:
            st.warning(str(error))
        finally:
            progress.empty()
    if "performance_run" not in st.session_state:
        st.info("Click Run benchmarks to collect measurements. Nothing runs automatically when you open this page.")
        return
    run = st.session_state.performance_run
    artifacts = st.session_state.performance_artifacts
    st.subheader("Latest completed run")
    st.caption(f"{run.metadata['started_utc']} · sizes {run.metadata['input_sizes']} · {run.metadata['trials_per_case']} trials per case. Changing the controls does not change these results until you run again.")
    st.dataframe([r.summary() for r in run.results], hide_index=True)
    st.caption("Runtime = median nanoseconds. P25/P75 show the middle half of measured samples.")
    st.image(artifacts["images/performance_chart.png"], caption="Actual runtime; shading shows sample variability.")
    st.image(artifacts["images/complexity_comparison.png"], caption="Predicted versus observed growth, normalized to each operation's smallest input size.")
    st.info("Big-O predicts growth, not exact runtime. Short timings are sensitive to timer overhead, allocation, and background activity. The downloaded report explains these limitations.")
    st.download_button("Download CSV", artifacts["data/benchmark_results.csv"], "benchmark_results.csv", "text/csv", key="download_benchmark_csv")
    st.download_button("Download full report bundle", st.session_state.performance_bundle, "benchmark_report.zip", "application/zip", key="download_benchmark_bundle")
    st.caption("Downloads belong to this session. UI runs do not overwrite the saved project reports.")


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
        render_complexity()
    elif page == "Performance":
        render_performance()
    else:
        st.title("About this lab")
        st.write("DataStruct Lab is a Python learning project for CSC506 Design and Analysis of Algorithms. It connects small, documented implementations with hands-on visual demonstrations.")
        st.subheader("What you can explore today")
        st.write("Stack, Queue, and singly Linked List operations, diagrams, and real-world use cases. All three structures keep independent state while you navigate.")
        st.write("The Complexity Analyzer explains time and space bounds for every public operation, with an illustrative growth comparison.")
        st.write("The Performance page measures repeated operations and exports CSV data, charts, and an analysis report.")
        st.caption("Built with Python, Streamlit, and Matplotlib. Final submission documentation and the demo are the next milestone.")


if __name__ == "__main__":
    main()
