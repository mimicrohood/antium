#!/usr/bin/env python3
"""Verify every /_assets/... reference in the mirrored site resolves to an existing file."""
import os, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
REF = re.compile(r"/_assets/[A-Za-z0-9._%/\-]+")

missing = {}
checked = 0
for root, _, files in os.walk(OUT):
    for f in files:
        if not f.endswith((".html", ".mjs", ".js", ".css", ".json")):
            continue
        fp = os.path.join(root, f)
        with open(fp, "r", encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
        for ref in set(REF.findall(txt)):
            checked += 1
            dst = os.path.join(OUT, ref.lstrip("/"))
            if not (os.path.exists(dst) and os.path.getsize(dst) > 0):
                missing.setdefault(ref, []).append(os.path.relpath(fp, OUT))

print(f"checked {checked} unique refs")
if not missing:
    print("ALL LOCAL ASSET REFERENCES RESOLVE ✔")
else:
    print(f"{len(missing)} MISSING:")
    for k, v in list(missing.items())[:40]:
        print(f"  {k}   <- {v[0]}")
