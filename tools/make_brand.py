#!/usr/bin/env python3
"""Build rayoid brand assets from rayoid.png: transparent centered favicon (PNG+ICO) and a social share image."""
from PIL import Image

SRC = "rayoid.png"
OUT_DIR = "site/_assets/rayoid"

import os
os.makedirs(OUT_DIR, exist_ok=True)

im = Image.open(SRC).convert("RGBA")
px = im.load()
W, H = im.size

# 1) Knock out near-black background -> transparent
thresh = 28  # pixels darker than this on all channels become transparent
data = im.getdata()
new = []
for r, g, b, a in data:
    if r <= thresh and g <= thresh and b <= thresh:
        new.append((r, g, b, 0))
    else:
        new.append((r, g, b, a))
im.putdata(new)

# 2) Crop to the non-transparent bounding box
bbox = im.getbbox()
cropped = im.crop(bbox)
cw, ch = cropped.size

# 3) Paste onto a square transparent canvas with ~8% padding
side = max(cw, ch)
pad = int(side * 0.08)
canvas_side = side + pad * 2
canvas = Image.new("RGBA", (canvas_side, canvas_side), (0, 0, 0, 0))
canvas.paste(cropped, ((canvas_side - cw) // 2, (canvas_side - ch) // 2), cropped)

# 4) Favicon master 512x512 (transparent)
fav = canvas.resize((512, 512), Image.LANCZOS)
fav.save(os.path.join(OUT_DIR, "rayoid-icon.png"))

# 5) Multi-size .ico
fav.save(os.path.join(OUT_DIR, "rayoid.ico"),
         sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

# 6) Social share image (og/twitter): 1200x630, dark bg to match site, rayoid centered
share = Image.new("RGBA", (1200, 630), (8, 8, 12, 255))
logo = canvas.resize((430, 430), Image.LANCZOS)
share.alpha_composite(logo, ((1200 - 430) // 2, (630 - 430) // 2))
share.convert("RGB").save(os.path.join(OUT_DIR, "rayoid-share.png"))

print("bbox", bbox, "cropped", cropped.size, "-> icon 512, ico multi, share 1200x630")
print("DONE")
