# Installation and Compatibility

This page covers installation details separately from usage guidance.

Canonical sources:

- [Repository README](https://github.com/August1314/Michael-Polanyi/blob/main/README.md)
- [Runtime package guide](https://github.com/August1314/Michael-Polanyi/blob/main/skills/michael-polanyi/README.md)

## Supported Layouts

This repository follows the common file-based skill layout used by:

- Claude Code
- Codex-style agent setups

Technical slug:

- `michael-polanyi`

Public title:

- `Michael Polanyi`

## Claude Code Installation

```bash
mkdir -p ~/.claude/skills
cp -R skills/michael-polanyi ~/.claude/skills/
```

Expected runtime path:

- `~/.claude/skills/michael-polanyi/SKILL.md`

## Codex-Style Installation

```bash
mkdir -p ~/.agents/skills
cp -R skills/michael-polanyi ~/.agents/skills/
```

Expected runtime path:

- `~/.agents/skills/michael-polanyi/SKILL.md`

## Installed File Surface

The installed runtime package should look like this:

```text
michael-polanyi/
  SKILL.md
  examples.md
  polanyi-notes.md
  references/
  scripts/
```

The important boundary is that this surface is the **runtime package**. Maintainer-only tooling lives in the repository workbench and should not be treated as part of the installed skill.

## Common Installation Mistakes

- wrong directory name: it must be `michael-polanyi`
- `SKILL.md` not at the top level of the installed directory
- expecting maintainer workbench files to be part of the installed package
- forgetting to restart the client when skills are loaded only at startup

## Compatibility Notes

- Claude Code users should install under `~/.claude/skills/`
- Codex-style users should install under `~/.agents/skills/`
- In practice, explicit invocation is more reliable than blind auto-discovery

If you want the fastest functional check after install, continue to [Using the Skill](Using-the-Skill).
