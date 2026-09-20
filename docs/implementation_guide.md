# Implementation guide

DataStruct Lab has three working structures, a Streamlit interface, a rule-based
complexity predictor, and a separate timing engine. Run commands from the
repository root. Core structures use only the Python standard library.

## Stack: last in, first out

Source: [stack.py](../src/structures/stack.py). Each instance owns a Python list
named `_items`. Its last element is the top. `push` calls `append`, `pop` removes
the last element, and `peek` reads index -1. Search uses equality from top to
bottom. An empty removal or peek raises `IndexError` before changing state.

| Public method | Result and behavior | Time |
| --- | --- | --- |
| `push(value)` | Add at top; return `None` | O(1) amortized; O(n) on resize |
| `pop()` | Remove/return top; empty raises `IndexError` | O(1) amortized; O(n) on resize |
| `peek()` | Return top without removal; empty raises `IndexError` | O(1) |
| `search(value)` | Boolean, no mutation | O(n) worst case; O(1) best case |
| `is_empty()` | Boolean | O(1) |
| `size()` | Stored length | O(1) |
| `to_list()` | New shallow list, top to bottom | O(n) time and result space |

```python
from src.structures import Stack

stack = Stack[int]()
stack.push(10)
stack.push(20)
assert stack.peek() == 20
assert stack.pop() == 20
assert stack.search(10) is True
assert stack.to_list() == [10]
```

## Queue: first in, first out

Source: [queue.py](../src/structures/queue.py). Each instance owns a
`collections.deque`. Enqueue appends on the right/rear; dequeue calls `popleft`
on the left/front. This avoids the shifts that removing index zero from a Python
list would require. Peek reads index zero and search uses equality in queue order.

| Public method | Result and behavior | Time |
| --- | --- | --- |
| `enqueue(value)` | Add at rear; return `None` | O(1) |
| `dequeue()` | Remove/return front; empty raises `IndexError` | O(1) |
| `peek()` | Return front without removal; empty raises `IndexError` | O(1) |
| `search(value)` | Boolean, no mutation | O(n) worst case; O(1) best case |
| `is_empty()` | Boolean | O(1) |
| `size()` | Stored length | O(1) |
| `to_list()` | New shallow list, front to rear | O(n) time and result space |

```python
from src.structures import Queue

queue = Queue[int]()
queue.enqueue(10)
queue.enqueue(20)
assert queue.peek() == 10
assert queue.dequeue() == 10
assert queue.search(20) is True
assert queue.to_list() == [20]
```

## Singly linked list: explicit nodes

Source: [linked_list.py](../src/structures/linked_list.py). `Node` stores `data`
and `next`; `LinkedList` maintains `_head` and `_size`. Insertion creates a node
whose next reference points at the old head, then replaces the head and increments
the count. There is no tail reference or direct indexed-access method.

Deletion walks with `current` and `previous` references. For a head match, it
assigns `_head = current.next`; otherwise it assigns `previous.next = current.next`.
It decreases `_size` once and stops at the first match. Missing values leave the
chain unchanged. Search and traversal use loops, avoiding recursion-depth limits.

| Public method | Result and behavior | Time |
| --- | --- | --- |
| `insert(value)` | Add at head; return `None` | O(1) |
| `delete(value)` | Remove first match; return success boolean | O(n) worst case; O(1) head match |
| `search(value)` | Boolean, no mutation | O(n) worst case; O(1) head match |
| `traverse()` | New shallow list, head to tail; `[]` when empty | O(n) time and result space |
| `is_empty()` | Whether head is `None` | O(1) |
| `size()` | Maintained count | O(1) |

```python
from src.structures import LinkedList

linked = LinkedList[int]()
for value in [10, 20, 30]:
    linked.insert(value)
assert linked.traverse() == [30, 20, 10]
assert linked.delete(20) is True
assert linked.traverse() == [30, 10]
assert linked.delete(99) is False
assert linked.size() == 2
```

All structures allow duplicates and use equality, so values need not be hashable.
Type hints do not enforce runtime types. Bounds assume constant-cost equality
and fixed-size references. Each structure stores O(n) values/references. Search
and linked-list deletion use O(1) auxiliary space; snapshots allocate an O(n)
result container. Mutable values in a snapshot remain shared. Stack resizing
can require O(n) temporary allocation.

## Interface flow

1. [app.py](../app.py) initializes independent instances in session state.
2. `perform_operation` validates signed integer input and invokes a public method.
3. It stores success or friendly error feedback. Reset replaces only the selected instance.
4. `render_structure` obtains `to_list()` or `traverse()` and redraws the diagram
   using [visualizer.py](../src/visualization/visualizer.py).

Switching pages preserves state within the session. A new session starts fresh.
The interface uses shallow snapshots rather than reading private fields.

## Complexity prediction tool

[complexity_analyzer.py](../src/analysis/complexity_analyzer.py) contains explicit
rules for all 20 public operations. `analyze_complexity` validates the structure,
operation, and positive integer n, then returns an immutable prediction. Unknown
combinations, booleans, and invalid sizes raise `ValueError`.

```python
from src.analysis import analyze_complexity

prediction = analyze_complexity("Linked List", "search", 10_000)
assert prediction.rule.time == "O(n)"
assert prediction.rule.auxiliary_space == "O(1)"
assert prediction.storage_space == "O(n)"
assert prediction.growth_points == ((10_000, 1), (20_000, 2), (40_000, 4))
```

In the app, select **Complexity Analyzer**, a structure, an operation, and n.
Compare Linked List Search with Insert (at head), or Stack Push with Peek.
The tool distinguishes best case, worst single operation, amortized time,
existing storage, auxiliary space, and result space. Its growth illustration
does not allocate n elements, time the method, or infer bounds from arbitrary code.

## Performance measurement and reproduction

[performance_tester.py](../src/benchmark/performance_tester.py) measures six
operation families on fresh fixtures. Only the bound method call is inside
`perf_counter_ns`; preparation, verification, and rendering are excluded.
[reporting.py](../src/benchmark/reporting.py) produces summary/raw CSVs, metadata,
two PNG charts, and a Markdown report from the same run.

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester --output-dir ..\benchmark-repeat
.\.venv\Scripts\python.exe -m pytest
```

The UI runs only when **Run benchmarks** is clicked and offers downloads. It
does not replace the saved report or mutate live structures. The CLI writes to
the chosen output directory. See the [performance comparison](../reports/performance_report.md)
and [selected test cases](selected_test_cases.md).
