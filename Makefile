.PHONY: audit sync enrich upstream-check upstream-apply install-standard bundle assets

audit:
	python3 scripts/audit_skills.py

sync:
	./scripts/sync-upstream.sh

enrich:
	python3 scripts/generate_enriched_catalog.py

upstream-check:
	python3 scripts/check_upstream_updates.py

upstream-apply:
	python3 scripts/check_upstream_updates.py --apply

install-standard:
	./scripts/install-standard-bundle.sh --dry-run

bundle:
	./scripts/build-bundle.sh

assets:
	python3 scripts/generate_assets.py
