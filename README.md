# Data Structure Learning Tool

## Overview

`datastruct-lab` is a Python learning tool for CSC506 Design and Analysis of
Algorithms. It will demonstrate stacks, queues, and singly linked lists, explain
operation complexity, and compare expected growth with measured runtime.

**Current milestone: Day 2 — Stack and Queue.** Both structures are implemented
with documented operations and automated tests. Linked List, the application,
and benchmarks are scheduled for subsequent days.

## Features

Available now:

- Stack: `push`, `pop`, `peek`, `search`, `is_empty`, and `size`.
- Queue: `enqueue`, `dequeue`, `peek`, `search`, `is_empty`, and `size`.
- Clear empty-operation errors, type hints, complexity docstrings, and tests.

Planned assignment features:

- Singly linked list operations.
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

From the repository folder, in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

These commands use the environment directly, so activation and PowerShell
execution-policy changes are unnecessary. On macOS/Linux, use
`.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

## Usage

Use the structures from Python, starting in the repository root:

```python
from src.structures import Stack, Queue

stack = Stack[int]()
stack.push(10)
stack.push(20)
print(stack.peek())       # 20 (does not remove)
print(stack.pop())        # 20 (last in, first out)
print(stack.search(10))   # True

queue = Queue[int]()
queue.enqueue(10)
queue.enqueue(20)
print(queue.peek())       # 10 (does not remove)
print(queue.dequeue())    # 10 (first in, first out)
print(queue.size())       # 1
```

Removal and peek raise `IndexError` on an empty structure. Search returns a
boolean and does not change state. See [Day 2 notes](docs/day_2.md) for details.

There is no Streamlit application yet. After the Day 4 interface is implemented,
the launch command will be:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Project Structure

```text
datastruct-lab/
├── README.md
├── requirements.txt
├── src/
│   ├── structures/       # Stack and queue ready; linked list on Day 3
│   ├── analysis/         # Complexity analyzer (Day 5)
│   ├── benchmark/        # Performance testing (Day 6)
│   └── visualization/    # Visual helpers (Days 4–6)
├── tests/                # Stack and queue tests; more on Day 3
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

The Day 2 suite covers ordering, duplicates, empty-operation errors, successful
and missing searches, non-mutating reads, instance independence, non-hashable
values, and repeated operations. The [test plan](docs/test_plan.md) describes
additional checks for later milestones. These initial tests were brought forward
from Day 3 to verify each implementation before committing it.

## Performance Analysis

Day 6 will measure stack push/search, queue enqueue/search, and linked-list
insert/search at input sizes 100, 1,000, 10,000, and 50,000 with repeated trials.
Results will go in `data/benchmark_results.csv`, charts in `images/`, and the
interpretation in `reports/performance_report.md`.

Big-O predicts growth as input size increases; it does not predict exact runtime.
No measured results or charts have been generated at the Day 2 milestone.
