.PHONY: audit sync bundle assets

audit:
	python3 scripts/audit_skills.py

sync:
	./scripts/sync-upstream.sh

bundle:
	./scripts/build-bundle.sh

assets:
	python3 scripts/generate_assets.py
