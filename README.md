# datastruct-lab — Data Structure Learning Tool

## Overview

Learn how data structures store, find, and remove values through small Python
examples. `datastruct-lab` is for students and anyone practicing data structure
fundamentals. It began as a project for CSC506 Design and Analysis of Algorithms.

Start with a **Stack** to understand last in, first out (LIFO), or a **Queue** to
understand first in, first out (FIFO). Explore a **Linked List** to see how nodes
connect values without contiguous storage. Import any of the three classes,
experiment with their operations, and read the tests as examples of behavior.

**Current milestone: Day 3 — all three core structures.** Stack, Queue, and
Linked List are implemented with documented operations and 23 passing tests.
The interface and benchmarks are scheduled for subsequent days.

## Features

Available now:

- Stack: `push`, `pop`, `peek`, `search`, `is_empty`, and `size`.
- Queue: `enqueue`, `dequeue`, `peek`, `search`, `is_empty`, and `size`.
- Linked List: `insert`, `delete`, `search`, `traverse`, `is_empty`, and `size`.
- Clear empty-operation errors, type hints, complexity docstrings, and tests.

Planned assignment features:

- Interactive diagrams, use cases, and friendly operation feedback.
- Big-O explanations for time and space usage.
- Repeated benchmarks, CSV results, and performance charts.
- A one-page analysis and a 3–5 minute demonstration video.

See [requirements](docs/requirements.md) for operation contracts and acceptance
criteria and [the assignment plan](docs/assignment_plan.md) for the schedule.

## Technology

- Python; the Day 1 environment uses Python 3.14.
- Streamlit for the interface.
- pytest for automated tests.
- Matplotlib for charts and pandas for result tables.
- `time.perf_counter_ns()` for runtime measurements.
- Git and GitHub for version control.

## Installation

### Prerequisites

- Git to clone the repository.
- Python 3.14, the version used to verify this project. Other Python versions
  have not been verified with the pinned dependencies.

### Windows (PowerShell)

```powershell
git clone https://github.com/Shreyash2942/datastruct-lab.git
cd datastruct-lab
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

### macOS / Linux

With Python 3.14 available as `python3`:

```bash
git clone https://github.com/Shreyash2942/datastruct-lab.git
cd datastruct-lab
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

These commands use the virtual environment directly; activation is optional.
The project has been tested on Windows with Python 3.14.4. The macOS/Linux
commands are provided for those platforms but have not been tested there.

The full dependency file includes libraries for the planned interface and
charts. The three core data structure modules themselves use only Python's
standard library.

## Usage

### Start a Python session

Keep your terminal in the cloned `datastruct-lab` folder and start Python:

```powershell
# Windows
.\.venv\Scripts\python.exe
```

```bash
# macOS / Linux
.venv/bin/python
```

At the Python prompt, paste any example below. Type `exit()` to return to
your terminal. You can also save an example as a `.py` file in the repository
root and run it with the same virtual-environment Python command.

### Stack: last in, first out

A stack removes the most recently added value first. Think of an undo history:
the latest action is the first one you undo.

```python
from src.structures import Stack

stack = Stack[int]()
stack.push(10)
stack.push(20)
print(stack.peek())       # 20: look at the top without removing it
print(stack.pop())        # 20: remove the most recent value
print(stack.search(10))   # True: 10 is still present
print(stack.size())       # 1
print(stack.is_empty())   # False
```

### Queue: first in, first out

A queue removes the oldest value first. Think of a printer processing jobs in
the order they arrive.

```python
from src.structures import Queue

queue = Queue[int]()
queue.enqueue(10)
queue.enqueue(20)
print(queue.peek())        # 10: look at the front without removing it
print(queue.dequeue())     # 10: remove the oldest value
print(queue.search(20))    # True: 20 is still waiting
print(queue.size())        # 1
print(queue.is_empty())    # False
```

### Linked List: nodes connected from head to tail

Each node holds a value and a reference to the next node. Insertion at the head
does not require shifting existing values. Finding or deleting a value may
require walking through the list.

```python
from src.structures import LinkedList

linked = LinkedList[int]()
linked.insert(10)
linked.insert(20)
linked.insert(10)
print(linked.traverse())   # [10, 20, 10]: newest value is at the head
print(linked.search(20))   # True
print(linked.delete(10))   # True: remove only the first match from the head
print(linked.traverse())   # [20, 10]: the other 10 remains
print(linked.delete(99))   # False: missing values leave the list unchanged
print(linked.size())       # 2
print(linked.is_empty())   # False
```

`traverse()` returns a new Python list. Changing its entries does not change
the node chain. It is a shallow copy, so mutable values themselves are shared.

### Handle an empty structure

Stack and Queue removal and peek raise `IndexError` when there are no values.
Catch the exception if your program needs to display a message and continue:

```python
from src.structures import Stack

empty_stack = Stack[int]()
try:
    empty_stack.pop()
except IndexError as error:
    print(error)  # Cannot pop from an empty stack.
```

For an empty Linked List, `traverse()` returns `[]`, and `search()` and `delete()`
return `False`.

All three structures allow duplicate values. Search compares values for equality,
returns a boolean, and preserves the contents. Type hints such as `Stack[int]`
help editors and type checkers; they do not enforce value types at runtime.

### Operation reference

| Action | Stack | Queue | Return value | Time |
| --- | --- | --- | --- | --- |
| Add a value | `push(value)` | `enqueue(value)` | `None` | O(1) amortized for Stack; O(1) for Queue |
| Remove next value | `pop()` | `dequeue()` | Removed value | O(1) amortized for Stack; O(1) for Queue |
| View next value | `peek()` | `peek()` | Next value | O(1) |
| Find a value | `search(value)` | `search(value)` | `True` or `False` | O(n) worst case |
| Check emptiness | `is_empty()` | `is_empty()` | `True` or `False` | O(1) |
| Count values | `size()` | `size()` | Integer count | O(1) |

Here, n is the number of stored values. Stack uses a Python list; occasional
resizing can make a single push/pop O(n), while the average cost over a sequence
is O(1). Queue uses `collections.deque`. Both structures use O(n) storage.
Search costs assume constant-time equality comparisons.

| Linked List operation | Return value | Time |
| --- | --- | --- |
| `insert(value)` | `None`; adds at the head | O(1) |
| `delete(value)` | `True` if the first match was removed; otherwise `False` | O(n) worst case |
| `search(value)` | `True` or `False` | O(n) worst case |
| `traverse()` | New list of values from head to tail | O(n) |
| `is_empty()` | `True` or `False` | O(1) |
| `size()` | Maintained integer count | O(1) |

Linked List uses O(n) storage; traversal also allocates O(n) space for its result.
Deletion and search use O(1) auxiliary space and assume constant-time equality.
`Node` is exported for studying its `data` and `next` attributes; normal usage
goes through `LinkedList` methods.

## Interface and Roadmap

The current release is used through Python. `app.py` and the Streamlit interface
are not implemented yet.

| Milestone | Work | Status |
| --- | --- | --- |
| Day 1 | Project setup and requirements | Complete |
| Day 2 | Stack, Queue, initial tests | Complete |
| Day 3 | Linked List and expanded tests | Complete |
| Day 4 | Interactive Streamlit interface and diagrams | Planned |
| Day 5 | Complexity analyzer | Planned |
| Day 6 | Benchmarks, CSV results, and charts | Planned |
| Day 7 | Final analysis, demo video, and submission | Planned |

## Project Structure

```text
datastruct-lab/
├── README.md
├── requirements.txt
├── src/
│   ├── structures/
│   │   ├── stack.py      # LIFO implementation
│   │   ├── queue.py      # FIFO implementation
│   │   └── linked_list.py # Node and singly linked list
│   ├── analysis/         # Complexity analyzer (Day 5)
│   ├── benchmark/        # Performance testing (Day 6)
│   └── visualization/    # Visual helpers (Days 4–6)
├── tests/                # Stack, queue, and linked-list tests
├── docs/                 # Plan, requirements, test plan, milestone status
├── reports/              # Performance report and one-page analysis
├── data/                 # Measured benchmark CSV output
└── images/               # Generated charts and screenshots
```

`app.py` and the remaining modules will be added at their scheduled milestones.

## Testing

Run the current suite from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

On macOS/Linux:

```bash
.venv/bin/python -m pytest
```

The current suite contains 23 passing tests: 5 Stack, 5 Queue, and 13 Node/Linked
List cases. To run one structure's tests, append `tests/test_stack.py`,
`tests/test_queue.py`, or `tests/test_linked_list.py` to the command.

The suite covers ordering, duplicates, empty-operation errors, successful
and missing searches, non-mutating reads, instance independence, non-hashable
values, and repeated operations. Linked-list tests also cover deletion at each
position, first-match deletion, independent traversal results, a deterministic
mixed-operation sequence, and a 3,000-node chain. The [test plan](docs/test_plan.md)
describes the checks and later milestones.

## Performance Analysis

Day 6 will measure stack push/search, queue enqueue/search, and linked-list
insert/search at input sizes 100, 1,000, 10,000, and 50,000 with repeated trials.
Results will go in `data/benchmark_results.csv`, charts in `images/`, and the
interpretation in `reports/performance_report.md`.

Big-O predicts growth as input size increases; it does not predict exact runtime.
No measured results or charts have been generated at the Day 3 milestone.

## Troubleshooting

- **`No module named 'src'`:** run Python from the repository root, the folder
  containing `README.md` and `src/`.
- **`No module named 'pytest'`:** install `requirements.txt` and run tests using
  the virtual-environment Python commands above.
- **Empty Stack or Queue error:** add a value first, check `is_empty()`, or catch
  `IndexError` as shown in the example.

## Further Reading

- [Operation contracts and assignment requirements](docs/requirements.md)
- [Seven-day assignment plan](docs/assignment_plan.md)
- [Test plan](docs/test_plan.md)
- [Day 1 setup notes](docs/day_1.md)
- [Day 2 implementation notes](docs/day_2.md)
- [Day 3 implementation and verification](docs/day_3.md)
