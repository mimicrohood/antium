# -*- coding: utf-8 -*-
"""Make the Framer CMS loader work on a plain static server (e.g. GitHub Pages).

The loader requests ?range=a-b,c-d and asserts the response length equals the
requested byte count. A static server ignores ?range and returns the whole file,
so the assertion throws and docs pages render blank.

Fix: instead of throwing on a length mismatch, treat the response as the full
file and slice each requested range out of it by its ABSOLUTE offset (the loader
already writes slices at e.from). When the server DOES honor ranges (serve.py),
behavior is unchanged.
"""
import io, os, sys

DIR = r"C:\Users\Administrator\Desktop\rayoid\frontend\site\_assets\framerusercontent.com\sites\4GgFjAnjYT1KMBZEvvLhvC"

# (filename, sparse-buffer class name used in that file)
TARGETS = [
    ("qVisrsydS.vVQrVlCj.mjs", "$e"),
    ("UIt_09VGw.0q8aEUhC.mjs", "Pt"),
]

def patch(fn, cls):
    p = os.path.join(DIR, fn)
    s = io.open(p, encoding="utf-8").read()
    old = (
        "if(l.length!==i)throw Error(`Request failed: Unexpected response length`);"
        "let u=new %s,d=0;for(let e of n){let t=e.to-e.from,n=d+t,r=l.subarray(d,n);"
        "u.write(e.from,r),d=n}return t.map(e=>u.read(e.from,e.to-e.from))" % cls
    )
    new = (
        "let u=new %s;if(l.length===i){let d=0;for(let e of n){let a=e.to-e.from,f=d+a,"
        "r=l.subarray(d,f);u.write(e.from,r),d=f}}else{for(let e of n)"
        "u.write(e.from,l.subarray(e.from,e.to))}return t.map(e=>u.read(e.from,e.to-e.from))" % cls
    )
    c = s.count(old)
    if c != 1:
        print(f"  !! {fn}: expected 1 match, found {c} — SKIPPED")
        return False
    io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print(f"  patched {fn} ({cls})")
    return True

ok = all(patch(fn, cls) for fn, cls in TARGETS)
print("ALL PATCHED" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
