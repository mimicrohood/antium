#!/usr/bin/env python3
"""Rebrand all pages from mycoid -> rayoid: favicon, title, og/twitter image + title."""
import re, glob

OLD_ICON = "/_assets/framerusercontent.com/images/VABonYO2hqDfa712352Jg7kYUU.png"
ICON = "/_assets/rayoid/rayoid-icon.png"
SHARE = "/_assets/rayoid/rayoid-share.png"

pages = glob.glob("site/**/*.html", recursive=True)
for p in pages:
    s = open(p, encoding="utf-8").read()
    orig = s

    # favicon <link rel="icon"> (light + dark) -> new transparent png
    s = s.replace(f'href="{OLD_ICON}" rel="icon"', f'href="{ICON}" rel="icon"')

    # og:image / twitter:image -> share image
    s = re.sub(r'(<meta property="og:image" content=")[^"]*(")', rf'\g<1>{SHARE}\g<2>', s)
    s = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', rf'\g<1>{SHARE}\g<2>', s)

    # any leftover reference to the old icon asset -> new icon
    s = s.replace(OLD_ICON, ICON)

    # title + og/twitter title: mycoid -> rayoid (only the exact brand token)
    s = s.replace("<title>mycoid</title>", "<title>rayoid</title>")
    s = s.replace('content="mycoid"', 'content="rayoid"')

    if s != orig:
        open(p, "w", encoding="utf-8").write(s)
        print("updated", p)

print("REBRAND DONE")
