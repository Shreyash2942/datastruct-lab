# Performance report

## Purpose

Compare theoretical growth with measured single-operation runtimes for Stack, Queue, and Linked List. These measurements do not prove asymptotic bounds or predict exact future runtimes.

## Environment and method

- Run: `3e088bc5908f4059911949ede1f398a3`; started 2026-09-20T02:35:58.138224+00:00.
- Python: CPython 3.14.4; platform: Windows-11-10.0.26200-SP0.
- Processor: AMD64 Family 26 Model 36 Stepping 0, AuthenticAMD; source: `885444a2e283482081f79c7a71923b6cc6edc0c4`.
- Timer: `time.perf_counter_ns`; reported resolution 100 ns; monotonic: True.
- Sizes: 100, 1000, 10000, 50000; 30 measured trials and 3 untimed warmups per case.
- Statistic: median nanoseconds; garbage collection enabled: True.
- Fresh fixtures contain range(n). Search uses absent -1; insertion adds -1 once to an n-element structure. Fixtures are rebuilt before every warmup and trial.
- Only the bound method call is timed. Setup, binding, verification, teardown, serialization, and charts are excluded. Cases run in the recorded fixed order.

## Measured results

Runtime is the median in nanoseconds. Full raw samples and environment metadata accompany the summary CSV.

| Structure | Operation | n | Predicted time | Median ns | P25–P75 ns |
| --- | --- | ---: | --- | ---: | ---: |
| Stack | push | 100 | O(1) amortized | 100.0 | 100.0–100.0 |
| Stack | push | 1,000 | O(1) amortized | 100.0 | 100.0–100.0 |
| Stack | push | 10,000 | O(1) amortized | 100.0 | 100.0–100.0 |
| Stack | push | 50,000 | O(1) amortized | 100.0 | 100.0–175.0 |
| Stack | search | 100 | O(n) | 700.0 | 600.0–700.0 |
| Stack | search | 1,000 | O(n) | 5,100.0 | 5,100.0–5,200.0 |
| Stack | search | 10,000 | O(n) | 48,400.0 | 48,300.0–48,400.0 |
| Stack | search | 50,000 | O(n) | 243,600.0 | 242,200.0–248,600.0 |
| Queue | enqueue | 100 | O(1) | 100.0 | 100.0–100.0 |
| Queue | enqueue | 1,000 | O(1) | 100.0 | 100.0–100.0 |
| Queue | enqueue | 10,000 | O(1) | 100.0 | 100.0–175.0 |
| Queue | enqueue | 50,000 | O(1) | 250.0 | 125.0–725.0 |
| Queue | search | 100 | O(n) | 1,200.0 | 1,100.0–1,200.0 |
| Queue | search | 1,000 | O(n) | 5,500.0 | 5,500.0–5,600.0 |
| Queue | search | 10,000 | O(n) | 35,300.0 | 35,300.0–35,475.0 |
| Queue | search | 50,000 | O(n) | 180,400.0 | 179,700.0–183,600.0 |
| Linked List | insert | 100 | O(1) | 150.0 | 100.0–200.0 |
| Linked List | insert | 1,000 | O(1) | 150.0 | 100.0–200.0 |
| Linked List | insert | 10,000 | O(1) | 200.0 | 200.0–375.0 |
| Linked List | insert | 50,000 | O(1) | 900.0 | 600.0–1,100.0 |
| Linked List | search | 100 | O(n) | 1,500.0 | 1,400.0–1,500.0 |
| Linked List | search | 1,000 | O(n) | 13,800.0 | 13,800.0–13,800.0 |
| Linked List | search | 10,000 | O(n) | 136,600.0 | 134,500.0–137,800.0 |
| Linked List | search | 50,000 | O(n) | 777,400.0 | 708,375.0–878,925.0 |

## Charts

![Measured runtime](../images/performance_chart.png)

![Growth comparison](../images/complexity_comparison.png)

Runtime axes use microseconds (CSV remains nanoseconds). Runtime-chart shading shows the interquartile range, not a confidence interval. Growth curves divide each family's medians by its smallest-size median; theoretical curves use 1 for constant/amortized operations or n/n0 for linear operations.

## Interpretation

- **Stack push:** from n=100 to n=50,000, observed median growth was 1.00x; the illustrative theoretical growth was 1.00x.
- **Stack search:** from n=100 to n=50,000, observed median growth was 348.00x; the illustrative theoretical growth was 500.00x.
- **Queue enqueue:** from n=100 to n=50,000, observed median growth was 2.50x; the illustrative theoretical growth was 1.00x.
- **Queue search:** from n=100 to n=50,000, observed median growth was 150.33x; the illustrative theoretical growth was 500.00x.
- **Linked List insert:** from n=100 to n=50,000, observed median growth was 6.00x; the illustrative theoretical growth was 1.00x.
- **Linked List search:** from n=100 to n=50,000, observed median growth was 518.27x; the illustrative theoretical growth was 500.00x.

Search traverses every value because the target is absent. Linear traversal should become more visible as n grows; timer and call overhead can dominate small inputs. Constant/amortized insertions may fluctuate because of allocation and scheduling. Stack list capacity after fixture construction can repeatedly include or exclude a resize; these isolated pushes do not establish amortized behavior over long insertion sequences.

## Limitations

- A single machine/run, fixed case order, interpreter overhead, background tasks, CPU frequency, cache state, allocator behavior, and garbage collection affect timings. Nanosecond units do not imply nanosecond accuracy.
- Timing one very short call includes clock/call overhead; no overhead subtraction is performed. Medians reduce some outlier effects but do not eliminate systematic bias. Shading and raw samples show variability.
- Only missing-value searches and one insertion position per structure are measured. This is not a best-case or general workload comparison. Integer equality and these exact Python implementations determine constants.
- Normalizing to the smallest n amplifies noise in that baseline. Zero baselines produce unavailable observed growth instead of division by zero. Theoretical curves illustrate scaling, not fitted runtime predictions.
- No fixed timing threshold or exact ratio is used as a correctness test. Unexpected ratios should prompt investigation or independent repeat runs, not claims that Big-O is disproved.

## Reproduce

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.benchmark.performance_tester --sizes 100 1000 10000 50000 --trials 30 --warmups 3
```

This regenerates the tracked output files. UI runs instead keep artifacts in the browser session and offer downloads without overwriting these files.

Timer reference: [Python time.perf_counter_ns](https://docs.python.org/3/library/time.html#time.perf_counter_ns).
