#!/usr/bin/env python3
"""Check whether official policy source homepages are reachable."""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "references" / "official-sources.md"


def main() -> int:
    text = SOURCES.read_text(encoding="utf-8")
    urls = sorted(set(re.findall(r"https://[^\s|]+", text)))
    ok = 0
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "policy-monitor/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = getattr(resp, "status", 0)
            result = "OK" if 200 <= status < 400 else f"HTTP {status}"
            if result == "OK":
                ok += 1
        except Exception as exc:  # noqa: BLE001
            result = f"ERR {type(exc).__name__}"
        print(f"{result}\t{url}")
    print(f"reachable={ok}/{len(urls)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
