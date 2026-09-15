# Day 2 — Stack and Queue

## Implemented operations

| Stack | Queue | Behavior |
| --- | --- | --- |
| `push(value)` | `enqueue(value)` | Add one value; return None |
| `pop()` | `dequeue()` | Remove and return next value in LIFO/FIFO order |
| `peek()` | `peek()` | Return next value without removing it |
| `search(value)` | `search(value)` | Return whether an equal value is present |
| `is_empty()` | `is_empty()` | Return whether no values remain |
| `size()` | `size()` | Return current element count |

Stack uses the end of a Python list as its top. Queue uses `collections.deque`
to add at the rear and remove from the front without shifting remaining values.
Both follow the [Day 1 contracts](requirements.md), accept duplicates, and own
independent storage. Empty removal and peek raise descriptive `IndexError`s.

Both structures use O(n) storage. Stack push/pop take O(1) amortized time,
including resizing across a sequence of operations; a single resize can take
O(n). Queue enqueue/dequeue take O(1). Peek, size, and empty checks take O(1).
Search takes O(n) worst-case time, assuming constant-cost equality comparisons.
Stack search starts at the top; queue search starts at the front.

## Verification

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The initial tests cover both structures' ordering, reads that preserve state,
empty errors, single-element reuse, duplicates, present/missing searches, size,
independent instances, lists/None as values, and repeated interleaved operations.
Tests were brought forward from Day 3 to verify the Day 2 feature commits.

## Git milestones

The assignment specifies separate commits:

1. `feat: implement stack data structure` — Stack implementation and tests.
2. `feat: implement queue data structure` — Queue implementation and tests,
   package exports, and updated Day 2 documentation.

Destination: `origin/main` in `Shreyash2942/datastruct-lab`.

## Next: Day 3

Implement Node and LinkedList, add linked-list tests, and run the full core suite.
The Streamlit UI remains scheduled for Day 4.
