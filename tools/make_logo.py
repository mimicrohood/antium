# -*- coding: utf-8 -*-
"""Remove the solid black background from rayoid.png, autocrop to the ray, save a transparent PNG."""
from PIL import Image
import sys

src = r"C:\Users\Administrator\Desktop\rayoid\rayoid.png"
dst = sys.argv[1]

img = Image.open(src).convert("RGBA")
px = img.load()
w, h = img.size

# Sample the corner to confirm the background color.
corner = px[2, 2]
print("corner pixel:", corner)

# Make near-black pixels transparent. The ray is vivid blue/yellow, so a low
# luminance threshold cleanly separates subject from the black field.
THRESH = 40  # 0-255; pixels darker than this on all channels become transparent
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if r <= THRESH and g <= THRESH and b <= THRESH:
            px[x, y] = (r, g, b, 0)

# Autocrop to the non-transparent bounding box, then pad a little breathing room.
bbox = img.getbbox()
if bbox:
    pad = 20
    l, t, r_, b_ = bbox
    l = max(0, l - pad); t = max(0, t - pad)
    r_ = min(w, r_ + pad); b_ = min(h, b_ + pad)
    img = img.crop((l, t, r_, b_))

img.save(dst)
print("saved", dst, "size", img.size)
