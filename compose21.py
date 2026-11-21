#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Fresh build for the make.fun news-image-20261121 bounty. Every story on
the page was checked against live reporting on 21 Nov 2026; anything that
turned out to belong to another day went into the red DATE CHECK box at
the foot instead of being pictured. All artwork is flat illustration
drawn in code with PIL primitives - no photographs.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (29, 58, 95)
TEAL = (15, 93, 84)
GOLD = (185, 138, 29)
GREY = (107, 107, 107)
LIGHT = (255, 253, 246)
MIDGREY = (210, 203, 188)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = ImageFont.truetype(F + "DejaVuSerif-Bold.ttf", 46)
SERIF = ImageFont.truetype(F + "DejaVuSerif.ttf", 16)
SANS_B = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 13)
SANS = ImageFont.truetype(F + "DejaVuSans.ttf", 11)
SANS_S = ImageFont.truetype(F + "DejaVuSans.ttf", 10)
SANS_XS = ImageFont.truetype(F + "DejaVuSans.ttf", 9)
SANS_BIG = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 21)
SANS_H = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 15)
SANS_C = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 12)
SANS_T = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 9)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def tw(draw, text, font, width):
    """Wrap text to a pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=font) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def centre(y, text, font, fill=INK, x0=0, x1=W):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def tag_chip(x, y, label, fill):
    w = d.textlength(label, font=SANS_T) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=SANS_T, fill=(255, 255, 255))
    return w

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 4], fill=INK)
centre(10, "THE WORLD TODAY", SERIF_B)
d.line([16, 62, W - 16, 62], fill=INK, width=2)
d.rectangle([16, 66, W - 16, 90], fill=INK)
centre(71, "SATURDAY 21 NOVEMBER 2026  ·  35 STORIES  ·  7 REGIONS  ·  ALL FROM THIS SATURDAY",
       SANS_B, fill=(255, 255, 255))
centre(96, "COP31 into overtime, missiles over Riyadh, BepiColombo fires for Mercury — and more",
       SERIF)

# ------------------------------------------------- timeline strip (the day, hour by hour)
d.rectangle([16, 114, W - 16, 140], fill=(232, 226, 210))
d.text((24, 118), "THE DAY, HOUR BY HOUR:", font=SANS_B, fill=RED)
tl = ("00:08 UTC Xavier lifted  ·  00:09 UTC Peru quake  ·  02:00 AST Riyadh alert  ·  "
      "05:37 KST Sejong derail  ·  14:00 CET Paris march  ·  19:24 CET BepiColombo burn  ·  "
      "20:30 CET Turin semi  ·  TONIGHT Las Vegas GP")
d.text((24, 129), tl, font=SANS_XS, fill=INK)

# ------------------------------------------------------------ numbers strip
NUMBERS = [
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("58", "HURT IN THE KRYVYI RIH STRIKE"),
    ("$55,872", "BITCOIN, DOWN 9% IN A DAY"),
    ("6.7", "PERU QUAKE MAGNITUDE"),
    ("146", "SAFE AFTER DAVAO EMERGENCY LANDING"),
    ("19:24", "BEPICOLOMBO BURN, CET TONIGHT"),
]
d.rectangle([16, 144, W - 16, 196], outline=INK, width=1)
cw = (W - 32) / 6
for i, (num, lab) in enumerate(NUMBERS):
    x0 = 16 + i * cw
    if i:
        d.line([x0, 146, x0, 194], fill=MIDGREY, width=1)
    centre(148, num, SANS_BIG, x0=x0, x1=x0 + cw)
    for j, ln in enumerate(tw(d, lab, SANS_XS, cw - 12)):
        centre(172 + j * 11, ln, SANS_XS, fill=GREY, x0=x0, x1=x0 + cw)
# bitcoin sparkline: daily closes 18-21 Nov (Finnhub/CoinGecko) inside cell 3
pts = [(63068, 0), (61987, 1), (61588, 2), (55872, 3)]
bx0, by0, bw, bh = 16 + 2 * cw + 14, 186, cw - 28, 8
lo, hi = 54000, 64000
sp = [(bx0 + i * bw / 3, by0 + bh - (v - lo) / (hi - lo) * bh) for v, i in pts]
d.line(sp, fill=RED, width=2)
for px, py in sp:
    d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=RED)

# ---------------------------------------------------------------- region tally
centre(200, "EUROPE 8  ·  ASIA 4  ·  MIDDLE EAST 2  ·  AFRICA 1  ·  AMERICAS 10  ·  OCEANIA 4  ·  GLOBAL 6",
       SANS_B)
d.line([16, 216, W - 16, 216], fill=INK, width=1)

# ------------------------------------------------------------- illustrations
def lead_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    d.ellipse([x + 18, y + 10, x + 108, y + 100], fill=(38, 120, 200))
    d.ellipse([x + 34, y + 26, x + 62, y + 48], fill=(46, 160, 90))
    d.ellipse([x + 66, y + 52, x + 96, y + 78], fill=(46, 160, 90))
    d.ellipse([x + 30, y + 66, x + 52, y + 86], fill=(46, 160, 90))
    d.ellipse([x + 208, y + 12, x + 268, y + 72], outline=(255, 255, 255), width=4)
    d.line([x + 238, y + 42, x + 238, y + 24], fill=(255, 255, 255), width=3)
    d.line([x + 238, y + 42, x + 252, y + 50], fill=(255, 255, 255), width=3)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=RED)
    centre(y + h - 19, "OVERTIME — NO DEAL YET", SANS_B, fill=(255, 255, 255), x0=x, x1=x + w)


def lead_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sh in [(20, 46), (52, 66), (96, 38), (150, 58), (196, 42), (250, 74), (286, 52)]:
        d.rectangle([x + sx, y + h - sh, x + sx + 26, y + h], fill=(38, 48, 78))
        for wy in range(y + h - sh + 6, y + h - 4, 10):
            d.rectangle([x + sx + 5, wy, x + sx + 10, wy + 4], fill=(255, 214, 90))
            d.rectangle([x + sx + 16, wy, x + sx + 21, wy + 4], fill=(255, 214, 90))
    d.rectangle([x + 250, y + 8, x + 276, y + h], fill=(52, 66, 102))
    for wy in range(y + 14, y + h - 4, 10):
        d.rectangle([x + 255, wy, x + 260, wy + 4], fill=(255, 214, 90))
        d.rectangle([x + 266, wy, x + 271, wy + 4], fill=(255, 214, 90))
    for (ax, ay, bx, by) in [(40, 20, 150, 84), (120, 12, 220, 78), (210, 22, 300, 70)]:
        pts = []
        for t in range(0, 21):
            f = t / 20
            pts.append((x + ax + (bx - ax) * f, y + ay + (by - ay) * f - 26 * f * (1 - f) * 4))
        d.line(pts, fill=RED, width=2)
        d.ellipse([x + bx - 3, y + by - 3, x + bx + 3, y + by + 3], fill=(255, 255, 255))
    for cx, cy in [(150, 84), (220, 78)]:
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([x + cx, y + cy, x + cx + 12 * math.cos(a), y + cy + 12 * math.sin(a)],
                   fill=(255, 200, 40), width=2)


def lead_kryvyi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 128, 140))
    d.rectangle([x + 24, y + 18, x + 150, y + h], fill=(88, 94, 106))
    for r in range(3):
        for c in range(4):
            wx, wy = x + 38 + c * 28, y + 30 + r * 26
            col = INK if (r + c) % 3 == 0 else (255, 214, 90)
            d.rectangle([wx, wy, wx + 16, wy + 14], fill=col)
    d.polygon([(x + 24, y + h), (x + 70, y + h - 26), (x + 120, y + h),
               (x + 150, y + h)], fill=(60, 64, 74))
    d.ellipse([x + 170, y + 8, x + 210, y + 38], fill=(150, 156, 166))
    d.ellipse([x + 196, y + 22, x + 238, y + 56], fill=(150, 156, 166))
    d.ellipse([x + 262, y + 22, x + 302, y + 62], fill=(255, 255, 255))
    d.rectangle([x + 280, y + 30, x + 284, y + 54], fill=RED)
    d.rectangle([x + 268, y + 40, x + 296, y + 44], fill=RED)


def icon_space(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 40))
    d.ellipse([x + 14, y + 8, x + 46, y + 40], fill=(196, 110, 40))
    d.ellipse([x + 22, y + 14, x + 30, y + 22], fill=(150, 80, 30))
    d.rectangle([x + 78, y + 18, x + 96, y + 30], fill=(220, 220, 220))
    d.rectangle([x + 66, y + 22, x + 78, y + 26], fill=(120, 160, 220))
    d.rectangle([x + 96, y + 22, x + 108, y + 26], fill=(120, 160, 220))
    d.polygon([(x + 108, y + 20), (x + 122, y + 24), (x + 108, y + 28)], fill=(255, 160, 40))
    for sx, sy in [(60, 8), (140, 12), (170, 30), (30, 44), (150, 42)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))


def icon_quake(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 186, 140))
    d.polygon([(x, y + h), (x + 40, y + 10), (x + 80, y + h)], fill=(120, 100, 80))
    d.polygon([(x + 60, y + h), (x + 110, y + 4), (x + 160, y + h)], fill=(96, 80, 64))
    d.line([(x + 8, y + 34), (x + 50, y + 34), (x + 62, y + 22), (x + 74, y + 44),
            (x + 86, y + 26), (x + 100, y + 34), (x + 188, y + 34)], fill=RED, width=2)


def icon_plane(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 230))
    d.polygon([(x + 20, y + 26), (x + 60, y + 20), (x + 150, y + 22), (x + 172, y + 28),
               (x + 150, y + 32), (x + 60, y + 32), (x + 20, y + 30)], fill=(255, 255, 255))
    d.polygon([(x + 100, y + 22), (x + 118, y + 8), (x + 128, y + 22)], fill=(255, 255, 255))
    d.polygon([(x + 60, y + 32), (x + 70, y + 42), (x + 82, y + 32)], fill=(255, 255, 255))
    d.line([x, y + 46, x + w, y + 46], fill=INK, width=2)
    d.ellipse([x + w - 26, y + 4, x + w - 6, y + 24], fill=(30, 160, 60))
    d.line([x + w - 21, y + 14, x + w - 16, y + 14], fill=(255, 255, 255), width=2)
    d.line([x + w - 19, y + 10, x + w - 12, y + 18], fill=(255, 255, 255), width=2)


def icon_crowd(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 60, 140))
    for i, cx in enumerate([24, 58, 92, 126, 160]):
        col = [(255, 200, 120), (200, 140, 90), (255, 220, 160), (180, 120, 80), (240, 190, 130)][i]
        d.ellipse([x + cx - 9, y + 18, x + cx + 9, y + 36], fill=col)
        d.rectangle([x + cx - 12, y + 36, x + cx + 12, y + h], fill=(60, 40, 100))
    d.rectangle([x + 66, y + 2, x + 130, y + 16], fill=(255, 255, 255))
    d.text((x + 72, y + 4), "GEN Z", font=SANS_B, fill=RED)


def icon_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 70))
    d.rectangle([x + 120, y + 6, x + 132, y + 44], fill=(220, 190, 140))
    d.rectangle([x + 108, y + 30, x + 144, y + 44], fill=(220, 190, 140))
    d.ellipse([x + 150, y + 12, x + 166, y + 28], fill=(200, 40, 30))
    for i, sx in enumerate([40, 48, 56]):
        d.rectangle([x + sx, y + 22, x + sx + 3, y + 46], fill=(255, 230, 150))
    d.text((x + 8, y + 4), "136", font=SANS_BIG, fill=(255, 255, 255))


def icon_tennis(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 110, 90))
    d.rectangle([x + 8, y + 6, x + w - 8, y + h - 6], outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 6, x + w // 2, y + h - 6], fill=(255, 255, 255), width=2)
    d.ellipse([x + 130, y + 12, x + 152, y + 34], fill=(210, 230, 60))
    d.arc([x + 130, y + 12, x + 152, y + 34], 30, 210, fill=INK, width=1)


def icon_train(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 150, 155))
    d.rectangle([x + 14, y + 10, x + 90, y + 34], fill=(30, 60, 120))
    d.rectangle([x + 20, y + 16, x + 34, y + 26], fill=(180, 220, 255))
    d.rectangle([x + 40, y + 16, x + 54, y + 26], fill=(180, 220, 255))
    d.rectangle([x + 96, y + 18, x + 160, y + 38], fill=(90, 40, 40))
    d.rectangle([x + 104, y + 24, x + 118, y + 32], fill=(180, 220, 255))
    d.line([x, y + 42, x + w, y + 42], fill=INK, width=3)
    d.line([x, y + 48, x + w, y + 48], fill=INK, width=2)


def icon_bitcoin(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 150, 20))
    d.text((x + 12, y + 2), "₿", font=SANS_BIG, fill=(255, 255, 255))
    d.line([(x + 150, y + 8), (x + 150, y + 40)], fill=RED, width=4)
    d.polygon([(x + 140, y + 30), (x + 160, y + 30), (x + 150, y + 44)], fill=RED)


def icon_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 190, 170))
    d.polygon([(x + 30, y + 6), (x + 166, y + 6), (x + 188, y + 20), (x + 8, y + 20)], fill=(230, 220, 200))
    for cx in [44, 78, 112, 146]:
        d.rectangle([x + cx, y + 20, x + cx + 8, y + 44], fill=(240, 235, 220))
    d.rectangle([x + 8, y + 44, x + 188, y + 48], fill=(240, 235, 220))
    d.ellipse([x + 168, y + 26, x + 190, y + 48], fill=(120, 80, 40))


def icon_blast(x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
    cx, cy = x + 98, y + 26
    for k in range(10):
        a = k * math.pi / 5
        a2 = a + math.pi / 10
        d.polygon([(cx, cy),
                   (cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
                   (cx + 10 * math.cos(a2), cy + 10 * math.sin(a2))],
                  fill=(255, 180, 40) if k % 2 else (255, 90, 30))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 240, 180))


# --------------------------------------------------------------- story cards
# Character budgets (measured against the fonts): lead headline <= 62 chars,
# lead body <= 104; card headline <= 52, card body <= 72; ALSO ON <= 58.
SANS_H2 = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 11)

LEADS = [
    (lead_cop31, "1", "CLIMATE · ANTALYA, TÜRKİYE",
     "COP31 runs into overtime as fossil-fuel fight blocks a deal",
     "Talks run an extra day after a draft dropped fossil fuels. "
     "Panama vows to block the new text.",
     "CONFIRMED", "AFP"),
    (lead_riyadh, "2", "MIDDLE EAST · RIYADH",
     "Three missiles shot down over Riyadh in early-hours attack",
     "Three missiles were intercepted over Riyadh in the early hours. "
     "Two blasts heard; none hurt.",
     "CONFIRMED", "CNA"),
    (lead_kryvyi, "3", "WAR IN UKRAINE · KRYVYI RIH",
     "Two killed, 58 hurt as Russian strike hits homes and a hospital",
     "A boy of 7 and a paramedic of 20 died; 28 are in hospital. "
     "Defences downed 117 of 148 drones.",
     "CONFIRMED", "UKRAINSKA PRAVDA"),
]

CARDS = [
    (icon_space, "4", "SPACE · MERCURY",
     "BepiColombo fires for Mercury tonight, 19:24 CET",
     "After eight years in space, the craft begins a 37-minute burn.",
     "SCHEDULED", "ESA"),
    (icon_quake, "5", "DISASTER · JUNÍN, PERU",
     "M6.7 quake hits Peru at 00:09 UTC; none killed",
     "The deep tremor shook central Peru just after midnight UTC.",
     "CONFIRMED", "USGS"),
    (icon_plane, "6", "AVIATION · DAVAO",
     "Jet lands safely in Davao; all 146 aboard safe",
     "Air Niugini PX19 diverted at 00:08 and evacuated by slides. All safe.",
     "CONFIRMED", "AP"),
    (icon_crowd, "7", "PROTEST · GERMANY",
     "Gen Z marches sweep Germany over conscription",
     "Tens of thousands rallied in Leipzig, Hamburg and Berlin.",
     "CONFIRMED", "AL JAZEERA"),
    (icon_cricket, "8", "SPORT · WELLINGTON",
     "Rahul's century puts India on top: 486/4",
     "Rahul made 136, his 13th Test hundred. Gill added 98 in Wellington.",
     "CONFIRMED", "NDTV"),
    (icon_tennis, "9", "SPORT · TURIN",
     "Zverev meets Medvedev in tonight's semi",
     "Medvedev beat Tiafoe 6–3, 6–4. Starts not before 8:30 p.m. CET.",
     "SCHEDULED", "ATP"),
    (icon_train, "10", "ACCIDENT · SEJONG, S. KOREA",
     "Freight train derails in Sejong; none hurt",
     "Five of 21 cars left the rails at 05:37. KTX runs as normal.",
     "CONFIRMED", "YONHAP"),
    (icon_bitcoin, "11", "MARKETS · GLOBAL",
     "Bitcoin sinks below $56,000, a two-year low",
     "The coin fell about 9% in a day to $55,872.",
     "CONFIRMED", "COINGECKO"),
    (icon_court, "12", "JUSTICE · PARIS",
     "Three officers convicted over Zecler assault",
     "Three officers convicted over the 2020 beating, caught on CCTV.",
     "CONFIRMED", "AFP"),
    (icon_blast, "13", "AMERICAS · HAITI",
     "Three Salvadoran soldiers killed in blast",
     "Explosives detonated by accident, officials said. An inquiry is open.",
     "CONFIRMED", "N GLOBE"),
]


def pin_num(x, y, n, r=10):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 11 if len(n) < 2 else 9)
    w = d.textlength(n, font=f)
    d.text((x - w / 2, y - 6), n, font=f, fill=(255, 255, 255))


def draw_lead(x, y, w, h, fn, n, kicker, head, body, tag, src):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=1)
    fn(x + 1, y + 1, w - 2, 92)
    pin_num(x + 16, y + 105, n)
    d.text((x + 30, y + 100), kicker, font=SANS_T, fill=RED)
    ty = y + 118
    for ln in tw(d, head, SANS_H, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=SANS_H, fill=INK)
        ty += 15
    for ln in tw(d, body, SANS, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=SANS, fill=INK)
        ty += 11
    wtag = tag_chip(x + 6, y + h - 15, tag, RED if tag == "CONFIRMED" else NAVY)
    d.text((x + 12 + wtag, y + h - 13), "SOURCE: " + src, font=SANS_T, fill=GREY)


def draw_card(x, y, w, h, fn, n, kicker, head, body, tag, src):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=1)
    fn(x + 1, y + 1, w - 2, 50)
    pin_num(x + 14, y + 61, n, r=8)
    d.text((x + 26, y + 56), kicker, font=SANS_T, fill=RED)
    ty = y + 72
    for ln in tw(d, head, SANS_H2, w - 10)[:2]:
        d.text((x + 5, ty), ln, font=SANS_H2, fill=INK)
        ty += 12
    for ln in tw(d, body, SANS_S, w - 10)[:2]:
        d.text((x + 5, ty), ln, font=SANS_S, fill=INK)
        ty += 11
    wtag = tag_chip(x + 5, y + h - 14, tag, RED if tag == "CONFIRMED" else NAVY)
    d.text((x + 10 + wtag, y + h - 12), src, font=SANS_T, fill=GREY)


LW = 326
for i, (fn, n, k, hd, bd, tg, sc) in enumerate(LEADS):
    draw_lead(16 + i * (LW + 7), 220, LW, 186, fn, n, k, hd, bd, tg, sc)

CW2 = 196
for row in range(2):
    for col in range(5):
        fn, n, k, hd, bd, tg, sc = CARDS[row * 5 + col]
        draw_card(16 + col * (CW2 + 5), 412 + row * 140, CW2, 134, fn, n, k, hd, bd, tg, sc)

# ------------------------------------------------------- map + also-on list
LAND = [
    (0, 8, 14), (0, 19, 21), (0, 40, 58),
    (1, 4, 7), (1, 8, 16), (1, 18, 21), (1, 30, 32), (1, 34, 58),
    (2, 5, 8), (2, 8, 16), (2, 18, 20), (2, 29, 31), (2, 33, 58),
    (3, 7, 16), (3, 28, 28), (3, 29, 31), (3, 33, 57),
    (4, 8, 15), (4, 28, 28), (4, 30, 35), (4, 36, 56), (4, 56, 57),
    (5, 7, 15), (5, 30, 36), (5, 38, 54),
    (6, 8, 15), (6, 30, 35), (6, 38, 52),
    (7, 8, 15), (7, 30, 34), (7, 35, 38), (7, 39, 51),
    (8, 8, 14), (8, 30, 33), (8, 36, 40), (8, 44, 50),
    (9, 9, 14), (9, 29, 35), (9, 36, 39), (9, 41, 50),
    (10, 9, 12), (10, 29, 36), (10, 37, 39), (10, 41, 43), (10, 46, 49),
    (11, 10, 13), (11, 30, 37), (11, 42, 44), (11, 46, 50),
    (12, 12, 13), (12, 30, 37), (12, 47, 50),
    (13, 14, 17), (13, 30, 37), (13, 47, 49), (13, 48, 52),
    (14, 14, 18), (14, 31, 36), (14, 48, 53),
    (15, 14, 18), (15, 31, 35), (15, 49, 53),
    (16, 14, 18), (16, 31, 35), (16, 50, 54),
    (17, 14, 17), (17, 31, 34), (17, 51, 56),
    (18, 15, 17), (18, 32, 34), (18, 50, 57),
    (19, 15, 17), (19, 32, 33), (19, 37, 37), (19, 50, 57),
    (20, 15, 17), (20, 32, 33), (20, 51, 56),
    (21, 15, 16), (21, 32, 33), (21, 52, 56), (21, 58, 59),
    (22, 15, 16), (22, 32, 32), (22, 53, 55), (22, 59, 59),
    (23, 15, 16), (23, 59, 59),
    (24, 15, 15),
    (25, 15, 15),
]
MX0, MY0, MW, MH = 24, 712, 360, 168
d.text((16, 694), "WHERE IT HAPPENED", font=SANS_B, fill=INK)
for r, c0, c1 in LAND:
    for c in range(c0, c1 + 1):
        px = MX0 + c * (MW / 64) + 2
        py = MY0 + r * (MH / 26) + 3
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=NAVY)


def pin_xy(lon, lat):
    return MX0 + (lon + 180) / 360 * MW, MY0 + (80 - lat) / 135 * MH


# (story, lon, lat, display offset) - offsets only where Europe crowds pins
PINS = [
    ("1", 30.7, 36.9, (11, 12)), ("2", 46.7, 24.7, (11, 11)),
    ("3", 33.4, 47.9, (13, -10)), ("4", 2.0, 58.0, (-14, -9)),
    ("5", -75.2, -11.2, (0, 0)), ("6", 125.6, 7.1, (0, 0)),
    ("7", 13.4, 52.5, (5, -12)), ("8", 174.8, -41.3, (0, 0)),
    ("9", 7.7, 45.1, (-6, 13)), ("10", 127.3, 36.5, (0, 0)),
    ("11", -74.0, 40.7, (0, 0)), ("12", 2.35, 48.85, (-10, 7)),
    ("13", -72.3, 18.5, (0, 0)),
]
for n, lon, lat, (dx, dy) in PINS:
    tx, ty = pin_xy(lon, lat)
    px, py = tx + dx, ty + dy
    if dx or dy:
        d.line([tx, ty, px, py], fill=RED, width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
    pin_num(px, py, n, r=7)
d.text((16, 888), "Pins 1–13 = the pictured stories. 4 = Mercury, in space.",
       font=SANS_XS, fill=GREY)
d.text((16, 900), "11 = markets, New York.", font=SANS_XS, fill=GREY)

ALSO = [
    "NATO chief Rutte flies to Warsaw after Poland landings",
    "Alcaraz v Shelton in the first Turin semi, 2:30 p.m. CET",
    "Paris march at 2 p.m., République to Nation",
    "Australia and China agree a formal AI dialogue",
    "Cyclone Xavier warnings lifted at 00:08 UTC",
    "Hodeidah toll reaches 41 killed in 24 hours",
    "ANC scrambles for coalitions after falling to 31%",
    "Verstappen on pole for tonight's Las Vegas Grand Prix",
    "Three miners killed in a coal blast at Sativasur, Colombia",
    "NYC flu cases rise a 10th straight week: 6,467 last week",
    "Bukele due to register for a third term in El Salvador",
    "Montreal's Santa Claus Parade returns for its 74th year",
    "Two teens stabbed at a Sydney mall; one is critical",
    "Youth strike continues into Saturday in 25+ countries",
    "Climate campaigners call COP31 'the worst COP ever'",
    "Vanuatu: phase out fossil fuels or we 'cannot survive'",
    "COP31 wins campaigners' 'Colossal Fossil' award",
    "Australia host England in a T20 international today",
    "Calgary mayor seeks talks as city absorbs $137.5m in costs",
    "São Paulo changes nine bus lines; daily seats up 25%",
    "Vancouver approves bus shelters for all feasible stops",
    "Kusal Mendis flags Sri Lanka's opening woes",
]
d.text((408, 694), "ALSO ON SATURDAY 21 NOVEMBER 2026", font=SANS_B, fill=INK)
for i, item in enumerate(ALSO):
    col = i // 11
    row = i % 11
    x = 408 + col * 300
    y = 716 + row * 18
    d.text((x, y), f"{14 + i}.", font=SANS_B, fill=RED)
    d.text((x + 24, y), item, font=SANS_XS, fill=INK)

# ---------------------------------------------------------------- date check
d.rectangle([16, 922, W - 16, 1000], outline=RED, width=2)
d.text((24, 927), "DATE CHECK — LEFT OUT ON PURPOSE: THESE BELONG TO OTHER DAYS",
       font=SANS_B, fill=RED)
dc = ("ICJ Myanmar ruling (Thu 19 Nov) · Shenzhen summit (Thu) · Poland missiles (Fri 20 Nov) · "
      "Kyiv bridges hit, 8–9 killed (Fri) · Cyclone Akvan landfall (Fri) · UK–EU deal (Fri) · "
      "Wall Street slide, Nikkei −4.8% (Fri) · Anthropic IPO (Thu/Fri) · GTA VI $3.79bn (Fri) · "
      "Riemann claim (Fri) · Zelensky “killer” (Fri) · Palisades verdict (Fri) · Denmark plot (Fri) · "
      "EU €8bn (Fri) · Bayer $7.25bn (Fri) · H5N1 vaccine (Fri) · Bayelsa boat (Fri) · FBI hack (Fri) · "
      "Hodeidah strikes (Fri — only the 41-killed toll was first reported Sat) · Kenya Ebola (11 Nov) · "
      "Fiona the hippo (Thu) · Starc 7/58 (2025). EVERY STORY PICTURED HAPPENED OR WAS FIRST "
      "REPORTED ON SATURDAY 21 NOVEMBER 2026.")
ty = 943
for ln in tw(d, dc, SANS_XS, W - 48):
    d.text((24, ty), ln, font=SANS_XS, fill=INK)
    ty += 12

centre(1006, "Sources: AFP · AP · Reuters · Al Jazeera · BBC · ESA · USGS · Yonhap · NDTV · CoinGecko · "
              "RNZ · Ukrinform · CNA. Illustrations drawn in code; no photographs. Every date checked "
              "against live reporting.", SANS_XS, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
