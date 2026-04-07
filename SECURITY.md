# Security Policy

## Scope

This repository contains prompt-engineering and skill-design artifacts.
It does not provide runtime isolation, sandboxing, or security guarantees by itself.

## What to report

Please report issues such as:

- prompts or examples that encourage unsafe, misleading, or overconfident advice
- prompt patterns that drift into pseudo-depth while hiding uncertainty or lack of evidence
- installation or compatibility issues that could cause users to think the skill is active when it is not
- content that creates confusion about the project's limits, claims, or intended use

## What is out of scope

The following are generally out of scope for this repository:

- security vulnerabilities in Claude Code, Codex, or other external clients
- operating system, shell, or package-manager vulnerabilities
- issues caused by third-party integrations outside this repository

## Reporting

Please open a private report if possible, or create a repository issue with enough detail to reproduce the problem safely.

Include:

- the prompt or scenario
- the observed output
- the expected safer behavior
- any relevant client/version information
