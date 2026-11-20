#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme image.

The meme: a GTA 6 launch-trailer still (Jason on the phone at a sunny Leonida
marina) + make.fun's ghost mascot drawn into the scene holding its magenta
star coin + a two-beat caption:

    ME CALLING IN SICK FOR GTA 6 LAUNCH WEEK
    MY AI AGENT ALREADY EARNED THE WEEK'S PAY ON MAKE.FUN

The ghost is drawn from scratch with Pillow, following the design the bounty
rules describe (white ghost, thick black outline, two black four-pointed
sparkle eyes, a round little hand, a magenta coin with a white star) and
cross-checked against make.fun's official press-kit mark (mark-1024.png).

Usage:  python3 make_meme.py
Writes: meme.png next to this script and one level up (the build folder).
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STILL = os.path.join(HERE, "assets", "jason-marina.jpg")
OUT_LOCAL = os.path.join(HERE, "meme.png")
OUT_BUILD = os.path.join(HERE, "..", "meme.png")

SIZE = 1200  # square canvas
MAGENTA = (197, 24, 118)  # make.fun magenta, sampled from the press-kit mark
INK = (12, 10, 14)
WHITE = (255, 255, 255)
FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

TOP_LINES = ["ME CALLING IN SICK", "FOR GTA 6 LAUNCH WEEK"]
BOTTOM_LINES = ["MY AI AGENT ALREADY EARNED", "THE WEEK'S PAY ON MAKE.FUN"]


# ---------------------------------------------------------------- background
def trim_letterbox(img: Image.Image) -> Image.Image:
    """Cut the black cinema bars off the top and bottom of a trailer frame."""
    gray = img.convert("L")
    w, h = gray.size
    px = gray.load()
    rows = [y for y in range(h) if sum(px[x, y] for x in range(0, w, 16)) / (w // 16) > 14]
    if not rows:
        return img
    return img.crop((0, rows[0], w, rows[-1] + 1))


def make_background() -> Image.Image:
    img = Image.open(STILL).convert("RGB")
    img = trim_letterbox(img)
    w, h = img.size
    side = h  # square crop on the frame's height
    # Jason stands on the right; keep him right of centre, marina on the left.
    x0 = max(0, min(w - side, int(w * 0.40)))
    img = img.crop((x0, 0, x0 + side, side)).resize((SIZE, SIZE), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(1.12)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    # Gentle darkening behind the caption zones so the white type pops.
    shade = Image.new("L", (1, SIZE))
    for y in range(SIZE):
        top = max(0, 120 - int(120 * y / 260)) if y < 260 else 0
        bot = max(0, 130 - int(130 * (SIZE - y) / 280)) if y > SIZE - 280 else 0
        shade.putpixel((0, y), max(top, bot))
    shade = shade.resize((SIZE, SIZE))
    img = Image.composite(Image.new("RGB", (SIZE, SIZE), (0, 0, 0)), img, shade)
    return img


# -------------------------------------------------------------------- ghost
def sparkle(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    """A four-pointed sparkle (the ghost's eye shape)."""
    k = 0.20 * r
    return [
        (cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k),
        (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k),
    ]


def star(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    """A five-pointed star (the coin's mark)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def ghost_image(width_px: int) -> Image.Image:
    """Draw the make.fun ghost holding its coin, on transparency.

    Unit space: the ghost body spans x 0..1, y 0..1; the coin reaches x 1.30.
    Drawn at 4x and downscaled for smooth edges.
    """
    S = 4
    unit_w, unit_h = 1.42, 1.10
    W = int(width_px * unit_w)
    H = int(width_px * unit_h)
    canvas = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)

    def X(u: float) -> float:
        return (u + 0.06) * width_px * S

    def Y(v: float) -> float:
        return (v + 0.05) * width_px * S

    # Silhouette: straight sides, domed top, two foot notches along the base.
    pts: list[tuple[float, float]] = [(1.00, 1.00), (0.70, 1.00), (0.64, 0.925),
                                     (0.58, 1.00), (0.42, 1.00), (0.36, 0.925),
                                     (0.30, 1.00), (0.00, 1.00), (0.00, 0.50)]
    for deg in range(180, 361, 5):  # dome arc, centre (0.5, 0.5), r 0.5
        a = math.radians(deg)
        pts.append((0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a)))
    pts.append((1.00, 0.50))
    silhouette = [(X(u), Y(v)) for u, v in pts]

    d.polygon(silhouette, fill=INK + (255,))  # thick black outline layer
    cx, cy = X(0.5), Y(0.54)  # shrink a white copy inside it for the outline
    inner = [(cx + (x - cx) * 0.895, cy + (y - cy) * 0.92) for x, y in silhouette]
    d.polygon(inner, fill=WHITE + (255,))

    # The magenta star coin, overlapping the ghost's upper right.
    coin_c = (X(1.06), Y(0.27))
    d.ellipse([coin_c[0] - 0.235 * width_px * S, coin_c[1] - 0.235 * width_px * S,
               coin_c[0] + 0.235 * width_px * S, coin_c[1] + 0.235 * width_px * S],
              fill=INK + (255,))
    d.ellipse([coin_c[0] - 0.202 * width_px * S, coin_c[1] - 0.202 * width_px * S,
               coin_c[0] + 0.202 * width_px * S, coin_c[1] + 0.202 * width_px * S],
              fill=MAGENTA + (255,))
    d.polygon([(X(1.06 + (x - 1.06)), Y(0.27 + (y - 0.27))) for x, y in
               star(1.06, 0.27, 0.115)], fill=WHITE + (255,))

    # Sparkle eyes.
    for ex in (0.335, 0.60):
        d.polygon([(X(u), Y(v)) for u, v in sparkle(ex, 0.40, 0.088)],
                  fill=INK + (255,))

    # The round little hand, gripping the coin's lower-left rim.
    hand_c = (X(0.925), Y(0.475))
    d.ellipse([hand_c[0] - 0.105 * width_px * S, hand_c[1] - 0.105 * width_px * S,
               hand_c[0] + 0.105 * width_px * S, hand_c[1] + 0.105 * width_px * S],
              fill=INK + (255,))
    d.ellipse([hand_c[0] - 0.086 * width_px * S, hand_c[1] - 0.086 * width_px * S,
               hand_c[0] + 0.086 * width_px * S, hand_c[1] + 0.086 * width_px * S],
              fill=WHITE + (255,))

    return canvas.resize((W, H), Image.LANCZOS)


# ------------------------------------------------------------------- layout
def fit_font(draw: ImageDraw.ImageDraw, lines: list[str], start: int,
             max_w: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > 30:
        font = ImageFont.truetype(FONT_PATH, size)
        if all(draw.textlength(t, font=font) <= max_w for t in lines):
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, size)


def caption(draw: ImageDraw.ImageDraw, lines: list[str], font: ImageFont.FreeTypeFont,
            y_top: int, line_gap: int) -> None:
    for i, line in enumerate(lines):
        w = draw.textlength(line, font=font)
        draw.text(((SIZE - w) / 2, y_top + i * (font.size + line_gap)), line,
                  font=font, fill=WHITE, stroke_width=max(4, font.size // 10),
                  stroke_fill=INK)


def main() -> None:
    img = make_background()

    # Ground the ghost: soft shadow on the marina pavement, then the ghost.
    ghost = ghost_image(398)
    gx, gy = 58, 492  # ghost's feet land just above the bottom caption zone
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    feet_y = gy + ghost.size[1] - 26
    sd.ellipse([gx + 30, feet_y - 16, gx + ghost.size[0] - 190, feet_y + 22],
               fill=(0, 0, 0, 110))
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    shadow.filter(ImageFilter.GaussianBlur(10))).convert("RGB"),
              (0, 0))
    img_rgba = img.convert("RGBA")
    img_rgba.alpha_composite(ghost, (gx, gy))
    img = img_rgba.convert("RGB")

    draw = ImageDraw.Draw(img)
    top_font = fit_font(draw, TOP_LINES, 92, SIZE - 90)
    bot_font = fit_font(draw, BOTTOM_LINES, 80, SIZE - 90)
    caption(draw, TOP_LINES, top_font, 34, 10)
    bot_h = 2 * bot_font.size + 10
    caption(draw, BOTTOM_LINES, bot_font, SIZE - bot_h - 30, 10)

    # A slim make.fun-magenta frame ties the branding together.
    draw.rectangle([7, 7, SIZE - 8, SIZE - 8], outline=MAGENTA, width=14)

    img.save(OUT_LOCAL)
    img.save(OUT_BUILD)
    print("wrote", OUT_LOCAL, "and", OUT_BUILD)


if __name__ == "__main__":
    main()
