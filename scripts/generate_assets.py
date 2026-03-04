#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_logo_png():
    w, h = 1200, 420
    img = Image.new("RGB", (w, h), "#0f172a")
    d = ImageDraw.Draw(img)

    # background bands
    d.rectangle((0, 0, w, h), fill="#0b1020")
    d.rectangle((0, h - 90, w, h), fill="#111827")

    # icon box
    d.rounded_rectangle((60, 70, 290, 300), radius=36, fill="#f8fafc")
    d.rectangle((95, 105, 255, 135), fill="#dc2626")
    d.rectangle((95, 160, 255, 190), fill="#0f172a")
    d.rectangle((95, 215, 255, 245), fill="#0f172a")

    # title
    d.text((340, 95), "boutique-openclaw-skills", font=font(54), fill="#f8fafc")
    d.text((344, 176), "ONE CAPABILITY  •  ONE SKILL", font=font(30), fill="#f87171")
    d.text((344, 236), "精选店模式 / 稳定优先 / 定期审计", font=font(28), fill="#cbd5e1")

    img.save(ASSETS / "logo.png", format="PNG")


def draw_hero_png():
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#0b1220")
    d = ImageDraw.Draw(img)

    # subtle gradient stripes
    for i in range(0, h, 3):
        c = int(18 + (i / h) * 20)
        d.line((0, i, w, i), fill=(c, c + 5, c + 12))

    # cards
    cards = [
        (120, 180, 420, 360, "Core", "基础能力基线"),
        (470, 180, 770, 360, "Finance", "金融研究与报告"),
        (820, 180, 1120, 360, "SaaS", "研发与运维"),
        (1170, 180, 1470, 360, "Growth", "营销增长"),
    ]
    for x1, y1, x2, y2, t, s in cards:
        d.rounded_rectangle((x1, y1, x2, y2), radius=20, fill="#f8fafc")
        d.rectangle((x1, y1, x2, y1 + 14), fill="#dc2626")
        d.text((x1 + 22, y1 + 42), t, font=font(36), fill="#111827")
        d.text((x1 + 22, y1 + 98), s, font=font(24), fill="#334155")

    d.text((120, 66), "Boutique OpenClaw Skills", font=font(72), fill="#f8fafc")
    d.text((120, 760), "精选而非堆叠：去重、审计、可维护", font=font(42), fill="#fca5a5")

    img.save(ASSETS / "hero.png", format="PNG")


def draw_logo_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420">
  <rect width="1200" height="420" fill="#0b1020"/>
  <rect x="0" y="330" width="1200" height="90" fill="#111827"/>
  <rect x="60" y="70" width="230" height="230" rx="36" fill="#f8fafc"/>
  <rect x="95" y="105" width="160" height="30" fill="#dc2626"/>
  <rect x="95" y="160" width="160" height="30" fill="#0f172a"/>
  <rect x="95" y="215" width="160" height="30" fill="#0f172a"/>
  <text x="340" y="150" fill="#f8fafc" font-size="54" font-family="Arial, Helvetica, sans-serif">boutique-openclaw-skills</text>
  <text x="344" y="205" fill="#f87171" font-size="30" font-family="Arial, Helvetica, sans-serif">ONE CAPABILITY • ONE SKILL</text>
  <text x="344" y="255" fill="#cbd5e1" font-size="28" font-family="Arial, Helvetica, sans-serif">精选店模式 / 稳定优先 / 定期审计</text>
</svg>
'''
    (ASSETS / "logo.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    draw_logo_png()
    draw_hero_png()
    draw_logo_svg()
    print("generated assets:")
    print(ASSETS / "logo.png")
    print(ASSETS / "hero.png")
    print(ASSETS / "logo.svg")
