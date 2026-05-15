#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def http_json(url: str, payload: dict, api_key: str):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, output: str):
    with urllib.request.urlopen(url, timeout=180) as r:
        body = r.read()
    with open(output, "wb") as f:
        f.write(body)


def main():
    p = argparse.ArgumentParser(description="Generate video via grok-imagine-1.0-video endpoint")
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--endpoint", default="/v1/videos/generations")
    args = p.parse_args()

    api_key = os.getenv("GROK_IMAGINE_API_KEY", "")
    base_url = os.getenv("GROK_IMAGINE_BASE_URL", "").rstrip("/")
    model = os.getenv("GROK_IMAGINE_MODEL", "grok-imagine-1.0-video")

    if not base_url:
        fail("GROK_IMAGINE_BASE_URL 未设置")

    url = f"{base_url}{args.endpoint}"
    payload = {"model": model, "prompt": args.prompt}
    data = http_json(url, payload, api_key)

    out_url = None
    if isinstance(data, dict):
        if isinstance(data.get("data"), list) and data["data"]:
            first = data["data"][0]
            if isinstance(first, dict):
                out_url = first.get("url") or first.get("video_url")
        out_url = out_url or data.get("url") or data.get("video_url") or data.get("output_url")

    if not out_url:
        fail(f"未解析到视频下载地址，可能需要异步轮询: {json.dumps(data, ensure_ascii=False)[:500]}")

    download(str(out_url), args.output)
    print(args.output)


if __name__ == "__main__":
    main()
