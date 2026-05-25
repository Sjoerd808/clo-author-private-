# Codex CLI Instructions

For substantive tasks, read:

1. `README.md`
2. `CLAUDE.md`
3. `.github/copilot-instructions.md`
4. `SKILL_PROVIDER.md` (for cross-repo provider usage)

## Preferred command entrypoints

- `make validate`
- `make dashboard`
- `make skill-partial ...`
- `make skill-bundle ...`
- `make skill-full ...`

## Cross-repo provider constraints

- Always use absolute `TARGET_REPO`.
- Keep outputs in consumer repo canonical folders.
- Use contract file mappings for bundle/full runs.
