# Curation Policy

Boutique mode means **one capability = one skill**.

## Rules

1. No overlapping skills for the same capability in `catalog/skills.json`.
2. Every skill must include:
   - explicit capability id
   - risk tier (`low|medium|high`)
   - dependency/env requirements
   - reason for selection
3. Prefer stable, actively maintained skills over novelty.
4. Additive changes must pass:
   - profile resolution check
   - audit script (`scripts/audit_skills.py`)
5. Removal is allowed if:
   - upstream abandoned,
   - repeated audit risk,
   - clearly superseded by a stronger single option.

## Why this policy exists

- Prevent token waste from redundant tools.
- Reduce tool-selection ambiguity in multi-skill agents.
- Keep version management deterministic.
- Keep incident response simple during breakages.
