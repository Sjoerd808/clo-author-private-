# CODEX.md

Operational guide for running Clo-Author with OpenAI Codex.

This repository is not a generic software project. It is an orchestration harness for empirical research workflows with structured review, validation, and reporting.

## Mental model

Treat the repository as:

- a research operating system,
- an agent workflow harness,
- and a reproducible paper-production scaffold.

The workflow is phase-oriented:

1. Discovery
2. Strategy
3. Execution
4. Review
5. Submission

Do not skip directly to implementation for large tasks.

---

## Mandatory startup routine

Before meaningful work:

```bash
make validate
```

Read:

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

For provider-mode work, also read:

- `SKILL_PROVIDER.md`

---

## Editing philosophy

Prefer:

- minimal diffs,
- localized edits,
- preserving structure,
- reproducibility,
- explicit validation.

Avoid:

- broad refactors without justification,
- silent behavioral changes,
- moving canonical outputs,
- editing generated artifacts directly.

---

## Canonical structure

| Purpose | Location |
|---|---|
| Paper source | `paper/main.tex` |
| Figures | `paper/figures/` |
| Tables | `paper/tables/` |
| Scripts | `scripts/` |
| Reviews and plans | `quality_reports/` |
| Exploration sandbox | `explorations/` |
| Replication package | `paper/replication/` |

---

## Recommended workflow for Codex

### Before risky edits

```bash
make codex-pre-edit
```

### After edits

```bash
make codex-post-edit
```

### Validation

```bash
make validate
```

### Generate project dashboard

```bash
make dashboard
```

---

## Review model

The repository assumes worker/critic separation.

Interpretation for Codex:

- generation and evaluation should be logically separated,
- self-grading should be avoided when possible,
- review outputs should explain reasoning,
- uncertainty should be surfaced explicitly.

---

## Safety constraints

Never:

- overwrite raw datasets,
- commit secrets,
- delete project structure casually,
- fabricate empirical results,
- claim validation that was not actually run.

If tests or validation were skipped, state that clearly.

---

## Provider mode

This repository can act as a reusable provider for another repository.

Health check:

```bash
make skill-health TARGET_REPO=/absolute/path/to/consumer-repo
```

Partial capability:

```bash
make skill-partial TARGET_REPO=/absolute/path/to/consumer-repo CAPABILITY=dashboard
```

Bundle execution:

```bash
make skill-bundle TARGET_REPO=/absolute/path/to/consumer-repo BUNDLE=execution CONTRACT=/absolute/path/to/consumer-repo/provider-contract.json
```

Full execution:

```bash
make skill-full TARGET_REPO=/absolute/path/to/consumer-repo CONTRACT=/absolute/path/to/consumer-repo/provider-contract.json
```

---

## Final-answer contract for Codex

For substantive tasks, end with:

1. What changed.
2. Which files changed.
3. Commands/tests run.
4. Validation outcome.
5. Remaining risks or assumptions.

Do not hide uncertainty.
