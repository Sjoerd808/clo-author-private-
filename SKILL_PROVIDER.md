# Skill Provider Interface

Use this repository as an external skill provider from other local repositories.

## Stable entrypoints

- `make skill-partial TARGET_REPO=/abs/path CAPABILITY=<capability> [CONTRACT=/abs/path/to/provider-contract.json] [INPUT=path]`
- `make skill-bundle TARGET_REPO=/abs/path BUNDLE=<bundle> [CONTRACT=/abs/path/to/provider-contract.json]`
- `make skill-full TARGET_REPO=/abs/path [CONTRACT=/abs/path/to/provider-contract.json]`

Capabilities:
- `dashboard`
- `literature`
- `strategy-review`
- `code-audit`
- `quality-gate`
- `peer-review`

Bundles:
- `discovery` -> `literature`
- `strategy` -> `strategy-review`
- `execution` -> `code-audit`, `quality-gate`
- `review` -> `peer-review`, `dashboard`

## Cross-repo contract

- `TARGET_REPO` must be an absolute path.
- `CONTRACT` must be an absolute path to a JSON file.
- Relative paths inside the contract are resolved against `TARGET_REPO`.
- Any path that escapes `TARGET_REPO` is rejected.

Example contract:
- `templates/consumer-adapters/provider-contract.example.json`

## Output contract

Provider writes only into the calling repository:

- `quality_reports/reviews/` (generated HTML reports)
- `quality_reports/provider/provider_run_manifest.json` (run metadata)
- ensures canonical directories exist:
  - `paper/figures/`
  - `paper/tables/`

The provider repository itself is not used as an output target.

## Version pinning

Recommended:
1. Add this repository to consumer repo as a pinned submodule.
2. Invoke via submodule path.
3. Upgrade intentionally by bumping submodule commit and reviewing `CHANGELOG.md`.

Alternative:
- Keep a local tagged clone and pin by explicit git commit.

## Upgrade workflow

1. Update provider repo once.
2. Validate provider:
   - `make validate`
   - `make dashboard`
3. In each consumer repo:
   - bump pinned provider reference
   - run compatibility checklist in `templates/consumer-adapters/compatibility-checklist.md`
   - review changelog impact
