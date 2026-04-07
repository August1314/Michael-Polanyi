# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-04-07

### Changed

- **SKILL.md**: restructured response framework into 6-step core sequence,
  optimized trigger description with explicit patterns, added anti-generic
  detection table and quality check red flags
- **examples.md**: added comparison analysis tables for all 5 examples,
  included pattern summary and anti-patterns reference
- **polanyi-notes.md**: restructured concepts into concept→implication pattern,
  added quick reference table

### Added

- **scripts/detect_fluff.py**: AI-generic pattern detection tool supporting
  Chinese and English, covers 8 pattern categories
- **scripts/check_assertions.py**: assertion checker for eval validation,
  supporting text_pattern, not_contains, and min_count types
- **evals/evals.json**: 10 test cases with 3-4 assertions each, covering
  8 trigger scenarios and 2 non-trigger exclusion tests
- **references/response-patterns.md**: extended reference with 6 response
  patterns, 4 deep anti-pattern analyses, and 4 domain-specific patterns
- **skills/README.md**: skill overview, file structure, quick start guide

### Fixed

- CI markdown lint false-positive caused by broken grep pipe logic
- Frontmatter validation corrected from `grep -q` pipeline to `grep -c` count
- Fluff detection made non-fatal for examples.md which intentionally contains
  anti-pattern reference examples

---

## [0.1.0] - 2026-04-07

### Added

- initial Michael Polanyi skill scaffold
- `SKILL.md` with response contract and discoverability-oriented description
- supporting notes distilled from Polanyi-inspired concepts
- before/after examples for architecture judgment, team stall, incomplete-information judgment, critique, and anti pseudo-depth pressure tests
- evaluation prompt set and rubric
- README with installation and usage guidance for Claude Code and Codex-style setups
- public release support files: MIT license, contribution guide, code of conduct, security policy, and GitHub templates

### Changed

- refined README for public-facing onboarding
- improved skill discoverability wording for Claude Code search
