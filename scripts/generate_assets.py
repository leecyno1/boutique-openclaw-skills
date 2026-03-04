#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)


def pick_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates += [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        ]
    candidates += [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
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


def draw_pixels(draw: ImageDraw.ImageDraw, ox: int, oy: int, scale: int, cells, color: str):
    for x, y in cells:
        draw.rectangle(
            (ox + x * scale, oy + y * scale, ox + (x + 1) * scale - 1, oy + (y + 1) * scale - 1),
            fill=color,
        )


def boutique_shop_cells():
    cells = {}
    frame = []
    for x in range(2, 18):
        frame += [(x, 5), (x, 16)]
    for y in range(6, 16):
        frame += [(2, y), (17, y)]
    cells["#f8fafc"] = frame
    roof = [(x, 4) for x in range(1, 19)] + [(x, 3) for x in range(3, 17)]
    cells["#ef4444"] = roof
    door = [(9, y) for y in range(11, 16)] + [(10, y) for y in range(11, 16)]
    cells["#0f172a"] = door
    sign = [(6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7)]
    cells["#fde047"] = sign
    win = [(4, 9), (5, 9), (4, 10), (5, 10), (14, 9), (15, 9), (14, 10), (15, 10)]
    cells["#38bdf8"] = win
    return cells


def lobster_cells():
    cells = {}
    red = []
    for x in range(8, 24):
        for y in range(8, 19):
            if not ((x in {8, 23}) and y in {8, 18}):
                red.append((x, y))
    red += [(4, 9), (5, 8), (6, 7), (7, 7), (5, 10), (4, 11), (6, 12), (7, 12)]
    red += [(24, 10), (25, 11), (26, 12), (24, 16), (25, 15), (26, 14)]
    red += [(10, 19), (12, 20), (14, 19), (16, 20), (18, 19), (20, 20)]
    red += [(9, 7), (8, 6), (7, 5), (6, 4), (10, 7), (11, 6), (12, 5), (13, 4)]
    cells["#dc2626"] = red
    cells["#7f1d1d"] = [(12, 11), (13, 12), (14, 13), (18, 12), (19, 13), (20, 14)]
    cells["#fca5a5"] = [(14, 10), (15, 10), (16, 10), (17, 10), (15, 15), (16, 15)]
    return cells


def draw_logo():
    w, h = 1600, 520
    img = Image.new("RGB", (w, h), "#0b1020")
    d = ImageDraw.Draw(img)

    # smooth background, no checker/grids
    for y in range(h):
        r = 10 + int((y / h) * 14)
        g = 14 + int((y / h) * 9)
        b = 26 + int((y / h) * 12)
        d.line((0, y, w, y), fill=(r, g, b))

    # pixel boutique icon (small, lightweight)
    s1 = 7
    for color, pts in boutique_shop_cells().items():
        draw_pixels(d, 80, 150, s1, pts, color)

    # pixel lobster (small-medium, not giant blocks)
    s2 = 7
    for color, pts in lobster_cells().items():
        draw_pixels(d, 1220, 120, s2, pts, color)

    d.text((320, 126), "BOUTIQUE OPENCLAW SKILLS", font=pick_font(58, bold=True), fill="#f8fafc")
    d.text((322, 202), "精选店模式  |  一功能一技能  |  稳定优先", font=pick_font(38, bold=True), fill="#f87171")
    d.text((322, 262), "NO DUPLICATE SKILLS · LOW TOKEN WASTE · AUDITED WEEKLY", font=pick_font(30), fill="#cbd5e1")
    d.text((322, 318), "Pixel Theme: Boutique Store + Lobster", font=pick_font(28), fill="#fde68a")

    d.line((320, 360, 1110, 360), fill="#334155", width=2)
    d.text((320, 388), "github.com/leecyno1/boutique-openclaw-skills", font=pick_font(27), fill="#93c5fd")

    img.save(ASSETS / "logo.png", "PNG")


def draw_hero():
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#0b1220")
    d = ImageDraw.Draw(img)

    # clean gradient only
    for y in range(h):
        r = 9 + int((y / h) * 20)
        g = 17 + int((y / h) * 13)
        b = 30 + int((y / h) * 15)
        d.line((0, y, w, y), fill=(r, g, b))

    d.text((90, 92), "Boutique Mode 宣传图", font=pick_font(74, bold=True), fill="#f8fafc")
    d.text((90, 194), "精选，不堆叠", font=pick_font(66, bold=True), fill="#f87171")
    d.text((90, 276), "每个功能只保留一个最优 skills", font=pick_font(48, bold=True), fill="#e2e8f0")

    bullets = [
        "减少 token 消耗：避免重复工具评估链路",
        "减少版本冲突：能力唯一映射，变更可追踪",
        "降低运维复杂度：周更 + 审计 + 报告",
        "行业化安装：按 profile 一键部署",
    ]
    y = 420
    for b in bullets:
        d.text((126, y), "• " + b, font=pick_font(40), fill="#cbd5e1")
        y += 84

    d.text((90, 804), "把复杂度放在编排层，而不是对话层。", font=pick_font(44, bold=True), fill="#fde68a")
    img.save(ASSETS / "hero.png", "PNG")


def draw_quick_nav():
    w, h = 1600, 840
    img = Image.new("RGB", (w, h), "#f8fafc")
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, w, 110), fill="#0f172a")
    d.text((48, 28), "Repository Quick Navigation", font=pick_font(54, bold=True), fill="#f8fafc")

    items = [
        "README: 项目总览与安装入口",
        "catalog/skills.json: 一功能一技能映射",
        "profiles/: 行业安装档",
        "scripts/install-profile.sh: 按行业一键安装",
        "scripts/sync-upstream.sh: 上游同步 + 审计",
        "scripts/audit_skills.py: 风险扫描与依赖检查",
        ".github/workflows/sync-audit.yml: 定时更新流水线",
        "docs/: 策略、SOP、视觉说明",
    ]

    y = 170
    for i, line in enumerate(items, start=1):
        d.text((70, y), f"{i:02d}. {line}", font=pick_font(38), fill="#1e293b")
        d.line((66, y + 54, 1540, y + 54), fill="#e2e8f0", width=2)
        y += 78

    d.text((66, 780), "精品店模式：去重、可维护、可审计、可复制。", font=pick_font(36, bold=True), fill="#dc2626")
    img.save(ASSETS / "profiles.png", "PNG")


def draw_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b1020"/>
      <stop offset="100%" stop-color="#1a2235"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="520" fill="url(#bg)"/>
  <text x="320" y="160" fill="#f8fafc" font-size="58" font-family="Arial, Helvetica, sans-serif">BOUTIQUE OPENCLAW SKILLS</text>
  <text x="322" y="220" fill="#f87171" font-size="38" font-family="Arial, Helvetica, sans-serif">精选店模式 | 一功能一技能 | 稳定优先</text>
  <text x="322" y="276" fill="#cbd5e1" font-size="30" font-family="Arial, Helvetica, sans-serif">NO DUPLICATE SKILLS · LOW TOKEN WASTE · AUDITED WEEKLY</text>
  <text x="322" y="330" fill="#fde68a" font-size="28" font-family="Arial, Helvetica, sans-serif">Pixel Theme: Boutique Store + Lobster</text>
</svg>
'''
    (ASSETS / "logo.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    draw_logo()
    draw_hero()
    draw_quick_nav()
    draw_svg()
    print("generated:")
    for name in ["logo.png", "hero.png", "profiles.png", "logo.svg"]:
        print(ASSETS / name)
