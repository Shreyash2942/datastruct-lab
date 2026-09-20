# Day 6 — Performance testing and charts

Implemented six benchmark families: Stack push/search, Queue enqueue/search,
and Linked List insert/search. The default run uses 100, 1,000, 10,000, and
50,000 elements, 30 measured trials per case, and 3 untimed warmups. Every call
gets a fresh fixture containing range(n); -1 makes search a full miss.
Only the bound method call is measured with perf_counter_ns.

## Deliverables

- Timing engine: `src/benchmark/performance_tester.py`.
- Export/chart/report generation: `src/benchmark/reporting.py`.
- Performance page: explicit execution, progress, result table, two charts,
  CSV download, and a complete six-file ZIP; live structures remain unchanged.
- [Summary CSV](../data/benchmark_results.csv), [raw trials](../data/benchmark_trials.csv),
  and [environment metadata](../data/benchmark_metadata.json).
- [Runtime chart](../images/performance_chart.png),
  [normalized comparison](../images/complexity_comparison.png), and
  [performance report](../reports/performance_report.md).

## Findings and interpretation

The recorded CLI run has 24 case summaries and 720 samples. Across a 500-fold
increase in n, missing-search median growth was 348x for Stack, 150.33x for
Queue, and 518.27x for Linked List. The 100-element baseline includes substantial
overhead; ratios from it are not exact estimates of asymptotic growth. From
10,000 to 50,000 elements, Stack and Queue searches grew about 5x, and Linked
List search about 5.69x, consistent with the expected direction of linear growth.

Insertion medians ranged from 100 to 900 ns, close enough to the reported
100 ns clock resolution that overhead and allocation matter. Queue enqueue
and linked-list insertion varied despite constant structural work. These
measurements do not establish a change in their Big-O bounds. Fresh Stack
fixtures also do not sample all list-resizing phases needed to demonstrate
amortized cost over a sequence.

## Verification

- Full pytest suite: **128 passed**.
- Default CLI run generated all six artifacts; actual charts visually inspected.
- Real Edge browser: separate default run, both charts, 24-row CSV and six-file
  ZIP download with 720 samples, preserved live Stack value, navigation
  persistence, no JavaScript errors, and no document overflow at 390 px.
- Benchmark tests verify timing boundaries and fixture isolation, not speed.

## Reproduce

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester
.\.venv\Scripts\python.exe -m pytest
```

The CLI overwrites the six output files unless a separate `--output-dir` is
specified. UI results remain in the current session until downloaded. Graphify
artifacts and caches stay in the sibling `../graphify-out/` directory.

Commit messages follow the plan: `perf: implement performance benchmarking
framework` and `docs: add performance charts and analysis`.
