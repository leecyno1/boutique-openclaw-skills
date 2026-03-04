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
        draw.rectangle((ox + x * scale, oy + y * scale, ox + (x + 1) * scale - 1, oy + (y + 1) * scale - 1), fill=color)


def boutique_shop_cells():
    cells = {}
    # building frame
    frame = []
    for x in range(2, 18):
        frame += [(x, 4), (x, 15)]
    for y in range(5, 15):
        frame += [(2, y), (17, y)]
    cells["#f8fafc"] = frame

    # roof stripe
    roof = [(x, 3) for x in range(1, 19)] + [(x, 2) for x in range(3, 17)]
    cells["#ef4444"] = roof

    # door
    door = [(8, y) for y in range(10, 15)] + [(9, y) for y in range(10, 15)] + [(10, y) for y in range(10, 15)] + [(11, y) for y in range(10, 15)]
    cells["#0f172a"] = door

    # window + sign
    win = [(4, 8), (5, 8), (4, 9), (5, 9), (14, 8), (15, 8), (14, 9), (15, 9)]
    cells["#38bdf8"] = win
    sign = [(6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6)]
    cells["#fde047"] = sign
    return cells


def lobster_cells():
    cells = {}
    body = []
    # head + body
    for x in range(8, 20):
        for y in range(8, 18):
            if (x + y) % 7 != 0:
                body.append((x, y))
    # tail
    tail = [(20,10),(21,11),(22,12),(20,15),(21,14),(22,13)]
    # claws
    claws = [(4,7),(5,6),(6,5),(4,8),(5,9),(3,8),(2,9),(1,10),(6,10),(7,11),(8,12),(5,11)]
    # legs
    legs = [(9,18),(10,19),(11,18),(12,19),(13,18),(14,19),(15,18),(16,19),(17,18),(18,19)]
    # antenna
    antenna = [(8,7),(7,6),(6,5),(5,4),(4,3),(9,7),(10,6),(11,5),(12,4),(13,3)]

    cells["#dc2626"] = body + tail + claws + legs + antenna
    cells["#7f1d1d"] = [(9,9),(10,10),(11,11),(15,12),(16,13),(18,14),(19,15)]
    cells["#fca5a5"] = [(12,9),(13,9),(14,9),(15,9),(13,13),(14,13)]
    cells["#ffffff"] = [(10,8),(17,8)]
    cells["#111827"] = [(10,8),(17,8)]
    return cells


def draw_logo():
    w, h = 1600, 520
    img = Image.new("RGB", (w, h), "#0b1020")
    d = ImageDraw.Draw(img)

    # subtle stripes
    for y in range(0, h, 4):
        c = 12 + int((y / h) * 18)
        d.line((0, y, w, y), fill=(c, c + 4, c + 10))

    # pixel boutique shop
    scale = 12
    for color, pts in boutique_shop_cells().items():
        draw_pixels(d, 80, 120, scale, pts, color)

    # big lobster
    l_scale = 14
    for color, pts in lobster_cells().items():
        draw_pixels(d, 860, 95, l_scale, pts, color)

    d.text((360, 122), "BOUTIQUE OPENCLAW SKILLS", font=pick_font(58, bold=True), fill="#f8fafc")
    d.text((360, 200), "精选店模式  |  一功能一技能  |  稳定优先", font=pick_font(38, bold=True), fill="#f87171")
    d.text((360, 258), "NO DUPLICATE SKILLS  ·  NO TOKEN WASTE  ·  AUDITED WEEKLY", font=pick_font(30), fill="#cbd5e1")
    d.text((360, 320), "主题：精品店 + 大龙虾（像素风）", font=pick_font(30), fill="#fde68a")

    # footer line
    d.rectangle((0, 450, w, h), fill="#111827")
    d.text((48, 470), "github.com/leecyno1/boutique-openclaw-skills", font=pick_font(28), fill="#93c5fd")

    img.save(ASSETS / "logo.png", "PNG")


def draw_hero():
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#0b1220")
    d = ImageDraw.Draw(img)

    # gradient background
    for y in range(h):
        r = 8 + int((y / h) * 22)
        g = 16 + int((y / h) * 14)
        b = 28 + int((y / h) * 18)
        d.line((0, y, w, y), fill=(r, g, b))

    # promo text only, no boxes
    d.text((90, 80), "Boutique Mode 宣传图", font=pick_font(70, bold=True), fill="#f8fafc")
    d.text((90, 180), "只选一个最优技能，拒绝功能重叠", font=pick_font(56, bold=True), fill="#f87171")
    d.text((90, 260), "减少 token 消耗 · 降低工具冲突 · 简化版本管理", font=pick_font(44), fill="#cbd5e1")

    lines = [
        "• 统一目录：one capability -> one skill",
        "• 行业档：金融 / SaaS / 运营 / 咨询 / 创作者",
        "• 自动更新：weekly sync from upstream",
        "• 本地审计：风险模式、依赖缺失、能力冲突",
        "• 稳定导向：可维护、可追踪、可复现",
    ]
    y = 380
    for line in lines:
        d.text((110, y), line, font=pick_font(38), fill="#e2e8f0")
        y += 72

    d.text((90, 790), "少即是多：把复杂度放在编排层，而不是对话层。", font=pick_font(42, bold=True), fill="#fde68a")

    img.save(ASSETS / "hero.png", "PNG")


def draw_quick_nav():
    w, h = 1600, 820
    img = Image.new("RGB", (w, h), "#f8fafc")
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, w, 108), fill="#0f172a")
    d.text((48, 28), "Repository Quick Navigation", font=pick_font(54, bold=True), fill="#f8fafc")

    rows = [
        "README: 项目总览与安装入口",
        "catalog/skills.json: 精选目录（唯一能力映射）",
        "profiles/: 行业安装档",
        "scripts/install-profile.sh: 一键安装某行业档",
        "scripts/sync-upstream.sh: 上游更新 + 本地审计",
        "scripts/audit_skills.py: 风险扫描与依赖检查",
        ".github/workflows/sync-audit.yml: 定时更新流水线",
        "docs/CURATION_POLICY.md: 精选策略",
        "docs/UPDATE_AND_AUDIT.md: 运维SOP",
    ]

    y = 150
    for row in rows:
        d.text((60, y), f"- {row}", font=pick_font(38), fill="#1e293b")
        y += 68

    d.text((60, 740), "精品店模式：每个功能只保留一个 skill，减少混乱并提升可靠性。", font=pick_font(34, bold=True), fill="#dc2626")

    img.save(ASSETS / "profiles.png", "PNG")


def draw_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520">
  <rect width="1600" height="520" fill="#0b1020"/>
  <rect x="0" y="450" width="1600" height="70" fill="#111827"/>
  <text x="360" y="160" fill="#f8fafc" font-size="58" font-family="Arial, Helvetica, sans-serif">BOUTIQUE OPENCLAW SKILLS</text>
  <text x="360" y="220" fill="#f87171" font-size="38" font-family="Arial, Helvetica, sans-serif">精选店模式 | 一功能一技能 | 稳定优先</text>
  <text x="360" y="275" fill="#cbd5e1" font-size="30" font-family="Arial, Helvetica, sans-serif">NO DUPLICATE SKILLS · NO TOKEN WASTE · AUDITED WEEKLY</text>
  <text x="360" y="325" fill="#fde68a" font-size="30" font-family="Arial, Helvetica, sans-serif">像素风主题：精品店 + 大龙虾</text>
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
