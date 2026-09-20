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

`tests/test_complexity.py` contains 48 cases verifying all 20 public operations,
best/worst and amortized time, total/auxiliary/result space, head insertion,
explanations, growth ratios, immutable results, and invalid selections/sizes.
Growth checks use n = 1, 100, and one trillion without allocating structures.

Five additional Streamlit cases exercise every analyzer operation, selector
changes, input-size updates, clearing the size field (which restores its default),
and preservation of live structure state. Browser checks cover changing
selections, visible explanations, input-size updates, and narrow layouts.
The complete Day 5 suite passes **99 tests**.

## Day 6: performance checks

The Day 6 suite passes **128 tests**. Twenty-seven benchmark cases verify fresh
fixtures, missing targets, untimed setup/warmups, exactly one timed call per
sample, validation, medians/quartiles, normalized growth (including a zero
baseline), metadata, raw/summary consistency, PNGs, ZIP exports, and safe output
paths. Two new Streamlit cases verify explicit execution, disabled invalid
selections, persistence, and unchanged live structures. No test asserts fixed
runtime thresholds or exact observed growth ratios.

The full CLI run generated 24 summaries and 720 raw samples across the four
required sizes. Real-browser verification covers a separate full run, both
charts, CSV/ZIP downloads, preserved Stack state, and a 390-pixel viewport.

## Day 7: submission checks

Run the full pytest suite and real-browser UI checks. Reproduce charts from saved
raw data, inspect the one-page PDF, verify documentation links, and check video
duration, audio, captions, and assignment coverage. See [Day 7 evidence](day_7.md)
for the completed checks and remaining course-portal upload.
