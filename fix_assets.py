#!/usr/bin/env python3
"""Second pass: localize any asset-host URLs still embedded in text assets (fonts loaded at runtime)."""
import os, re, urllib.request, urllib.parse

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
ASSET_HOSTS = {"framerusercontent.com", "fonts.gstatic.com", "fonts.googleapis.com", "app.framerstatic.com"}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

# strict URL: stop at backtick, quote, paren, comma, whitespace, backslash
URL_RE = re.compile(r"https://(?:framerusercontent\.com|fonts\.gstatic\.com|fonts\.googleapis\.com|app\.framerstatic\.com)/[^\s\"'`,()<>\\]+")

def local_for(url):
    p = urllib.parse.urlparse(url)
    path = p.path or "/index"
    if p.query:
        safe_q = re.sub(r"[^A-Za-z0-9._-]", "_", p.query)
        base, ext = os.path.splitext(path)
        path = f"{base}__{safe_q}{ext}"
    return f"/_assets/{p.netloc}{path}"

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f"  !! FAIL {url}: {e}", flush=True)
        return None

# collect all text assets
targets = []
for root, _, files in os.walk(OUT):
    for f in files:
        if f.endswith((".mjs", ".js", ".css", ".json", ".map")):
            targets.append(os.path.join(root, f))

all_urls = set()
for t in targets:
    with open(t, "r", encoding="utf-8", errors="replace") as fh:
        all_urls.update(URL_RE.findall(fh.read()))

print(f"{len(targets)} text assets, {len(all_urls)} unique asset-host URLs embedded", flush=True)

# download missing
dl = 0
for url in sorted(all_urls):
    local = local_for(url)
    dst = os.path.join(OUT, local.lstrip("/"))
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        continue
    data = fetch(url)
    if data is None:
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    dl += 1
    if dl % 5 == 0:
        print(f"  downloaded {dl}", flush=True)
print(f"downloaded {dl} new font/asset files", flush=True)

# rewrite text assets
changed = 0
for t in targets:
    with open(t, "r", encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    new = URL_RE.sub(lambda m: local_for(m.group(0)), txt)
    if new != txt:
        with open(t, "w", encoding="utf-8") as fh:
            fh.write(new)
        changed += 1
print(f"rewrote {changed} text assets", flush=True)
print("FIX DONE", flush=True)
