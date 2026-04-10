#!/usr/bin/env python3
"""Check Michael Polanyi eval assertions against a single file or the full fixture suite.

Usage:
    python workbench/scripts/check_assertions.py <text-file> <eval-id>
    python workbench/scripts/check_assertions.py --suite
    python workbench/scripts/check_assertions.py --suite --output workbench/evals/results/latest.json
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

DEFAULT_EVALS_PATH = Path(__file__).resolve().parent.parent / "evals" / "evals.json"
DEFAULT_RESULTS_PATH = Path(__file__).resolve().parent.parent / "evals" / "results" / "latest.json"


def load_evals(path: Path = DEFAULT_EVALS_PATH) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def short_pattern(pattern: str, limit: int = 40) -> str:
    if len(pattern) <= limit:
        return pattern
    return f"{pattern[:limit]}..."


def check_assertion(text: str, assertion: dict) -> dict:
    """Check a single assertion against text."""
    name = assertion["name"]
    description = assertion["description"]
    assertion_type = assertion.get("type", "text_pattern")
    pattern = assertion.get("pattern", "")

    if assertion_type == "text_pattern":
        found = bool(re.search(pattern, text))
        return {
            "name": name,
            "description": description,
            "passed": found,
            "evidence": f"Pattern '{short_pattern(pattern)}' {'found' if found else 'not found'}",
        }

    if assertion_type == "not_contains":
        found = bool(re.search(pattern, text))
        return {
            "name": name,
            "description": description,
            "passed": not found,
            "evidence": (
                f"Pattern '{short_pattern(pattern)}' "
                f"{'found (FAIL)' if found else 'not found (PASS)'}"
            ),
        }

    if assertion_type == "min_count":
        matches = re.findall(pattern, text)
        count = len(matches)
        min_count = assertion.get("min_count", 1)
        return {
            "name": name,
            "description": description,
            "passed": count >= min_count,
            "evidence": f"Found {count} matches (need >= {min_count})",
        }

    return {
        "name": name,
        "description": description,
        "passed": False,
        "evidence": f"Unknown assertion type: {assertion_type}",
    }


def find_eval(evals_data: dict, eval_id: int) -> dict | None:
    for eval_entry in evals_data.get("evals", []):
        if eval_entry.get("id") == eval_id:
            return eval_entry
    return None


def summarize_assertions(assertion_results: list[dict]) -> tuple[int, int, float]:
    passed = sum(1 for result in assertion_results if result["passed"])
    total = len(assertion_results)
    pass_rate = passed / total if total else 0.0
    return passed, total, pass_rate


def run_eval(text: str, eval_entry: dict) -> dict:
    assertion_results = [check_assertion(text, assertion) for assertion in eval_entry["assertions"]]
    passed, total, pass_rate = summarize_assertions(assertion_results)
    return {
        "id": eval_entry["id"],
        "eval_name": eval_entry.get("eval_name", "unnamed"),
        "prompt": eval_entry.get("prompt", ""),
        "passed": passed,
        "total": total,
        "pass_rate": pass_rate,
        "all_passed": passed == total,
        "assertions": assertion_results,
    }


def resolve_fixture_paths(eval_entry: dict, evals_path: Path) -> list[Path]:
    fixture_paths = []
    files = eval_entry.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError(f"eval {eval_entry.get('id')} has empty files")

    for relative_path in files:
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise ValueError(f"eval {eval_entry.get('id')} has invalid file path")
        fixture_path = (evals_path.parent / relative_path).resolve()
        fixture_paths.append(fixture_path)

    return fixture_paths


def validate_evals(evals_data: dict, evals_path: Path = DEFAULT_EVALS_PATH) -> list[str]:
    errors = []
    eval_entries = evals_data.get("evals")
    if not isinstance(eval_entries, list) or not eval_entries:
        return ["evals.json missing non-empty 'evals' list"]

    seen_ids = set()
    for index, eval_entry in enumerate(eval_entries, start=1):
        label = f"eval #{index}"
        eval_id = eval_entry.get("id")
        eval_name = eval_entry.get("eval_name", "unnamed")

        if eval_id in seen_ids:
            errors.append(f"{label} ({eval_name}) has duplicate id: {eval_id}")
        else:
            seen_ids.add(eval_id)

        for key in ["id", "eval_name", "prompt", "assertions", "files"]:
            if key not in eval_entry:
                errors.append(f"{label} ({eval_name}) missing required key: {key}")

        assertions = eval_entry.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{label} ({eval_name}) has empty assertions")
        else:
            assertion_names = set()
            for assertion in assertions:
                assertion_name = assertion.get("name")
                if not assertion_name:
                    errors.append(f"{label} ({eval_name}) has assertion without name")
                    continue
                if assertion_name in assertion_names:
                    errors.append(f"{label} ({eval_name}) has duplicate assertion: {assertion_name}")
                assertion_names.add(assertion_name)

        try:
            fixture_paths = resolve_fixture_paths(eval_entry, evals_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        for fixture_path in fixture_paths:
            if not fixture_path.exists():
                errors.append(f"eval {eval_id} fixture not found: {fixture_path}")

    return errors


def print_single_run(result: dict) -> None:
    print(f"Checking eval {result['id']}: {result['eval_name']}")
    print(f"Prompt: {result['prompt']}")
    print(f"Assertions: {result['total']}")
    print("-" * 60)
    for assertion in result["assertions"]:
        status = "PASS" if assertion["passed"] else "FAIL"
        print(f"  [{status}] {assertion['name']}: {assertion['evidence']}")
    print("-" * 60)
    print(f"Result: {result['passed']}/{result['total']} passed ({result['pass_rate']:.0%})")


def run_suite(evals_data: dict, evals_path: Path) -> dict:
    suite_results = []
    for eval_entry in evals_data["evals"]:
        fixture_paths = resolve_fixture_paths(eval_entry, evals_path)
        combined_text = "\n\n".join(
            fixture_path.read_text(encoding="utf-8").strip() for fixture_path in fixture_paths
        )
        result = run_eval(combined_text, eval_entry)
        result["files"] = [str(path.relative_to(evals_path.parent)) for path in fixture_paths]
        suite_results.append(result)

    overall_passed = sum(result["passed"] for result in suite_results)
    overall_assertions = sum(result["total"] for result in suite_results)
    passed_evals = sum(1 for result in suite_results if result["all_passed"])
    total_evals = len(suite_results)

    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "evals_path": str(evals_path),
        "summary": {
            "total_evals": total_evals,
            "passed_evals": passed_evals,
            "overall_passed": overall_passed,
            "overall_assertions": overall_assertions,
            "overall_pass_rate": (
                overall_passed / overall_assertions if overall_assertions else 0.0
            ),
        },
        "evals": suite_results,
    }


def print_suite_run(suite_result: dict) -> None:
    for eval_result in suite_result["evals"]:
        status = "PASS" if eval_result["all_passed"] else "FAIL"
        files = ", ".join(eval_result.get("files", []))
        print(
            f"[{status}] #{eval_result['id']} {eval_result['eval_name']} "
            f"({eval_result['passed']}/{eval_result['total']})"
        )
        print(f"       files: {files}")

    summary = suite_result["summary"]
    print("-" * 60)
    print(
        "Suite result: "
        f"{summary['passed_evals']}/{summary['total_evals']} evals passed, "
        f"{summary['overall_passed']}/{summary['overall_assertions']} assertions passed "
        f"({summary['overall_pass_rate']:.0%})"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Michael Polanyi eval assertions")
    parser.add_argument("text_file", nargs="?", help="Text file to check in single-file mode")
    parser.add_argument("eval_id", nargs="?", type=int, help="Eval id to run in single-file mode")
    parser.add_argument(
        "--suite",
        action="store_true",
        help="Run the full fixture suite declared in evals.json",
    )
    parser.add_argument(
        "--evals",
        type=Path,
        default=DEFAULT_EVALS_PATH,
        help="Path to evals.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_RESULTS_PATH,
        help="Result JSON path for suite mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    evals_data = load_evals(args.evals)
    validation_errors = validate_evals(evals_data, args.evals)
    if validation_errors:
        for error in validation_errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)

    if args.suite:
        suite_result = run_suite(evals_data, args.evals)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(suite_result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print_suite_run(suite_result)
        print(f"Saved result JSON: {args.output}")
        raise SystemExit(0 if suite_result["summary"]["passed_evals"] == suite_result["summary"]["total_evals"] else 1)

    if not args.text_file or args.eval_id is None:
        print("Usage: python workbench/scripts/check_assertions.py <text-file> <eval-id>")
        print("   or: python workbench/scripts/check_assertions.py --suite")
        raise SystemExit(1)

    text = Path(args.text_file).read_text(encoding="utf-8")
    eval_entry = find_eval(evals_data, args.eval_id)
    if not eval_entry:
        print(f"Eval ID {args.eval_id} not found")
        raise SystemExit(1)

    result = run_eval(text, eval_entry)
    print_single_run(result)
    raise SystemExit(0 if result["all_passed"] else 1)


if __name__ == "__main__":
    main()
