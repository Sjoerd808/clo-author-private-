# External Skill Provider Adapter (Codex CLI)

This repository delegates selected tasks to the external `clo-author` provider.

## Provider declaration

- Provider repo path: `/ABS/PATH/TO/clo-author-private-`
- Provider command: `python3 /ABS/PATH/TO/clo-author-private-/scripts/skill_provider.py`
- Supported modes: `partial`, `bundle`, `full`

## Dispatch rules

- `partial`: one capability only (`dashboard`, `literature`, `strategy-review`, `code-audit`, `quality-gate`, `peer-review`)
- `bundle`: grouped phase execution (`discovery`, `strategy`, `execution`, `review`)
- `full`: all capabilities in provider order

## Required arguments

- `--target-repo /ABS/PATH/TO/THIS_REPO`
- `--contract /ABS/PATH/TO/THIS_REPO/provider-contract.json` for bundle/full and most report runs

## Examples

- Partial dashboard:
  - `python3 /ABS/PATH/TO/clo-author-private-/scripts/skill_provider.py --target-repo /ABS/PATH/TO/THIS_REPO --mode partial --capability dashboard`
- Bundle execution:
  - `python3 /ABS/PATH/TO/clo-author-private-/scripts/skill_provider.py --target-repo /ABS/PATH/TO/THIS_REPO --mode bundle --bundle execution --contract /ABS/PATH/TO/THIS_REPO/provider-contract.json`
- Full:
  - `python3 /ABS/PATH/TO/clo-author-private-/scripts/skill_provider.py --target-repo /ABS/PATH/TO/THIS_REPO --mode full --contract /ABS/PATH/TO/THIS_REPO/provider-contract.json`

## Verification

- Confirm run manifest exists:
  - `quality_reports/provider/provider_run_manifest.json`
- Confirm expected outputs exist in:
  - `quality_reports/reviews/`
