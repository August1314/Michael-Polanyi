# Evaluation Workflow

This page is the maintainer entrypoint for measuring whether changes are real improvements.

Canonical sources:

- [Evaluation protocol](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/evals/protocol.md)
- [Evaluation rubric](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/evals/rubric.md)
- [Workbench guide](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/README.md)

## Evaluation Goal

The goal is **not** to make answers longer, warmer, more literary, or more philosophical.

The goal is to make answers:

- more grounded
- more directional
- more bounded
- more useful

## Inputs

The workbench evaluation flow depends on:

- prompt set: `workbench/evals/prompts.md`
- fixture set: `workbench/evals/fixtures/`
- scoring rubric: `workbench/evals/rubric.md`
- protocol: `workbench/evals/protocol.md`
- assertion suite output: `workbench/evals/results/latest.json`
- optional HTML review output: `workbench/evals/results/review.html`

## Test Method

For each prompt:

1. run it once without the skill
2. run the same prompt again with the skill
3. keep model, context, and framing as stable as possible
4. do not rewrite the prompt between runs

For unstable prompts, use 2-3 repetitions before calling the result.

For repository-level regression checks, keep a separate distinction:

- `prompts.md` is the human prompt bank
- `fixtures/` is the canonical machine-checked sample set
- `check_assertions.py --suite` is the formal assertion run
- the HTML page can be either `spec-only` or `results mode` depending on whether a result JSON is supplied

## Scoring Dimensions

Score both baseline and with-skill output across six dimensions:

1. clarity of judgment
2. practical signal density
3. fact / interpretation / hypothesis separation
4. trade-offs and boundaries
5. actionability
6. resistance to pseudo-depth

The comparison should focus on whether the skill improved decision value, not whether the answer simply sounds more polished.

## Failure Signals

Treat these as regressions:

- the answer becomes more mystical or atmospheric
- the answer sounds more like a philosopher than a practitioner
- confidence increases without grounds
- the answer gets longer without getting sharper
- the next step gets weaker or disappears

## Recording Results

For each prompt, record:

- baseline score and note
- with-skill score and note
- what improved
- what regressed
- final call

Useful supporting artifacts:

- assertion helpers in `workbench/scripts/`
- blind comparison prompts in `workbench/agents/`
- generated suite JSON in `workbench/evals/results/`
- generated HTML review in `workbench/evals/results/`

Important boundary:

- do not run the formal assertion suite against the whole `skills/michael-polanyi/examples.md`
- use the canonical fixture files declared in `workbench/evals/evals.json`
- treat `examples.md` as teaching/reference material, not as the test corpus

If you want the broader maintainer loop around these checks, continue to [Maintainer Guide](Maintainer-Guide).
