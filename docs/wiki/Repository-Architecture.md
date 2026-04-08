# Repository Architecture

This page explains how the repository is split between the public runtime package and the maintainer workbench.

Canonical sources:

- [Repository README](https://github.com/August1314/Michael-Polanyi/blob/main/README.md)
- [Runtime package guide](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/README.md)
- [Workbench guide](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/README.md)

## Runtime Package

The runtime package lives under:

- [`skills/michael-polanyi/`](https://github.com/August1314/Michael-Polanyi/tree/main/skills/michael-polanyi)

This is the part Claude should load at runtime. It contains:

- `SKILL.md`
- `examples.md`
- `polanyi-notes.md`
- `references/`
- `scripts/detect_fluff.py`

Think of this layer as the public, installable skill surface.

## Maintainer Workbench

The workbench lives under:

- [`workbench/`](https://github.com/August1314/Michael-Polanyi/tree/main/workbench)

This is maintainer-only infrastructure. It contains:

- eval prompt sets and scoring guidance
- blind comparison and grading prompts
- assertion and benchmark helpers
- the HTML review generator

Think of this layer as the internal iteration surface, not part of the installed package.

## Documentation Layers

The repository now has three documentation roles:

- [`README.md`](https://github.com/August1314/Michael-Polanyi/blob/main/README.md): public overview, install, usage, quick verification
- [`skills/michael-polanyi/README.md`](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/README.md): runtime package guide
- [`workbench/README.md`](https://github.com/August1314/Michael-Polanyi/blob/main/workbench/README.md): maintainer workflow guide

The wiki sits above these as a reader-oriented documentation layer.

## What Belongs Where

Use this rule of thumb:

- if Claude should read it at runtime, it belongs in the runtime package
- if maintainers use it to measure, compare, or review changes, it belongs in the workbench

Examples:

- example answer shape → runtime package
- eval rubric → workbench
- trigger contract → runtime package
- blind comparison prompt → workbench

If you want the operational side of this split, continue to [Maintainer Guide](Maintainer-Guide).
