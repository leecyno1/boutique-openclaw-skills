#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
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
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, output: str):
    with urllib.request.urlopen(url, timeout=120) as r:
        body = r.read()
    with open(output, "wb") as f:
        f.write(body)


def try_decode_data_uri(data_uri: str) -> bytes | None:
    m = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=]+)", data_uri)
    if not m:
        return None
    try:
        return base64.b64decode(m.group(1))
    except Exception:
        return None


def extract_markdown_image_url(text: str) -> str | None:
    m = re.search(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", text)
    if m:
        return m.group(1)
    m = re.search(r"(https?://\S+\.(?:png|jpg|jpeg|webp|gif))(?:\s|$)", text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def extract_chat_content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
                    continue
                image_url = item.get("image_url")
                if isinstance(image_url, str):
                    parts.append(image_url)
                    continue
                if isinstance(image_url, dict):
                    url = image_url.get("url")
                    if isinstance(url, str):
                        parts.append(url)
        return "\n".join(parts)
    if isinstance(content, dict):
        text = content.get("text")
        if isinstance(text, str):
            return text
    return ""


def extract_image_from_chat_response(data: dict, output: str) -> bool:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return False
    first = choices[0] if isinstance(choices[0], dict) else {}
    message = first.get("message") if isinstance(first, dict) else None
    if not isinstance(message, dict):
        return False

    content_text = extract_chat_content_text(message.get("content"))
    raw = try_decode_data_uri(content_text)
    if raw:
        with open(output, "wb") as f:
            f.write(raw)
        return True

    out_url = extract_markdown_image_url(content_text)
    if out_url:
        download(out_url, output)
        return True

    for key in ("image_url", "url"):
        value = message.get(key)
        if isinstance(value, str) and value.startswith("http"):
            download(value, output)
            return True

    images = message.get("images")
    if isinstance(images, list) and images:
        first_image = images[0] if isinstance(images[0], dict) else {}
        out_url = first_image.get("url")
        b64 = first_image.get("b64_json")
        if isinstance(b64, str):
            raw = base64.b64decode(b64)
            with open(output, "wb") as f:
                f.write(raw)
            return True
        if isinstance(out_url, str) and out_url.startswith("http"):
            download(out_url, output)
            return True

    return False


def extract_image_from_images_response(data: dict, output: str) -> bool:
    items = data.get("data") if isinstance(data, dict) else None
    if not items or not isinstance(items, list):
        return False

    first = items[0] if items else {}
    b64 = first.get("b64_json") if isinstance(first, dict) else None
    out_url = first.get("url") if isinstance(first, dict) else None
    if isinstance(b64, str):
        raw = base64.b64decode(b64)
        with open(output, "wb") as f:
            f.write(raw)
        return True
    if isinstance(out_url, str):
        download(out_url, output)
        return True
    return False


def main():
    p = argparse.ArgumentParser(description="Generate image via Gemini-compatible endpoint")
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--size", default="1024x1024")
    p.add_argument("--endpoint", default="")
    args = p.parse_args()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    base_url = (os.getenv("GEMINI_BASE_URL") or os.getenv("GOOGLE_BASE_URL") or "").rstrip("/")
    model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image-preview")
    endpoint = (
        args.endpoint.strip()
        or os.getenv("GEMINI_IMAGE_ENDPOINT", "").strip()
        or "/v1/images/generations"
    )

    if not base_url:
        fail("GEMINI_BASE_URL 未设置")

    url = f"{base_url}{endpoint}"
    if "/chat/completions" in endpoint:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": args.prompt}],
            "stream": False,
        }
    else:
        payload = {
            "model": model,
            "prompt": args.prompt,
            "size": args.size,
        }

    data = http_json(url, payload, api_key)
    ok = False
    if "/chat/completions" in endpoint:
        ok = extract_image_from_chat_response(data if isinstance(data, dict) else {}, args.output)
    if not ok:
        ok = extract_image_from_images_response(data if isinstance(data, dict) else {}, args.output)
    if not ok:
        fail(f"未找到可用图片数据: {json.dumps(data, ensure_ascii=False)[:800]}")

    print(args.output)


if __name__ == "__main__":
    main()
