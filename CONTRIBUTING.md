# Contributing

## Add a new curated skill

1. Add one entry in `catalog/skills.json` with a **new capability id**.
2. Do not duplicate existing capabilities.
3. Add required env vars if needed.
4. Run audit:

```bash
python3 scripts/audit_skills.py
```

5. If profile changes are needed, edit `profiles/*.json`.

## Validation checklist

- [ ] one capability -> one skill
- [ ] no high-risk audit findings
- [ ] docs updated (README + profile notes)
