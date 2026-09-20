"""CSV, metadata, PNG charts, and a report generated from one measured run."""

import csv
from io import BytesIO, StringIO
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from matplotlib.figure import Figure

from src.benchmark.performance_tester import BenchmarkRun, CASES


def _csv_bytes(rows: list[dict]) -> bytes:
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def growth_rows(run: BenchmarkRun) -> list[dict]:
    """Normalize each case family to its smallest n; zero-time baselines yield None."""
    rows = []
    for structure, operation in CASES:
        family = sorted((r.summary() for r in run.results if r.structure == structure and r.operation == operation), key=lambda r: r["Input_Size"])
        if not family:
            continue
        base = family[0]
        for row in family:
            rows.append({"Structure": structure, "Operation": operation, "Input_Size": row["Input_Size"],
                         "Predicted_Growth": row["Input_Size"] / base["Input_Size"] if row["Predicted_Complexity"] == "O(n)" else 1.0,
                         "Observed_Growth": row["Runtime"] / base["Runtime"] if base["Runtime"] > 0 else None})
    return rows


def _png(figure: Figure) -> bytes:
    output = BytesIO()
    figure.savefig(output, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    return output.getvalue()


def _charts(run: BenchmarkRun) -> tuple[bytes, bytes]:
    colors = {"Stack": "#087f72", "Queue": "#3266ad", "Linked List": "#b05c22"}
    runtime = Figure(figsize=(12, 5.5), layout="constrained")
    axes = runtime.subplots(1, 2)
    for axis, search in zip(axes, (False, True)):
        for structure, operation in CASES:
            if (operation == "search") != search:
                continue
            rows = sorted((r.summary() for r in run.results if r.structure == structure and r.operation == operation), key=lambda r: r["Input_Size"])
            x = [r["Input_Size"] for r in rows]
            y = [r["Runtime"] / 1000 for r in rows]
            axis.plot(x, y, "o-", color=colors[structure], label=f"{structure} {operation}")
            axis.fill_between(x, [r["P25_ns"] / 1000 for r in rows], [r["P75_ns"] / 1000 for r in rows], color=colors[structure], alpha=0.12)
        axis.set(title="Missing-value search" if search else "Single insertion", xlabel="Input size n (log scale)", ylabel="Median runtime (microseconds)", xscale="log", ylim=(0, None))
        axis.grid(alpha=0.2)
        axis.legend(fontsize=8)
    runtime.suptitle(f"Input size vs measured runtime | {run.metadata['trials_per_case']} trials per case\nShading: 25th–75th percentile of measured samples", fontsize=12)

    comparison = Figure(figsize=(12, 8), layout="constrained")
    growth = growth_rows(run)
    for axis, (structure, operation) in zip(comparison.subplots(3, 2).flat, CASES):
        rows = [r for r in growth if r["Structure"] == structure and r["Operation"] == operation]
        x = [r["Input_Size"] for r in rows]
        axis.plot(x, [r["Predicted_Growth"] for r in rows], "--", color="#7b8289", label="Theoretical model")
        axis.plot(x, [float("nan") if r["Observed_Growth"] is None else r["Observed_Growth"] for r in rows], "o-", color=colors[structure], label="Observed median")
        axis.set(title=f"{structure} · {operation}", xlabel="Input size n (log scale)", ylabel="Growth relative to smallest n", xscale="log", ylim=(0, None))
        axis.grid(alpha=0.2)
        axis.legend(fontsize=8)
    comparison.suptitle("Predicted vs observed growth\nEach series normalized to 1 at its smallest n; models do not predict exact runtime", fontsize=12)
    return _png(runtime), _png(comparison)


def _report(run: BenchmarkRun) -> str:
    meta = run.metadata
    lines = ["# Performance report", "", "## Purpose", "",
             "Compare theoretical growth with measured single-operation runtimes for Stack, Queue, and Linked List. These measurements do not prove asymptotic bounds or predict exact future runtimes.", "",
             "## Environment and method", "",
             f"- Run: `{meta['run_id']}`; started {meta['started_utc']}.",
             f"- Python: {meta['implementation']} {meta['python']}; platform: {meta['platform']}.",
             f"- Processor: {meta['processor']}; source: `{meta['source_revision']}`.",
             f"- Timer: `{meta['timer']}`; reported resolution {meta['timer_resolution_ns']:g} ns; monotonic: {meta['timer_monotonic']}.",
             f"- Sizes: {', '.join(str(n) for n in meta['input_sizes'])}; {meta['trials_per_case']} measured trials and {meta['warmups_per_case']} untimed warmups per case.",
             f"- Statistic: median nanoseconds; garbage collection enabled: {meta['gc_enabled']}.",
             "- Fresh fixtures contain range(n). Search uses absent -1; insertion adds -1 once to an n-element structure. Fixtures are rebuilt before every warmup and trial.",
             "- Only the bound method call is timed. Setup, binding, verification, teardown, serialization, and charts are excluded. Cases run in the recorded fixed order.", "",
             "## Measured results", "", "Runtime is the median in nanoseconds. Full raw samples and environment metadata accompany the summary CSV.", "",
             "| Structure | Operation | n | Predicted time | Median ns | P25–P75 ns |",
             "| --- | --- | ---: | --- | ---: | ---: |"]
    for result in run.results:
        row = result.summary()
        lines.append(f"| {result.structure} | {result.operation} | {result.input_size:,} | {result.predicted_complexity} | {row['Runtime']:,.1f} | {row['P25_ns']:,.1f}–{row['P75_ns']:,.1f} |")
    lines += ["", "## Charts", "", "![Measured runtime](../images/performance_chart.png)", "", "![Growth comparison](../images/complexity_comparison.png)", "",
              "Runtime axes use microseconds (CSV remains nanoseconds). Runtime-chart shading shows the interquartile range, not a confidence interval. Growth curves divide each family's medians by its smallest-size median; theoretical curves use 1 for constant/amortized operations or n/n0 for linear operations.", "",
              "## Interpretation", ""]
    growth = growth_rows(run)
    for structure, operation in CASES:
        rows = [r for r in growth if r["Structure"] == structure and r["Operation"] == operation]
        if not rows:
            continue
        last = rows[-1]
        observed = "unavailable (zero baseline)" if last["Observed_Growth"] is None else f"{last['Observed_Growth']:.2f}x"
        lines.append(f"- **{structure} {operation}:** from n={rows[0]['Input_Size']:,} to n={last['Input_Size']:,}, observed median growth was {observed}; the illustrative theoretical growth was {last['Predicted_Growth']:.2f}x.")
    lines += ["", "Search traverses every value because the target is absent. Linear traversal should become more visible as n grows; timer and call overhead can dominate small inputs. Constant/amortized insertions may fluctuate because of allocation and scheduling. Stack list capacity after fixture construction can repeatedly include or exclude a resize; these isolated pushes do not establish amortized behavior over long insertion sequences.", "",
              "## Limitations", "",
              "- A single machine/run, fixed case order, interpreter overhead, background tasks, CPU frequency, cache state, allocator behavior, and garbage collection affect timings. Nanosecond units do not imply nanosecond accuracy.",
              "- Timing one very short call includes clock/call overhead; no overhead subtraction is performed. Medians reduce some outlier effects but do not eliminate systematic bias. Shading and raw samples show variability.",
              "- Only missing-value searches and one insertion position per structure are measured. This is not a best-case or general workload comparison. Integer equality and these exact Python implementations determine constants.",
              "- Normalizing to the smallest n amplifies noise in that baseline. Zero baselines produce unavailable observed growth instead of division by zero. Theoretical curves illustrate scaling, not fitted runtime predictions.",
              "- No fixed timing threshold or exact ratio is used as a correctness test. Unexpected ratios should prompt investigation or independent repeat runs, not claims that Big-O is disproved.", "",
              "## Reproduce", "", "From the repository root:", "", "```powershell",
              f".\\.venv\\Scripts\\python.exe -m src.benchmark.performance_tester --sizes {' '.join(str(n) for n in meta['input_sizes'])} --trials {meta['trials_per_case']} --warmups {meta['warmups_per_case']}",
              "```", "", "This regenerates the tracked output files. UI runs instead keep artifacts in the browser session and offer downloads without overwriting these files.", "",
              "Timer reference: [Python time.perf_counter_ns](https://docs.python.org/3/library/time.html#time.perf_counter_ns).", ""]
    return "\n".join(lines)


def build_artifacts(run: BenchmarkRun) -> dict[str, bytes]:
    """Create six consistent artifacts in memory without rerunning measurements."""
    if not run.results:
        raise ValueError("Cannot export an empty benchmark run.")
    summary = [r.summary() for r in run.results]
    raw = [{"Structure": r.structure, "Operation": r.operation, "Input_Size": r.input_size,
            "Trial": trial, "Runtime_ns": elapsed}
           for r in run.results for trial, elapsed in enumerate(r.samples_ns, 1)]
    runtime, comparison = _charts(run)
    return {
        "data/benchmark_results.csv": _csv_bytes(summary),
        "data/benchmark_trials.csv": _csv_bytes(raw),
        "data/benchmark_metadata.json": json.dumps(run.metadata, indent=2).encode("utf-8"),
        "images/performance_chart.png": runtime,
        "images/complexity_comparison.png": comparison,
        "reports/performance_report.md": _report(run).encode("utf-8"),
    }


def write_artifacts(artifacts: dict[str, bytes], root: Path) -> None:
    """Save generated artifacts beneath root, rejecting paths outside it."""
    root = Path(root).resolve()
    for name in artifacts:
        if not (root / name).resolve().is_relative_to(root):
            raise ValueError("Artifact path must stay inside the output directory.")
    for name, content in artifacts.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def zip_artifacts(artifacts: dict[str, bytes]) -> bytes:
    """Bundle generated results, raw data, metadata, charts, and report for download."""
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, content in artifacts.items():
            archive.writestr(name, content)
    return output.getvalue()
