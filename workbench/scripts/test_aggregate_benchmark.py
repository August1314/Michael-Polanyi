"""Tests for aggregate_benchmark.py using stdlib unittest."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# Ensure the script is importable
sys.path.insert(0, str(Path(__file__).parent))
from aggregate_benchmark import aggregate_results


def make_run_result(evals: list) -> dict:
    """Create a minimal valid run-result JSON with an evals list."""
    return {"evals": evals}


class TestReingestionSafety(unittest.TestCase):
    """Test that re-running the aggregator in the same directory is safe."""

    def test_repeated_run_does_not_crash(self):
        """Running aggregate twice with a benchmark.json in the dir must not crash."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Write a valid suite result file
            run_data = make_run_result([
                {"id": 1, "eval_name": "test-eval", "passed": 8, "total": 10},
            ])
            (tmp_path / "run-1.json").write_text(json.dumps(run_data))

            # First run: produce benchmark.json
            result1 = aggregate_results(tmp_path)
            summary1 = result1["summary"]
            self.assertEqual(summary1["total_runs"], 1)

            # Write the benchmark output alongside the run file
            (tmp_path / "benchmark.json").write_text(json.dumps(result1) + "\n")

            # Second run: re-read the directory that now contains both files
            result2 = aggregate_results(tmp_path)
            summary2 = result2["summary"]

            # Must count exactly one valid run, not crash on benchmark.json
            self.assertEqual(
                summary2["total_runs"], 1,
                f"Expected 1 run but got {summary2['total_runs']}; "
                f"benchmark.json may have been re-ingested"
            )

    def test_aggregate_output_json_is_skipped(self):
        """Files with evals as a dict (not list) must be silently skipped."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            run_data = make_run_result([
                {"id": 1, "eval_name": "test-eval", "passed": 5, "total": 5},
            ])
            (tmp_path / "run-1.json").write_text(json.dumps(run_data))

            # Write a benchmark.json with evals as a dict (aggregate output shape)
            aggregate_data = {
                "generated_at": "2026-01-01T00:00:00",
                "summary": {"total_runs": 1, "total_evals": 1, "overall_pass_rate": 1.0},
                "evals": {"1": {"eval_name": "test-eval", "runs": []}},  # dict, not list
            }
            (tmp_path / "benchmark.json").write_text(json.dumps(aggregate_data))

            output = io.StringIO()
            with redirect_stdout(output):
                result = aggregate_results(tmp_path)

            printed = output.getvalue()
            self.assertIn("Skipping benchmark.json", printed)

            summary = result["summary"]
            self.assertEqual(summary["total_runs"], 1)

    def test_valid_suite_results_still_aggregate(self):
        """Existing valid suite result files must aggregate correctly."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            runs = [
                {"id": 1, "eval_name": "eval-a", "passed": 7, "total": 10},
                {"id": 2, "eval_name": "eval-b", "passed": 9, "total": 10},
            ]
            (tmp_path / "run-1.json").write_text(json.dumps(make_run_result(runs)))

            (tmp_path / "run-2.json").write_text(json.dumps(make_run_result([
                {"id": 1, "eval_name": "eval-a", "passed": 8, "total": 10},
                {"id": 2, "eval_name": "eval-b", "passed": 6, "total": 10},
            ])))

            result = aggregate_results(tmp_path)
            summary = result["summary"]

            self.assertEqual(summary["total_runs"], 2)
            self.assertEqual(summary["total_evals"], 2)
            self.assertEqual(summary["overall_passed"], 30)  # 7+9 + 8+6
            self.assertEqual(summary["overall_assertions"], 40)  # 10+10 + 10+10

    def test_file_discovery_is_deterministic(self):
        """Result file discovery order must be stable across calls."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for i in range(5):
                (tmp_path / f"run-{i}.json").write_text(json.dumps(make_run_result([
                    {"id": 1, "eval_name": "eval-1", "passed": 1, "total": 1},
                ])))

            run1 = aggregate_results(tmp_path)
            run2 = aggregate_results(tmp_path)
            run3 = aggregate_results(tmp_path)

            ids_run1 = list(run1["evals"].get("1", {}).get("runs", []))
            ids_run2 = list(run2["evals"].get("1", {}).get("runs", []))
            ids_run3 = list(run3["evals"].get("1", {}).get("runs", []))

            self.assertEqual(ids_run1, ids_run2)
            self.assertEqual(ids_run2, ids_run3)


if __name__ == "__main__":
    unittest.main()
