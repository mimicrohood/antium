# -*- coding: utf-8 -*-
import io, os
ROOT = r"C:\Users\Administrator\Desktop\rayoid\site"
FILES = [
    os.path.join(ROOT, "tracks", "index.html"),
    os.path.join(ROOT, "_assets", "framerusercontent.com", "sites",
                 "4GgFjAnjYT1KMBZEvvLhvC",
                 "i4iEQBE5cYq7AOcBdrCRX4DKmvKZjF6BEsMZayWoT9Y.BHHEVs3H.mjs"),
]

# (old, new) — full phrases / inline-strong inner text. Order matters slightly.
REPLACEMENTS = [
    # --- Phase titles ---
    ("Spore Emergence", "Pulse Emergence"),
    ("Thread Expansion", "Current Expansion"),
    # "Web Formation" kept (ray-web fits)

    # --- Phase descriptions ---
    ("Silent links begin to form across digital soil.",
     "Silent links begin to form across the digital deep."),
    ("Towards a distributed ecosystem of fungal intelligence.",
     "Towards a distributed ecosystem of electric intelligence."),
    # "From fragments to the first signals of cognition." kept

    # --- Phase 1 bullets ---
    ("spore signals", "electric pulses"),  # <strong> inner (Release the first ...)
    ("Establish the foundation of a living dataset of fungal cognition",
     "Establish the foundation of a living dataset of electric-sense cognition"),
    ("Frame cognition as growth rather than direct language",
     "Frame cognition as drift rather than direct language"),

    # --- Phase 2 bullets ---
    ("Spore signals interconnect into", "Electric pulses interconnect into"),
    ("threads of meaning", "currents of meaning"),  # <strong> inner
    ("Study autonomy through persistent, hidden growth",
     "Study autonomy through persistent, hidden drift"),

    # --- Phase 3 bullets ---
    ("Spore and thread signals evolve into", "Pulse and current signals evolve into"),
    ("mycelial webs", "ray-webs"),  # <strong> inner
    ("Explore broader implications: intelligence as silent, collective growth",
     "Explore broader implications: intelligence as silent, collective drift"),
]

for p in FILES:
    s = io.open(p, encoding="utf-8").read()
    print("\n===", os.path.basename(p)[:24], "===")
    for old, new in REPLACEMENTS:
        c = s.count(old)
        if c != 1:
            print(f"  WARN count={c} for {old!r}")
        s = s.replace(old, new)
        print(f"  {c}x  {old[:40]!r} -> {new[:40]!r}")
    io.open(p, "w", encoding="utf-8").write(s)
print("\ndone")
