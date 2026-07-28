"""
Build a consistent golden social-icon set from the Carrd-style reference.

Reference glyphs are gold silhouettes with sky-colored cutouts.
We recolor gold, paint monogram holes cream, and normalize optical size.
"""
from PIL import Image
import math
import os

SRC = r"C:\Users\maria\.grok\sessions\C%3A%5CUsers%5Cmaria%5Cgood-day-sunshine\019fa9e4-dc19-79c0-928a-efac3a13a1b1\assets\image-c7183dba-6748-4c32-8833-35fd0493183b.png"
OUT_DIR = r"C:\Users\maria\good-day-sunshine\assets\social"
NAMES = ["instagram", "facebook", "youtube", "tiktok", "pinterest"]

GOLD = (232, 196, 90, 255)        # #E8C45A
CREAM = (250, 244, 225, 255)      # soft cream letter cutouts
TARGET = 192
CONTENT = 0.88


def is_gold(r, g, b):
    return (
        r >= 175 and g >= 145 and b <= 175
        and r >= g - 10
        and (r + g) / 2 >= b + 25
        and (r + g) > 330
    )


def is_background(r, g, b, x, w):
    if x < 100 or x > w - 100:
        if r > 230 and g > 220 and b > 200:
            return True
    if b >= 205 and g >= 200 and r >= 160 and (b - r) >= 8:
        return True
    return False


def gold_pixels(icon):
    w, h = icon.size
    px = icon.load()
    pts = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 20:
                pts.append((x, y))
    return pts


def fill_circle_cutouts(icon, cream=CREAM, inset=0.985):
    """
    For circular monogram badges (FB, Pinterest): any transparent pixel
    inside the fitted gold circle becomes cream. Handles open cutouts
    that touch the circle edge (f stem, p stem).
    """
    pts = gold_pixels(icon)
    if not pts:
        return icon
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    radius = max(math.hypot(x - cx, y - cy) for x, y in pts) * inset

    w, h = icon.size
    px = icon.load()
    r2 = radius * radius
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 20:
                continue
            if (x - cx) ** 2 + (y - cy) ** 2 <= r2:
                px[x, y] = cream
    return icon


def flood_exterior(bin_alpha):
    """Transparent pixels connected to the image border."""
    w, h = bin_alpha.size
    ap = bin_alpha.load()
    exterior = set()
    stack = []

    def push(x, y):
        if 0 <= x < w and 0 <= y < h and (x, y) not in exterior and ap[x, y] == 0:
            exterior.add((x, y))
            stack.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            push(nx, ny)
    return exterior


def fill_enclosed_holes(icon, cream=CREAM):
    """
    Fill fully enclosed transparent holes (e.g. YouTube 'Tube' letters)
    without filling open exterior space.
    """
    w, h = icon.size
    alpha = icon.split()[-1].point(lambda v: 255 if v > 20 else 0)
    exterior = flood_exterior(alpha)
    px = icon.load()
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if ap[x, y] == 0 and (x, y) not in exterior:
                px[x, y] = cream
    return icon


def snap_colors(canvas):
    cp = canvas.load()
    tw, th = canvas.size
    for y in range(th):
        for x in range(tw):
            r, g, b, a = cp[x, y]
            if a < 18:
                cp[x, y] = (0, 0, 0, 0)
                continue
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum > 215 and b > 180 and abs(r - g) < 35:
                cp[x, y] = (CREAM[0], CREAM[1], CREAM[2], a)
            else:
                cp[x, y] = (GOLD[0], GOLD[1], GOLD[2], a)
    return canvas


def main():
    src = Image.open(SRC).convert("RGBA")
    w, h = src.size
    sp = src.load()

    gold = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gp = gold.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = sp[x, y]
            if is_background(r, g, b, x, w):
                continue
            if is_gold(r, g, b) or (r > 160 and g > 140 and b < 200 and r + g > 300):
                gp[x, y] = GOLD

    cols = []
    in_icon = False
    start = 0
    for x in range(w):
        has = any(gp[x, y][3] > 0 for y in range(h))
        if has and not in_icon:
            in_icon = True
            start = x
        elif not has and in_icon:
            in_icon = False
            cols.append((start, x - 1))
    if in_icon:
        cols.append((start, w - 1))

    bands = [(a, b) for a, b in cols if 70 <= (b - a) <= 180]
    print("bands:", bands)
    if len(bands) != 5:
        bands = sorted(cols, key=lambda t: t[1] - t[0], reverse=True)[:5]
        bands = sorted(bands, key=lambda t: t[0])
        print("fallback:", bands)

    os.makedirs(OUT_DIR, exist_ok=True)

    for name, (x0, x1) in zip(NAMES, bands):
        ys = [y for y in range(h) for x in range(x0, x1 + 1) if gp[x, y][3] > 0]
        y0, y1 = min(ys), max(ys)
        pad = 6
        box = (max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad + 1), min(h, y1 + pad + 1))
        crop = gold.crop(box)
        bbox = crop.split()[-1].getbbox()
        if bbox:
            crop = crop.crop(bbox)

        crop = crop.copy()
        if name in ("facebook", "pinterest"):
            crop = fill_circle_cutouts(crop)
        elif name == "youtube":
            # Reference: gold "You" above badge + cream "Tube" cutouts inside badge
            crop = fill_enclosed_holes(crop)

        cw, ch = crop.size
        scale = (TARGET * CONTENT) / max(cw, ch)
        nw = max(1, int(round(cw * scale)))
        nh = max(1, int(round(ch * scale)))
        resized = crop.resize((nw, nh), Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
        ox = (TARGET - nw) // 2
        oy = (TARGET - nh) // 2
        canvas.paste(resized, (ox, oy), resized)
        canvas = snap_colors(canvas)

        out = os.path.join(OUT_DIR, f"{name}.png")
        canvas.save(out, "PNG", optimize=True)
        print(f"saved {name}: {nw}x{nh}")

    print("done")


if __name__ == "__main__":
    main()
