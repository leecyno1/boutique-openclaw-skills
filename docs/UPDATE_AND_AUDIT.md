# Upstream Update and Security Audit

## Manual monthly review

```bash
./scripts/import_installer_default_skills.py --installer-root /path/to/OpenClawInstaller
./scripts/sync-upstream.sh  # compatibility-profile sync and local audit
python3 scripts/generate_enriched_catalog.py
```

This does:
1. Refresh local skill copies from the installer or upstream source.
2. Preserve installer URLs as mirror sources, not native origins.
3. Generate `catalog/skills.enriched.json` with native origin fields, horizontal tiers, vertical categories, dependency labels, risk, conflict groups, preset exclusions, and star ratings.
4. Generate `catalog/standard-bundle.json` with at most 30 non-duplicated recommended skills.
5. Regenerate `docs/generated/*.md` and the README index block.
6. Validate the standard bundle uniqueness rules and native-origin review count in local audit (`scripts/audit_skills.py`).
7. Write reports to `reports/`.

## Native origin policy

Every skill must eventually have a first-party `origin.origin_url` from one of these source types:

- GitHub original project or original skill directory.
- ClawHub / CL.Up skill listing.
- skills.h skill page.
- Official project website when the skill wraps a non-GitHub service.

Installer repositories, this repository, forks, and copied bundle paths are only `origin.mirror_source_url`. They do not count as native upstream. Skills without a verified or locally referenced native origin are marked `needs_origin_review: true` and cannot score above 2★.

## Scheduled run (GitHub Actions)

Workflow: `.github/workflows/sync-audit.yml`

- Monthly cron review on the 1st day of each month.
- Manual trigger supported.
- Uploads audit artifacts.
- Regenerates enriched catalog, generated indexes, standard bundle, and README index block.

## Release bundle

```bash
./scripts/build-bundle.sh
```

Output is generated under `dist/`.

## Standard bundle install

```bash
./scripts/install-standard-bundle.sh --dry-run
./scripts/install-standard-bundle.sh
```

The standard bundle is generated at `catalog/standard-bundle.json` and enforces at most 30 skills, one skill per capability, and one skill per conflict group.

## Risk gates

Audit is **FAIL** when:
- duplicate curated capabilities are detected,
- high-risk patterns are found in curated skill code.

Audit is **WARN** when:
- required env vars are missing,
- curated skills are not installed locally,
- skills are missing native origin URLs.

## Monthly reviewer checklist

- Confirm new or changed skills have a native `origin.origin_url`.
- Check whether Open or Hermes has added preset skills and update `catalog/presets/*.json`.
- Review `catalog/standard-bundle.json` for duplicate capability or conflict-group overlap.
- Update `catalog/native-origin-overrides.json` when first-party URLs are confirmed.
- Re-run `python3 scripts/generate_enriched_catalog.py` before committing README or generated index changes.
