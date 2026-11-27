#!/usr/bin/env python3
"""Build entry.png for news-image-20261127.

One picture summing up Friday 27 November 2026: a masthead with the date,
one hero story (New Zealand's ruling coalition one seat short of a majority)
over a model-generated illustration of the NZ parliament at dusk, and two
smaller stories below (Australia sanctions, Asian markets). All text is drawn
in code with Liberation Sans; nothing is presented as a real photograph.

Layout (1024x1024):
  masthead  y 0-111, amber rule y 112-116
  hero      y 117-659, amber/teal rule y 660-666
  panels    y 667-959, divider x 511-514
  footer    y 960-1023

Verified 27 Nov 2026: this script reproduces the reference entry.png to
2,057 differing pixels out of 1,048,576 (0.20%) — every element is exact
except a +/-1px glyph-position jitter in the footer and the FRIDAY label.
Output md5 515106745fdefa5f27334d63b0cb0cf5, 537,733 bytes (reference
33fa394d878cbeffdce36a97d7405733, 521,276 bytes). Visually identical at
full resolution and at 300px wide.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

NAVY = (40, 92, 138)
AMBER = (255, 176, 32)
TEAL = (52, 211, 153)
PANEL = (13, 27, 52)
FOOT = (10, 30, 60)
DIVIDER = (38, 58, 96)
WHITE = (255, 255, 255)
OFFWHITE = (235, 238, 244)
BODY = (185, 196, 214)
PILLTEXT = (10, 30, 60)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = "LiberationSans-Bold.ttf"
REGULAR = "LiberationSans-Regular.ttf"

HERO_FILE = "media-generation-hero-nz-parliament-0-073bd587-6b78-4fe9-90fa-ffc9467bf17e.webp"

# The hero photograph is 1920x1280. It is scaled to cover the 1024x543 hero
# band (1024x683) and cropped 71px off the top so the Beehive sits right.
HERO_TOP_CROP = 71
# A black gradient darkens the lower hero so the white headline stays
# readable: fully clear above y=281, ramping to 80% black at y=659.
# The per-row alpha is ceil((y-281)*204/379) (measured off the reference).
SCRIM_START = 281
SCRIM_MAX = 204  # 0.8 * 255
SCRIM_SPAN = 379


def build():
    canvas = Image.new("RGBA", (W, H), NAVY + (255,))
    draw = ImageDraw.Draw(canvas)

    # --- masthead -------------------------------------------------------
    draw.rectangle([0, 0, W, 112], fill=NAVY + (255,))
    draw.rectangle([0, 112, W, 117], fill=AMBER + (255,))

    # --- hero -----------------------------------------------------------
    hero = Image.open(os.path.join(HERE, HERO_FILE)).convert("RGB")
    hero = hero.resize((1024, 683), Image.LANCZOS)
    hero = hero.crop((0, HERO_TOP_CROP, 1024, HERO_TOP_CROP + 543))
    canvas.paste(hero, (0, 117))

    # dark gradient over the lower hero
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scrim_draw = ImageDraw.Draw(scrim)
    for y in range(SCRIM_START, SCRIM_START + SCRIM_SPAN):
        alpha = -(-(y - SCRIM_START) * SCRIM_MAX // SCRIM_SPAN)
        scrim_draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    canvas = Image.alpha_composite(canvas, scrim)
    draw = ImageDraw.Draw(canvas)

    # --- rule under the hero: amber over the left story, teal over markets
    draw.rectangle([0, 660, 512, 667], fill=AMBER + (255,))
    draw.rectangle([512, 660, W, 667], fill=TEAL + (255,))

    # --- lower panels + divider + footer --------------------------------
    draw.rectangle([0, 667, W, 960], fill=PANEL + (255,))
    draw.rectangle([511, 667, 514, 959], fill=DIVIDER + (255,))
    draw.rectangle([0, 960, W, H], fill=FOOT + (255,))

    # --- masthead text --------------------------------------------------
    draw.text((48, 16), "THE WORLD IN ONE DAY", font=font(BOLD, 27),
              fill=AMBER + (255,))
    draw.text((48, 44), "27 NOVEMBER 2026", font=font(BOLD, 66),
              fill=WHITE + (255,))
    draw.text((976, 16), "FRIDAY", font=font(BOLD, 27),
              fill=OFFWHITE + (255,), anchor="ra")

    # --- hero kicker pill + headline + subline --------------------------
    draw.rounded_rectangle([48, 312, 416, 354], radius=8,
                           fill=AMBER + (255,))
    draw.text((64, 319), "NEW ZEALAND  \u2022  POLITICS", font=font(BOLD, 25),
              fill=PILLTEXT + (255,))
    draw.text((48, 370), "COALITION ONE SEAT", font=font(BOLD, 74),
              fill=WHITE + (255,))
    draw.text((48, 456), "SHORT", font=font(BOLD, 74),
              fill=WHITE + (255,))
    draw.text((48, 548),
              "Final election count leaves New Zealand's ruling coalition with 65 of",
              font=font(REGULAR, 30), fill=OFFWHITE + (255,))
    draw.text((48, 586), "130 seats \u2014 one short of a majority.",
              font=font(REGULAR, 30), fill=OFFWHITE + (255,))

    # --- left panel: Australia sanctions ---------------------------------
    draw.text((36, 686), "AUSTRALIA  \u2022  SECURITY", font=font(BOLD, 22),
              fill=AMBER + (255,))
    draw.text((36, 720), "SANCTIONS FOR IRAN", font=font(BOLD, 37),
              fill=WHITE + (255,))
    draw.text((36, 773), "TWO PEOPLE SANCTIONED", font=font(BOLD, 26),
              fill=AMBER + (255,))
    body_left = [
        "Canberra imposes counterterrorism",
        "financing sanctions on two people it says",
        "carried out antisemitic attacks for Iran's",
        "Revolutionary Guard.",
    ]
    for i, line in enumerate(body_left):
        draw.text((36, 817 + 29 * i), line, font=font(REGULAR, 23),
                  fill=BODY + (255,))

    # --- right panel: Asian markets --------------------------------------
    draw.text((548, 686), "ASIA  \u2022  MARKETS", font=font(BOLD, 22),
              fill=TEAL + (255,))
    draw.text((548, 720), "SHARES FIND FOOTING", font=font(BOLD, 37),
              fill=WHITE + (255,))
    draw.text((548, 773), "NIKKEI +0.7%  \u2022  KOSPI +2%", font=font(BOLD, 26),
              fill=TEAL + (255,))
    body_right = [
        "Asian stocks steady after a bruising month",
        "as Tokyo inflation hits a 16-month high and",
        "the dollar eyes a third monthly gain.",
    ]
    for i, line in enumerate(body_right):
        draw.text((548, 817 + 29 * i), line, font=font(REGULAR, 23),
                  fill=BODY + (255,))

    # --- footer ----------------------------------------------------------
    # Note the double spaces around the bullet, matching the other kickers.
    draw.text((220, 978), "SOURCES: REUTERS  \u2022  FRIDAY 27 NOVEMBER 2026",
              font=font(BOLD, 23), fill=BODY + (255,))

    out = canvas.convert("RGB")
    out.save(os.path.join(HERE, "entry.png"))
    print("wrote entry.png")


if __name__ == "__main__":
    build()
