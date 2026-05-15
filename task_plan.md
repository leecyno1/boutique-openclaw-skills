# Boutique Skills Repository Migration Plan

## Goal
Move default OpenClaw skills ownership from `OpenClawInstaller` into `boutique-openclaw-skills`, split skills into low / medium / high tiers, and make the installer treat this repo as the skills source of truth.

## Phases
- [completed] Phase 1: Inspect installer and boutique skill structures.
- [completed] Phase 2: Add boutique tier catalog tests.
- [completed] Phase 3: Import installer default skills into boutique.
- [completed] Phase 4: Generate tier docs, manuals, and source links.
- [completed] Phase 5: Update installer sync scripts/docs to use boutique.
- [completed] Phase 6: Run targeted validations in both repos.

## Constraints
- Do not delete installer skills until sync path and tests are updated.
- Keep installer focused on installer, website, registry, and tests.
- Boutique owns skill curation and default skill docs going forward.
- Preserve existing dirty work in OpenClawInstaller; do not revert unrelated changes.

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|

## Validation

- `python3 -m unittest discover -s tests` passed.
- `./scripts/install-tier.sh high --dry-run` passed.
- `./scripts/build-bundle.sh` includes `tiers/`, `skills/`, and generated manuals.

## Final Validation

- Boutique README/docs regenerated for default-tier-first messaging.
- `python3 -m unittest discover -s tests` passed.
- `./scripts/install-tier.sh high --dry-run` passed.
- OpenClawInstaller `./scripts/release-check.sh` passed after installer slim-down.
