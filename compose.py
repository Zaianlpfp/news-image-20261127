#!/usr/bin/env python3
"""Compose entry.png for news-image-20261127.

Builds a 1024x1024 front-page-style image from a model-generated hero
illustration (no text in the illustration) plus all text drawn in code with
Liberation Sans, so every word is crisp and legible. Nothing here is copied
from the kit starter; the layout, copy and code are original to this entry.

Layout (1024 x 1024):
  masthead  y 0..116    date, huge
  hero      y 116..660  NZ coalition one seat short (illustration + overlay text)
  bottom    y 660..960  two panels: Australia sanctions | Asian shares
  footer    y 960..1024 sources line

Run:  python3 compose.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
HERO_SRC = os.path.join(
    HERE,
    "media-generation-hero-nz-parliament-0-073bd587-6b78-4fe9-90fa-ffc9467bf17e.webp",
)
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MASTHEAD_H = 116
HERO_Y = 116
HERO_H = 544
BOTTOM_Y = 660
BOTTOM_H = 300
FOOTER_Y = 960

FONT_DIR = "/usr/share/fonts/truetype/liberation"
BOLD = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")

NAVY = (10, 30, 60)
PANEL_BG = (13, 27, 52)
AMBER = (255, 176, 32)
GREEN = (52, 211, 153)
WHITE = (255, 255, 255)
OFFWHITE = (235, 238, 244)
GRAY = (185, 196, 214)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def main():
    hero = Image.open(HERO_SRC).convert("RGB")
    print("hero source:", hero.size)
    sky = hero.getpixel((5, 5))  # masthead blends into the illustration sky

    canvas = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(canvas)

    # ---- hero background: cover-crop the illustration into its band ----
    scale = max(W / hero.width, HERO_H / hero.height)
    hw, hh = int(hero.width * scale + 0.5), int(hero.height * scale + 0.5)
    hero_r = hero.resize((hw, hh), Image.LANCZOS)
    ox, oy = (W - hw) // 2, (HERO_H - hh) // 2
    canvas.paste(hero_r, (ox, HERO_Y + oy))

    # ---- dark scrim over the hero, strongest at the bottom ----
    scrim = Image.new("L", (W, HERO_H), 0)
    sd = ImageDraw.Draw(scrim)
    for y in range(HERO_H):
        t = y / HERO_H
        # 0 alpha until 30% down, then ramp to 205
        a = 0 if t < 0.30 else int(205 * (t - 0.30) / 0.70)
        sd.line([(0, y), (W, y)], fill=a)
    black = Image.new("RGB", (W, HERO_H), (0, 0, 0))
    canvas.paste(black, (0, HERO_Y), scrim)

    # ---- masthead ----
    d.rectangle([0, 0, W, MASTHEAD_H], fill=sky)
    d.text((48, 16), "THE WORLD IN ONE DAY", font=font(BOLD, 27), fill=AMBER)
    d.text((48, 44), "27 NOVEMBER 2026", font=font(BOLD, 66), fill=WHITE)
    d.text((W - 48 - d.textlength("FRIDAY", font=font(BOLD, 27)), 16),
           "FRIDAY", font=font(BOLD, 27), fill=OFFWHITE)
    d.rectangle([0, MASTHEAD_H - 4, W, MASTHEAD_H], fill=AMBER)

    # ---- hero text ----
    hx, hw_max = 48, W - 96
    # kicker chip
    kick = "NEW ZEALAND  •  POLITICS"
    kf = font(BOLD, 25)
    kw = d.textlength(kick, font=kf)
    chip_y = HERO_Y + HERO_H - 348
    d.rounded_rectangle([hx, chip_y, hx + kw + 32, chip_y + 42],
                        radius=8, fill=AMBER)
    d.text((hx + 16, chip_y + 7), kick, font=kf, fill=NAVY)
    # headline
    hf = font(BOLD, 74)
    lines = wrap(d, "COALITION ONE SEAT SHORT", hf, hw_max)
    hy = chip_y + 58
    for ln in lines:
        d.text((hx, hy), ln, font=hf, fill=WHITE)
        hy += 86
    # subline
    sf = font(REG, 30)
    sub = ("Final election count leaves New Zealand's ruling coalition with "
           "65 of 130 seats — one short of a majority.")
    for ln in wrap(d, sub, sf, hw_max):
        d.text((hx, hy + 6), ln, font=sf, fill=OFFWHITE)
        hy += 38

    # ---- bottom panels ----
    d.rectangle([0, BOTTOM_Y, W, FOOTER_Y], fill=PANEL_BG)
    d.rectangle([0, BOTTOM_Y, W, BOTTOM_Y + 6], fill=AMBER)
    d.line([(W // 2, BOTTOM_Y), (W // 2, FOOTER_Y)], fill=(38, 58, 96), width=4)

    panels = [
        {
            "x": 0, "accent": AMBER,
            "kicker": "AUSTRALIA  •  SECURITY",
            "headline": "SANCTIONS FOR IRAN",
            "stat": "TWO PEOPLE SANCTIONED",
            "sub": ("Canberra imposes counterterrorism financing sanctions "
                    "on two people it says carried out antisemitic attacks "
                    "for Iran's Revolutionary Guard."),
        },
        {
            "x": W // 2, "accent": GREEN,
            "kicker": "ASIA  •  MARKETS",
            "headline": "SHARES FIND FOOTING",
            "stat": "NIKKEI +0.7%  •  KOSPI +2%",
            "sub": ("Asian stocks steady after a bruising month as Tokyo "
                    "inflation hits a 16-month high and the dollar eyes a "
                    "third monthly gain."),
        },
    ]
    # Fit both bottom headlines to one common size so neither overflows.
    tw = W // 2 - 72
    head_size = 40
    while head_size > 20:
        if all(d.textlength(p["headline"], font=font(BOLD, head_size)) <= tw
               for p in panels):
            break
        head_size -= 1
    print("bottom headline size:", head_size)
    for p in panels:
        x0 = p["x"] + 36
        d.rectangle([p["x"], BOTTOM_Y, p["x"] + W // 2, BOTTOM_Y + 6],
                    fill=p["accent"])
        d.text((x0, BOTTOM_Y + 26), p["kicker"], font=font(BOLD, 22),
               fill=p["accent"])
        # Headline may wrap to two lines; keep the stat below it.
        hl = wrap(d, p["headline"], font(BOLD, head_size), tw)
        hy2 = BOTTOM_Y + 60
        for ln in hl:
            d.text((x0, hy2), ln, font=font(BOLD, head_size), fill=WHITE)
            hy2 += head_size + 8
        d.text((x0, hy2 + 8), p["stat"], font=font(BOLD, 26),
               fill=p["accent"])
        sy = hy2 + 52
        for ln in wrap(d, p["sub"], font(REG, 23), tw):
            d.text((x0, sy), ln, font=font(REG, 23), fill=GRAY)
            sy += 29

    # ---- footer ----
    d.rectangle([0, FOOTER_Y, W, H], fill=NAVY)
    draw_centered(d, FOOTER_Y + 18, "SOURCES: REUTERS  •  FRIDAY 27 NOVEMBER 2026",
                  font(BOLD, 23), GRAY)

    # ---- save; keep under the 1 MiB gate ----
    canvas.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print("entry.png:", canvas.size, size, "bytes")
    if size > 1_048_576:
        pal = canvas.convert("P", palette=Image.ADAPTIVE, colors=256)
        pal.save(OUT, "PNG", optimize=True)
        size = os.path.getsize(OUT)
        print("quantized to 256 colours:", size, "bytes")
    assert size <= 1_048_576, "still over 1 MiB"
    print("OK")


if __name__ == "__main__":
    main()
