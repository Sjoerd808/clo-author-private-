# Copilot Instructions for clo-author

This repository was originally designed for Claude Code. Use these rules to run it effectively with Copilot CLI.

## Session defaults

- Read `README.md` and `CLAUDE.md` at the start of substantive tasks.
- Treat `CLAUDE.md` as the project constitution.
- Keep paper as the source of truth: `paper/main.tex`.
- Prefer minimal, surgical edits and preserve existing folder conventions.

## Planning and execution

- Plan first for non-trivial tasks; do not skip straight to broad refactors.
- Keep outputs in canonical locations:
  - Figures: `paper/figures/`
  - Tables: `paper/tables/`
  - Reports: `quality_reports/`
  - Analysis scripts: `scripts/`
- Do not edit generated artifacts unless explicitly asked.

## Validation workflow

- Before and after meaningful changes, run repository checks:
  - `make validate`
- For reporting utilities:
  - `make dashboard`
  - `make report-peer-review`
  - `make report-code-audit`
  - `make report-strategy-review`
  - `make report-quality-gate`
  - `make report-literature`

## Hooks and orchestration

- Reuse existing guard hooks from `.claude/hooks/` when needed:
  - `session-guard.py`
  - `protect-files.sh`
  - `post-edit-lint.sh`
- Use `make copilot-pre-edit` before risky edits and `make copilot-post-edit` after edits.
- Keep orchestration explicit in task updates: discovery -> strategy -> execution -> review -> submission.

## External skill provider mode

- For cross-repo invocation, use `scripts/skill_provider.py` via Make targets:
  - `make skill-partial TARGET_REPO=/abs/path CAPABILITY=dashboard`
  - `make skill-bundle TARGET_REPO=/abs/path BUNDLE=execution CONTRACT=/abs/path/provider-contract.json`
  - `make skill-full TARGET_REPO=/abs/path CONTRACT=/abs/path/provider-contract.json`
- Read `SKILL_PROVIDER.md` for the full contract and version-pinning workflow.

## Safety

- Never commit secrets.
- Never delete or overwrite raw data in `data/raw/`.
- Ask before destructive operations or major architecture changes.
