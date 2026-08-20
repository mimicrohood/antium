#!/usr/bin/env python3
"""Recursively fetch relative ./*.mjs (and .js) imports within the Framer sites/<id> dir."""
import os, re, urllib.request

BASE_URL = "https://framerusercontent.com/sites/4GgFjAnjYT1KMBZEvvLhvC/"
LOCAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "site", "_assets", "framerusercontent.com", "sites", "4GgFjAnjYT1KMBZEvvLhvC")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
REL_RE = re.compile(r'\./([A-Za-z0-9._-]+\.mjs)')

os.makedirs(LOCAL_DIR, exist_ok=True)

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f"  !! FAIL {url}: {e}", flush=True)
        return None

# seed queue from every existing .mjs already on disk
queue = []
seen = set()
for f in os.listdir(LOCAL_DIR):
    if f.endswith(".mjs"):
        with open(os.path.join(LOCAL_DIR, f), encoding="utf-8", errors="replace") as fh:
            for m in REL_RE.findall(fh.read()):
                if m not in seen:
                    seen.add(m); queue.append(m)

dl = 0
while queue:
    name = queue.pop(0)
    dst = os.path.join(LOCAL_DIR, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        # still scan it for further imports
        with open(dst, encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
    else:
        data = fetch(BASE_URL + name)
        if data is None:
            continue
        txt = data.decode("utf-8", "replace")
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(txt)
        dl += 1
        print(f"  + {name}", flush=True)
    for m in REL_RE.findall(txt):
        if m not in seen:
            seen.add(m); queue.append(m)

print(f"downloaded {dl} new modules; total tracked {len(seen)}", flush=True)
print("MODULES DONE", flush=True)
