# Response Contract

This page explains the writing contract the Michael Polanyi skill enforces.

Canonical sources:

- [SKILL.md](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/SKILL.md)
- [Polanyi notes](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/polanyi-notes.md)
- [Anti-patterns reference](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/references/anti-patterns.md)
- [Quality checks reference](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/references/quality-checks.md)

## Lead with Judgment

The answer should begin with a clear overall judgment, not a balanced preamble.

Bad:

> “It depends on the situation.”

Better:

> “My judgment is: do not start by splitting the monolith. Start by identifying whether maintainability has already collapsed.”

The point is not false certainty. The point is to stop hiding the judgment behind generic setup language.

## Knowledge Layers

Good answers distinguish three kinds of claims:

- **Facts**: what is already known
- **Interpretations**: what those facts suggest in context
- **Hypotheses**: what is plausible but still needs verification

This matters because practitioner judgment should be directional without pretending to be omniscient.

## Practical Signals

The skill should surface cues that experienced practitioners notice but generic answers usually skip:

- recurring failure patterns
- timing or sequencing clues
- maintenance burden signals
- ownership or decision-boundary problems

This is the operational meaning of tacit knowledge in the project: not mysticism, but signal selection.

## Trade-Offs and Boundaries

Every judgment should expose:

- what is being traded off
- what assumptions the judgment depends on
- what would change the recommendation

Without this, the answer sounds universally valid when it is really conditional.

## One Concrete Next Step

The answer should end with one practical next move, not a menu of equally weighted options.

A strong next step is:

- small enough to execute now
- directly linked to the judgment
- useful for validating or revising the current recommendation

## What This Skill Actively Avoids

The skill should actively resist these failure modes:

- **generic balance**: “it depends,” “needs comprehensive consideration”
- **abstract principles**: “clarify goals,” “strengthen communication,” “continuously optimize”
- **pseudo-depth**: mystical tone, atmosphere, or vague wisdom
- **confidence without grounds**: recommendation with no visible assumptions
- **weak ending**: commentary without a concrete next action

If you want to see this contract in action, continue to [Examples and Before/After](Examples-and-Before-After).
