# Selected test cases

Three existing tests per structure are highlighted below. All nine passed in the
latest full run of **128 tests**. The full suite is retained; this is a reporting
selection, not a reduction in coverage.

| Case | Action | Expected outcome |
| --- | --- | --- |
| S1 Stack ordering | Push 10, 20, 10, 30; peek/search, then pop. | Peek = 30; reads keep size 4; pops = 30, 10, 20, 10. |
| S2 Stack empty removal | Pop an empty stack, then reuse it with 42. | IndexError; size stays 0; reuse succeeds. |
| S3 Stack independence | Put a list and None in one of two stacks. | Equality search works; the second stack stays independent. |
| Q1 Queue ordering | Enqueue 10, 20, 10, 30; peek/search, then dequeue. | Peek = 10; reads keep size 4; removals = 10, 20, 10, 30. |
| Q2 Queue empty removal | Dequeue an empty queue, then reuse it with 42. | IndexError; size stays 0; reuse succeeds. |
| Q3 Queue independence | Put a list and None in one of two queues. | Equality search works; the second queue stays independent. |
| L1 Head insertion | Insert 10, 20, 30; traverse and search. | Order = 30, 20, 10; search 99 = False; size = 3. |
| L2 Middle deletion | From 30, 20, 10, delete 20. | Returns True; order = 30, 10; size = 2. |
| L3 Duplicate deletion | Insert 7, 3, 7; delete 7. | Only the first match is removed: 3, 7; size = 2. |

## Exact pytest identifiers

Run from the repository root. Each command selects one case:

**S1**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_stack.py::test_stack_follows_lifo_and_preserves_state_during_reads"
```

**S2**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_stack.py::test_empty_operations_raise_clear_errors_and_allow_reuse[pop]"
```

**S3**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_stack.py::test_stacks_are_independent_and_accept_non_hashable_values"
```

**Q1**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_queue.py::test_queue_follows_fifo_and_preserves_state_during_reads"
```

**Q2**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_queue.py::test_empty_operations_raise_clear_errors_and_allow_reuse[dequeue]"
```

**Q3**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_queue.py::test_queues_are_independent_and_accept_non_hashable_values"
```

**L1**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_linked_list.py::test_insert_at_head_and_read_operations_preserve_order"
```

**L2**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_linked_list.py::test_delete_relinks_neighbors_and_updates_count[middle]"
```

**L3**

```powershell
.\.venv\Scripts\python.exe -m pytest "tests/test_linked_list.py::test_delete_only_first_duplicate_from_head"
```

## Additional verification

The remaining suite covers all 20 complexity-rule combinations, invalid input,
snapshots, UI state, benchmark timing boundaries, fixture isolation, and exports.
For example, Linked List Search at n = 10,000 predicts O(n), while head insertion
predicts O(1). The benchmark tests verify samples and artifacts without imposing
machine-dependent speed thresholds.
