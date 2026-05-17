.PHONY: audit sync enrich install-standard bundle assets

audit:
	python3 scripts/audit_skills.py

sync:
	./scripts/sync-upstream.sh

enrich:
	python3 scripts/generate_enriched_catalog.py

install-standard:
	./scripts/install-standard-bundle.sh --dry-run

bundle:
	./scripts/build-bundle.sh

assets:
	python3 scripts/generate_assets.py
