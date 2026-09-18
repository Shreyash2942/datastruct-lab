# Test plan

## Day 1 environment checks

Verify the virtual environment runs, `pip check` reports no broken requirements,
and Streamlit, pytest, Matplotlib, pandas, and all `src` packages import. Confirm
`.venv` and Python caches are ignored by Git. No structure tests are expected yet.

## Days 2–3: data structures

Day 2 includes `tests/test_stack.py` and `tests/test_queue.py` so each new
implementation is verified before its feature commit. Day 3 adds
`tests/test_linked_list.py` and strengthens the Stack ordering example.
All 23 cases pass: 5 Stack, 5 Queue, and 13 Node/Linked List cases.

- Verify LIFO/FIFO order across multiple additions and removals.
- Cover empty, single-element, duplicate, and repeated-operation cases.
- Check successful/missing searches and that search/peek leave state unchanged.
- Check empty stack/queue removal and peek raise `IndexError`.
- Delete linked-list head, middle, tail, missing value, and first duplicate.
- Check traversal order, empty traversal, and returned-list independence.
- Verify size and empty status after each mutation and instance independence.
- Compare 300 deterministic mixed linked-list operations to a Python-list model.
- Exercise a 3,000-node chain to check iterative search, deletion, and traversal.
- Verify that traversal copies the container while preserving references to values.

## Day 4: interface and visualization checks

`tests/test_app.py` uses Streamlit AppTest for 14 cases: all seven pages, every
structure operation, reset, invalid input, empty feedback, navigation/reruns,
independent structure state, and separate sessions. `tests/test_visualizer.py`
adds 9 cases for labels, HTML escaping, ordering, unsupported diagram types,
and independent Stack/Queue snapshots. With the 23 core cases, 46 tests pass.

Browser checks supplement AppTest: launch the real server, perform additions
and removals on all three structure pages, inspect desktop and narrow layouts,
and verify TOP, FRONT/REAR, HEAD/None, operation feedback, and scrolling.

## Day 5: complexity checks

Add `tests/test_complexity.py`. Cover every structure/operation combination,
head-insertion assumptions, amortized list operations, storage versus auxiliary
space, explanations, and rejection of invalid operations/input sizes.

## Day 6: performance checks

Verify every requested size/operation produces nonnegative measured runtimes,
the documented trial count, readable CSV output with declared units, and both
charts. Check setup is outside timing and search fixtures really miss. Do not
assert fixed timing thresholds or exact growth ratios in correctness tests.

## Day 7: submission checks

Run the full pytest suite and manual UI checks. Reproduce charts from saved data,
review the one-page report, and verify video duration and assignment coverage.
