# Michael Polanyi Wiki

Michael Polanyi is a writing skill for turning correct-but-generic model output into practitioner-style judgment: grounded, directional, bounded, and useful. It is designed for ambiguous situations where the user wants a real recommendation, not a polished summary.

This wiki serves two reader paths without mixing them:

- **Users**: what the skill does, when to use it, how to install it, and how to tell if it is working
- **Maintainers**: how the repository is structured, how the evaluation workflow works, and where follow-up improvements live

## What Michael Polanyi Is

This project is a prompt-engineering skill inspired by Michael Polanyi's ideas of tacit knowledge, personal knowledge, and integrative judgment.

It is **not**:

- a simulation of Michael Polanyi as a person
- a philosophy explainer
- a universal answer improver for every task

Canonical repo entrypoint:

- [Repository README](https://github.com/August1314/Michael-Polanyi/blob/main/README.md)

## Who This Wiki Is For

Use this wiki if you want to:

- decide whether this skill fits your prompt
- install it in a Claude Code or Codex-style setup
- understand the response contract behind the skill
- maintain or improve the skill using the workbench and eval flow

## Choose Your Path

### I want to use the skill

Start here:

1. [Using the Skill](Using-the-Skill)
2. [Installation and Compatibility](Installation-and-Compatibility)
3. [Examples and Before/After](Examples-and-Before-After)

### I want to maintain or contribute to the skill

Start here:

1. [Repository Architecture](Repository-Architecture)
2. [Evaluation Workflow](Evaluation-Workflow)
3. [Maintainer Guide](Maintainer-Guide)
4. [Roadmap and Open Questions](Roadmap-and-Open-Questions)

## Core Concepts at a Glance

- **Runtime package**: the files Claude should actually consume at runtime
- **Workbench**: maintainer-only tooling for evaluation, comparison, and review
- **Response contract**: lead with judgment, surface practical signals, show boundaries, end with one next step
- **Evaluation goal**: improve groundedness, directionality, boundedness, and usefulness without drifting into pseudo-depth

Canonical docs:

- [Runtime package guide](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/README.md)
- [Workbench guide](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/README.md)
- [Skill definition](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/SKILL.md)
