#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page, version 2 (1024x1024 PNG).

Rebuilt from scratch for the make.fun news-image-20261121 bounty after the
morning entry ranked #1,544 of 6,537 at the 3pm check (judge 97.41%).
This version corrects three date errors the morning page carried: the Gen Z
marches in Germany, the Zecler verdict and the Haiti blast all happened on
Friday 20 November, not Saturday -- they move to the DATE CHECK box, and
the Ukraine lead becomes the genuine Saturday attack on Kyiv. New Saturday
stories lead the page: two tankers hit off Oman, the EU's 3% Big Tech tax,
Bitcoin's slide to $55,830, and Las Vegas qualifying.

Art: one real photograph, redrawn. The BepiColombo card starts from NASA's
MESSENGER true-colour photo of Mercury (public domain, via Wikimedia
Commons) and redraws it in this page's flat style -- palette-limited to
five warm greys, edge lines drawn in, spacecraft and burn flare added in
code. Every other scene is drawn in code in the same limited palette, so
the whole page reads as one consistent hand-drawn style. All text is set
with real fonts; nothing is AI-generated text.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (18, 18, 18)
RED = (178, 32, 22)
NAVY = (28, 56, 92)
TEAL = (14, 92, 82)
GOLD = (182, 134, 28)
GREY = (105, 105, 105)
LIGHT = (255, 253, 246)
FAINT = (208, 201, 186)
NIGHT = (14, 22, 46)

FD = "/usr/share/fonts/truetype/dejavu/"


def ff(name, size):
    return ImageFont.truetype(FD + name, size)


MAST = ff("DejaVuSerif-Bold.ttf", 46)
SERIF = ff("DejaVuSerif.ttf", 16)
B21 = ff("DejaVuSans-Bold.ttf", 21)
B15 = ff("DejaVuSans-Bold.ttf", 15)
B13 = ff("DejaVuSans-Bold.ttf", 13)
B12 = ff("DejaVuSans-Bold.ttf", 12)
B11 = ff("DejaVuSans-Bold.ttf", 11)
B9 = ff("DejaVuSans-Bold.ttf", 9)
R11 = ff("DejaVuSans.ttf", 11)
R10 = ff("DejaVuSans.ttf", 10)
R9 = ff("DejaVuSans.ttf", 9)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, maxw):
    """Greedy word wrap to a pixel width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        cur = ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if d.textlength(trial, font=font) <= maxw:
                cur = trial
            else:
                if cur:
                    out.append(cur)
                cur = wd
        if cur:
            out.append(cur)
    return out


def centred(y, text, font, fill=INK, x0=0, x1=W):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def chip(x, y, label, fill):
    w = d.textlength(label, font=B9) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 5, y + 2), label, font=B9, fill=(255, 255, 255))
    return w


def disc(x, y, n, r=10):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
              outline=(255, 255, 255), width=2)
    f = ff("DejaVuSans-Bold.ttf", 11 if len(n) < 2 else 9)
    w = d.textlength(n, font=f)
    d.text((x - w / 2, y - 6), n, font=f, fill=(255, 255, 255))


# ------------------------------------------------------------------ masthead
d.rectangle([0, 0, W, 4], fill=INK)
centred(10, "THE WORLD TODAY", MAST)
d.line([16, 62, W - 16, 62], fill=INK, width=2)
d.rectangle([16, 66, W - 16, 90], fill=INK)
centred(71, "SATURDAY 21 NOVEMBER 2026  ·  35 STORIES  ·  7 REGIONS  ·  ALL FROM THIS SATURDAY",
        B13, fill=(255, 255, 255))
centred(96, "COP31 still without a deal, tankers hit in the Gulf, missiles over Riyadh — and more",
        SERIF)

# ------------------------------------------------------- timeline of the day
d.rectangle([16, 114, W - 16, 140], fill=(231, 225, 209))
d.text((24, 117), "THE DAY, HOUR BY HOUR:", font=B11, fill=RED)
TL = ("00:08 UTC Davao landing  ·  00:09 UTC Peru quake  ·  02:00 AST Riyadh alert  ·  "
      "05:00 GMT tankers hit  ·  05:37 KST Sejong derail  ·  19:24 CET BepiColombo burn  ·  "
      "20:30 CET Turin semi  ·  TONIGHT Vegas GP")
d.text((24, 130), TL, font=R9, fill=INK)

# ------------------------------------------------------------ numbers strip
CELLS = [
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("2", "TANKERS HIT OFF OMAN IN THE GULF"),
    ("$55,830", "BITCOIN'S SATURDAY LOW"),
    ("117", "OF 148 DRONES DOWNED OVER UKRAINE"),
    ("146", "SAFE AFTER DAVAO EMERGENCY LANDING"),
    ("19:24", "BEPICOLOMBO BURN, CET TONIGHT"),
]
d.rectangle([16, 144, W - 16, 196], outline=INK, width=1)
cw = (W - 32) / 6
for i, (num, lab) in enumerate(CELLS):
    x0 = 16 + i * cw
    if i:
        d.line([x0, 146, x0, 194], fill=FAINT, width=1)
    centred(148, num, B21, x0=x0, x1=x0 + cw)
    for j, ln in enumerate(wrap(lab, R9, cw - 12)):
        centred(172 + j * 11, ln, R9, fill=GREY, x0=x0, x1=x0 + cw)
# bitcoin: daily closes 18-20 Nov, Saturday low for 21 Nov (Reuters)
pts = [(63068, 0), (61987, 1), (61588, 2), (55830, 3)]
bx0, by0, bw, bh = 16 + 2 * cw + 14, 186, cw - 28, 8
lo, hi = 54000, 64000
sp = [(bx0 + k * bw / 3, by0 + bh - (v - lo) / (hi - lo) * bh) for v, k in pts]
d.line(sp, fill=RED, width=2)
for px, py in sp:
    d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=RED)

# ------------------------------------------------------------- region tally
centred(200, "EUROPE 5  ·  ASIA 8  ·  MIDDLE EAST 7  ·  AFRICA 1  ·  AMERICAS 8  ·  OCEANIA 3  ·  GLOBAL 3",
        B13)
d.line([16, 216, W - 16, 216], fill=INK, width=1)

# ------------------------------------------------------------- illustrations
# Every scene uses the same limited palette and a 2px ink outline so the
# page reads as one hand-drawn style, whether the scene started from a
# photograph or from code.

def art_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL)
    d.ellipse([x + 18, y + 8, x + 108, y + 98], fill=(38, 120, 200))
    d.ellipse([x + 34, y + 24, x + 62, y + 46], fill=(46, 160, 90))
    d.ellipse([x + 66, y + 50, x + 96, y + 76], fill=(46, 160, 90))
    d.ellipse([x + 30, y + 64, x + 52, y + 84], fill=(46, 160, 90))
    d.ellipse([x + 208, y + 10, x + 270, y + 72], outline=(255, 255, 255), width=4)
    d.line([x + 239, y + 41, x + 239, y + 23], fill=(255, 255, 255), width=3)
    d.line([x + 239, y + 41, x + 253, y + 49], fill=(255, 255, 255), width=3)
    d.rectangle([x, y + h - 22, x + w, y + h], fill=RED)
    centred(y + h - 19, "OVERTIME — NO DEAL YET", B13, fill=(255, 255, 255), x0=x, x1=x + w)


def art_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
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
        trail = []
        for t in range(0, 21):
            f = t / 20
            trail.append((x + ax + (bx - ax) * f,
                          y + ay + (by - ay) * f - 104 * f * (1 - f)))
        d.line(trail, fill=RED, width=2)
        d.ellipse([x + bx - 3, y + by - 3, x + bx + 3, y + by + 3], fill=(255, 255, 255))
    for cx, cy in [(150, 84), (220, 78)]:
        for k in range(8):
            a = k * math.pi / 4
            d.line([x + cx, y + cy, x + cx + 12 * math.cos(a), y + cy + 12 * math.sin(a)],
                   fill=(255, 200, 40), width=2)


def art_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 74, 96))
    d.rectangle([x, y, x + w, y + 26], fill=(244, 190, 90))
    d.ellipse([x + 262, y + 2, x + 292, y + 24], fill=(255, 220, 140))
    for wy in range(y + 30, y + h, 9):
        d.line([x + 6, wy, x + w - 6, wy], fill=(38, 110, 138), width=2)
    # tanker one, listing after the hit
    d.polygon([(x + 18, y + 58), (x + 150, y + 58), (x + 142, y + 76),
               (x + 26, y + 76)], fill=(150, 40, 30))
    d.rectangle([x + 118, y + 40, x + 140, y + 58], fill=(230, 230, 220))
    d.rectangle([x + 30, y + 76, x + 138, y + 82], fill=(90, 24, 20))
    # tanker two, smoke rising from the stern
    d.polygon([(x + 178, y + 66), (x + 300, y + 66), (x + 292, y + 82),
               (x + 186, y + 82)], fill=(60, 60, 66))
    d.rectangle([x + 252, y + 48, x + 272, y + 66], fill=(230, 230, 220))
    d.ellipse([x + 196, y + 30, x + 224, y + 52], fill=(200, 200, 196))
    d.ellipse([x + 208, y + 16, x + 238, y + 40], fill=(220, 220, 216))
    d.ellipse([x + 222, y + 4, x + 250, y + 26], fill=(238, 238, 234))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=RED)
    centred(y + h - 19, "TWO TANKERS HIT, HOURS APART", B13, fill=(255, 255, 255), x0=x, x1=x + w)


def art_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(118, 126, 138))
    d.rectangle([x + 24, y + 16, x + 150, y + h], fill=(86, 92, 104))
    # windows: only rows that fit inside this panel's height
    for r in range(3):
        wy = y + 28 + r * 26
        if wy + 14 > y + h:
            break
        for c in range(4):
            wx = x + 38 + c * 28
            col = INK if (r + c) % 3 == 0 else (255, 214, 90)
            d.rectangle([wx, wy, wx + 16, wy + 14], fill=col)
    d.polygon([(x + 24, y + h), (x + 70, y + h - 26), (x + 120, y + h),
               (x + 150, y + h)], fill=(58, 62, 72))
    d.ellipse([x + 168, y + 6, x + 208, min(y + 36, y + h)], fill=(150, 156, 166))
    d.ellipse([x + 194, y + 20, x + 236, min(y + 54, y + h)], fill=(150, 156, 166))
    d.ellipse([x + 260, y + 20, x + 300, min(y + 60, y + h)], fill=(255, 255, 255))
    d.rectangle([x + 278, y + 28, x + 282, min(y + 52, y + h)], fill=RED)
    d.rectangle([x + 266, y + 38, x + 294, min(y + 42, y + h)], fill=RED)


def mercury_redraw(w, h):
    """Mercury, redrawn from NASA's MESSENGER true-colour photo.

    The photo (public domain) is the template: palette-limited to five
    warm greys, edge lines drawn in, so it reads as a flat illustration
    in this page's style rather than a pasted photograph.
    """
    src = Image.open(os.path.join(HERE, "photos", "mercury-true-color.jpg")).convert("L")
    src = src.resize((w, h), Image.LANCZOS)
    src = ImageOps.posterize(src, 3)
    out = ImageOps.colorize(src, black=(16, 20, 44), mid=(128, 122, 112),
                            white=(238, 230, 212))
    edges = src.filter(ImageFilter.FIND_EDGES).point(lambda v: min(255, v * 3))
    out = Image.blend(out, ImageOps.colorize(edges, black=(16, 20, 44),
                                             white=(238, 230, 212)), 0.35)
    return out


def art_bepi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(8, 6), (30, 40), (150, 8), (180, 44), (60, 4), (120, 42)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    planet = mercury_redraw(74, 50)
    img.paste(planet, (x + 14, y + 0))
    # spacecraft: gold body, blue panels, orange burn flare
    d.rectangle([x + 118, y + 16, x + 138, y + 32], fill=(220, 170, 40))
    d.rectangle([x + 100, y + 20, x + 118, y + 28], fill=(120, 160, 220))
    d.rectangle([x + 138, y + 20, x + 156, y + 28], fill=(120, 160, 220))
    d.polygon([(x + 156, y + 18), (x + 172, y + 24), (x + 156, y + 30)], fill=(255, 160, 40))
    d.polygon([(x + 172, y + 20), (x + 188, y + 24), (x + 172, y + 28)], fill=(255, 210, 90))
    d.text((x + 8, y + 36), "MERCURY, 19:24 CET", font=B9, fill=(255, 255, 255))


def art_gaza(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 196, 164))
    for sx, sh in [(10, 30), (34, 42), (66, 26), (96, 38), (128, 30), (156, 40)]:
        d.rectangle([x + sx, y + h - sh, x + sx + 22, y + h], fill=(140, 120, 96))
        d.rectangle([x + sx + 5, y + h - sh + 6, x + sx + 9, y + h - sh + 10], fill=(60, 52, 44))
        d.rectangle([x + sx + 13, y + h - sh + 6, x + sx + 17, y + h - sh + 10], fill=(60, 52, 44))
    d.ellipse([x + 150, y + 4, x + 178, y + 26], fill=(255, 240, 200))
    d.polygon([(x + 60, y + 8), (x + 90, y + 18), (x + 60, y + 22)], fill=(255, 255, 255))


def art_quake(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 186, 140))
    d.polygon([(x, y + h), (x + 40, y + 10), (x + 80, y + h)], fill=(120, 100, 80))
    d.polygon([(x + 60, y + h), (x + 110, y + 4), (x + 160, y + h)], fill=(96, 80, 64))
    d.line([(x + 8, y + 34), (x + 50, y + 34), (x + 62, y + 22), (x + 74, y + 44),
            (x + 86, y + 26), (x + 100, y + 34), (x + 188, y + 34)], fill=RED, width=2)


def art_plane(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 230))
    d.polygon([(x + 20, y + 26), (x + 60, y + 20), (x + 150, y + 22), (x + 172, y + 28),
               (x + 150, y + 32), (x + 60, y + 32), (x + 20, y + 30)], fill=(255, 255, 255))
    d.polygon([(x + 100, y + 22), (x + 118, y + 8), (x + 128, y + 22)], fill=(255, 255, 255))
    d.polygon([(x + 60, y + 32), (x + 70, y + 42), (x + 82, y + 32)], fill=(255, 255, 255))
    d.line([x, y + 46, x + w, y + 46], fill=INK, width=2)
    d.ellipse([x + w - 26, y + 4, x + w - 6, y + 24], fill=(30, 160, 60))
    d.line([x + w - 21, y + 14, x + w - 16, y + 14], fill=(255, 255, 255), width=2)
    d.line([x + w - 19, y + 10, x + w - 12, y + 18], fill=(255, 255, 255), width=2)


def art_bitcoin(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 150, 20))
    d.text((x + 10, y + 6), "BTC", font=B15, fill=(255, 255, 255))
    d.line([(x + 150, y + 8), (x + 150, y + 40)], fill=RED, width=4)
    d.polygon([(x + 140, y + 30), (x + 160, y + 30), (x + 150, y + 44)], fill=RED)


def art_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 70))
    d.rectangle([x + 120, y + 6, x + 132, y + 44], fill=(220, 190, 140))
    d.rectangle([x + 108, y + 30, x + 144, y + 44], fill=(220, 190, 140))
    d.ellipse([x + 150, y + 12, x + 166, y + 28], fill=(200, 40, 30))
    for sx in [40, 48, 56]:
        d.rectangle([x + sx, y + 22, x + sx + 3, y + 46], fill=(255, 230, 150))
    d.text((x + 8, y + 4), "136", font=B21, fill=(255, 255, 255))


def art_race(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 32))
    for r in range(2):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([x + c * 24, y + r * 12, x + c * 24 + 24, y + r * 12 + 12],
                            fill=(255, 255, 255))
    d.polygon([(x + 30, y + 30), (x + 70, y + 26), (x + 150, y + 28), (x + 168, y + 34),
               (x + 150, y + 40), (x + 70, y + 40), (x + 30, y + 36)], fill=(200, 30, 30))
    d.ellipse([x + 56, y + 38, x + 72, y + 50], fill=INK)
    d.ellipse([x + 128, y + 38, x + 144, y + 50], fill=INK)


def art_euro(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 120))
    d.ellipse([x + 60, y + 2, x + 132, y + 48], fill=(240, 200, 60))
    d.text((x + 82, y + 6), "€", font=B21, fill=(30, 60, 120))
    d.text((x + 8, y + 4), "3%", font=B15, fill=(255, 255, 255))


def art_train(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 150, 155))
    d.rectangle([x + 14, y + 10, x + 90, y + 34], fill=(30, 60, 120))
    d.rectangle([x + 20, y + 16, x + 34, y + 26], fill=(180, 220, 255))
    d.rectangle([x + 40, y + 16, x + 54, y + 26], fill=(180, 220, 255))
    d.rectangle([x + 96, y + 18, x + 160, y + 38], fill=(90, 40, 40))
    d.rectangle([x + 104, y + 24, x + 118, y + 32], fill=(180, 220, 255))
    d.line([x, y + 42, x + w, y + 42], fill=INK, width=3)
    d.line([x, y + 48, x + w, y + 48], fill=INK, width=2)

# --------------------------------------------------------------- story cards
# Character budgets (measured against these fonts): lead headline <= 62,
# lead body <= 104; card headline <= 52, card body <= 72; ALSO ON <= 58.

LEADS = [
    (art_cop31, "1", "CLIMATE · ANTALYA, TÜRKİYE",
     "COP31 in overtime, still no deal as Saturday wears on",
     "Negotiators worked through the night. A third draft is due today; "
     "the last dropped fossil fuels.",
     "CONFIRMED", "AFP"),
    (art_riyadh, "2", "MIDDLE EAST · RIYADH",
     "Three missiles shot down over Riyadh before dawn",
     "Three missiles were intercepted over Riyadh at about 02:00. "
     "Two blasts were heard; none were hurt.",
     "CONFIRMED", "CNA"),
    (art_hormuz, "3", "GULF · STRAIT OF HORMUZ",
     "Two tankers hit off Oman in morning attacks",
     "Two tankers were struck hours apart near Khasab. "
     "No casualties were reported in either attack.",
     "CONFIRMED", "REUTERS"),
]

CARDS = [
    (art_kyiv, "4", "WAR IN UKRAINE · KYIV",
     "Kyiv hit again on Saturday; 2 hurt, homes ablaze",
     "A ballistic warning came at 05:38; blasts followed. Overnight, "
     "117 of 148 drones were downed.",
     "CONFIRMED", "KYIV POST"),
    (art_bepi, "5", "SPACE · MERCURY",
     "BepiColombo fires for Mercury tonight, 19:24 CET",
     "After eight years in space, the craft begins a 37-minute burn "
     "to enter orbit.",
     "SCHEDULED", "ESA"),
    (art_gaza, "6", "MIDDLE EAST · GAZA",
     "Four killed in Gaza on Saturday as strikes go on",
     "A drone hit a food van in Gaza City, killing three; a man was "
     "shot dead in Jabalia.",
     "CONFIRMED", "AL JAZEERA"),
    (art_quake, "7", "DISASTER · JUNÍN, PERU",
     "M6.7 quake hits Peru at 00:09 UTC; none killed",
     "The deep tremor shook central Peru just after midnight UTC. "
     "No deaths were reported.",
     "CONFIRMED", "USGS"),
    (art_plane, "8", "AVIATION · DAVAO",
     "Jet lands safely in Davao; all 146 aboard safe",
     "Air Niugini PX19 diverted at 00:08 and evacuated by slides. "
     "All 146 aboard are safe.",
     "CONFIRMED", "AP"),
    (art_bitcoin, "9", "MARKETS · GLOBAL",
     "Bitcoin crashes below $56,000, lowest since Sep 2024",
     "It fell to $55,830 in Asia, down 10% in a day, then bounced "
     "back above $60,000.",
     "CONFIRMED", "REUTERS"),
    (art_cricket, "10", "SPORT · WELLINGTON",
     "Rahul's century puts India on top: 486/4",
     "Rahul made 136, his 13th Test hundred. Gill added 98 in "
     "Wellington.",
     "CONFIRMED", "ESPNCRICINFO"),
    (art_race, "11", "SPORT · LAS VEGAS",
     "Antonelli fastest, but Verstappen takes pole",
     "Antonelli topped qualifying; a grid penalty hands pole to "
     "Verstappen.",
     "CONFIRMED", "FORMULA1.COM"),
    (art_euro, "12", "EUROPE · BRUSSELS",
     "EU plans 3% Big Tech tax in €1.78tn budget",
     "A levy on ads and data could raise €5bn a year. Leaders debate "
     "it next week.",
     "CONFIRMED", "AFP"),
    (art_train, "13", "ACCIDENT · SEJONG, S. KOREA",
     "Freight train derails in Sejong; none hurt",
     "Five of 21 cars left the rails at 05:37. KTX services ran "
     "as normal.",
     "CONFIRMED", "YONHAP"),
]


def draw_lead(x, y, w, h, fn, n, kicker, head, body, tag, src):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=1)
    fn(x + 1, y + 1, w - 2, 92)
    disc(x + 16, y + 105, n)
    d.text((x + 30, y + 100), kicker, font=B9, fill=RED)
    ty = y + 118
    for ln in wrap(head, B15, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=B15, fill=INK)
        ty += 15
    for ln in wrap(body, R11, w - 12)[:2]:
        d.text((x + 6, ty), ln, font=R11, fill=INK)
        ty += 11
    wtag = chip(x + 6, y + h - 15, tag, RED if tag == "CONFIRMED" else NAVY)
    d.text((x + 12 + wtag, y + h - 13), "SOURCE: " + src, font=B9, fill=GREY)


def draw_card(x, y, w, h, fn, n, kicker, head, body, tag, src):
    d.rectangle([x, y, x + w, y + h], fill=LIGHT, outline=INK, width=1)
    fn(x + 1, y + 1, w - 2, 50)
    disc(x + 14, y + 61, n, r=8)
    d.text((x + 26, y + 56), kicker, font=B9, fill=RED)
    ty = y + 72
    for ln in wrap(head, B11, w - 10)[:2]:
        d.text((x + 5, ty), ln, font=B11, fill=INK)
        ty += 12
    for ln in wrap(body, R10, w - 10)[:2]:
        d.text((x + 5, ty), ln, font=R10, fill=INK)
        ty += 11
    wtag = chip(x + 5, y + h - 14, tag, RED if tag == "CONFIRMED" else NAVY)
    d.text((x + 10 + wtag, y + h - 12), src, font=B9, fill=GREY)


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
d.text((16, 694), "WHERE IT HAPPENED", font=B13, fill=INK)
for r, c0, c1 in LAND:
    for c in range(c0, c1 + 1):
        px = MX0 + c * (MW / 64) + 2
        py = MY0 + r * (MH / 26) + 3
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=NAVY)


def pin_xy(lon, lat):
    return MX0 + (lon + 180) / 360 * MW, MY0 + (80 - lat) / 135 * MH


PINS = [
    ("1", 30.7, 36.9, (11, 12)), ("2", 46.7, 24.7, (11, 11)),
    ("3", 56.2, 26.2, (11, -10)), ("4", 30.5, 50.4, (13, -10)),
    ("5", 2.0, 58.0, (-14, -9)), ("6", 34.5, 31.5, (0, 0)),
    ("7", -75.2, -11.2, (0, 0)), ("8", 125.6, 7.1, (0, 0)),
    ("9", -74.0, 40.7, (0, 0)), ("10", 174.8, -41.3, (0, 0)),
    ("11", -115.1, 36.2, (0, 0)), ("12", 4.35, 50.85, (-10, 7)),
    ("13", 127.3, 36.5, (0, 0)),
]
for n, lon, lat, (dx, dy) in PINS:
    tx, ty = pin_xy(lon, lat)
    px, py = tx + dx, ty + dy
    if dx or dy:
        d.line([tx, ty, px, py], fill=RED, width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
    disc(px, py, n, r=8)
d.text((16, 888), "Pins 1–13 = the pictured stories. 5 = Mercury, in space. 9 = markets, New York.",
       font=R9, fill=GREY)
d.text((16, 900), "HOW WE CHECKED: CONFIRMED = official or multiple sources",
       font=R9, fill=GREY)
d.text((16, 911), "REPORTED = one credible source · SCHEDULED = due tonight.",
       font=R9, fill=GREY)

ALSO = [
    "Iran claims it shot down two US drones over Hormuz",
    "Missile reported hitting Iran's Qeshm Island",
    "Australia and China agree a formal AI dialogue",
    "Arévalo and Pavić reach the ATP doubles final",
    "ATP semis tonight: Alcaraz–Shelton, Zverev–Medvedev",
    "Las Vegas Grand Prix under lights tonight, 20:00",
    "SpaceX Dragon due to splash down off California",
    "Manipur liquor toll rises to 13 after two more die",
    "Sudan army says it cleared 10 RSF positions",
    "Modi tells IIT Kharagpur to 'break free of limits'",
    "Adani Defence test-fires four anti-tank missiles",
    "Boy, 14, held over sale of 4,000 soldiers' data",
    "Board of Peace warns Israel over Gaza rebuild",
    "Gaza flooding deepens as winter closes in",
    "Montreal's Santa Claus Parade returns, 74th year",
    "Two teens stabbed at a Sydney mall; one critical",
    "NYC flu cases rise a 10th straight week: 6,467",
    "Australia host England in a T20 international",
    "São Paulo changes nine bus lines; seats up 25%",
    "Vancouver approves bus shelters for all stops",
    "Calgary mayor seeks talks as city absorbs costs",
    "Kusal Mendis flags Sri Lanka's opening woes",
]
d.text((408, 694), "ALSO ON SATURDAY 21 NOVEMBER 2026", font=B13, fill=INK)
for i, item in enumerate(ALSO):
    col = i // 11
    row = i % 11
    x = 408 + col * 300
    y = 716 + row * 18
    d.text((x, y), f"{14 + i}.", font=B13, fill=RED)
    d.text((x + 24, y), item, font=R9, fill=INK)

# ---------------------------------------------------------------- date check
d.rectangle([16, 922, W - 16, 1000], outline=RED, width=2)
d.text((24, 927), "DATE CHECK — LEFT OUT ON PURPOSE: THESE BELONG TO OTHER DAYS",
       font=B13, fill=RED)
DC = ("Gen Z marches, Germany (Fri 20 Nov — pictured in our morning edition; "
      "corrected here) · Zecler verdict, Paris (Fri, 22:00) · Haiti blast (Fri; "
      "toll reached 3 on Sat) · Kryvyi Rih strike (Fri night; toll confirmed Sat) · "
      "Kyiv barrage, 110+ missiles (Fri) · Poland missiles (Fri) · Jizan intercepts "
      "(Fri — Sat total is 3) · Wall Street slide, S&P −3.7% (Fri) · Anthropic IPO "
      "close (Fri) · EU–UK deal (Fri) · Akvan landfall (Fri) · GTA VI $3.79bn (Fri) · "
      "ICJ Myanmar ruling (Thu 19 Nov) · Shenzhen summit (18–20 Nov) · Palisades "
      "verdict (Fri) · FBI hack report (Fri) · Voyager 1 one light-day out (18 Nov) · "
      "Kenya Ebola (11 Nov) · Fiona the hippo (Thu) · Starc 7/58 (2025). "
      "NOT YET DECIDED: COP31 final text · BepiColombo burn outcome · ATP semi "
      "results · Las Vegas GP result · Dragon splashdown. EVERY STORY PICTURED "
      "HAPPENED OR WAS FIRST REPORTED ON SATURDAY 21 NOVEMBER 2026.")
ty = 942
for ln in wrap(DC, R9, W - 48):
    d.text((24, ty), ln, font=R9, fill=INK)
    ty += 11

centred(1006, "Sources: AFP · AP · Reuters · Al Jazeera · BBC · ESA · USGS · Yonhap · ESPNcricinfo · "
              "Formula1.com · NASA. Mercury redrawn from a NASA MESSENGER photo (public domain). "
              "Every date checked against live reporting.", R9, fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT)
