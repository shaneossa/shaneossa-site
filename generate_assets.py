#!/usr/bin/env python3
"""Generate favicon.ico (pixelated) and duotone headshot from source photo."""
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import struct, zlib, os

SRC = os.path.join(os.path.dirname(__file__), "headshot.jpg")
OUT_DIR = os.path.dirname(__file__)

# ── 1. Pixelated favicon ──────────────────────────────────────────────────────
def make_favicon(src_path, out_path):
    img = Image.open(src_path).convert("RGBA")
    # Crop to square (center)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    # Shrink to 16x16 (pixelated) then scale up to embed in ico
    tiny = img.resize((16, 16), Image.NEAREST)
    # Save as multi-size ico
    img32 = img.resize((32, 32), Image.NEAREST)
    img16 = tiny
    img32.save(out_path, format="ICO", sizes=[(16,16),(32,32)])
    print(f"  favicon saved: {out_path}")

# ── 2. Duotone illustration ───────────────────────────────────────────────────
def make_duotone(src_path, out_path):
    img = Image.open(src_path).convert("RGB")
    # Crop square
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, (h - side) // 2 - h // 10)  # slightly favor top (face)
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((400, 400), Image.LANCZOS)

    # Increase contrast + convert to grayscale
    img = ImageEnhance.Contrast(img).enhance(1.4)
    gray = ImageOps.grayscale(img)

    # Map: dark tone = #0f1117 (bg), light tone = #f6821f (accent orange)
    dark  = (15,  17,  23)   # --bg
    light = (246, 130, 31)   # --accent orange

    # Create duotone by mapping grayscale 0-255 to dark->light
    duotone = Image.new("RGB", gray.size)
    pixels_in  = gray.load()
    pixels_out = duotone.load()
    for y in range(gray.height):
        for x in range(gray.width):
            t = pixels_in[x, y] / 255.0
            r = int(dark[0] + (light[0] - dark[0]) * t)
            g = int(dark[1] + (light[1] - dark[1]) * t)
            b = int(dark[2] + (light[2] - dark[2]) * t)
            pixels_out[x, y] = (r, g, b)

    # Slight sharpen for illustration feel
    duotone = duotone.filter(ImageFilter.SHARPEN)
    duotone.save(out_path, "JPEG", quality=90)
    print(f"  duotone saved: {out_path}")

if __name__ == "__main__":
    make_favicon(SRC, os.path.join(OUT_DIR, "favicon.ico"))
    make_duotone(SRC, os.path.join(OUT_DIR, "headshot-duotone.jpg"))
    print("Done.")
