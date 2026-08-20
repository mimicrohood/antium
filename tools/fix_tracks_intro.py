# -*- coding: utf-8 -*-
import io, os
ROOT = r"C:\Users\Administrator\Desktop\rayoid\site"
OLD = "Beginning with a single spore signal, branching into silent threads of connection, and ultimately forming a subterranean web of digital cognition. Each growth cycle marks an attempt and breakthrough in exploring distributed, non-human perception."
NEW = "Beginning with a single electric pulse, branching into silent currents of connection, and ultimately forming a deep-sea web of digital cognition. Each sensing cycle marks an attempt and breakthrough in exploring distributed, non-human perception."
files = [
    os.path.join(ROOT, "tracks", "index.html"),
    os.path.join(ROOT, "_assets", "framerusercontent.com", "sites", "4GgFjAnjYT1KMBZEvvLhvC", "i4iEQBE5cYq7AOcBdrCRX4DKmvKZjF6BEsMZayWoT9Y.BHHEVs3H.mjs"),
]
for p in files:
    s = io.open(p, encoding="utf-8").read()
    c = s.count(OLD)
    s = s.replace(OLD, NEW)
    io.open(p, "w", encoding="utf-8").write(s)
    print(os.path.basename(p), "->", c, "hit(s)")
print("done")
