# External Provider Compatibility Checklist

Use this in each consumer repository before first production use and after provider upgrades.

- [ ] Provider path is pinned (submodule commit or explicit commit hash).
- [ ] `TARGET_REPO` uses an absolute path.
- [ ] `provider-contract.json` exists and maps required inputs.
- [ ] Dry-run health check passes:
  - `make -C /ABS/PATH/TO/clo-author-private- skill-health TARGET_REPO=/ABS/PATH/TO/THIS_REPO`
- [ ] Partial mode check passes (dashboard).
- [ ] Bundle mode check passes for at least one bundle used by this repo.
- [ ] Full mode check passes if full orchestration is used.
- [ ] Output paths are created only in this repo:
  - `quality_reports/reviews/provider_*.html`
  - `quality_reports/provider/provider_run_manifest.json`
- [ ] No provider output is written into provider repo.
- [ ] Changelog impact reviewed before pin update.
