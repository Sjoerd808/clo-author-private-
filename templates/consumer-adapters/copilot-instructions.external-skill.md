# External Skill Provider Adapter (Copilot CLI)

Use `clo-author` as an external provider from this repository.

## Provider source

- Local path: `/ABS/PATH/TO/clo-author-private-`
- Entrypoint: `scripts/skill_provider.py`
- Interface: `partial`, `bundle`, `full`

## Invocation policy

- Use `partial` for one capability (single report or dashboard).
- Use `bundle` for phase-level grouped work.
- Use `full` only when a complete end-to-end pass is requested.

## Allowed provider capabilities

- `dashboard`
- `literature`
- `strategy-review`
- `code-audit`
- `quality-gate`
- `peer-review`

## Command patterns

- Partial:
  - `make -C /ABS/PATH/TO/clo-author-private- skill-partial TARGET_REPO=/ABS/PATH/TO/THIS_REPO CAPABILITY=dashboard`
- Bundle:
  - `make -C /ABS/PATH/TO/clo-author-private- skill-bundle TARGET_REPO=/ABS/PATH/TO/THIS_REPO BUNDLE=execution CONTRACT=/ABS/PATH/TO/THIS_REPO/provider-contract.json`
- Full:
  - `make -C /ABS/PATH/TO/clo-author-private- skill-full TARGET_REPO=/ABS/PATH/TO/THIS_REPO CONTRACT=/ABS/PATH/TO/THIS_REPO/provider-contract.json`

## Safety

- Always pass absolute `TARGET_REPO`.
- Keep provider outputs inside this repo only.
- Validate after provider run:
  - verify `quality_reports/provider/provider_run_manifest.json`
  - verify expected `quality_reports/reviews/provider_*.html`
