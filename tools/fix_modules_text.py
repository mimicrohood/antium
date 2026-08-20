# -*- coding: utf-8 -*-
import io, os
d = r"C:\Users\Administrator\Desktop\rayoid\site\_assets\framerusercontent.com\sites\4GgFjAnjYT1KMBZEvvLhvC"
edits = {
 "EpTcCjtRE4cV0xitOwGc4sS7i57yqlxVsqdIQaSCZDA.ChxfC8MA.mjs": [
   ("Mycoid:~$ docs", "rayoid:~$ docs"),
   ("From spores to networks: A complete interpretation of the Mycoid project. These documents record Mycoid’s ideas, experiments, and fungal threads.",
    "From signals to networks: a complete reading of rayoid. These documents trace its ideas, experiments, and the currents running beneath the deep."),
 ],
 "i4iEQBE5cYq7AOcBdrCRX4DKmvKZjF6BEsMZayWoT9Y.BHHEVs3H.mjs": [("Mycoid:~$ tracks", "rayoid:~$ tracks")],
 "VV9un9fsFicXnqFSb3VOhskW_Y7bCFhIA1IaOUH1Ct0.BSGOI6pL.mjs": [("Mycoid:~$ docs", "rayoid:~$ docs")],
}
for fn, subs in edits.items():
    p = os.path.join(d, fn)
    if not os.path.exists(p + ".orig"):
        io.open(p + ".orig", "w", encoding="utf-8").write(io.open(p, encoding="utf-8").read())
    s = io.open(p, encoding="utf-8").read()
    for old, new in subs:
        c = s.count(old)
        s = s.replace(old, new)
        print(fn[:20], repr(old[:28]), "->", c, "hit(s)")
    io.open(p, "w", encoding="utf-8").write(s)
print("done")
