# Data Structure Learning Tool

## Overview

`datastruct-lab` is a Python learning tool for CSC506 Design and Analysis of
Algorithms. It will demonstrate stacks, queues, and singly linked lists, explain
operation complexity, and compare expected growth with measured runtime.

**Current milestone: Day 1 — project foundation.** The requirements and package
folders are ready. Data structures, the application, and benchmarks are scheduled
for subsequent days.

## Features

Planned assignment features:

- Stack (LIFO), queue (FIFO), and singly linked list operations.
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

Day 1 provides the foundation; there is no runnable application yet. After the
Day 4 interface is implemented, the launch command will be:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Project Structure

```text
datastruct-lab/
├── README.md
├── requirements.txt
├── src/
│   ├── structures/       # Stack, queue, linked list (Days 2–3)
│   ├── analysis/         # Complexity analyzer (Day 5)
│   ├── benchmark/        # Performance testing (Day 6)
│   └── visualization/    # Visual helpers (Days 4–6)
├── tests/                # Unit tests begin on Day 3
├── docs/                 # Plan, requirements, test plan, milestone status
├── reports/              # Performance report and one-page analysis
├── data/                 # Measured benchmark CSV output
└── images/               # Generated charts and screenshots
```

`app.py` and implementation modules will be added at their scheduled milestones.

## Testing

The [test plan](docs/test_plan.md) defines the future correctness checks. Once
tests are added on Day 3, run:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

No automated tests exist at the Day 1 milestone; pytest currently reports no
tests collected (exit code 5). Day 1 verification checks dependency consistency
and imports of the installed libraries and project packages.

## Performance Analysis

Day 6 will measure stack push/search, queue enqueue/search, and linked-list
insert/search at input sizes 100, 1,000, 10,000, and 50,000 with repeated trials.
Results will go in `data/benchmark_results.csv`, charts in `images/`, and the
interpretation in `reports/performance_report.md`.

Big-O predicts growth as input size increases; it does not predict exact runtime.
No measured results or charts have been generated at the Day 1 milestone.
