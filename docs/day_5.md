# Day 5 — Complexity prediction analyzer

## Delivered

`src/analysis/complexity_analyzer.py` supplies an immutable prediction model,
supported-structure/operation discovery, and `analyze_complexity()` independently
of Streamlit. The Complexity Analyzer page now accepts structure, operation, and
input size and displays predictions, rationale, and an illustrative growth chart.

All 20 public operations are covered: seven Stack, seven Queue, and six Linked
List operations, including display snapshots. Unsupported combinations and
nonpositive/noninteger input sizes raise `ValueError`; booleans are rejected.

## Interpretation and assumptions

- Bounds reflect this repository's implementations: list-backed Stack,
  deque-backed Queue, and singly Linked List with a maintained size counter.
- Stack push/pop are O(1) amortized; a single resize can take O(n) time and
  temporarily require O(n) extra allocation.
- Queue endpoint operations are O(1). Search is O(n) worst case and O(1) when
  the first inspected value matches.
- Linked-list insertion is specifically at the head, O(1). Deletion searches
  for the first equal value, O(n) worst case; relinking known neighbors is O(1).
- Total structure storage is O(n), distinct from operation auxiliary space and
  returned-result space. Traversal and snapshots return O(n) containers; value
  references are copied without deep-copying the values.
- Equality comparisons and value-reference operations are assumed O(1). Costs
  of custom equality, destructors, or variable-size payloads are outside the model.
- Predictions describe growth, not exact runtime, bytes, or instruction counts.

The chart uses three points at n, 2n, and 4n, normalized to 1 at the chosen n.
Constant/amortized models stay at 1; linear models show 1, 2, and 4. This is an
illustration of the selected bound, not experimental evidence. No n-element
structure is allocated. The UI allows 1–1,000,000,000; the Python API accepts any
positive integer. Existing live structure state is unaffected.

## Try it

Launch the lab from the repository root:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Choose **Complexity Analyzer → Linked List → Search → 10,000**. Compare with
**Insert (at head)**, then inspect **Stack → Push** for the resizing qualification.
Choose **Traverse** or **To list (snapshot)** to see O(n) result space.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: **99 passed** (23 core, 9 diagram/snapshot, 19 UI, 48 complexity cases).
The suite checks every operation, best/worst and space bounds, growth ratios,
boundary/invalid sizes, invalid names, immutable rules, changing UI selections,
and preservation of live structures. Browser verification covers selector and
size changes, explanations, and narrow layouts.

## References

The source code and [operation contracts](requirements.md) define the project
assumptions. For the underlying Python containers, see the
[Python deque documentation](https://docs.python.org/3/library/collections.html#collections.deque)
and [Python's time-complexity reference](https://wiki.python.org/moin/TimeComplexity).

## Git milestones

1. `feat: implement complexity prediction analyzer` — prediction module and UI.
2. `test: add complexity analyzer tests` — unit/UI checks and updated documentation.

Next: Day 6 will add actual benchmark measurements, CSV export, and performance
charts. The Performance page remains a labeled placeholder until then.
