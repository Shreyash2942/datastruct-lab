"""Repeated single-operation timings with fresh fixtures outside the timer."""

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import gc
from importlib.metadata import version
from pathlib import Path
import platform
from statistics import median, quantiles
import subprocess
import time
from typing import Callable
from uuid import uuid4

from src.analysis import analyze_complexity
from src.structures import LinkedList, Queue, Stack


DEFAULT_SIZES = (100, 1_000, 10_000, 50_000)
CASES = (("Stack", "push"), ("Stack", "search"), ("Queue", "enqueue"),
         ("Queue", "search"), ("Linked List", "insert"), ("Linked List", "search"))


@dataclass(frozen=True)
class BenchmarkResult:
    """One structure/operation/size case, retaining every measured nanosecond sample."""

    structure: str
    operation: str
    input_size: int
    predicted_complexity: str
    samples_ns: tuple[int, ...]

    def summary(self) -> dict:
        """Return a CSV-ready row; Runtime is the median in nanoseconds."""
        lower, _, upper = quantiles(self.samples_ns, n=4, method="inclusive")
        return {
            "Structure": self.structure, "Operation": self.operation,
            "Input_Size": self.input_size, "Predicted_Complexity": self.predicted_complexity,
            "Runtime": median(self.samples_ns), "Trials": len(self.samples_ns),
            "Min_ns": min(self.samples_ns), "P25_ns": lower, "P75_ns": upper,
            "Max_ns": max(self.samples_ns),
        }


@dataclass(frozen=True)
class BenchmarkRun:
    """A complete set of cases and the environment/method used to collect them."""

    results: tuple[BenchmarkResult, ...]
    metadata: dict


def _build_fixture(structure: str, size: int):
    """Build exactly size elements through public operations, outside timing."""
    factories = {"Stack": (Stack, "push"), "Queue": (Queue, "enqueue"), "Linked List": (LinkedList, "insert")}
    factory, method_name = factories[structure]
    fixture = factory()
    add = getattr(fixture, method_name)
    for value in range(size):
        add(value)
    return fixture


def _source_revision() -> str:
    """Record the local source revision without depending on Git being installed."""
    try:
        root = Path(__file__).resolve().parents[2]
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True, timeout=5).stdout.strip()
        changes = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=root, capture_output=True, text=True, check=True, timeout=5).stdout
        return revision + (" (tracked working changes)" if changes else "")
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def run_benchmarks(sizes=DEFAULT_SIZES, trials: int = 30, warmups: int = 3,
                   progress: Callable[[int, int], None] | None = None) -> BenchmarkRun:
    """Measure six operation types with fresh n-element fixtures per invocation.

    Sizes must contain at least two distinct integers in 1..100,000; trials
    must be 2..100 and warmups 0..10 (bool is rejected). The UI uses 20..50
    trials; smaller counts support quick checks. Invalid settings raise ValueError.
    Setup, binding, verification, teardown, progress, and serialization are not
    timed. The measured call uses -1, which is absent from range(n) fixtures.
    Optional progress receives completed-case and total-case counts.
    """
    try:
        sizes = tuple(sizes)
    except TypeError as error:
        raise ValueError("Choose at least two distinct integer input sizes.") from error
    if (len(sizes) < 2 or any(type(n) is not int or not 1 <= n <= 100_000 for n in sizes)
            or len(set(sizes)) != len(sizes)):
        raise ValueError("Choose at least two distinct integer sizes from 1 to 100,000.")
    if type(trials) is not int or not 2 <= trials <= 100:
        raise ValueError("Trials must be an integer from 2 to 100.")
    if type(warmups) is not int or not 0 <= warmups <= 10:
        raise ValueError("Warmups must be an integer from 0 to 10.")
    sizes = tuple(sorted(sizes))
    started = datetime.now(timezone.utc).isoformat()
    clock_info = time.get_clock_info("perf_counter")
    wall_start = time.perf_counter()
    results = []
    total = len(CASES) * len(sizes)
    for structure, operation in CASES:
        for size in sizes:
            samples = []
            for trial in range(warmups + trials):
                fixture = _build_fixture(structure, size)
                method = getattr(fixture, operation)
                if trial < warmups:
                    outcome = method(-1)
                else:
                    start = time.perf_counter_ns()
                    outcome = method(-1)
                    elapsed = time.perf_counter_ns() - start
                    samples.append(elapsed)
                if operation == "search":
                    if outcome is not False or fixture.size() != size:
                        raise RuntimeError("Search fixture must miss and remain unchanged.")
                elif fixture.size() != size + 1:
                    raise RuntimeError("Insertion must add exactly one element.")
                del method, fixture
            prediction = analyze_complexity(structure, operation, size).rule.time
            results.append(BenchmarkResult(structure, operation, size, prediction, tuple(samples)))
            if progress is not None:
                progress(len(results), total)
    metadata = {
        "run_id": uuid4().hex, "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "wall_seconds": time.perf_counter() - wall_start,
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "platform": platform.platform(), "processor": platform.processor() or "unreported",
        "packages": {name: version(name) for name in ("streamlit", "matplotlib", "pandas")},
        "source_revision": _source_revision(), "timer": "time.perf_counter_ns",
        "timer_resolution_ns": clock_info.resolution * 1e9,
        "timer_monotonic": clock_info.monotonic, "gc_enabled": gc.isenabled(),
        "input_sizes": list(sizes), "trials_per_case": trials, "warmups_per_case": warmups,
        "runtime_unit": "nanoseconds", "summary_statistic": "median",
        "fixture": "Fresh values range(n) before every invocation; argument -1 is absent.",
        "timed_region": "One bound method call; setup, binding, verification, teardown, and rendering excluded.",
        "case_order": [f"{s}.{o}" for s, o in CASES],
    }
    return BenchmarkRun(tuple(results), metadata)


def main() -> None:
    """Run the assignment benchmark and write its reproducible artifact bundle."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES)
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        run = run_benchmarks(args.sizes, args.trials, args.warmups,
                             lambda done, total: print(f"Measured case {done}/{total}", flush=True))
    except ValueError as error:
        parser.error(str(error))
    from src.benchmark.reporting import build_artifacts, write_artifacts
    artifacts = build_artifacts(run)
    write_artifacts(artifacts, args.output_dir)
    print(f"Saved {len(artifacts)} artifacts to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
