# Roadmap and Open Questions

This page tracks the current forward-looking maintainer queue.

## Active Follow-Ups

### Issue #3 — Trim `examples.md` to a minimum high-value runtime set

Link:

- [Issue #3](https://github.com/August1314/Michael-Polanyi/issues/3)

Theme:

- reduce runtime surface area in `examples.md`
- keep only the strongest teaching examples
- move summary or inventory material out of the runtime example file where appropriate

### Issue #4 — Refine `SKILL.md` discoverability and trigger surface

Link:

- [Issue #4](https://github.com/August1314/Michael-Polanyi/issues/4)

Theme:

- reduce ambiguity in trigger logic
- improve false-positive / false-negative tuning
- make discoverability iteration easier without re-bloating `SKILL.md`

## Recently Completed Work

The repository split that created the public runtime package / internal workbench boundary is complete.

Historical references:

- [Issue #1](https://github.com/August1314/Michael-Polanyi/issues/1)
- [PR #2](https://github.com/August1314/Michael-Polanyi/pull/2)

That work delivered:

- runtime package / workbench separation
- clearer public vs maintainer documentation layers
- a tighter `SKILL.md` routing surface
- a documented maintainer workflow

## Deferred Questions

These are not active issues yet, but are worth watching:

- should the wiki eventually become the primary onboarding surface, or stay secondary to `README.md`?
- how much of the runtime example explanation should live in the wiki versus repo references?
- should discoverability changes eventually get their own dedicated eval prompts?

The default for now is conservative:

- keep the runtime package lean
- keep the workbench explicit
- create small, focused issues rather than broad restructuring tickets
