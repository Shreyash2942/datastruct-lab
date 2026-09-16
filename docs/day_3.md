# Day 3 — Linked List and core tests

## Implementation

`src/structures/linked_list.py` defines `Node` with `data` and `next`, plus a
`LinkedList` that owns a head reference and maintains an element count.
Both are available through `from src.structures import LinkedList, Node`.

| Operation | Behavior | Time |
| --- | --- | --- |
| `insert(value)` | Add at the head; return None | O(1) |
| `delete(value)` | Remove first match from the head; return success boolean | O(n) worst case |
| `search(value)` | Return whether an equal value exists | O(n) worst case |
| `traverse()` | Return a new list of values in head-to-tail order | O(n) |
| `is_empty()` | Return whether the head is absent | O(1) |
| `size()` | Return the maintained count | O(1) |

Empty search and deletion return False. Empty traversal returns `[]`. Missing
deletion leaves the list unchanged. Duplicate values are allowed. Traversal
copies the container, while stored values are shared. Search and deletion assume
constant-cost equality comparisons. Total storage is O(n); traversal allocates
an O(n) result, while search and deletion use O(1) auxiliary space.

Methods use loops, so walking a long node chain does not depend on recursion
depth. Their docstrings explain behavior, return values, and complexity.

## Quality gate

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Verified result: **23 passed** (5 Stack, 5 Queue, 13 Node/Linked List cases).

- Stack and Queue preserve LIFO/FIFO order and handle empty operations.
- Node stores data and a next-node reference.
- Linked List handles empty and single-element states, head insertion,
  successful/missing searches, and head/middle/tail/missing deletion.
- Deleting duplicates removes only the first match from the head.
- Traversal results have independent containers; instances have independent nodes.
- Size remains correct through reuse and 300 deterministic mixed operations.
- Search, deletion, and traversal work on a 3,000-node chain.

The Stack test now uses a sequence whose reverse differs from its insertion
order, so the basic ordering test independently detects FIFO behavior.

## Git milestones

The assignment specifies these separate commits:

1. `feat: implement linked list data structure` — Node, LinkedList, and exports.
2. `test: add unit tests for core data structures` — Linked List tests,
   strengthened Stack test, and updated usage/verification documentation.

Destination: `origin/main` in `Shreyash2942/datastruct-lab`.

## Next: Day 4

Build the Streamlit interface and structure visualizations, preserve state across
reruns, and show friendly feedback and appropriate use cases.
