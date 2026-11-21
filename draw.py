#!/usr/bin/env python3
"""Draw the Saturday 21 November 2026 world-news infographic.

One 1024x1024 PNG: a header naming the day, a 2x2 grid of four
story panels, and a source footer. Deterministic: no timestamps,
no randomness, fixed font paths, so repeated runs are byte-identical.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (13, 27, 46)
PANEL_BG = (25, 46, 70)
PANEL_LINE = (48, 78, 108)
GOLD = (212, 175, 55)
WHITE = (245, 245, 240)
MUTED = (168, 184, 200)

STORIES = [
    {
        "tag": "STRIKES",
        "accent": (214, 69, 65),
        "head": "Russia hits Ukraine with 400+ drones",
        "body": "Over 110 missiles fired overnight; at least 8 killed in Kyiv. "
                "Two missiles land in Poland; PM Tusk calls it a deliberate "
                "provocation.",
    },
    {
        "tag": "MARKETS",
        "accent": (66, 160, 90),
        "head": "AI sell-off sinks US stocks",
        "body": "The S&P 500 drops 3.7% into correction territory and the "
                "Nasdaq falls 5.3% as AI shares slide.",
    },
    {
        "tag": "QUAKE",
        "accent": (222, 158, 44),
        "head": "Strong quake shakes Peruvian Andes",
        "body": "A powerful earthquake strikes the Andes. Damage reports "
                "are still coming in from the region.",
    },
    {
        "tag": "HEALTH",
        "accent": (74, 144, 204),
        "head": "Trial pill beats back pancreatic cancer",
        "body": "Daraxonrasib makes tumours undetectable on scans in 1 in "
                "12 patients in an early trial.",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(draw, x, y, pw, ph, story):
    draw.rounded_rectangle([x, y, x + pw, y + ph], radius=10,
                           fill=PANEL_BG, outline=PANEL_LINE, width=2)
    draw.rectangle([x, y, x + pw, y + 8], fill=story["accent"])
    pad = 24
    tx = x + pad
    ty = y + 26
    tag_f = font(SANS_BOLD, 24)
    draw.text((tx, ty), story["tag"], font=tag_f, fill=story["accent"])
    ty += 38
    head_f = font(SANS_BOLD, 31)
    inner_w = pw - 2 * pad
    for line in wrap_text(draw, story["head"], head_f, inner_w):
        draw.text((tx, ty), line, font=head_f, fill=WHITE)
        ty += 40
    ty += 8
    body_f = font(SANS, 23)
    for line in wrap_text(draw, story["body"], body_f, inner_w):
        draw.text((tx, ty), line, font=body_f, fill=MUTED)
        ty += 32


def build():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    title_f = font(SANS_BOLD, 62)
    draw.text((40, 26), "WORLD NEWS", font=title_f, fill=WHITE)
    date_f = font(SANS_BOLD, 29)
    draw.text((40, 96), "SATURDAY 21 NOVEMBER 2026", font=date_f, fill=GOLD)
    draw.rectangle([40, 140, W - 40, 144], fill=GOLD)
    margin = 28
    gap = 20
    pw = (W - 2 * margin - gap) // 2
    ph = (930 - 160 - gap) // 2
    for i, story in enumerate(STORIES):
        px = margin + (i % 2) * (pw + gap)
        py = 160 + (i // 2) * (ph + gap)
        draw_panel(draw, px, py, pw, ph, story)
    foot_f = font(SANS, 21)
    foot = "Sources: major wire and newspaper roundups, 21 Nov 2026"
    fw = draw.textlength(foot, font=foot_f)
    draw.text(((W - fw) / 2, 962), foot, font=foot_f, fill=MUTED)
    img.save(OUT, format="PNG")
    return OUT


def verify_output(path=OUT):
    """Check the PNG exists, is within limits, and report its hash."""
    if not os.path.exists(path):
        raise SystemExit("missing output: " + path)
    size = os.path.getsize(path)
    with Image.open(path) as im:
        dims = im.size
        mode = im.mode
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    ok = size <= 1048576 and dims == (1024, 1024)
    print("file: %s  bytes: %d  size: %s  mode: %s" % (path, size, dims, mode))
    print("sha256: %s" % digest)
    print("within limits: %s" % ok)
    if not ok:
        raise SystemExit("output failed limits check")
    return digest


def describe():
    """One-line summary of what the image covers, for the build log."""
    tags = ", ".join(s["tag"] for s in STORIES)
    print("image: WORLD NEWS, Saturday 21 November 2026; panels: " + tags)


if __name__ == "__main__":
    build()
    describe()
    verify_output()
