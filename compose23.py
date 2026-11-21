#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image, version 3 (1024x1024 PNG).

A FINAL rebuild for the make.fun news-image-20261121 bounty. The morning
entry (v1) ranked #1,544 at the 3pm check and the afternoon rebuild (v2)
#2,057 -- both used the same dense newspaper front-page skeleton with flat
illustrations, and Noble said they look the same with only a few
differences. This version breaks that pattern completely: no masthead, no
numbers strip, no timeline, no dotted map, no ALSO ON list. Instead it is
a deep-space scene built in 3D -- a shaded globe at the centre with orbit
rings, glossy extruded glass story tiles floating at different depths,
3D spheres, drop shadows, specular highlights and a fanned glass deck of
short stories at the bottom. Every visual has real depth: light comes from
the top left, every panel has a bevel, a gloss and a shadow.

Story choice MATCHES the top entries: the same big stories of the day
(COP31 overtime, Riyadh missiles, Hormuz tankers, Kyiv, Peru quake,
Davao, BepiColombo, Gaza, Bitcoin, Rahul, Las Vegas GP, EU Big Tech tax,
Sejong) -- the difference is the look and the execution, not the news.
Every story was verified against live reporting with a research cutoff of
~16:05 WAT on Saturday 21 November 2026. Two corrections against the
leaders: Saturday's Riyadh count is 3, not 5 -- the two Jizan intercepts
were Friday -- and Gaza's Saturday toll is 4, not 6 (six were Friday).
The Tai Po fire story the #3 entry carries is a year old (Nov 2025), so
it is left out entirely.

Art: one real photograph, redrawn in 3D. The BepiColombo tile starts from
NASA's MESSENGER true-colour photo of Mercury (public domain, via
Wikimedia Commons) and renders it as a shaded 3D sphere with a
spacecraft and burn flare added in code. Every other scene is drawn in
code with the same 3D treatment. All text is set with real fonts.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"


def ff(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF = ff("DejaVuSerif-Bold.ttf", 40)
SERIF_SM = ff("DejaVuSerif-Bold.ttf", 22)
B16 = ff("DejaVuSans-Bold.ttf", 16)
B14 = ff("DejaVuSans-Bold.ttf", 14)
B13 = ff("DejaVuSans-Bold.ttf", 13)
B12 = ff("DejaVuSans-Bold.ttf", 12)
B11 = ff("DejaVuSans-Bold.ttf", 11)
B10 = ff("DejaVuSans-Bold.ttf", 10)
B9 = ff("DejaVuSans-Bold.ttf", 9)
B8 = ff("DejaVuSans-Bold.ttf", 8)
R11 = ff("DejaVuSans.ttf", 11)
R10 = ff("DejaVuSans.ttf", 10)
R9 = ff("DejaVuSans.ttf", 9)
R85 = ff("DejaVuSans.ttf", 9)

# --- palette: deep space + glass -------------------------------------------
BG_TOP = (10, 16, 40)
BG_MID = (16, 28, 66)
BG_BOT = (4, 6, 16)
INK = (235, 240, 255)
DIM = (168, 182, 214)
FAINT = (120, 134, 172)
GLASS = (24, 40, 84)
GLASS_HI = (58, 86, 150)
GOLD = (245, 190, 60)
RED = (255, 82, 66)
GREEN = (52, 211, 153)
AMBER = (251, 191, 36)
BLUE = (96, 165, 250)

REGION = {
    "Europe": (79, 142, 247),
    "Middle East": (245, 158, 11),
    "Asia": (34, 197, 94),
    "Americas": (168, 85, 247),
    "Oceania": (6, 182, 212),
    "Africa": (249, 115, 22),
    "Global": (226, 232, 240),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(w, h, c1, c2):
    """Vertical gradient RGB image."""
    g = Image.new("RGB", (1, h))
    g.putdata([lerp(c1, c2, y / max(h - 1, 1)) for y in range(h)])
    return g.resize((w, h))


def vgrad_rgba(w, h, c1, c2):
    """Vertical gradient RGBA image (lerps all four channels)."""
    g = Image.new("RGBA", (1, h))
    g.putdata([tuple(int(c1[i] + (c2[i] - c1[i]) * y / max(h - 1, 1))
                     for i in range(4)) for y in range(h)])
    return g.resize((w, h))


def radial_glow(size, colour, inner_a=200, outer_a=0):
    """Square RGBA image: soft radial glow, brightest at centre."""
    s = size
    img = Image.new("L", (s, s), 0)
    px = img.load()
    cx = cy = s / 2.0
    for y in range(s):
        for x in range(s):
            d = math.hypot(x - cx, y - cy) / (s / 2.0)
            if d < 1:
                px[x, y] = int(inner_a + (outer_a - inner_a) * d)
    glow = Image.new("RGBA", (s, s), colour + (0,))
    glow.putalpha(img)
    return glow


def sphere(size, base, light=(0.32, 0.28)):
    """A glossy 3D sphere: radial light from top-left, rim, shadow."""
    s = size
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # base disc with vertical gradient (light top-left -> dark bottom-right)
    grad = vgrad(s, s, lerp(base, (255, 255, 255), 0.35), lerp(base, (0, 0, 0), 0.55))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse([1, 1, s - 2, s - 2], fill=255)
    lay.paste(grad, (0, 0), mask)
    # specular highlight, top-left
    hl = radial_glow(int(s * 0.62), (255, 255, 255), 210, 0)
    lay.alpha_composite(hl, (int(s * light[0] - s * 0.31), int(s * light[1] - s * 0.31)))
    # dark crescent, bottom-right (terminator)
    sh = radial_glow(int(s * 0.8), (0, 0, 0), 0, 150)
    lay.alpha_composite(sh, (int(s * 0.55), int(s * 0.55)))
    # bright rim on the top-left edge
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.arc([2, 2, s - 3, s - 3], start=140, end=320, fill=(255, 255, 255, 170), width=max(2, s // 28))
    rim = rim.filter(ImageFilter.GaussianBlur(1))
    lay.alpha_composite(rim)
    return lay


def soft_shadow(w, h, r, blur=10, alpha=170, dy=6, dx=4):
    """Blurred dark rounded-rect shadow, returned as (image, offset)."""
    sh = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20 + dx, 20 + dy, 20 + dx + w, 20 + dy + h],
                                         radius=r, fill=(0, 0, 0, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def glass_panel(base, box, r=18, fill=(24, 40, 84, 215), edge=(150, 180, 235, 90)):
    """Glass slab with gloss, bevel and drop shadow. box = (x, y, w, h)."""
    x, y, w, h = box
    sh = soft_shadow(w, h, r, blur=9, alpha=160, dy=7, dx=3)
    base.alpha_composite(sh, (x - 20, y - 20))
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=fill)
    # gloss: faint sheen across the top quarter, clipped to the rounded rect
    gloss = vgrad_rgba(w, max(h // 4, 8), (255, 255, 255, 30),
                       (255, 255, 255, 0))
    full_gloss = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    full_gloss.paste(gloss, (0, 0))
    gmask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(gmask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    lay.paste(full_gloss, (0, 0), gmask)
    # bevel: light top/left, dark bottom/right
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, outline=(255, 255, 255, 110), width=2)
    d.line([(r, h - 2), (w - r, h - 2)], fill=(0, 0, 0, 120), width=2)
    d.line([(w - 2, r), (w - 2, h - r)], fill=(0, 0, 0, 120), width=2)
    base.alpha_composite(lay, (x, y))


def card_3d(base, box, depth=7, r=14, fill=(24, 40, 84, 225)):
    """Thick 3D card: extruded side faces + glass front + shadow."""
    x, y, w, h = box
    sh = soft_shadow(w + depth, h + depth, r, blur=8, alpha=170, dy=7, dx=3)
    base.alpha_composite(sh, (x - 20, y - 20))
    # extruded sides (darker, offset down-right)
    side = Image.new("RGBA", (w + depth + 4, h + depth + 4), (0, 0, 0, 0))
    sd = ImageDraw.Draw(side)
    sd.rounded_rectangle([depth, depth, depth + w, depth + h], radius=r,
                         fill=(10, 18, 44, 235))
    base.alpha_composite(side, (x - 2, y - 2))
    glass_panel(base, (x, y, w, h), r=r, fill=fill)


def pill(base, x, y, text, font, bg, fg=(255, 255, 255)):
    """Small 3D pill chip; returns its width."""
    tw = ImageDraw.Draw(base).textlength(text, font=font)
    w = int(tw) + 12
    h = font.size + 7
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([0, 1, w - 1, h - 1], radius=h // 2, fill=bg + (235,))
    d.rounded_rectangle([0, 1, w - 1, h // 2], radius=h // 2, fill=(255, 255, 255, 60))
    d.text((6, 3), text, font=font, fill=fg + (255,))
    base.alpha_composite(lay, (x, y))
    return w


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_3d(draw, pos, text, font, fill, shadow=(0, 0, 0, 200), dy=2):
    """Embossed text: dark offset copy, then the face."""
    x, y = pos
    draw.text((x, y + dy), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)


# --- background: deep space -----------------------------------------------
img = Image.new("RGB", (W, H), BG_TOP)
bg = vgrad(W, H, BG_TOP, BG_BOT)
img.paste(bg, (0, 0))
d = ImageDraw.Draw(img, "RGBA")
# nebula washes
for (cx, cy, s, col, a) in [(820, 180, 520, (64, 90, 180), 46),
                            (140, 820, 560, (40, 70, 150), 40),
                            (520, 480, 700, (28, 50, 120), 26)]:
    neb = radial_glow(s, col, a, 0)
    img.paste(Image.new("RGB", (s, s), (0, 0, 0)), (cx - s // 2, cy - s // 2),
              Image.new("L", (s, s), 0))
    base_rgba = img.convert("RGBA")
    base_rgba.alpha_composite(neb, (cx - s // 2, cy - s // 2))
    img = base_rgba.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
# stars (fixed seed -> deterministic)
rng = random.Random(20261121)
for _ in range(260):
    sx, sy = rng.randrange(6, W - 6), rng.randrange(6, H - 6)
    r = rng.choice([1, 1, 1, 2])
    a = rng.randrange(70, 220)
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, a))
for _ in range(14):
    sx, sy = rng.randrange(10, W - 10), rng.randrange(10, H - 10)
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255, 200))
    d.line([(sx - 5, sy), (sx + 5, sy)], fill=(255, 255, 255, 110), width=1)
    d.line([(sx, sy - 5), (sx, sy + 5)], fill=(255, 255, 255, 110), width=1)

# --- the 3D globe -----------------------------------------------------------
GX, GY, GR = 512, 392, 150
# atmosphere glow + floor shadow
img_rgba = img.convert("RGBA")
glow = radial_glow(GR * 2 + 90, (70, 120, 220), 90, 0)
img_rgba.alpha_composite(glow, (GX - GR - 45, GY - GR - 45))
fsh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(fsh).ellipse([GX - GR - 20, GY + GR - 8, GX + GR + 20, GY + GR + 34],
                            fill=(0, 0, 0, 150))
img_rgba.alpha_composite(fsh.filter(ImageFilter.GaussianBlur(14)), (0, 0))
img = img_rgba.convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

LAT0, LON0 = 18.0, -30.0


def project(lat, lon):
    """Orthographic projection onto the globe; None if on the far side."""
    la, lo = math.radians(lat), math.radians(lon - LON0)
    la0 = math.radians(LAT0)
    cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo)
    if cosc <= 0.02:
        return None
    x = GR * math.cos(la) * math.sin(lo)
    y = -GR * (math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo))
    return (GX + x, GY + y)


CONTINENTS = {
    # coarse outlines (lat, lon) -- recognisable, not survey-grade
    "N America": [(70, -168), (70, -140), (66, -125), (60, -128), (54, -132),
                  (48, -126), (40, -124), (34, -120), (30, -114), (27, -110),
                  (24, -106), (19, -104), (16, -98), (14, -92), (10, -85),
                  (8, -80), (12, -79), (18, -76), (24, -80), (30, -82),
                  (35, -76), (40, -74), (44, -68), (48, -60), (52, -56),
                  (56, -62), (60, -66), (64, -58), (68, -55), (70, -62)],
    "S America": [(10, -75), (6, -78), (0, -80), (-5, -82), (-12, -78),
                  (-18, -71), (-25, -70), (-33, -71), (-42, -73), (-50, -74),
                  (-54, -68), (-52, -65), (-45, -66), (-38, -58), (-30, -58),
                  (-22, -48), (-15, -40), (-8, -35), (-3, -38), (0, -50),
                  (4, -52), (8, -58), (10, -63)],
    "Africa": [(35, -6), (35, 10), (32, 20), (30, 32), (27, 35), (20, 37),
               (15, 40), (12, 44), (10, 46), (5, 48), (0, 42), (-5, 40),
               (-10, 40), (-16, 40), (-22, 35), (-28, 32), (-33, 26),
               (-35, 20), (-30, 17), (-24, 14), (-18, 12), (-12, 13),
               (-6, 12), (0, 9), (4, 6), (6, -2), (5, -8), (9, -14),
               (14, -17), (19, -17), (25, -15), (30, -10), (33, -8)],
    "Eurasia": [(36, -9), (38, -9), (43, -9), (48, -5), (50, -2), (53, 1),
                (56, 6), (58, 8), (60, 10), (62, 6), (66, 13), (70, 19),
                (70, 29), (68, 42), (68, 55), (70, 62), (68, 72), (70, 78),
                (72, 85), (70, 95), (73, 105), (72, 115), (70, 125),
                (68, 135), (66, 145), (65, 155), (62, 165), (60, 162),
                (56, 158), (52, 150), (47, 142), (42, 136), (38, 132),
                (34, 128), (30, 122), (25, 120), (22, 114), (19, 109),
                (14, 105), (9, 100), (8, 98), (12, 95), (16, 93),
                (21, 90), (24, 86), (26, 81), (22, 76), (18, 73),
                (13, 74), (8, 77), (10, 80), (15, 81), (18, 85),
                (22, 88), (26, 90), (29, 94), (32, 97), (36, 101),
                (39, 105), (41, 110), (44, 116), (47, 121), (50, 127),
                (53, 133), (56, 138), (59, 141), (61, 137), (64, 132),
                (67, 126), (70, 120), (69, 110), (66, 100), (63, 90),
                (60, 80), (57, 72), (54, 66), (51, 60), (48, 55),
                (45, 50), (42, 48), (40, 45), (38, 42), (36, 36),
                (36, 30), (35, 25), (36, 20), (38, 15), (40, 10),
                (42, 5), (44, 0), (43, -5), (40, -8), (37, -9)],
    "Australia": [(-12, 132), (-14, 136), (-17, 141), (-20, 146), (-23, 149),
                  (-26, 151), (-29, 153), (-32, 152), (-35, 150), (-38, 146),
                  (-38, 142), (-35, 140), (-32, 138), (-29, 135), (-26, 133),
                  (-23, 131), (-20, 128), (-17, 126), (-14, 128), (-12, 130)],
    "Greenland": [(60, -45), (64, -40), (68, -32), (72, -26), (76, -22),
                  (80, -25), (82, -38), (80, -52), (77, -58), (72, -56),
                  (67, -53), (62, -48)],
}

globe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(globe)
# ocean: radial light from top-left
ocean = Image.new("RGBA", (GR * 2 + 4, GR * 2 + 4), (0, 0, 0, 0))
od = ImageDraw.Draw(ocean)
for i in range(GR, 0, -1):
    t = i / GR
    col = lerp((38, 86, 168), (8, 20, 56), t)
    od.ellipse([GR - i, GR - i, GR + i, GR + i], fill=col + (255,))
ocean = ocean.filter(ImageFilter.GaussianBlur(1))
globe.paste(ocean, (GX - GR - 2, GY - GR - 2), ocean)
# continents: relief shadow then land
land_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(land_layer)
for name, pts in CONTINENTS.items():
    proj = [project(la, lo) for la, lo in pts]
    proj = [p for p in proj if p]
    if len(proj) >= 4:
        ld.polygon(proj, fill=(46, 130, 84, 255))
land_layer = land_layer.filter(ImageFilter.GaussianBlur(1))
land_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(land_mask).ellipse([GX - GR, GY - GR, GX + GR, GY + GR], fill=255)
# relief: dark offset copy
relief = Image.new("RGBA", (W, H), (0, 0, 0, 0))
relief.paste(land_layer, (2, 3))
relief.putalpha(Image.composite(relief.split()[3], Image.new("L", (W, H), 0),
                                land_mask))
tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tmp.paste(Image.new("RGBA", (W, H), (0, 0, 0, 120)), (0, 0),
          Image.composite(land_layer.split()[3], Image.new("L", (W, H), 0), land_mask))
globe.alpha_composite(tmp, (2, 3))
globe.alpha_composite(land_layer, (0, 0))
# graticule: curved meridians + parallels, clipped to the disc
grat = Image.new("RGBA", (W, H), (0, 0, 0, 0))
grd = ImageDraw.Draw(grat)
for lon in range(-180, 181, 30):
    pts = []
    for lat in range(-75, 76, 4):
        p = project(lat, lon)
        if p:
            pts.append(p)
    if len(pts) > 2:
        grd.line(pts, fill=(255, 255, 255, 42), width=1)
for lat in range(-60, 61, 30):
    pts = []
    for lon in range(-180, 181, 4):
        p = project(lat, lon)
        if p:
            pts.append(p)
    if len(pts) > 2:
        grd.line(pts, fill=(255, 255, 255, 42), width=1)
globe.alpha_composite(grat, (0, 0))
# night terminator on the right + specular highlight top-left
term = radial_glow(GR * 2, (0, 0, 0), 0, 165)
globe.alpha_composite(term, (GX - 10, GY - GR))
hl = radial_glow(int(GR * 0.9), (255, 255, 255), 120, 0)
globe.alpha_composite(hl, (GX - GR + 8, GY - GR + 6))
# atmosphere rim
rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(rim)
rd.ellipse([GX - GR - 3, GY - GR - 3, GX + GR + 3, GY + GR + 3],
           outline=(140, 180, 255, 120), width=3)
globe.alpha_composite(rim.filter(ImageFilter.GaussianBlur(2)), (0, 0))

img_rgba = img.convert("RGBA")
img_rgba.alpha_composite(globe, (0, 0))
img = img_rgba.convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# --- orbit rings + numbered story orbs --------------------------------------
ORB_COLOURS = [REGION[s["region"]] for s in []]  # filled in below (data first)


# --- story data: all verified as Saturday 21 November 2026 ----------------
# tags: CONFIRMED = official or multiple sources; REPORTED = one credible
# source; SCHEDULED = due later on Saturday; CLAIM = one side's claim.
STORIES = [
    dict(n=1, region="Europe", tag="CONFIRMED", source="AFP",
         title="COP31 in overtime, still no deal",
         summary="Day 13 in Antalya; a third draft is due today, fossil fuels still out.",
         icon="cop31"),
    dict(n=2, region="Middle East", tag="CONFIRMED", source="CNA",
         title="Three missiles shot down over Riyadh",
         summary="Intercepted before dawn, about 02:00 AST; nobody hurt.",
         icon="missiles"),
    dict(n=3, region="Middle East", tag="CONFIRMED", source="Reuters",
         title="Two tankers hit off Oman",
         summary="Struck 50 minutes apart near Khasab; no casualties.",
         icon="tanker"),
    dict(n=4, region="Europe", tag="CONFIRMED", source="Kyiv Post",
         title="Kyiv hit again on Saturday",
         summary="Two houses burn in Podil; 117 of 148 drones downed.",
         icon="kyiv"),
    dict(n=5, region="Americas", tag="CONFIRMED", source="USGS",
         title="M6.7 quake shakes Peru",
         summary="Deep quake at 00:09 UTC in Junin; no deaths.",
         icon="quake"),
    dict(n=6, region="Asia", tag="CONFIRMED", source="AP",
         title="Jet lands safely in Davao",
         summary="Air Niugini PX19 diverts after an alert; all 146 safe.",
         icon="plane"),
    dict(n=7, region="Global", tag="SCHEDULED", source="ESA",
         title="BepiColombo fires for Mercury",
         summary="Tonight 19:24 CET, a 39-minute burn into orbit.",
         icon="mercury"),
    dict(n=8, region="Middle East", tag="CONFIRMED", source="Al Jazeera",
         title="Four killed in Gaza on Saturday",
         summary="A drone hits a food van in Gaza City; one shot in Jabalia.",
         icon="aid"),
    dict(n=9, region="Global", tag="CONFIRMED", source="Reuters",
         title="Bitcoin crashes below $56,000",
         summary="Low $55,830, weakest since September 2024.",
         icon="bitcoin"),
    dict(n=10, region="Oceania", tag="CONFIRMED", source="ESPNcricinfo",
         title="Rahul 136 puts India on top",
         summary="India 486/4 at stumps in Wellington, lead 118.",
         icon="cricket"),
    dict(n=11, region="Americas", tag="CONFIRMED", source="Formula1.com",
         title="Antonelli fastest, Verstappen on pole",
         summary="1:33.893 in qualifying; a penalty drops Antonelli to P6.",
         icon="race"),
    dict(n=12, region="Europe", tag="CONFIRMED", source="AFP",
         title="EU plans 3% Big Tech tax",
         summary="Costa's 1.78tn euro budget draft; leaders debate next week.",
         icon="euro"),
    dict(n=13, region="Asia", tag="CONFIRMED", source="Yonhap",
         title="Freight train derails in Sejong",
         summary="Five of 21 cars off the rails at 05:37; none hurt.",
         icon="train"),
]

ALSO_ON = [
    ("Iran claims it downed two US drones over Hormuz", "Al Jazeera", "CLAIM"),
    ("Zelensky: Crimea Bridge \u201cwill not stay\u201d", "NBC", "REPORTED"),
    ("Geneva: killer-robot rules pushed to 2028", "Reuters", "CONFIRMED"),
    ("Paris: sixth Saturday of cost-of-living marches", "AFP", "CONFIRMED"),
    ("Australia and China agree a formal AI dialogue", "ABC", "CONFIRMED"),
    ("Arevalo and Pavic reach the ATP doubles final", "ATP", "CONFIRMED"),
    ("Las Vegas GP under lights tonight, 20:00 local", "Formula1.com", "SCHEDULED"),
    ("SpaceX Dragon splashdown due off California", "NASA", "SCHEDULED"),
    ("Manipur liquor toll rises to 13", "", "REPORTED"),
    ("Sudan army clears 10 RSF positions", "", "REPORTED"),
    ("Modi at IIT Kharagpur", "", "REPORTED"),
    ("Adani Defence test-fires four anti-tank missiles", "", "REPORTED"),
    ("Calgary mayor seeks talks as city absorbs costs", "", "REPORTED"),
    ("Board of Peace warns Israel over Gaza rebuild", "The National", "REPORTED"),
    ("Gaza flooding deepens in winter rains", "Al Jazeera", "CONFIRMED"),
    ("Kryvyi Rih toll rises to 58 hurt (attack Fri night)", "", "CONFIRMED"),
    ("Montreal Santa Claus Parade, 74th year", "", "REPORTED"),
    ("Two teens stabbed at a Sydney mall", "", "REPORTED"),
    ("NYC flu rises a 10th straight week", "", "REPORTED"),
    ("Australia host England in a T20", "", "REPORTED"),
    ("Sao Paulo changes nine bus lines", "", "REPORTED"),
    ("Vancouver approves bus shelters for all stops", "", "REPORTED"),
]

TAG_BG = {"CONFIRMED": (16, 122, 80), "REPORTED": (176, 124, 12),
          "SCHEDULED": (30, 90, 200), "CLAIM": (178, 80, 12)}


# --- 3D icons (each returns an RGBA layer) ----------------------------------
def icon_cop31(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    g = sphere(int(s * 0.62), (38, 110, 90))
    lay.alpha_composite(g, (int(s * 0.06), int(s * 0.10)))
    d = ImageDraw.Draw(lay)
    # red thermometer: 3D stem + bulb
    d.rounded_rectangle([int(s * 0.72), int(s * 0.08), int(s * 0.86), int(s * 0.72)],
                        radius=int(s * 0.07), fill=(200, 40, 30, 255))
    d.rounded_rectangle([int(s * 0.72), int(s * 0.08), int(s * 0.79), int(s * 0.72)],
                        radius=int(s * 0.04), fill=(255, 110, 90, 255))
    d.ellipse([int(s * 0.66), int(s * 0.66), int(s * 0.92), int(s * 0.92)],
              fill=(220, 50, 38, 255))
    d.ellipse([int(s * 0.70), int(s * 0.70), int(s * 0.82), int(s * 0.82)],
              fill=(255, 120, 100, 255))
    return lay


def icon_missiles(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([2, 2, s - 3, s - 3], fill=(12, 20, 48, 255))
    # glowing interceptor arcs
    for (box, a0, a1, col, wd) in [([6, 10, s - 6, s - 6], 200, 330, (255, 200, 80), 4),
                                   ([14, 18, s - 14, s - 10], 210, 320, (255, 240, 170), 3),
                                   ([22, 26, s - 22, s - 18], 220, 310, (255, 255, 255), 2)]:
        d.arc(box, start=a0, end=a1, fill=col + (255,), width=wd)
    # burst where they meet
    burst = radial_glow(int(s * 0.4), (255, 220, 120), 230, 0)
    lay.alpha_composite(burst, (int(s * 0.62), int(s * 0.30)))
    # shield dome at the bottom
    d.pieslice([int(s * 0.22), int(s * 0.62), int(s * 0.78), int(s * 1.02)],
               start=180, end=360, fill=(70, 130, 220, 255))
    d.pieslice([int(s * 0.22), int(s * 0.62), int(s * 0.50), int(s * 1.02)],
               start=180, end=360, fill=(130, 180, 255, 255))
    return lay


def icon_tanker(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # waves: layered glossy curves
    for i, y in enumerate([int(s * 0.78), int(s * 0.86), int(s * 0.94)]):
        d.arc([4, y - 8, s - 4, y + 14], start=0, end=180,
              fill=(60 + i * 30, 110 + i * 25, 200, 255), width=4)
    # hull: 3D box with shading
    d.polygon([(int(s * 0.10), int(s * 0.52)), (int(s * 0.90), int(s * 0.52)),
               (int(s * 0.82), int(s * 0.74)), (int(s * 0.18), int(s * 0.74))],
              fill=(150, 40, 30, 255))
    d.polygon([(int(s * 0.10), int(s * 0.52)), (int(s * 0.90), int(s * 0.52)),
               (int(s * 0.86), int(s * 0.60)), (int(s * 0.14), int(s * 0.60))],
              fill=(205, 70, 50, 255))
    # deck + bridge
    d.rectangle([int(s * 0.16), int(s * 0.40), int(s * 0.84), int(s * 0.52)],
                fill=(220, 220, 220, 255))
    d.rectangle([int(s * 0.62), int(s * 0.26), int(s * 0.80), int(s * 0.40)],
                fill=(240, 240, 240, 255))
    d.rectangle([int(s * 0.65), int(s * 0.30), int(s * 0.77), int(s * 0.37)],
                fill=(40, 90, 160, 255))
    # funnel with smoke
    d.rectangle([int(s * 0.24), int(s * 0.30), int(s * 0.34), int(s * 0.42)],
                fill=(245, 190, 60, 255))
    smoke = radial_glow(int(s * 0.3), (200, 200, 200), 120, 0)
    lay.alpha_composite(smoke, (int(s * 0.20), int(s * 0.06)))
    return lay


def icon_kyiv(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([2, 2, s - 3, s - 3], fill=(10, 16, 40, 255))
    # skyline: 3D boxes with lit windows
    for (bx, bw, bh, col) in [(0.08, 0.16, 0.42, (40, 60, 110)),
                              (0.28, 0.18, 0.58, (30, 48, 95)),
                              (0.50, 0.15, 0.46, (40, 60, 110)),
                              (0.68, 0.20, 0.62, (28, 44, 88))]:
        x0, w0, h0 = int(s * bx), int(s * bw), int(s * bh)
        d.rectangle([x0, s - h0, x0 + w0, s - 6], fill=col + (255,))
        d.rectangle([x0, s - h0, x0 + w0 // 2, s - 6], fill=lerp(col, (255, 255, 255), 0.25) + (255,))
        for wy in range(s - h0 + 8, s - 12, 12):
            for wx in range(x0 + 4, x0 + w0 - 4, 9):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 110, 255))
    # explosion glow top-right
    burst = radial_glow(int(s * 0.55), (255, 170, 60), 235, 0)
    lay.alpha_composite(burst, (int(s * 0.60), int(s * 0.02)))
    d = ImageDraw.Draw(lay)
    d.ellipse([int(s * 0.72), int(s * 0.14), int(s * 0.86), int(s * 0.28)],
              fill=(255, 230, 150, 255))
    return lay


def icon_quake(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # cracked ground slab: 3D box
    d.polygon([(int(s * 0.08), int(s * 0.62)), (int(s * 0.92), int(s * 0.62)),
               (int(s * 0.82), int(s * 0.90)), (int(s * 0.18), int(s * 0.90))],
              fill=(120, 95, 60, 255))
    d.polygon([(int(s * 0.08), int(s * 0.62)), (int(s * 0.92), int(s * 0.62)),
               (int(s * 0.88), int(s * 0.70)), (int(s * 0.12), int(s * 0.70))],
              fill=(170, 140, 90, 255))
    # crack lines
    d.line([(int(s * 0.30), int(s * 0.64)), (int(s * 0.42), int(s * 0.74)),
            (int(s * 0.38), int(s * 0.84))], fill=(60, 45, 25, 255), width=2)
    d.line([(int(s * 0.65), int(s * 0.64)), (int(s * 0.58), int(s * 0.76)),
            (int(s * 0.66), int(s * 0.86))], fill=(60, 45, 25, 255), width=2)
    # shockwave rings rising from the slab
    for i, (ry, rx, a) in enumerate([(0.52, 0.30, 220), (0.40, 0.38, 170),
                                     (0.28, 0.46, 120), (0.16, 0.54, 80)]):
        d.ellipse([int(s * (0.5 - rx)), int(s * ry), int(s * (0.5 + rx)),
                   int(s * (ry + 0.10))], outline=(255, 120, 60, a), width=3)
    return lay


def icon_plane(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([2, 2, s - 3, s - 3], fill=(14, 32, 70, 255))
    # runway in perspective
    d.polygon([(int(s * 0.42), int(s * 0.98)), (int(s * 0.58), int(s * 0.98)),
               (int(s * 0.52), int(s * 0.66)), (int(s * 0.48), int(s * 0.66))],
              fill=(150, 150, 160, 255))
    # fuselage: glossy capsule
    d.rounded_rectangle([int(s * 0.14), int(s * 0.40), int(s * 0.86), int(s * 0.56)],
                        radius=int(s * 0.08), fill=(225, 230, 240, 255))
    d.rounded_rectangle([int(s * 0.14), int(s * 0.40), int(s * 0.86), int(s * 0.47)],
                        radius=int(s * 0.07), fill=(255, 255, 255, 255))
    # nose + cockpit
    d.polygon([(int(s * 0.86), int(s * 0.42)), (int(s * 0.97), int(s * 0.48)),
               (int(s * 0.86), int(s * 0.54))], fill=(200, 210, 225, 255))
    d.ellipse([int(s * 0.78), int(s * 0.42), int(s * 0.86), int(s * 0.50)],
              fill=(40, 90, 160, 255))
    # wings (shaded polygons) + tail
    d.polygon([(int(s * 0.42), int(s * 0.54)), (int(s * 0.58), int(s * 0.54)),
               (int(s * 0.66), int(s * 0.78)), (int(s * 0.50), int(s * 0.78))],
              fill=(180, 190, 205, 255))
    d.polygon([(int(s * 0.16), int(s * 0.42)), (int(s * 0.24), int(s * 0.42)),
               (int(s * 0.18), int(s * 0.26)), (int(s * 0.12), int(s * 0.26))],
              fill=(200, 210, 225, 255))
    # green check orb (safe landing)
    chk = sphere(int(s * 0.26), (34, 160, 90))
    lay.alpha_composite(chk, (int(s * 0.68), int(s * 0.66)))
    dd = ImageDraw.Draw(lay)
    dd.line([(int(s * 0.73), int(s * 0.79)), (int(s * 0.77), int(s * 0.83)),
             (int(s * 0.84), int(s * 0.74))], fill=(255, 255, 255, 255), width=3)
    return lay


def icon_mercury(s):
    """Real NASA MESSENGER photo of Mercury, rendered as a 3D sphere."""
    photo = Image.open(os.path.join(HERE, "photos", "mercury-true-color.jpg"))
    photo = photo.convert("RGB").resize((s, s), Image.LANCZOS)
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse([1, 1, s - 2, s - 2], fill=255)
    lay.paste(photo, (0, 0), mask)
    # 3D shading: highlight top-left, terminator bottom-right, rim
    hl = radial_glow(int(s * 0.6), (255, 255, 255), 110, 0)
    lay.alpha_composite(hl, (int(s * 0.02), int(s * 0.00)))
    sh = radial_glow(int(s * 0.85), (0, 0, 0), 0, 150)
    lay.alpha_composite(sh, (int(s * 0.45), int(s * 0.45)))
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(rim).arc([2, 2, s - 3, s - 3], start=140, end=320,
                            fill=(255, 255, 255, 160), width=max(2, s // 30))
    lay.alpha_composite(rim.filter(ImageFilter.GaussianBlur(1)))
    # spacecraft + burn flare
    d = ImageDraw.Draw(lay)
    d.polygon([(int(s * 0.62), int(s * 0.30)), (int(s * 0.78), int(s * 0.36)),
               (int(s * 0.62), int(s * 0.44))], fill=(230, 235, 245, 255))
    d.rectangle([int(s * 0.55), int(s * 0.33), int(s * 0.64), int(s * 0.41)],
                fill=(200, 210, 225, 255))
    flare = radial_glow(int(s * 0.34), (255, 200, 90), 240, 0)
    lay.alpha_composite(flare, (int(s * 0.42), int(s * 0.24)))
    return lay


def icon_aid(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    g = sphere(int(s * 0.88), (225, 228, 235))
    lay.alpha_composite(g, (int(s * 0.06), int(s * 0.06)))
    d = ImageDraw.Draw(lay)
    # red cross, slightly embossed
    cx, cy, w = s // 2, s // 2, int(s * 0.13)
    d.rectangle([cx - w, cy - int(s * 0.26), cx + w, cy + int(s * 0.26)],
                fill=(200, 30, 25, 255))
    d.rectangle([cx - int(s * 0.26), cy - w, cx + int(s * 0.26), cy + w],
                fill=(200, 30, 25, 255))
    d.rectangle([cx - w, cy - int(s * 0.26), cx - w // 2, cy + int(s * 0.26)],
                fill=(255, 90, 80, 255))
    d.rectangle([cx - int(s * 0.26), cy - w, cx + int(s * 0.26), cy - w // 2],
                fill=(255, 90, 80, 255))
    return lay


def icon_bitcoin(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # coin rim: darker offset ellipse behind = thickness
    d.ellipse([int(s * 0.06), int(s * 0.10), int(s * 0.94), int(s * 0.98)],
              fill=(140, 95, 10, 255))
    # face: radial gold gradient
    face = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    fd = ImageDraw.Draw(face)
    for i in range(int(s * 0.44), 0, -1):
        t = i / (s * 0.44)
        col = lerp((255, 215, 90), (190, 130, 20), t)
        fd.ellipse([s // 2 - i, s // 2 - i - 2, s // 2 + i, s // 2 + i - 2],
                   fill=col + (255,))
    lay.alpha_composite(face, (0, 0))
    # shine + inner ring
    hl = radial_glow(int(s * 0.5), (255, 255, 255), 130, 0)
    lay.alpha_composite(hl, (int(s * 0.10), int(s * 0.06)))
    d = ImageDraw.Draw(lay)
    d.ellipse([int(s * 0.16), int(s * 0.14), int(s * 0.84), int(s * 0.82)],
              outline=(150, 105, 15, 255), width=2)
    f = ff("DejaVuSans-Bold.ttf", int(s * 0.34))
    txt = "BTC"
    tw = d.textlength(txt, font=f)
    d.text((s // 2 - tw / 2 + 1, s // 2 - int(s * 0.17) + 2), txt, font=f,
           fill=(120, 80, 5, 255))
    d.text((s // 2 - tw / 2, s // 2 - int(s * 0.17)), txt, font=f,
           fill=(255, 240, 180, 255))
    return lay


def icon_cricket(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    g = sphere(int(s * 0.88), (178, 34, 34))
    lay.alpha_composite(g, (int(s * 0.06), int(s * 0.06)))
    d = ImageDraw.Draw(lay)
    # seam: curved dashed white line
    pts = []
    for a in range(200, 340, 6):
        ang = math.radians(a)
        pts.append((s // 2 + int(s * 0.36 * math.cos(ang)),
                    s // 2 + int(s * 0.30 * math.sin(ang)) - int(s * 0.04)))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(255, 255, 255, 230), width=2)
    return lay


def icon_race(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([2, 2, s - 3, s - 3], fill=(12, 18, 42, 255))
    # speed lines
    for y in [int(s * 0.30), int(s * 0.42), int(s * 0.54)]:
        d.line([(int(s * 0.04), y), (int(s * 0.30), y)], fill=(120, 150, 220, 160), width=3)
    # car body: metallic gradient polygon
    body = [(int(s * 0.14), int(s * 0.62)), (int(s * 0.20), int(s * 0.48)),
            (int(s * 0.42), int(s * 0.44)), (int(s * 0.58), int(s * 0.50)),
            (int(s * 0.86), int(s * 0.56)), (int(s * 0.88), int(s * 0.62))]
    d.polygon(body, fill=(200, 30, 40, 255))
    d.polygon([(int(s * 0.20), int(s * 0.48)), (int(s * 0.42), int(s * 0.44)),
               (int(s * 0.58), int(s * 0.50)), (int(s * 0.52), int(s * 0.52)),
               (int(s * 0.40), int(s * 0.52)), (int(s * 0.24), int(s * 0.52))],
              fill=(255, 120, 120, 255))
    # cockpit
    d.polygon([(int(s * 0.44), int(s * 0.46)), (int(s * 0.56), int(s * 0.50)),
               (int(s * 0.54), int(s * 0.54)), (int(s * 0.44), int(s * 0.52))],
              fill=(30, 40, 70, 255))
    # wheels: 3D spheres with hubs
    for wx in [int(s * 0.28), int(s * 0.72)]:
        wh = sphere(int(s * 0.22), (20, 20, 28))
        lay.alpha_composite(wh, (wx - int(s * 0.11), int(s * 0.58)))
        dd = ImageDraw.Draw(lay)
        dd.ellipse([wx - int(s * 0.05), int(s * 0.64), wx + int(s * 0.05),
                    int(s * 0.74)], fill=(180, 190, 210, 255))
    return lay


def icon_euro(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    g = sphere(int(s * 0.88), (30, 80, 180))
    lay.alpha_composite(g, (int(s * 0.06), int(s * 0.06)))
    d = ImageDraw.Draw(lay)
    # stars: small gold dots around the top
    for a in range(-60, 61, 30):
        ang = math.radians(a - 90)
        sx = s // 2 + int(s * 0.33 * math.cos(ang))
        sy = s // 2 + int(s * 0.33 * math.sin(ang))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 90, 255))
    f = ff("DejaVuSans-Bold.ttf", int(s * 0.42))
    txt = "\u20ac"
    tw = d.textlength(txt, font=f)
    d.text((s // 2 - tw / 2 + 1, s // 2 - int(s * 0.21) + 2), txt, font=f,
           fill=(10, 40, 110, 255))
    d.text((s // 2 - tw / 2, s // 2 - int(s * 0.21)), txt, font=f,
           fill=(255, 255, 255, 255))
    return lay


def icon_train(s):
    lay = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # rails converging in perspective
    d.polygon([(int(s * 0.30), int(s * 0.98)), (int(s * 0.70), int(s * 0.98)),
               (int(s * 0.56), int(s * 0.70)), (int(s * 0.44), int(s * 0.70))],
              fill=(120, 120, 135, 255))
    d.line([(int(s * 0.36), int(s * 0.98)), (int(s * 0.47), int(s * 0.70))],
           fill=(200, 200, 210, 255), width=3)
    d.line([(int(s * 0.64), int(s * 0.98)), (int(s * 0.53), int(s * 0.70))],
           fill=(200, 200, 210, 255), width=3)
    # locomotive front: 3D box
    d.rounded_rectangle([int(s * 0.20), int(s * 0.22), int(s * 0.80), int(s * 0.72)],
                        radius=int(s * 0.06), fill=(30, 90, 170, 255))
    d.rounded_rectangle([int(s * 0.20), int(s * 0.22), int(s * 0.50), int(s * 0.72)],
                        radius=int(s * 0.06), fill=(70, 140, 220, 255))
    # windshield with gloss
    d.rounded_rectangle([int(s * 0.28), int(s * 0.30), int(s * 0.72), int(s * 0.48)],
                        radius=int(s * 0.04), fill=(15, 25, 50, 255))
    d.polygon([(int(s * 0.30), int(s * 0.32)), (int(s * 0.48), int(s * 0.32)),
               (int(s * 0.38), int(s * 0.46)), (int(s * 0.30), int(s * 0.46))],
              fill=(140, 190, 255, 255))
    # headlights
    for hx in [int(s * 0.30), int(s * 0.66)]:
        d.ellipse([hx, int(s * 0.56), hx + int(s * 0.08), int(s * 0.64)],
                  fill=(255, 240, 160, 255))
    return lay


ICONS = {"cop31": icon_cop31, "missiles": icon_missiles, "tanker": icon_tanker,
         "kyiv": icon_kyiv, "quake": icon_quake, "plane": icon_plane,
         "mercury": icon_mercury, "aid": icon_aid, "bitcoin": icon_bitcoin,
         "cricket": icon_cricket, "race": icon_race, "euro": icon_euro,
         "train": icon_train}


# --- compose ----------------------------------------------------------------
img = img.convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

# title plaque: floating glass slab
glass_panel(img, (28, 20, 968, 78), r=20, fill=(20, 34, 74, 225))
d = ImageDraw.Draw(img, "RGBA")
title = "SATURDAY 21 NOVEMBER 2026"
tw = d.textlength(title, font=SERIF)
text_3d(d, (512 - tw / 2, 27), title, SERIF, (255, 255, 255, 255))
d.line([(392, 72), (632, 72)], fill=GOLD + (255,), width=3)
d.line([(392, 74), (632, 74)], fill=(0, 0, 0, 160), width=1)
sub = "THE WORLD IN ONE PICTURE  \u00b7  35 STORIES  \u00b7  7 REGIONS  \u00b7  ALL FROM THIS SATURDAY"
sw = d.textlength(sub, font=B13)
d.text((512 - sw / 2, 80), sub, font=B13, fill=(200, 214, 245, 255))

# orbit rings (thin, in front of the globe like a gyroscope) + story orbs
def ellipse_pt(t_deg, rx, ry, rot_deg):
    t = math.radians(t_deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    r = math.radians(rot_deg)
    return (GX + x * math.cos(r) - y * math.sin(r),
            GY + x * math.sin(r) + y * math.cos(r))


for (rx, ry, rot) in [(205, 120, -20), (205, 120, 20)]:
    pts = [ellipse_pt(t, rx, ry, rot) for t in range(0, 361, 3)]
    d.line(pts, fill=(150, 185, 255, 110), width=2)
RING1 = [0, 30, 150, 180, 210, 330, 345]
RING2 = [15, 165, 195, 345, 30, 210]
for i, st in enumerate(STORIES):
    if i < 7:
        ox, oy = ellipse_pt(RING1[i], 205, 120, -20)
    else:
        ox, oy = ellipse_pt(RING2[i - 7], 205, 120, 20)
    orb = sphere(24, REGION[st["region"]])
    img.alpha_composite(orb, (int(ox - 12), int(oy - 12)))
    d = ImageDraw.Draw(img, "RGBA")
    num = str(st["n"])
    nw = d.textlength(num, font=B9)
    d.text((ox - nw / 2, oy - 6), num, font=B9, fill=(255, 255, 255, 255))


def draw_tile(st, box, kind):
    x, y, w, h = box
    card_3d(img, box, depth=7, r=14, fill=(24, 40, 84, 228))
    d = ImageDraw.Draw(img, "RGBA")
    col = REGION[st["region"]]
    if kind == "side":
        icon = ICONS[st["icon"]](62)
        img.alpha_composite(icon, (x + 12, y + 34))
        # number badge: small 3D sphere, top-left
        badge = sphere(26, col)
        img.alpha_composite(badge, (x + 10, y + 8))
        d = ImageDraw.Draw(img, "RGBA")
        nb = str(st["n"])
        d.text((x + 10 + 13 - d.textlength(nb, font=B10) / 2, y + 14), nb,
               font=B10, fill=(255, 255, 255, 255))
        tx = x + 84
        twd = w - 96
        lines = wrap(d, st["title"], B14, twd)
        ly = y + 12
        for ln in lines[:2]:
            text_3d(d, (tx, ly), ln, B14, INK + (255,))
            ly += 17
        sl = wrap(d, st["summary"], R10, twd)
        ly = y + 52
        for ln in sl[:3]:
            d.text((tx, ly), ln, font=R10, fill=DIM + (255,))
            ly += 12
        # source line (tag pill is painted right-aligned below, after all tiles)
        src = st["source"] + "  \u00b7  " + st["region"].upper()
        d.text((tx, y + h - 20), src, font=B9, fill=FAINT + (255,))
        d = ImageDraw.Draw(img, "RGBA")
    else:
        icon = ICONS[st["icon"]](50)
        img.alpha_composite(icon, (x + (w - 50) // 2, y + 8))
        badge = sphere(24, col)
        img.alpha_composite(badge, (x + 6, y + 6))
        d = ImageDraw.Draw(img, "RGBA")
        nb = str(st["n"])
        d.text((x + 6 + 12 - d.textlength(nb, font=B9) / 2, y + 11), nb,
               font=B9, fill=(255, 255, 255, 255))
        lines = wrap(d, st["title"], B12, w - 16)
        ly = y + 58
        for ln in lines[:2]:
            text_3d(d, (x + 8, ly), ln, B12, INK + (255,))
            ly += 15
        sl = wrap(d, st["summary"], R9, w - 16)
        ly = y + 92
        for ln in sl[:2]:
            d.text((x + 8, ly), ln, font=R9, fill=DIM + (255,))
            ly += 11
        d.text((x + 8, y + h - 15), st["source"], font=B8, fill=FAINT + (255,))


# side tiles: stories 1-4 left, 5-8 right
for j, st in enumerate(STORIES[:4]):
    draw_tile(st, (18, 112 + j * 138, 300, 128), "side")
for j, st in enumerate(STORIES[4:8]):
    draw_tile(st, (706, 112 + j * 138, 300, 128), "side")
# bottom tiles: stories 9-13
for j, st in enumerate(STORIES[8:13]):
    draw_tile(st, (18 + j * 199, 668, 190, 136), "bottom")

# fix tag pills: the pill() calls above drew at the tile's right edge minus
# nothing; repaint them right-aligned (measure, then place)
for j, st in enumerate(STORIES[:4]):
    x, y, w, h = 18, 112 + j * 138, 300, 128
    pw = ImageDraw.Draw(img, "RGBA").textlength(st["tag"], font=B8) + 12
    pill(img, x + w - int(pw) - 10, y + h - 22, st["tag"], B8, TAG_BG[st["tag"]])
for j, st in enumerate(STORIES[4:8]):
    x, y, w, h = 706, 112 + j * 138, 300, 128
    pw = ImageDraw.Draw(img, "RGBA").textlength(st["tag"], font=B8) + 12
    pill(img, x + w - int(pw) - 10, y + h - 22, st["tag"], B8, TAG_BG[st["tag"]])
for j, st in enumerate(STORIES[8:13]):
    x, y, w, h = 18 + j * 199, 668, 190, 136
    pw = ImageDraw.Draw(img, "RGBA").textlength(st["tag"], font=B8) + 12
    pill(img, x + w - int(pw) - 8, y + h - 17, st["tag"], B8, TAG_BG[st["tag"]])

# --- ALSO ON deck: fanned glass slab with 3D sphere bullets -----------------
glass_panel(img, (18, 814, 988, 110), r=16, fill=(20, 34, 74, 215))
d = ImageDraw.Draw(img, "RGBA")
d.text((34, 822), "MORE FROM SATURDAY  \u2014  22 STORIES", font=B10,
       fill=(200, 214, 245, 255))
cols = [(34, ALSO_ON[0:8]), (352, ALSO_ON[8:16]), (670, ALSO_ON[16:22])]
for (cx, items) in cols:
    for k, (txt, src, tag) in enumerate(items):
        ry = 844 + k * 10
        n = ALSO_ON.index((txt, src, tag)) + 14
        # region colour per item is not stored; use gold bullets for all
        dot = sphere(12, (120, 150, 220))
        img.alpha_composite(dot, (cx, ry))
        d = ImageDraw.Draw(img, "RGBA")
        label = str(n) + "  " + txt + (" (" + src + ")" if src else "")
        if d.textlength(label, font=R9) > 300:
            while d.textlength(label + "\u2026", font=R9) > 300 and len(label) > 10:
                label = label[:-1]
            label += "\u2026"
        d.text((cx + 16, ry), label, font=R9, fill=INK + (255,))

# --- DATE CHECK: red-tinted glass panel + 3D seal ---------------------------
glass_panel(img, (18, 932, 988, 72), r=14, fill=(58, 16, 22, 215),
            edge=(255, 120, 100, 120))
d = ImageDraw.Draw(img, "RGBA")
d.text((34, 939), "DATE CHECK  \u2014  LEFT OUT ON PURPOSE", font=B11,
       fill=(255, 110, 90, 255))
dc = ("Fri 20 Nov: Kyiv barrage, Poland missiles, Wall Street slide, Anthropic IPO, "
      "UK\u2013EU deal, Akvan landfall, GTA VI $3.79bn, Palisades verdict.  Thu 19 Nov: "
      "Shenzhen summit, ICJ Myanmar ruling.  18 Nov: Voyager 1 one light-day out.  "
      "11 Nov: Kenya Ebola.  NOT YET: COP31 final text, BepiColombo burn, ATP semis, "
      "Vegas GP, Dragon splashdown.  Riyadh count is 3 \u2014 the 2 Jizan intercepts "
      "were Friday.  HOW WE CHECKED: CONFIRMED = official or multiple sources \u00b7 "
      "REPORTED = one credible source \u00b7 SCHEDULED = due tonight.")
lines = wrap(d, dc, R9, 940)
ly = 956
for ln in lines[:4]:
    d.text((34, ly), ln, font=R9, fill=(235, 220, 220, 255))
    ly += 11
# 3D seal overlapping the panel's top-right corner
seal = sphere(44, (200, 40, 30))
img.alpha_composite(seal, (946, 912))
d = ImageDraw.Draw(img, "RGBA")
d.line([(960, 934), (966, 941), (978, 926)], fill=(255, 255, 255, 255), width=4)

# --- footer ------------------------------------------------------------------
foot = ("Sources: AFP \u00b7 Reuters \u00b7 AP \u00b7 Al Jazeera \u00b7 USGS \u00b7 ESPNcricinfo "
        "\u00b7 Formula1.com \u00b7 Yonhap \u00b7 CNA \u00b7 Kyiv Post \u00b7 Ukrinform \u00b7 ABC "
        "\u00b7 ATP \u00b7 NASA  \u2014  every story dated Saturday 21 November 2026")
fw = d.textlength(foot, font=R85)
d.text((512 - fw / 2, 1009), foot, font=R85, fill=FAINT + (255,))

img.convert("RGB").save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
