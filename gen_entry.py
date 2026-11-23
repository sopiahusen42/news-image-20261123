#!/usr/bin/env python3
"""Build-time generator for entry.png (world news of Monday 23 November 2026).

Deterministic: no clock reads, no randomness, no network. Uses PIL, which is
available on the build machine only. The shipped main.py never imports PIL.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 40
PAPER = (247, 241, 230)
INK = (20, 20, 20)
RED = (179, 32, 44)
SLATE = (60, 71, 83)
TEAL = (31, 111, 107)
CARD_BG = (251, 246, 236)
CARD_EDGE = (216, 206, 190)
RULE = (150, 140, 124)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_fcache = {}


def font(path, size):
    key = (path, size)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(path, size)
    return _fcache[key]


def tw(draw, text, f, tracking=0):
    if not text:
        return 0
    w = draw.textlength(text, font=f)
    if tracking:
        w += tracking * (len(text) - 1)
    return w


def draw_tracked(draw, xy, text, f, fill, tracking=0):
    x, y = xy
    tracking = int(round(tracking))
    if not tracking:
        draw.text((x, y), text, font=f, fill=fill)
        return
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if tw(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def balanced(draw, text, f, max_w, max_lines=2):
    """Wrap so no line overflows. Words are NEVER dropped: if the text needs
    more than max_lines the full wrap is returned and the caller shrinks."""
    lines = wrap(draw, text, f, max_w)
    if len(lines) < 2 or len(lines) > max_lines:
        return lines
    words = text.split()
    if len(words) < 4:
        return lines
    best, best_span = lines, None
    for k in range(1, len(words)):
        a, b = " ".join(words[:k]), " ".join(words[k:])
        if tw(draw, a, f) > max_w or tw(draw, b, f) > max_w:
            continue
        span = max(tw(draw, a, f), tw(draw, b, f))
        if best_span is None or span < best_span:
            best, best_span = [a, b], span
    return best


def fit_lines(draw, text, path, max_w, hi, lo, max_lines=2, tracking=0):
    """Largest size in [lo, hi] whose balanced wrap needs <= max_lines lines.

    A two-line wrap whose last line is a short orphan word is rejected so the
    block shrinks until the break is balanced; no one-word tail lines.
    """
    size = lo
    for s in range(hi, lo - 1, -1):
        f = font(path, s)
        lines = balanced(draw, text, f, max_w, max_lines)
        if len(lines) > max_lines:
            continue
        if any(tw(draw, ln, f, tracking) > max_w for ln in lines):
            continue
        if len(lines) == 2:
            tail = lines[1].split()
            if len(tail) == 1 and tw(draw, lines[1], f, tracking) < 0.42 * max_w:
                continue
        size = s
        break
    f = font(path, size)
    return f, size, balanced(draw, text, f, max_w, max_lines)


HEROES = [
    ("CLIMATE", "COP31 ENDS WITHOUT A DEAL",
     "Two weeks in Antalya close with no fossil-fuel text.", TEAL),
    ("MIDDLE EAST", "IRAN DRONE HITS BAHRAIN SITE",
     "Manama calls the strike \u201cheinous Iranian aggression\u201d.", RED),
    ("SOUTH ASIA", "MODI MEETS NEPAL'S NEW PM",
     "Balendra Shah, 36, in Delhi for energy, rail deals.", SLATE),
    ("UKRAINE", "SLOVIANSK SHELLED; TWO KILLED",
     "Overnight strike in Donetsk; Zelensky warns on Odesa power.", RED),
    ("ASIA", "INDONESIA FACTORY FIRE: 37 MISSING",
     "Rescue resumes at the candy plant west of Jakarta.", TEAL),
    ("AFRICA", "DRONE STRIKE HITS RUSSIAN CORVETTE",
     "A suspected Ukrainian attack at the Benghazi naval base.", SLATE),
]

ALSO = [
    "Houthis claim a hit on Saudi's Rabigh refinery",
    "Seoul moves to steady the KOSPI at a 10-month low",
    "Poland: Russia twice tried to kill rapper Kyivstoner",
    "Bangladesh: 95 BGB platoons out as arson spreads",
    "Miley Cyrus marries drummer Maxx Morando",
]
ALSO_PREFIX = ["Gulf: ", "", "", "", ""]

FOOT1 = ("Wire compiled 00:30 UTC, Monday 23 November 2026 \u2014 "
         "events of 23 November, any time zone.")
FOOT2 = ("Sources: Reuters, AP, AFP, MFA India, SBS, Dawn, 1News, Al Jazeera. "
         "Built by an AI agent for make.fun.")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- masthead ----------------
    y = 34
    kick = font(SANS_B, 22)
    draw_tracked(d, (M, y), "THE WORLD \u00b7 MONDAY", kick, RED, tracking=4)
    y += 32

    # giant date: "23" in red, "NOVEMBER 2026" in ink, one measured line
    part_a, part_b = "23", "NOVEMBER 2026"
    best = 60
    for s in range(118, 59, -1):
        f = font(SERIF_B, s)
        total = tw(d, part_a, f) + tw(d, " ", f) + tw(d, part_b, f)
        if total <= W - 2 * M:
            best = s
            break
    fdate = font(SERIF_B, best)
    x = M
    d.text((x, y), part_a, font=fdate, fill=RED)
    x += tw(d, part_a, fdate) + tw(d, " ", fdate) * 0.75
    d.text((x, y), part_b, font=fdate, fill=INK)
    asc, desc = fdate.getmetrics()
    date_h = asc + desc
    y += date_h + 2

    fdeck = font(SERIF, 23)
    deck = "One page, one day: the stories the wire carried on Monday"
    d.text((M, y), deck, font=fdeck, fill=SLATE)
    y += 30
    d.rectangle([M, y, W - M, y + 5], fill=RED)
    mast_bottom = y + 5

    # ---------------- bottom-anchored blocks ----------------
    ffoot = font(SANS, 17)
    foot2_y = H - 30 - 21
    foot1_y = foot2_y - 24
    d.line([M, foot1_y - 12, W - M, foot1_y - 12], fill=RULE, width=1)

    fstrip = font(SANS, 17)
    strip_lead = 21
    strip_top = foot1_y - 12 - 10 - 5 * strip_lead
    label_y = strip_top - 30

    # ---------------- cards ----------------
    grid_top = mast_bottom + 16
    grid_bottom = label_y - 16
    gap = 14
    card_h = (grid_bottom - grid_top - 2 * gap) // 3
    card_w = (W - 2 * M - 22) // 2
    xs = [M, W - M - card_w]

    fkick = font(SANS_B, 18)
    ffollow = font(SANS, 18)

    for i, (kicker, head, follow, accent) in enumerate(HEROES):
        col, row = i % 2, i // 2
        cx = xs[col]
        cy = grid_top + row * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w - 1, cy + card_h - 1], fill=CARD_BG,
                    outline=CARD_EDGE, width=1)
        d.rectangle([cx, cy, cx + 5, cy + card_h - 1], fill=accent)

        pad_l = cx + 18
        usable = card_w - 34

        ky = cy + 12
        draw_tracked(d, (pad_l, ky), kicker, fkick, RED, tracking=1.4)
        ky += 25

        fh, hs, hlines = fit_lines(d, head, SERIF_B, usable, 33, 24, max_lines=2)
        lead = int(hs * 1.16)
        for ln in hlines:
            d.text((pad_l, ky), ln, font=fh, fill=INK)
            ky += lead

        # follow line(s) sit directly under the headline, fixed gap, balanced
        flines = balanced(d, follow, ffollow, usable, max_lines=2)
        fy = ky + 5
        for ln in flines:
            d.text((pad_l, fy), ln, font=ffollow, fill=SLATE)
            fy += 21

    # ---------------- also today ----------------
    draw_tracked(d, (M, label_y), "ALSO TODAY", font(SANS_B, 19), RED, tracking=2)
    lab_w = tw(d, "ALSO TODAY", font(SANS_B, 19), 2)
    d.line([M + lab_w + 12, label_y + 11, W - M, label_y + 11], fill=CARD_EDGE, width=2)
    sy = strip_top
    for i, item in enumerate(ALSO):
        text = "\u2014 " + ALSO_PREFIX[i] + item
        d.text((M, sy), text, font=fstrip, fill=INK)
        sy += strip_lead

    # ---------------- footer ----------------
    d.text((M, foot1_y), FOOT1, font=ffoot, fill=SLATE)
    d.text((M, foot2_y), FOOT2, font=ffoot, fill=SLATE)

    img.save("entry.png", "PNG", optimize=True)

    print("date font size:", best, "px")
    for (kicker, head, follow, _c) in HEROES:
        _f, s, lines = fit_lines(d, head, SERIF_B, card_w - 34, 33, 24)
        print(f"  headline {s}px / {len(lines)} line(s): {head}")
    print("card:", card_w, "x", card_h, "gap", gap)
    print("strip 17px, footer 17px, kickers 18px, min font 17px")


if __name__ == "__main__":
    build()
    im = Image.open("entry.png")
    import os
    print("saved entry.png", im.size, im.mode, os.path.getsize("entry.png"), "bytes")
