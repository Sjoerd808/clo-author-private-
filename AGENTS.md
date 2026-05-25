# Codex Instructions for Clo-Author

This repository is a domain-specific research harness for empirical economics. It was originally designed for Claude Code, but Codex should treat it as an agentic research scaffold with explicit planning, verification, quality gates, and human review.

## First files to read

For any substantive task, read these files before editing:

1. `README.md` - public overview, command surface, and project structure.
2. `CODEX.md` - Codex-specific operating guide.
3. `CLAUDE.md` - project constitution and research workflow contract.
4. `.github/copilot-instructions.md` - parallel instructions for Copilot; useful compatibility reference.
5. `SKILL_PROVIDER.md` - only when using this repository as an external provider for another repository.

## Core operating model

Use the same phase flow throughout:

`discovery -> strategy -> execution -> review -> submission`

For non-trivial tasks:

- Plan first; do not begin broad edits without a clear plan.
- Make small, auditable changes.
- Preserve the research paper as the source of truth: `paper/main.tex`.
- Keep outputs in canonical folders.
- Verify after meaningful edits.
- Report what was changed, what was tested, and what remains uncertain.

## Preferred command entrypoints

Use these Make targets rather than calling scripts directly unless debugging a script:

```bash
make validate
make codex-pre-edit
make codex-post-edit
make dashboard
make skill-health TARGET_REPO=/absolute/path/to/consumer-repo
make skill-partial TARGET_REPO=/absolute/path/to/consumer-repo CAPABILITY=dashboard
make skill-bundle TARGET_REPO=/absolute/path/to/consumer-repo BUNDLE=execution CONTRACT=/absolute/path/to/consumer-repo/provider-contract.json
make skill-full TARGET_REPO=/absolute/path/to/consumer-repo CONTRACT=/absolute/path/to/consumer-repo/provider-contract.json
```

If `codex-pre-edit` or `codex-post-edit` is unavailable in an older checkout, use `copilot-pre-edit` and `copilot-post-edit`; they call the same guard hooks.

## Safety and data rules

- Never commit secrets, tokens, local credentials, API keys, private data, or raw restricted datasets.
- Never delete, overwrite, or normalize `data/raw/` unless the user explicitly asks and the change is reversible.
- Do not edit generated artifacts unless explicitly asked; edit the source instead.
- Do not make destructive shell changes without first explaining the impact.
- If validation fails, preserve the failure output and explain whether the failure was introduced by the current change.

## Research-output conventions

- Figures: `paper/figures/`
- Tables: `paper/tables/`
- Analysis scripts: `scripts/`
- Reviews, plans, scores, logs: `quality_reports/`
- Exploratory material: `explorations/`
- Replication material: `paper/replication/`

## Quality gates

Respect the harness thresholds:

- 80/100: commit allowed.
- 90/100: PR allowed.
- 95/100 and all components >= 80: submission allowed.

Critics review; creators edit. Do not let a creator score its own work.

## External provider mode

When this repository is used from another repository:

- Always pass an absolute `TARGET_REPO`.
- Keep all generated outputs in the consumer repository's canonical folders.
- Use contract file mappings for bundle and full runs.
- Prefer dry-run/health checks before modifying a consumer repository.

## Final response checklist

When finishing a Codex task, summarize:

1. Files changed.
2. Commands run.
3. Test/validation result.
4. Any limitations, skipped checks, or follow-up risks.
