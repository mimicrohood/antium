#!/usr/bin/env python3
"""Fix Framer CMS chunk loading for offline: download .framercms data chunks and patch new URL() bases."""
import os, re, urllib.request, urllib.parse

SITES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "site", "_assets", "framerusercontent.com", "sites", "4GgFjAnjYT1KMBZEvvLhvC")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

# Match: new URL(`<rel>`,`</_assets/framerusercontent.com/modules/.../<name>.js`)
PAT = re.compile(r'new URL\(`(\.[^`]*)`,`(/_assets/framerusercontent\.com/modules/[^`]*?)`\)')

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()
    except Exception as e:
        print(f"  !! FAIL {url}: {e}", flush=True)
        return None

targets = [f for f in os.listdir(SITES) if f.endswith((".mjs", ".js"))]
chunks = {}   # local_rel_path (under site) -> remote url

for fn in targets:
    fp = os.path.join(SITES, fn)
    txt = open(fp, encoding="utf-8", errors="replace").read()
    for rel, base_local in PAT.findall(txt):
        # resolve rel against the base's directory (base is a .../x.js file path)
        base_dir = base_local.rsplit("/", 1)[0] + "/"
        resolved_local = urllib.parse.urljoin(base_dir, rel)      # /_assets/.../modules/.../chunk.framercms
        cms_local = resolved_local.replace("/modules/", "/cms/")  # what runtime will request
        # remote equivalent
        remote = "https://framerusercontent.com" + cms_local.replace("/_assets/framerusercontent.com", "")
        chunks[cms_local] = remote

print(f"{len(chunks)} unique CMS chunk(s) to download", flush=True)
for local_rel, remote in sorted(chunks.items()):
    dst = os.path.join(ROOT, local_rel.lstrip("/"))
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print(f"  = exists {local_rel}", flush=True); continue
    data = fetch(remote)
    if data is None:
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    print(f"  + {local_rel} ({len(data)} bytes)", flush=True)

# Patch the new URL() base to be absolute against location.href
patched = 0
for fn in targets:
    fp = os.path.join(SITES, fn)
    txt = open(fp, encoding="utf-8", errors="replace").read()
    new = PAT.sub(lambda m: f'new URL(`{m.group(1)}`,new URL(`{m.group(2)}`,location.href))', txt)
    if new != txt:
        open(fp, "w", encoding="utf-8").write(new)
        patched += 1
        print(f"  patched {fn}", flush=True)
print(f"patched {patched} module(s)", flush=True)
print("CMS FIX DONE", flush=True)
