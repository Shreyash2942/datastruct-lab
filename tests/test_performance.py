"""Verify benchmark isolation and exports without asserting machine speed."""

import csv
from dataclasses import replace
from io import BytesIO, StringIO
from itertools import count
import json
from statistics import median
from zipfile import ZipFile

from PIL import Image
import pytest

from src.benchmark import performance_tester as runner
from src.benchmark.reporting import build_artifacts, growth_rows, write_artifacts, zip_artifacts


@pytest.fixture(scope="module")
def measured_run():
    return runner.run_benchmarks((3, 7), trials=3, warmups=1)


@pytest.mark.parametrize("structure,operation", runner.CASES)
def test_fixtures_have_exact_size_and_absent_target(structure, operation):
    fixture = runner._build_fixture(structure, 7)
    assert fixture.size() == 7
    assert fixture.search(-1) is False
    outcome = getattr(fixture, operation)(-1)
    if operation == "search":
        assert outcome is False and fixture.size() == 7
    else:
        assert outcome is None and fixture.size() == 8


def test_timer_encloses_only_one_call_and_every_trial_has_fresh_fixture(monkeypatch):
    events = []
    fixtures = []
    original = runner._build_fixture

    class TracedFixture:
        def __init__(self, structure, size):
            self.real = original(structure, size)

        def __getattr__(self, name):
            method = getattr(self.real, name)
            def call(*args):
                events.append(name)
                return method(*args)
            return call

    def build(structure, size):
        events.append("build")
        fixture = TracedFixture(structure, size)
        fixtures.append(fixture)
        return fixture

    ticks = count(100, 7)
    def clock():
        events.append("clock")
        return next(ticks)

    monkeypatch.setattr(runner, "_build_fixture", build)
    monkeypatch.setattr(runner.time, "perf_counter_ns", clock)
    monkeypatch.setattr(runner, "_source_revision", lambda: "test-source")
    progress = []
    run = runner.run_benchmarks((2, 4), trials=2, warmups=1, progress=lambda done, total: progress.append((done, total)))
    expected = []
    for _, operation in runner.CASES:
        for _ in (2, 4):
            expected += ["build", operation, "size"]
            for _ in range(2):
                expected += ["build", "clock", operation, "clock", "size"]
    assert events == expected
    assert len(fixtures) == len({id(f) for f in fixtures}) == 36
    assert all(result.samples_ns == (7, 7) for result in run.results)
    assert progress == [(done, 12) for done in range(1, 13)]


def test_real_run_has_all_cases_and_metadata(measured_run):
    assert len(measured_run.results) == 12
    assert {(r.structure, r.operation, r.input_size) for r in measured_run.results} == {(s, o, n) for s, o in runner.CASES for n in (3, 7)}
    for result in measured_run.results:
        assert len(result.samples_ns) == 3
        assert all(type(t) is int and t >= 0 for t in result.samples_ns)
        assert result.predicted_complexity == ("O(n)" if result.operation == "search" else "O(1) amortized" if result.structure == "Stack" else "O(1)")
    assert measured_run.metadata["timer"] == "time.perf_counter_ns"
    assert measured_run.metadata["summary_statistic"] == "median"
    assert measured_run.metadata["input_sizes"] == [3, 7]


def test_median_and_quartiles_are_computed_from_samples():
    result = runner.BenchmarkResult("Stack", "push", 10, "O(1) amortized", (1, 3, 5, 100))
    summary = result.summary()
    assert summary["Runtime"] == 4
    assert summary["P25_ns"] == 2.5
    assert summary["P75_ns"] == 28.75
    assert summary["Min_ns"] == 1 and summary["Max_ns"] == 100


@pytest.mark.parametrize("settings", [
    {"sizes": []}, {"sizes": [1]}, {"sizes": [1, 1]}, {"sizes": [0, 2]},
    {"sizes": [-1, 2]}, {"sizes": [1, 100001]}, {"sizes": [True, 2]},
    {"sizes": [1.5, 2]}, {"sizes": None}, {"trials": 1}, {"trials": 101},
    {"trials": True}, {"warmups": -1}, {"warmups": 11}, {"warmups": False},
])
def test_invalid_settings_fail_before_any_measurement(monkeypatch, settings):
    def unexpected(*args):
        pytest.fail("Validation must happen before building fixtures")
    monkeypatch.setattr(runner, "_build_fixture", unexpected)
    with pytest.raises(ValueError):
        runner.run_benchmarks(**settings)


def test_growth_normalization_and_zero_baseline(measured_run):
    rows = growth_rows(measured_run)
    for row in rows:
        assert row["Predicted_Growth"] == (row["Input_Size"] / 3 if row["Operation"] == "search" else 1)
    zero = replace(measured_run, results=tuple(replace(r, samples_ns=(0, 0, 0)) for r in measured_run.results))
    assert all(row["Observed_Growth"] is None for row in growth_rows(zero))


def test_exported_csv_charts_report_and_zip_match_same_samples(measured_run, tmp_path):
    artifacts = build_artifacts(measured_run)
    assert len(artifacts) == 6
    summary = list(csv.DictReader(StringIO(artifacts["data/benchmark_results.csv"].decode())))
    raw = list(csv.DictReader(StringIO(artifacts["data/benchmark_trials.csv"].decode())))
    assert len(summary) == 12 and len(raw) == 36
    for row in summary:
        samples = [int(r["Runtime_ns"]) for r in raw if all(r[key] == row[key] for key in ("Structure", "Operation", "Input_Size"))]
        assert float(row["Runtime"]) == median(samples)
        assert int(row["Trials"]) == len(samples)
    metadata = json.loads(artifacts["data/benchmark_metadata.json"])
    assert metadata["run_id"] == measured_run.metadata["run_id"]
    for name in ("images/performance_chart.png", "images/complexity_comparison.png"):
        with Image.open(BytesIO(artifacts[name])) as image:
            assert image.format == "PNG" and image.width > 500 and image.height > 300
            image.verify()
    report = artifacts["reports/performance_report.md"].decode()
    assert metadata["run_id"] in report
    assert "Limitations" in report and "not a confidence interval" in report
    assert "median nanoseconds" in report
    with ZipFile(BytesIO(zip_artifacts(artifacts))) as archive:
        assert set(archive.namelist()) == set(artifacts)
        assert all(archive.read(name) == data for name, data in artifacts.items())
    write_artifacts(artifacts, tmp_path)
    assert all((tmp_path / name).read_bytes() == data for name, data in artifacts.items())


def test_export_rejects_empty_runs_and_outside_paths(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        build_artifacts(runner.BenchmarkRun((), {}))
    with pytest.raises(ValueError, match="inside"):
        write_artifacts({"ok.txt": b"ok", "../outside.txt": b"bad"}, tmp_path)
    assert not (tmp_path / "ok.txt").exists()
