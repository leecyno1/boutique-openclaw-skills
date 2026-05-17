# Findings

- `skills/default` contains 318 skill directories.
- `catalog/default-skills.json` has 320 tier entries but only 179 unique skill IDs because low/medium/high are cumulative.
- Every default catalog entry currently has `source` pointing to `leecyno1/auto-install-Openclaw`, which is a mirror/copy path rather than native upstream.
- `README.md` claims original repository links are included, but current default catalog does not provide them.
- Existing workflow runs weekly; requirement is monthly review.
