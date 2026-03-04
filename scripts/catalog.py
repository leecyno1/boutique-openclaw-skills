#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = REPO_ROOT / "catalog" / "skills.json"
PROFILES_DIR = REPO_ROOT / "profiles"


def load_catalog() -> dict:
    with CATALOG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_profile(profile_id: str) -> dict:
    p = PROFILES_DIR / f"{profile_id}.json"
    if not p.exists():
        raise FileNotFoundError(f"Profile not found: {profile_id}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def index_by_capability(catalog: dict) -> Dict[str, dict]:
    index = {}
    for item in catalog.get("skills", []):
        cap = item["capability"]
        if cap in index:
            raise ValueError(f"Duplicate capability in catalog: {cap}")
        index[cap] = item
    return index


def resolve_profile_skills(profile_id: str) -> List[str]:
    catalog = load_catalog()
    profile = load_profile(profile_id)
    idx = index_by_capability(catalog)
    resolved = []
    for cap in profile.get("capabilities", []):
        if cap not in idx:
            raise KeyError(f"Profile {profile_id} references unknown capability: {cap}")
        resolved.append(idx[cap]["skill"])
    for extra in profile.get("extra_skills", []):
        if extra not in resolved:
            resolved.append(extra)
    return resolved


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Resolve boutique-openclaw-skills profiles")
    parser.add_argument("profile", help="Profile ID, e.g. core")
    args = parser.parse_args()

    for s in resolve_profile_skills(args.profile):
        print(s)


if __name__ == "__main__":
    main()
