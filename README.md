# DataStruct Lab

An interactive Python lab for learning **stacks, queues, and singly linked lists**.
Add, find, and remove values, watch the diagrams change, explore Big-O estimates,
and compare predictions with measured runtimes.

Built by **Shreyashkumar Patel** for **CSC506: Design and Analysis of Algorithms**
at Colorado State University Global.

[Quick start](#quick-start) · [Using the app](#using-the-app) ·
[Python examples](#python-examples) · [Performance](#performance) ·
[Reports and demo](#reports-and-demo) · [Tests](#tests)

## What you can explore

- **Three working structures:** a Python-list-backed Stack, a deque-backed Queue,
  and a custom singly linked list with explicit nodes.
- **Interactive diagrams:** labeled values and links, operation feedback,
  independent session state, and Reset for each structure.
- **Complexity predictions:** time and space explanations for all 20 public
  operations, including best-case, worst-case, and amortized bounds.
- **Performance experiments:** repeated measurements, CSV downloads, two charts,
  and a downloadable report bundle.
- **Supporting material:** implementation documentation, selected tests, an
  APA-style report, and a narrated app walkthrough.

![Stack interface showing three values with 30 at the top](images/day4-stack.png)

## Quick start

Install Git and Python 3.14. The project was verified on **Windows 11 with
CPython 3.14.4**. Dependencies are pinned in [requirements.txt](requirements.txt).

### Windows — PowerShell

```powershell
git clone https://github.com/Shreyash2942/datastruct-lab.git
cd datastruct-lab
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS / Linux

With Python 3.14 available as `python3`:

```bash
git clone https://github.com/Shreyash2942/datastruct-lab.git
cd datastruct-lab
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

The macOS/Linux commands have not been tested on those platforms. These commands
use the virtual environment directly; activation is optional.

Open the local URL printed in the terminal, usually `http://localhost:8501`.
Press `Ctrl+C` to stop the server. **No email or Streamlit account is required.**
Launch from the repository root so the project settings disable the email
prompt and usage statistics.

## Using the app

### Try the structures

1. Select **Stack**, **Queue**, or **Linked List** in the sidebar.
2. Enter an integer, such as `10` or `-5`, and click **Push**, **Enqueue**, or **Insert**.
3. Add more values, then try removal, search, peek, or traversal.
4. Watch the diagram and element count update. **Values as text** shows the same contents.
5. Switch pages to compare structures, or **Reset** the selected one.

The Stack labels its **TOP**; the Queue labels **FRONT** and **REAR**; the Linked
List shows **HEAD**, next links, and the final **None** reference. Linked-list
insertion adds at the head; deletion removes the first matching value from the
head. Duplicates are allowed. Invalid input and empty operations show friendly
feedback without changing the contents.

Each structure keeps independent state while you navigate. A new or reloaded
browser session starts fresh. Benchmarks use separate fixtures and preserve
your live values.

### Explore Big-O

Open **Complexity Analyzer** and choose a structure, operation, and positive
input size. Try **Linked List → Search → 10,000**: the tool shows O(n)
worst-case time, O(n) structure storage, and O(1) auxiliary space. Compare this
with **Insert (at head)**, which takes O(1) time.

The predictor uses documented rules for the implemented methods. It separates
existing storage, auxiliary work, and returned-result space. Its growth chart
compares n, 2n, and 4n, normalized to 1 at n. These are illustrative growth
ratios, not measured runtimes. Changing n does not allocate a structure or
change the operation's asymptotic class.

## Python examples

The core structures use only Python's standard library and can be imported
independently of Streamlit. Save an example as `example.py` in the repository
root and run `.\.venv\Scripts\python.exe example.py` on Windows, or
`.venv/bin/python example.py` on macOS/Linux.

```python
from src.structures import LinkedList, Queue, Stack

# Stack: last in, first out — useful for undo history.
stack = Stack[int]()
stack.push(10)
stack.push(20)
print(stack.peek())       # 20, without removal
print(stack.pop())        # 20
print(stack.to_list())    # [10], top to bottom

# Queue: first in, first out — useful for jobs in arrival order.
queue = Queue[int]()
queue.enqueue(10)
queue.enqueue(20)
print(queue.dequeue())    # 10
print(queue.to_list())    # [20], front to rear

# Linked list: nodes connected from head to tail.
linked = LinkedList[int]()
for value in [10, 20, 10]:
    linked.insert(value)
print(linked.traverse())  # [10, 20, 10]
print(linked.delete(10))  # True: remove only the first match
print(linked.traverse())  # [20, 10]
print(linked.search(99))  # False
```

All three support `search(value)`, `size()`, and `is_empty()`. Core values need
not be integers or hashable; the app restricts input to integers. Snapshots are
shallow copies: editing the returned container leaves the structure unchanged,
while mutable values remain shared.

Stack/Queue removal and peek raise `IndexError` when empty. Check `is_empty()`
first or catch the exception. Empty linked-list traversal returns `[]`;
missing searches and linked-list deletions return `False`.

### Operation reference

Here, n is the number of stored values. Search and deletion bounds are worst-case
and assume constant-cost equality comparisons.

| Action | Stack | Queue | Linked List | Time |
| --- | --- | --- | --- | --- |
| Add | `push(value)` | `enqueue(value)` | `insert(value)` at head | O(1) amortized for Stack; O(1) for others |
| Remove | `pop()` | `dequeue()` | `delete(value)` | O(1) amortized for Stack; O(1) for Queue; O(n) for Linked List |
| Peek | `peek()` | `peek()` | — | O(1) |
| Search | `search(value)` | `search(value)` | `search(value)` | O(n) |
| Count | `size()` | `size()` | `size()` | O(1) |
| Check empty | `is_empty()` | `is_empty()` | `is_empty()` | O(1) |
| Snapshot | `to_list()` | `to_list()` | `traverse()` | O(n) time and result space |

Each structure uses O(n) storage. A single Stack push/pop can take O(n) when
the underlying list resizes; its cost over a sequence is O(1) amortized.
The [implementation guide](docs/implementation_guide.md) explains algorithms,
return values, errors, and space bounds for every public method.

The predictor is also available through Python:

```python
from src.analysis import analyze_complexity

prediction = analyze_complexity("Linked List", "search", 10_000)
print(prediction.rule.time)             # O(n)
print(prediction.storage_space)         # O(n)
print(prediction.rule.auxiliary_space)  # O(1)
print(prediction.growth_points)        # ((10000, 1), (20000, 2), (40000, 4))
```

`supported_structures()` and `supported_operations(structure)` in `src.analysis`
list valid choices. Invalid combinations and nonpositive or noninteger sizes
raise `ValueError`; booleans are rejected too.

## Performance

In **Performance**, choose at least two sizes and 20–50 trials per case, then
click **Run benchmarks**. Results include median runtimes, variability, and
measured-versus-predicted growth. **Download CSV** saves the summary;
**Download full report bundle** includes raw and summary CSVs, environment
metadata, both charts, and a Markdown report.

To run a new experiment and save its output outside the repository:

```powershell
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester --output-dir ..\benchmark-repeat
```

On macOS/Linux, use `.venv/bin/python` and `--output-dir ../benchmark-repeat`.
Optional `--sizes`, `--trials`, and `--warmups` flags control the experiment.
Omitting `--output-dir` writes to the current directory and replaces the saved
benchmark artifacts.

The saved experiment used:

| Setting | Value |
| --- | --- |
| Operations | Stack push/search, Queue enqueue/search, Linked List insert/search |
| Input sizes | 100; 1,000; 10,000; 50,000 |
| Repetitions | 30 timed trials and 3 untimed warmups per case |
| Timer | `time.perf_counter_ns()` |
| Outputs | 24 summaries and 720 raw samples |
| Runtime units | Nanoseconds in CSV; microseconds in the runtime chart |

Every timed call starts with a fresh n-element fixture. Searches use a missing
value. Setup, verification, and chart rendering are outside the timed region.
Big-O describes growth, not exact speed: clock overhead and allocation matter
for these short measurements. Isolated Stack pushes do not establish amortized
behavior. See the [performance report](reports/performance_report.md) for
results and limitations.

![Median runtime by input size, with interquartile ranges](images/performance_chart.png)

[Growth comparison chart](images/complexity_comparison.png) ·
[Summary CSV](data/benchmark_results.csv) · [Raw trials](data/benchmark_trials.csv) ·
[Run metadata](data/benchmark_metadata.json)

## Reports and demo

| Material | What it contains |
| --- | --- |
| [Refined final Word report](reports/DataStruct_Lab_Refined_Final_Report.docx) | Updated analysis, implementation explanations, selected tests, performance tables, charts, and references |
| [Earlier analysis PDF](reports/data_structure_analysis.pdf) | Three analysis pages plus references; this is an earlier analysis version, not an export of the refined Word report |
| [Markdown analysis](reports/data_structure_analysis.md) | Earlier analysis of structure importance, implementation, and selection criteria |
| [Implementation guide](docs/implementation_guide.md) | All 20 methods, runnable examples, and how the app and analysis tools work |
| [Selected test cases](docs/selected_test_cases.md) | Three existing cases per structure, with inputs, expected outcomes, and commands |
| [Performance report](reports/performance_report.md) | Measured comparisons, methodology, charts, and limitations |
| [App walkthrough — 12:08 MP4](demo/datastruct-lab-demo.mp4) | Updated screen recording supplied by the author, compressed for repository download |

Download the MP4 if GitHub does not preview it. The earlier generated-voice
transcript and captions remain as historical material; they do not describe or
synchronize with the new recording. See [recording notes](demo/README.md).
Any benchmark run in the video is separate from the saved CLI results in data/.

**Submission status:** the author has supplied an updated recording and refined
Word report, with September 20, 2026 on the title page. The planned
`v1.0-assignment` release tag has not been created. See the
[submission checklist](docs/day_7.md) before uploading to the course portal.

## Tests

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m pip check
```

On macOS/Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.
To run one area, append a file such as `tests/test_linked_list.py` or
`tests/test_complexity.py` to the pytest command.

The latest full run passed **128 tests**: 23 core structure cases, 9 diagram
and snapshot cases, 21 Streamlit interaction cases, 48 complexity cases, and
27 benchmark cases. They cover ordering, empty operations, duplicates, node
relinking, independent state, predictions, timing boundaries, and exports.

The report highlights only [nine selected tests](docs/selected_test_cases.md);
the full suite remains in the project. See the [test plan](docs/test_plan.md)
and [verification notes](docs/day_7.md) for coverage and browser checks.

## Project layout

```text
datastruct-lab/
├── app.py                 # Streamlit entry point
├── .streamlit/config.toml # Theme, email prompt, and usage-statistics settings
├── requirements.txt       # Pinned dependencies
├── src/
│   ├── structures/        # Stack, Queue, Node, and LinkedList
│   ├── analysis/          # Complexity rules and prediction API
│   ├── benchmark/         # Timing, CSVs, charts, and report generation
│   └── visualization/     # Structure diagrams
├── tests/                 # Automated tests
├── docs/                  # Implementation guide, requirements, and test notes
├── reports/               # APA report, analysis, and performance report
├── data/                  # Saved benchmark summaries, raw trials, and metadata
├── images/                # App screenshot and performance charts
└── demo/                  # Walkthrough, transcript, captions, and demo results
```

The interface uses Streamlit; charts use Matplotlib; result tables use pandas;
tests use pytest. Core structure logic is independent of the interface and
benchmark packages.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `No module named 'src'` | Run from the repository root, alongside `app.py` and `src/`. |
| A dependency cannot be imported | Install `requirements.txt` and use the virtual-environment Python shown above. |
| Port 8501 is already in use | Add `--server.port 8502` to the Streamlit command and open the printed URL. |
| Empty Stack/Queue removal or peek | Add a value first, check `is_empty()`, or catch `IndexError` in Python. |
| Values disappear after reloading | Structure state is temporary and belongs to the browser session. |

## Further development

- Add trees and hash tables for more lookup and ordering comparisons.
- Animate individual comparisons and node-link changes.
- Benchmark deletion, successful searches, and mixed workloads.
- Measure long insertion sequences, randomized case order, and memory use.
- Verify additional operating systems and Python versions.

For the original scope and history, see the [requirements](docs/requirements.md),
[seven-day plan](docs/assignment_plan.md), and milestone notes:
[Day 1](docs/day_1.md) · [Day 2](docs/day_2.md) · [Day 3](docs/day_3.md) ·
[Day 4](docs/day_4.md) · [Day 5](docs/day_5.md) · [Day 6](docs/day_6.md) ·
[Day 7](docs/day_7.md).
