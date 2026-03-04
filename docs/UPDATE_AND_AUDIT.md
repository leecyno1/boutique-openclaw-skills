# Upstream Update and Security Audit

## Manual run

```bash
./scripts/sync-upstream.sh
```

This does:
1. Iterate all curated skills.
2. Pull latest upstream from ClawHub (`clawhub update <skill>`).
3. Run local audit (`scripts/audit_skills.py`).
4. Write reports to `reports/`.

## Scheduled run (GitHub Actions)

Workflow: `.github/workflows/sync-audit.yml`

- Weekly cron update.
- Manual trigger supported.
- Uploads audit artifacts.

## Release bundle

```bash
./scripts/build-bundle.sh
```

Output is generated under `dist/`.

## Risk gates

Audit is **FAIL** when:
- duplicate capabilities detected,
- high-risk patterns found in curated skill code.

Audit is **WARN** when:
- required env vars are missing,
- some curated skills are not installed locally.
