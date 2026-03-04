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


def draw_store_icon(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    # Body
    draw.rounded_rectangle((x, y + 90, x + 220, y + 280), radius=22, fill="#f8fafc", outline="#cbd5e1", width=3)
    # Roof
    draw.rounded_rectangle((x - 6, y + 42, x + 226, y + 118), radius=18, fill="#ef4444")
    # Awning stripes
    for i in range(0, 8):
        sx1 = x + 6 + i * 26
        sx2 = sx1 + 13
        draw.rectangle((sx1, y + 52, sx2, y + 112), fill="#fee2e2")
    # Door
    draw.rounded_rectangle((x + 92, y + 170, x + 128, y + 280), radius=8, fill="#0f172a")
    # Windows
    draw.rounded_rectangle((x + 24, y + 164, x + 68, y + 206), radius=8, fill="#38bdf8")
    draw.rounded_rectangle((x + 152, y + 164, x + 196, y + 206), radius=8, fill="#38bdf8")
    # Shop label
    draw.rounded_rectangle((x + 56, y + 126, x + 164, y + 152), radius=8, fill="#fde047")


def draw_lobster_icon(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    red = "#dc2626"
    deep = "#7f1d1d"
    light = "#fca5a5"

    # Body + head
    draw.ellipse((x + 46, y + 66, x + 230, y + 224), fill=red)
    draw.ellipse((x + 18, y + 92, x + 88, y + 182), fill=red)

    # Tail fins
    draw.polygon([(x + 228, y + 122), (x + 286, y + 96), (x + 268, y + 152)], fill=red)
    draw.polygon([(x + 228, y + 166), (x + 286, y + 192), (x + 268, y + 136)], fill=red)

    # Claws
    draw.pieslice((x - 40, y + 54, x + 48, y + 142), 30, 290, fill=red)
    draw.pieslice((x - 38, y + 130, x + 52, y + 220), 70, 320, fill=red)

    # Legs
    for i in range(6):
        lx = x + 70 + i * 24
        draw.line((lx, y + 220, lx - 16, y + 262), fill=deep, width=5)

    # Antennae
    draw.arc((x - 10, y - 6, x + 146, y + 136), 190, 330, fill=deep, width=4)
    draw.arc((x + 10, y - 26, x + 188, y + 126), 198, 340, fill=deep, width=4)

    # Highlights
    draw.ellipse((x + 92, y + 102, x + 176, y + 150), fill=light)
    draw.ellipse((x + 108, y + 154, x + 170, y + 186), fill=light)


def draw_logo() -> None:
    w, h = 1600, 520
    img = Image.new("RGB", (w, h), "#0b1020")
    d = ImageDraw.Draw(img)

    # Smooth gradient background
    for yy in range(h):
        r = 10 + int((yy / h) * 14)
        g = 14 + int((yy / h) * 9)
        b = 26 + int((yy / h) * 12)
        d.line((0, yy, w, yy), fill=(r, g, b))

    draw_store_icon(d, 70, 72)
    draw_lobster_icon(d, 1190, 72)

    d.text((340, 110), "BOUTIQUE OPENCLAW SKILLS", font=pick_font(58, bold=True), fill="#f8fafc")
    d.text((342, 186), "精选店模式  |  一功能一技能  |  稳定优先", font=pick_font(38, bold=True), fill="#f87171")
    d.text((342, 248), "NO DUPLICATE SKILLS · LOW TOKEN WASTE · AUDITED WEEKLY", font=pick_font(30), fill="#cbd5e1")
    d.text((342, 304), "Theme: Boutique Store + Lobster", font=pick_font(28), fill="#fde68a")

    d.line((340, 350, 1110, 350), fill="#334155", width=2)
    d.text((340, 380), "github.com/leecyno1/boutique-openclaw-skills", font=pick_font(27), fill="#93c5fd")

    img.save(ASSETS / "logo.png", "PNG")


def draw_hero() -> None:
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), "#0b1220")
    d = ImageDraw.Draw(img)

    for yy in range(h):
        r = 9 + int((yy / h) * 20)
        g = 17 + int((yy / h) * 13)
        b = 30 + int((yy / h) * 15)
        d.line((0, yy, w, yy), fill=(r, g, b))

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
    for line in bullets:
        d.text((126, y), "• " + line, font=pick_font(40), fill="#cbd5e1")
        y += 84

    d.text((90, 804), "把复杂度放在编排层，而不是对话层。", font=pick_font(44, bold=True), fill="#fde68a")
    img.save(ASSETS / "hero.png", "PNG")


def draw_quick_nav() -> None:
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


def draw_svg() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="520" viewBox="0 0 1600 520">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b1020"/>
      <stop offset="100%" stop-color="#1a2235"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="520" fill="url(#bg)"/>
  <g transform="translate(70 72)">
    <rect x="0" y="90" width="220" height="190" rx="22" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
    <rect x="-6" y="42" width="232" height="76" rx="18" fill="#ef4444"/>
  </g>
  <text x="340" y="160" fill="#f8fafc" font-size="58" font-family="Arial, Helvetica, sans-serif">BOUTIQUE OPENCLAW SKILLS</text>
  <text x="342" y="220" fill="#f87171" font-size="38" font-family="Arial, Helvetica, sans-serif">精选店模式 | 一功能一技能 | 稳定优先</text>
  <text x="342" y="278" fill="#cbd5e1" font-size="30" font-family="Arial, Helvetica, sans-serif">NO DUPLICATE SKILLS · LOW TOKEN WASTE · AUDITED WEEKLY</text>
  <text x="342" y="334" fill="#fde68a" font-size="28" font-family="Arial, Helvetica, sans-serif">Theme: Boutique Store + Lobster</text>
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
