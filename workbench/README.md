# Michael Polanyi Workbench

This directory contains **maintainer-only** tooling for evaluating and refining the Michael Polanyi skill.

The published GitHub Wiki is versioned in the main repository under `docs/wiki/`.

## Directory map

- `agents/` - blind comparison and grading prompts
- `evals/` - eval set, prompt list, rubric, and protocol
- `scripts/` - assertion and benchmark helpers
- `eval-viewer/` - HTML review generator

## Standard iteration loop

1. Edit one runtime-facing asset:
   - `skills/michael-polanyi/SKILL.md`
   - `skills/michael-polanyi/examples.md`
   - `skills/michael-polanyi/polanyi-notes.md`
   - `skills/michael-polanyi/references/*`
2. Run the fixture suite described in `workbench/evals/protocol.md`.
3. Review suite assertions, blind comparison, and generated result report.
4. Decide whether the change improved the skill, regressed it, or needs revision.
5. Commit only after the updated runtime docs and workbench checks agree.

## Core commands

Run the fixture suite:

```bash
python3 workbench/scripts/check_assertions.py \
  --suite \
  --output workbench/evals/results/latest.json
```

Generate the HTML review page from the latest suite run:

```bash
python3 workbench/eval-viewer/generate_review.py \
  --results workbench/evals/results/latest.json \
  --output workbench/evals/results/review.html
```

Run lightweight fluff detection against the examples:

```bash
python3 skills/michael-polanyi/scripts/detect_fluff.py skills/michael-polanyi/examples.md
```

Important maintenance rule:

- `workbench/evals/fixtures/` is the canonical eval input set.
- Do not point assertion checks at the whole `skills/michael-polanyi/examples.md`; that file is teaching material, not the formal suite input.
