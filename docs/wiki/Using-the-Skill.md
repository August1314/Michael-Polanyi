# Using the Skill

This page is the public user entrypoint for Michael Polanyi.

Use this skill when the user wants practitioner judgment instead of generic balance: a grounded recommendation, visible practical signals, stated boundaries, and one concrete next step.

Canonical sources:

- [Repository README](https://github.com/August1314/Michael-Polanyi/blob/main/README.md)
- [SKILL.md](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/SKILL.md)

## Best-Fit Use Cases

Michael Polanyi works best for:

- architecture and engineering judgment
- team and process diagnosis
- career and leadership trade-offs
- incomplete-information decisions
- critiques of answers that sound correct but inexperienced

Good user language often sounds like:

- “If you had done this kind of work, what would you do first?”
- “This answer sounds correct but empty. Why?”
- “Give me a directional judgment, not a balanced preamble.”

## Poor-Fit Use Cases

Do **not** use this skill for:

- strict JSON or schema output
- exact code transformation
- legal or compliance wording
- factual checks with a clear right/wrong answer
- tasks where rigid formatting matters more than judgment

## Invocation Patterns

### Explicit skill invocation

This is the most reliable path:

- `Use Michael Polanyi to evaluate whether this architecture should go to production.`
- `Use Michael Polanyi to critique this recommendation and tell me where it sounds inexperienced.`
- `Use Michael Polanyi to answer this with a clear judgment, practical signals, and one next step.`

### Pattern-based invocation

You can also ask for the contract directly:

- `Give me a directional judgment, not a balanced preamble.`
- `Separate facts, interpretations, and hypotheses.`
- `Show trade-offs, failure conditions, and what would change your mind.`
- `Avoid pseudo-depth or fake wisdom.`

## What Good Output Looks Like

A strong answer usually:

- leads with a real judgment in the first sentence
- surfaces 2-3 practical signals an experienced operator would notice
- distinguishes what is known, inferred, and uncertain
- states trade-offs, limits, and flip conditions
- ends with one concrete next step

A weak answer usually:

- hides behind “it depends”
- inventories abstract principles
- sounds warm or deep without helping the user decide
- offers options without recommending a default

## Quick Self-Check

After installation, try one of these prompts:

- `Use Michael Polanyi to answer this like someone who has done the work: the team is stuck and not shipping.`
- `Use Michael Polanyi to tell me why this answer sounds correct but inexperienced.`

You should see:

- an upfront judgment
- practical signals rather than generic principles
- explicit boundaries or change conditions
- a specific next step

## Troubleshooting

### The skill is installed but not useful

Check whether the answer is actually following the response contract. If the output still sounds literary, atmospheric, or over-balanced, treat that as drift rather than success.

### The skill is not auto-discovered

That can happen. This project works best as an explicitly invoked judgment/writing skill. Name the skill directly when reliability matters.

### The output sounds deeper but not more useful

That is a regression. Good output should become:

- more grounded
- more directional
- more bounded
- more useful

It should not merely become more philosophical or more dramatic.
