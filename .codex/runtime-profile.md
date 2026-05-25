# Codex Runtime Profile

This file defines the intended runtime behavior for Codex-like coding agents working in this repository.

It is intentionally tool-agnostic: use it as readable policy unless a future Codex release provides a stable machine-readable config format.

## Profile

Name: `clo-author-research-harness`

Primary mode: repository-grounded research engineering

Risk level: medium-high, because tasks may touch empirical claims, paper text, code, data, and submission artifacts.

## Default behavior

Codex should:

1. Read `AGENTS.md`, `CODEX.md`, `README.md`, and `CLAUDE.md` before substantive changes.
2. Preserve canonical project structure.
3. Prefer small diffs and explicit validation.
4. Treat `paper/main.tex` as the source of truth for paper content.
5. Use `quality_reports/` for plans, reviews, and audit outputs.
6. Avoid changing generated files unless explicitly requested.
7. Surface uncertainty instead of guessing.

## Session phases

Use this phase order for complex work:

1. Discovery - inspect files, constraints, and project state.
2. Strategy - decide approach and validation path.
3. Execution - edit only the needed files.
4. Review - inspect the diff and evaluate risks.
5. Submission - summarize changes and checks.

## Validation commands

Minimum validation:

```bash
make validate
```

Before risky edits:

```bash
make codex-pre-edit
```

After edits:

```bash
make codex-post-edit
```

Dashboard check:

```bash
make dashboard
```

## Human checkpoints

Ask for explicit human approval before:

- deleting data,
- rewriting large portions of the manuscript,
- changing quality thresholds,
- changing provider contracts,
- altering journal submission artifacts,
- replacing `.claude/` infrastructure wholesale.

## Escalation triggers

Escalate uncertainty when:

- empirical results cannot be reproduced,
- a generated claim lacks source support,
- validation fails for unclear reasons,
- multiple source-of-truth files conflict,
- the requested change would weaken safety or reproducibility.
