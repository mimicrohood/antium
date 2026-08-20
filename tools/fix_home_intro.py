# -*- coding: utf-8 -*-
import io, os
ROOT = r"C:\Users\Administrator\Desktop\rayoid\site"
FILES = [
    os.path.join(ROOT, "index.html"),
    os.path.join(ROOT, "_assets", "framerusercontent.com", "sites",
                 "4GgFjAnjYT1KMBZEvvLhvC",
                 "hNGLef-ywOXWB9cjddW73xsLN1--dYzlYPbyP45H0gE.CYvtoMPA.mjs"),
]
OLD = "an electric organism gliding across Solana that refuses to hold still."
NEW = "an electric organism powered by Claude Fable 5 that refuses to hold still."
for p in FILES:
    if not os.path.exists(p + ".orig"):
        io.open(p + ".orig", "w", encoding="utf-8").write(io.open(p, encoding="utf-8").read())
    s = io.open(p, encoding="utf-8").read()
    c = s.count(OLD)
    s = s.replace(OLD, NEW)
    io.open(p, "w", encoding="utf-8").write(s)
    print(os.path.basename(p)[:24], "->", c, "hit(s)")
print("done")
