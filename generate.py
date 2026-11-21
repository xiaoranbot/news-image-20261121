"""Draw the front page summing up Saturday 21 November 2026's world news.

Pure Pillow drawing: no external images, no network, deterministic.
Writes entry.png (1024 x 1024) next to this file.

News checked against wire reporting available on 21 November 2026
(Beijing time, morning): the Polish missile incident, the Wall Street
correction, the Peru quake, GTA 6's first-day sales, the Kyiv barrage,
the Brazil storm, the ICJ follow-up, the UK-EU deals, the Palisades
verdict and Cyclone Akvan.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 42)
NAVY = (31, 58, 95)
GREY = (110, 108, 100)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, fill=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(SANS_B, 19), fill=RED)
    return y + 25


def headline(draw, x, y, text, width):
    fnt = font(SERIF_B, 30)
    return para(draw, x, y, text, fnt, width, 36)


def body(draw, x, y, text, width, size=20, leading=25):
    return para(draw, x, y, text, font(SERIF, size), width, leading)


def draw_masthead(draw):
    rule(draw, 36, 40, 988, 3)
    draw.text((36, 50), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 56),
              fill=INK)
    draw.text((36, 116), "SATURDAY 21 NOVEMBER 2026",
              font=font(SANS_B, 24), fill=RED)
    draw.text((988, 116), "ONE DAY  ·  ONE IMAGE",
              font=font(SANS_B, 24), fill=INK, anchor="ra")
    rule(draw, 36, 150, 988, 3)
    rule(draw, 36, 156, 988, 1)


def draw_panel(draw, x, y, w, h):
    """Schematic of the impact sites in south-east Poland."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.text((x + 14, y + 10), "SCHEMATIC — SE POLAND",
              font=font(SANS_B, 14), fill=(220, 225, 235))
    px, py = x + 16, y + h - 52
    for i in range(9):
        seg = 14
        draw.line([(px + i * seg, py - i * 6),
                   (px + (i + 1) * seg - 5, py - (i + 1) * 6 + 2)],
                  fill=(150, 165, 190), width=2)
    spots = [(0.34, 0.52), (0.58, 0.38), (0.76, 0.60)]
    for fx, fy in spots:
        cx, cy = x + int(w * fx), y + int(h * fy)
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22],
                     outline=(255, 120, 120), width=2)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 70, 70))
    draw.text((x + 14, y + h - 32),
              "NOWY LIPOWIEC · RUDNIK NAD SANEM",
              font=font(SANS_B, 12), fill=(220, 225, 235))
    draw.text((x + 14, y + h - 16), "MOLODYCZ",
              font=font(SANS_B, 12), fill=(220, 225, 235))


def draw_lead(draw):
    y = kicker(draw, 36, 170, "WAR IN EUROPE  ·  POLAND")
    draw.text((36, y), "MISSILES FALL ON POLAND",
              font=font(SERIF_B, 54), fill=INK)
    y += 62
    tx = 36
    y = para(draw, tx, y,
             "Two Russian missiles and a suspected drone crashed in "
             "south-east Poland during a huge overnight attack on "
             "Ukraine. Warsaw calls it an \u201cintentional "
             "provocation\u201d; NATO calls it a \u201cgrave "
             "violation\u201d of allied airspace.",
             font(SERIF, 22), 620, 28)
    y += 6
    y = para(draw, tx, y,
             "Jets scrambled, Patriots on alert. No injuries; "
             "Rutte visits Poland this weekend.",
             font(SERIF, 22), 620, 28)
    draw_panel(draw, 688, 262, 300, y - 262)
    return y


def draw_markets(draw, x, y, w):
    y = kicker(draw, x, y, "MARKETS")
    y = headline(draw, x, y, "MARKETS IN FREEFALL", w)
    y += 4
    bars = [("S&P 500", -3.7), ("Nasdaq", -5.3),
            ("Dow", -1.9), ("Nvidia", -12.0)]
    for name, val in bars:
        draw.text((x, y), name, font=font(SANS_B, 18), fill=INK)
        blen = int(abs(val) / 13.0 * 250)
        draw.rectangle([x + 108, y + 1, x + 108 + blen, y + 19], fill=RED)
        draw.text((x + 108 + blen + 8, y), "%.1f%%" % val,
                  font=font(SANS_B, 18), fill=RED)
        y += 28
    y += 4
    y = body(draw, x, y,
             "AI sell-off wipes out the Nasdaq's 2026 gains. "
             "VIX tops 30.", w)
    return y


def draw_quake(draw, x, y, w):
    y = kicker(draw, x, y, "EARTHQUAKE  ·  PERU")
    y = headline(draw, x, y, "PERU SHAKEN BY M6.9", w)
    y += 4
    sx, sy, sw, sh = x, y, w, 60
    draw.rectangle([sx, sy, sx + sw, sy + sh], outline=GREY, width=1)
    pts = []
    for i in range(0, sw, 4):
        t = i / sw
        amp = 22 * math.exp(-3.0 * abs(t - 0.42)) + 3
        v = (i * 7) % 13 - 6
        pts.append((sx + i, sy + sh // 2 + int(amp * math.sin(i * 0.55))
                    + v // 2))
    draw.line(pts, fill=RED, width=2)
    tw = draw.textlength("00:09 GMT", font=font(SANS_B, 16))
    draw.rectangle([sx + 4, sy + 3, sx + 12 + tw, sy + 23], fill=PAPER)
    draw.text((sx + 8, sy + 5), "00:09 GMT", font=font(SANS_B, 16),
              fill=GREY)
    y = sy + sh + 8
    y = body(draw, x, y,
             "Magnitude 6.9 near Jun\u00edn, felt strongly in Lima. "
             "No casualties reported.", w)
    return y


def draw_gta(draw, x, y, w):
    y = kicker(draw, x, y, "ENTERTAINMENT")
    y = headline(draw, x, y, "GTA 6: $3.79BN DAY ONE", w)
    y += 4
    y = body(draw, x, y,
             "The biggest entertainment launch ever — four times "
             "GTA 5's first day. 24.6m copies sold.",
             w)
    return y


def draw_kyiv(draw, x, y, w):
    y = kicker(draw, x, y, "WAR IN EUROPE  ·  UKRAINE")
    y = headline(draw, x, y, "KYIV'S BRIDGES HIT", w)
    y += 4
    y = body(draw, x, y,
             "Overnight barrage damages three Dnipro bridges and "
             "kills nine. Power, heat and water cut.", w)
    return y


def draw_also(draw, y):
    rule(draw, 36, y, 988, 2)
    y += 10
    draw.text((36, y), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    y += 26
    items = [
        "Brazil storm kills 3, wrecks 5,000 homes in Tupanciret\u00e3.",
        "Malaysia offers to resettle 10,000 Rohingya after ICJ ruling.",
        "UK\u2013EU sign food, carbon and youth-mobility deals.",
        "Palisades fire: LA jury convicts the arsonist.",
        "Cyclone Akvan weakens over India's east coast.",
    ]
    for item in items:
        draw.text((52, y), "\u2022", font=font(SERIF, 18), fill=INK)
        y = para(draw, 72, y, item, font(SERIF, 18), 880, 20)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    lead_end = draw_lead(draw)
    rule(draw, 36, lead_end + 14, 988, 1, fill=GREY)
    y2 = lead_end + 28
    m_end = draw_markets(draw, 36, y2, 452)
    q_end = draw_quake(draw, 516, y2, 472)
    mid = max(m_end, q_end)
    draw.line([(500, y2), (500, mid)], fill=GREY, width=1)
    rule(draw, 36, mid + 14, 988, 1, fill=GREY)
    y3 = mid + 28
    g_end = draw_gta(draw, 36, y3, 452)
    k_end = draw_kyiv(draw, 516, y3, 472)
    low = max(g_end, k_end)
    draw.line([(500, y3), (500, low)], fill=GREY, width=1)
    end = draw_also(draw, low + 10)
    draw.text((36, end + 2),
              "Sources: wire reporting, 21 Nov 2026  ·  Drawn entirely "
              "in code  ·  make.fun news-image-20261121",
              font=font(SANS, 13), fill=GREY)
    print("bottom y:", end + 8 + 13)
    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
