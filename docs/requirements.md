# Assignment requirements and operation contracts

## Scope and source

Source: [assignment plan](assignment_plan.md), especially sections 1 and 4–10.
The existing repository name is `datastruct-lab`; it replaces the plan's example
name `dsa-learning-tool`. Version 1.0 targets the assignment. Portfolio extensions
follow submission. The original instructor rubric has not been supplied separately.

The operation details below are Day 1 design decisions that resolve unspecified
return values, insertion position, and error behavior in the plan.

## Shared conventions

- Core structures hold arbitrary Python values with equality-based search.
  The initial UI accepts integers and validates input before changing state.
- Duplicate values are allowed. Each instance owns independent state.
- `search(value)` returns a boolean; it does not change the structure.
- `is_empty()` returns a boolean. `size()` returns the stored element count.
- Mutations that add an element return `None`.
- Removing or peeking at an empty stack/queue raises `IndexError` with a clear
  message. The UI catches it and presents friendly feedback.
- Structure logic stays independent of Streamlit and timing/chart code.
- Public methods document purpose, parameters, return values, errors, and
  expected complexity. Complexity assumes constant-cost value equality.

## Stack — Day 2

Use a Python list with the top at its end to demonstrate last in, first out.

| Operation | Contract | Expected time |
| --- | --- | --- |
| `push(value)` | Add at the top | O(1) amortized |
| `pop()` | Remove and return the top; empty raises `IndexError` | O(1) amortized with dynamic-array resizing |
| `peek()` | Return the top without removing it; empty raises `IndexError` | O(1) |
| `search(value)` | Return whether a matching value exists | O(n) worst case |
| `is_empty()` | Return whether no elements remain | O(1) |
| `size()` | Return the element count | O(1) |

Acceptance example: push 10, then 20; peek returns 20, pop returns 20, size is 1.
The plan lists pop as O(1); the analyzer should explain the amortized qualification
for a list-backed implementation. A single resizing push/pop can take O(n).

## Queue — Day 2

Wrap `collections.deque`, adding at the rear and removing from the front, to
demonstrate first in, first out without shifting a Python list on each removal.

| Operation | Contract | Expected time |
| --- | --- | --- |
| `enqueue(value)` | Add at the rear | O(1) |
| `dequeue()` | Remove and return the front; empty raises `IndexError` | O(1) |
| `peek()` | Return the front without removing it; empty raises `IndexError` | O(1) |
| `search(value)` | Return whether a matching value exists | O(n) worst case |
| `is_empty()` | Return whether no elements remain | O(1) |
| `size()` | Return the element count | O(1) |

Acceptance example: enqueue 10, then 20; dequeue returns 10, peek returns 20.
Using deque is a project design choice; revisit it if the instructor requires a
queue implemented entirely with custom nodes.

## Singly linked list — Day 3

Implement a `Node` with `data` and `next`, and a `LinkedList` with a head reference
and maintained element count.

| Operation | Contract | Expected time |
| --- | --- | --- |
| `insert(value)` | Insert at the head | O(1) |
| `delete(value)` | Remove first match from the head; return `True` if removed, otherwise `False` | O(n) worst case |
| `search(value)` | Return whether a matching value exists | O(n) worst case |
| `traverse()` | Return a new Python list of values from head to tail | O(n) |
| `is_empty()` | Return whether the head is absent | O(1) |
| `size()` | Return the maintained count | O(1) |

Acceptance example: insert 10, then 20; traverse returns `[20, 10]`. Deleting 20
returns `True`; deleting a missing value returns `False`. An empty traversal is
`[]`. Deleting a duplicate removes only its first occurrence.

## UI and visual demonstrations — Day 4

- Provide Home, Stack, Queue, Linked List, Complexity Analyzer, Performance,
  and About navigation in `app.py` using Streamlit.
- Expose the plan's add/remove/peek/search/traverse controls where applicable,
  plus Reset. Preserve independent structure state across Streamlit reruns.
- Show stack TOP, queue FRONT/REAR, and linked-list HEAD/next/None labels;
  update the diagram after each successful mutation.
- Explain stack undo/call use cases, queue scheduling/request processing, and
  linked-list dynamic storage and insertion/deletion trade-offs.
- Show friendly invalid-input and empty-operation feedback without losing state.

Acceptance: a user can perform each supported operation, observe the resulting
state, switch pages without losing it, and reset a structure to empty.

Day 4 display API: `Stack.to_list()` returns top-to-bottom values;
`Queue.to_list()` returns front-to-rear values. Both return independent shallow
list snapshots in O(n) time and space, so the interface never reads private
storage or duplicates the data structure state. Linked List uses `traverse()`.
UI values are signed decimal integers of at most 64 digits. Session state is
temporary and is not persisted across a fresh browser session.

## Complexity analyzer — Day 5

- Accept structure, supported operation, and positive integer input size.
- Return predicted time complexity, a plain-language explanation, and growth
  behavior; reject unsupported combinations and invalid sizes clearly.
- Use the operation tables above, including head insertion and amortized costs.
- Distinguish total storage O(n) for each structure from auxiliary operation
  space, ordinarily O(1); `traverse()` returns an O(n) result list. Account for
  dynamic-array resizing when explaining transient allocation.
- Explain why a value near the head/top/front can be found early but worst-case
  search is linear. Big-O is not a prediction of exact milliseconds.

Acceptance: every supported combination has a tested, consistent explanation.

## Benchmarks and charts — Day 6

- Minimum operations: stack push/search, queue enqueue/search, linked-list
  insert/search, at n = 100, 1,000, 10,000, and 50,000.
- Use `time.perf_counter_ns()` and 30 trials per case (within the plan's 20–50).
  Report median elapsed nanoseconds and record trial count.
- Build/reset fixtures outside the timed region so each insertion starts with n
  elements. Use a missing search value for reproducible worst-case traversal.
  Warm up before trials; document timer noise and machine-specific effects.
- Save `data/benchmark_results.csv` with `Structure`, `Operation`, `Input_Size`,
  `Predicted_Complexity`, and `Runtime`; define Runtime as median nanoseconds.
  Additional trial-count/environment metadata may accompany those columns.
- Generate `images/performance_chart.png` (input size versus runtime) and
  `images/complexity_comparison.png` (predicted versus observed growth).
- Label axes, units, titles, legends, and the normalization/reference point for
  theoretical curves. Do not equate asymptotic complexity with exact runtime.

Acceptance: repeatable benchmark runs produce populated CSV data and both charts
from actual measurements. Reports describe noise, overhead, and limitations.

## Reporting, documentation, and submission — Days 6–7

- `reports/performance_report.md`: purpose, environment, sizes, trials, expected
  complexity, measured results, charts, interpretation, and limitations.
- `reports/data_structure_analysis.md`: one-page analysis explaining the three
  structures, operation trade-offs, application scenarios, and selection criteria.
- README: installation, running the app, feature usage, tests, performance,
  screenshots, and future development. Keep milestone status accurate.
- `docs/demo_script.md` and a 3–5 minute video demonstrating the structures,
  complexity analyzer, performance results, and conclusions.
- Pass automated and manual checks; push final work and preserve the submitted
  version with `v1.0-assignment` at Day 7.

## Day 1 acceptance

The repository has the package/directory skeleton, working virtual environment,
four installed dependencies, this requirements document, a README, and the first
foundation commit pushed to GitHub. See [Day 1 status](day_1.md) for verification.
