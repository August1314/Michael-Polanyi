#!/usr/bin/env python3
"""Generate a standalone HTML page for Michael Polanyi eval specs or result runs.

Usage:
    python generate_review.py
    python generate_review.py --results ../evals/results/latest.json
    python generate_review.py --results ../evals/results/latest.json --output ../evals/results/review.html
"""

import argparse
import json
from html import escape
from pathlib import Path

DEFAULT_EVALS_PATH = Path(__file__).parent.parent / "evals" / "evals.json"
DEFAULT_OUTPUT_PATH = Path(__file__).parent / "review.html"


def truncate(value: str, limit: int = 50) -> str:
    if len(value) <= limit:
        return value
    return f"{value[:limit]}..."


def load_json(path: Path | None) -> dict | None:
    if path is None:
        return None
    if not path.exists():
        print(f"Error: {path} not found", flush=True)
        raise SystemExit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def result_map(results_data: dict | None) -> dict[int, dict]:
    if not results_data:
        return {}
    return {result["id"]: result for result in results_data.get("evals", [])}


def render_summary(evals_data: dict, results_data: dict | None) -> str:
    evals = evals_data.get("evals", [])
    if results_data:
        summary = results_data.get("summary", {})
        generated_at = escape(results_data.get("generated_at", "unknown"))
        return f"""
        <div class="summary">
            <h2>Run Summary</h2>
            <div class="note success">results mode · generated at {generated_at}</div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{summary.get('passed_evals', 0)}/{summary.get('total_evals', len(evals))}</div>
                    <div class="stat-label">Passed Evals</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{summary.get('overall_passed', 0)}/{summary.get('overall_assertions', 0)}</div>
                    <div class="stat-label">Passed Assertions</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{summary.get('overall_pass_rate', 0):.0%}</div>
                    <div class="stat-label">Overall Pass Rate</div>
                </div>
            </div>
        </div>
        """

    non_trigger_count = len([entry for entry in evals if "no-trigger" in entry.get("eval_name", "")])
    total_assertions = sum(len(entry.get("assertions", [])) for entry in evals)
    return f"""
    <div class="summary">
        <h2>Spec Summary</h2>
        <div class="note warning">spec-only · this page shows eval definitions, not execution results</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(evals)}</div>
                <div class="stat-label">Total Evals</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_assertions}</div>
                <div class="stat-label">Total Assertions</div>
            </div>
            <div class="stat">
                <div class="stat-value">{non_trigger_count}</div>
                <div class="stat-label">Non-Trigger Tests</div>
            </div>
        </div>
    </div>
    """


def render_assertions(spec_assertions: list[dict], result_assertions: list[dict] | None) -> str:
    rows = []
    result_by_name = {result["name"]: result for result in (result_assertions or [])}
    for assertion in spec_assertions:
        result = result_by_name.get(assertion.get("name"))
        status = "PASS" if result and result.get("passed") else "FAIL" if result else "SPEC"
        status_class = status.lower()
        evidence = escape(result.get("evidence", "spec-only")) if result else "spec-only"
        rows.append(
            f"""
            <tr>
                <td><code>{escape(assertion.get('name', '?'))}</code></td>
                <td>{escape(assertion.get('description', ''))}</td>
                <td><span class="type-badge">{escape(assertion.get('type', 'text_pattern'))}</span></td>
                <td><code>{escape(truncate(assertion.get('pattern', '')))}</code></td>
                <td><span class="status-badge {status_class}">{status}</span></td>
                <td>{evidence}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def render_eval_cards(evals_data: dict, results_data: dict | None) -> str:
    cards = []
    results_by_id = result_map(results_data)

    for eval_entry in evals_data.get("evals", []):
        eval_id = eval_entry.get("id", "?")
        eval_name = escape(eval_entry.get("eval_name", "unnamed"))
        prompt = escape(eval_entry.get("prompt", ""))
        expected = escape(eval_entry.get("expected_output", ""))
        spec_assertions = eval_entry.get("assertions", [])
        files = [escape(path) for path in eval_entry.get("files", [])]

        eval_result = results_by_id.get(eval_id)
        header_status = "SPEC-ONLY"
        header_class = "spec"
        result_meta = ""
        if eval_result:
            header_status = "PASS" if eval_result.get("all_passed") else "FAIL"
            header_class = "pass" if eval_result.get("all_passed") else "fail"
            result_meta = (
                f"<div class=\"result-meta\">"
                f"{eval_result.get('passed', 0)}/{eval_result.get('total', 0)} assertions passed · "
                f"{eval_result.get('pass_rate', 0):.0%}"
                f"</div>"
            )

        file_list = "<br>".join(files) if files else "<span class=\"muted\">none</span>"
        assertions_html = render_assertions(spec_assertions, eval_result.get("assertions") if eval_result else None)

        cards.append(
            f"""
            <div class="eval-card">
                <div class="eval-header">
                    <div class="eval-title">
                        <span class="eval-id">#{eval_id}</span>
                        <span class="eval-name">{eval_name}</span>
                    </div>
                    <span class="status-badge {header_class}">{header_status}</span>
                </div>
                <div class="eval-body">
                    {result_meta}
                    <div class="field">
                        <label>Prompt</label>
                        <div class="prompt-text">{prompt}</div>
                    </div>
                    <div class="field">
                        <label>Expected Output</label>
                        <div class="expected-text">{expected}</div>
                    </div>
                    <div class="field">
                        <label>Fixture Files</label>
                        <div class="fixture-text">{file_list}</div>
                    </div>
                    <div class="field">
                        <label>Assertions ({len(spec_assertions)})</label>
                        <table class="assertions-table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Description</th>
                                    <th>Type</th>
                                    <th>Pattern</th>
                                    <th>Status</th>
                                    <th>Evidence</th>
                                </tr>
                            </thead>
                            <tbody>
                                {assertions_html}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            """
        )

    return "\n".join(cards)


def generate_html(evals_data: dict, output_path: Path, results_data: dict | None = None) -> None:
    skill_name = escape(evals_data.get("skill_name", "michael-polanyi"))
    evals = evals_data.get("evals", [])
    mode_label = "Eval Review" if results_data else "Eval Review (spec-only)"
    summary_html = render_summary(evals_data, results_data)
    cards_html = render_eval_cards(evals_data, results_data)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{skill_name} - {mode_label}</title>
    <style>
        :root {{
            --bg: #faf9f5;
            --surface: #ffffff;
            --border: #e8e6dc;
            --text: #141413;
            --text-muted: #666;
            --accent: #d97757;
            --header-bg: #141413;
            --header-text: #faf9f5;
            --pass: #1f7a45;
            --fail: #b42318;
            --spec: #9a6700;
            --note-pass: #edf7ed;
            --note-warn: #fff7e6;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}

        .header {{
            background: var(--header-bg);
            color: var(--header-text);
            padding: 1.5rem 2rem;
        }}

        .header h1 {{
            font-size: 1.5rem;
            font-weight: 600;
        }}

        .header .subtitle {{
            opacity: 0.75;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }}

        .main {{
            max-width: 1080px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .summary {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}

        .summary h2 {{
            font-size: 1rem;
            margin-bottom: 1rem;
        }}

        .stats {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
        }}

        .stat {{
            min-width: 180px;
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: 600;
            color: var(--accent);
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .note {{
            margin-bottom: 1rem;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
        }}

        .note.success {{
            background: var(--note-pass);
            color: var(--pass);
        }}

        .note.warning {{
            background: var(--note-warn);
            color: var(--spec);
        }}

        .eval-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }}

        .eval-header {{
            background: var(--bg);
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}

        .eval-title {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .eval-id {{
            background: var(--accent);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .eval-name {{
            font-weight: 600;
        }}

        .eval-body {{
            padding: 1rem;
        }}

        .result-meta {{
            margin-bottom: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }}

        .field {{
            margin-bottom: 1rem;
        }}

        .field:last-child {{
            margin-bottom: 0;
        }}

        .field label {{
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }}

        .prompt-text,
        .expected-text,
        .fixture-text {{
            background: var(--bg);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            font-size: 0.875rem;
        }}

        .muted {{
            color: var(--text-muted);
        }}

        .assertions-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
        }}

        .assertions-table th {{
            text-align: left;
            padding: 0.6rem;
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            font-weight: 600;
        }}

        .assertions-table td {{
            padding: 0.6rem;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }}

        .assertions-table code {{
            background: #f0f0f0;
            padding: 0.125rem 0.25rem;
            border-radius: 3px;
            font-size: 0.75rem;
        }}

        .type-badge,
        .status-badge {{
            display: inline-block;
            padding: 0.125rem 0.5rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
        }}

        .type-badge {{
            background: #ececec;
            color: #333;
        }}

        .status-badge.pass {{
            background: #e8f5e9;
            color: var(--pass);
        }}

        .status-badge.fail {{
            background: #fdecea;
            color: var(--fail);
        }}

        .status-badge.spec {{
            background: #fff4db;
            color: var(--spec);
        }}

        @media (max-width: 820px) {{
            .main {{
                padding: 1rem;
            }}

            .assertions-table {{
                display: block;
                overflow-x: auto;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>{skill_name}</h1>
        <div class="subtitle">{mode_label} · {len(evals)} test cases</div>
    </header>

    <main class="main">
        {summary_html}
        {cards_html}
    </main>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✓ Generated: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate eval review HTML")
    parser.add_argument(
        "--evals",
        "-e",
        type=Path,
        default=DEFAULT_EVALS_PATH,
        help="Path to evals.json",
    )
    parser.add_argument(
        "--results",
        "-r",
        type=Path,
        help="Optional result JSON generated by check_assertions.py --suite",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output HTML path",
    )
    args = parser.parse_args()

    evals_data = load_json(args.evals)
    results_data = load_json(args.results)
    generate_html(evals_data, args.output, results_data)


if __name__ == "__main__":
    main()
