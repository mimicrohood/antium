#!/usr/bin/env python3
"""Mirror the Framer site witty-goal-587605.framer.app for fully-offline local hosting."""
import os, re, sys, time, urllib.request, urllib.parse

SITE = "https://witty-goal-587605.framer.app"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

PAGES = [
    "/",
    "/tracks",
    "/docs",
    "/docs/the-origins-of-mycoid-why-a-fungal-network",
    "/docs/inside-mycela-s-mind-spores-threads-and-silent-growth",
    "/docs/spore-signals-how-mycoid-communicates",
    "/docs/a-living-web-the-research-value-of-mycoid",
    "/docs/the-future-of-mycoid-distributed-cognition-and-beyond",
]

# Hosts whose assets we mirror locally under site/_assets/<host>/...
ASSET_HOSTS = {
    "framerusercontent.com",
    "fonts.gstatic.com",
    "fonts.googleapis.com",
    "app.framerstatic.com",
}

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

downloaded = {}   # url -> local relative path (from site root, starts with /_assets/...)
queue = []
seen = set()

def fetch(url, tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.read(), r.headers.get("Content-Type", "")
        except Exception as e:
            last = e
            if i + 1 < tries:
                time.sleep(0.5)
    print(f"  !! FAILED {url}: {last}", flush=True)
    return None, None

def local_for_asset(url):
    """Map an absolute asset URL to a local path like /_assets/<host>/<path>."""
    p = urllib.parse.urlparse(url)
    host = p.netloc
    path = p.path
    if not path or path.endswith("/"):
        path = path + "index"
    # keep query in filename to disambiguate (rare for framer)
    if p.query:
        safe_q = re.sub(r"[^A-Za-z0-9._-]", "_", p.query)
        base, ext = os.path.splitext(path)
        path = f"{base}__{safe_q}{ext}"
    return f"/_assets/{host}{path}"

def is_asset_host(host):
    return host in ASSET_HOSTS

def valid_asset_url(url):
    """Reject junk the regex may harvest from minified JS (truncated / placeholder urls)."""
    p = urllib.parse.urlparse(url)
    if p.netloc not in ASSET_HOSTS:
        return False
    if not p.path or p.path == "/":
        return False
    # framer asset paths always have an extension or a known prefix
    if len(url) > 400:
        return False
    if any(c in url for c in ("${", "`", "\\")):
        return False
    return True

def enqueue(url):
    if url not in seen and valid_asset_url(url):
        seen.add(url)
        queue.append(url)

# Regex to find URLs in text (html/css/js)
URL_RE = re.compile(r"""(https?://[^\s"'()<>\\]+)""")

def process_asset_text(url, text):
    """Rewrite absolute asset URLs inside a text asset (js/css) to local, enqueue new ones."""
    found = set(URL_RE.findall(text))
    for f in found:
        f_clean = f.rstrip('\\')
        host = urllib.parse.urlparse(f_clean).netloc
        if is_asset_host(host):
            enqueue(f_clean)
    # rewrite after all enqueued (paths computed deterministically)
    def repl(m):
        u = m.group(1)
        host = urllib.parse.urlparse(u).netloc
        if is_asset_host(host):
            return local_for_asset(u)
        return u
    return URL_RE.sub(repl, text)

def save(relpath_from_root, data):
    dst = os.path.join(OUT, relpath_from_root.lstrip("/"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)

TEXT_EXT = (".mjs", ".js", ".css", ".json", ".map", ".svg")

def run_assets():
    processed = 0
    while queue:
        url = queue.pop(0)
        local = local_for_asset(url)
        dst = os.path.join(OUT, local.lstrip("/"))
        # resume: skip files we've already saved, but still record + process text for rewrites
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            downloaded[url] = local
            # re-scan text assets for further deps so the queue stays complete
            p0 = urllib.parse.urlparse(url)
            if p0.path.endswith((".mjs", ".js", ".css")):
                try:
                    with open(dst, "r", encoding="utf-8", errors="replace") as fh:
                        for f in URL_RE.findall(fh.read()):
                            host = urllib.parse.urlparse(f).netloc
                            if is_asset_host(host):
                                enqueue(f)
                except Exception:
                    pass
            continue
        data, ctype = fetch(url)
        if data is None:
            continue
        p = urllib.parse.urlparse(url)
        if p.path.endswith((".mjs", ".js", ".css", ".json", ".map")):
            text = data.decode("utf-8", "replace")
            text = process_asset_text(url, text)
            data = text.encode("utf-8")
        save(local, data)
        downloaded[url] = local
        processed += 1
        if processed % 10 == 0:
            print(f"  ... {processed} new assets, {len(queue)} queued", flush=True)
    print(f"  assets done: {processed} new", flush=True)

def strip_and_rewrite_html(html):
    # 1) strip Framer editor bootstrap + telemetry
    html = re.sub(r'<script[^>]*src="https://framer\.com/edit/init\.mjs"[^>]*>\s*</script>', "", html)
    html = re.sub(r'<link[^>]*href="https://framer\.com/edit/init\.mjs"[^>]*>', "", html)
    # events.framer.com beacons -> neutralize any absolute ref (leave DOM but no network)
    html = html.replace("https://events.framer.com", "about:blank#events")
    # 2) enqueue + rewrite asset-host absolute URLs
    for m in URL_RE.findall(html):
        host = urllib.parse.urlparse(m).netloc
        if is_asset_host(host):
            enqueue(m)
    def repl(m):
        u = m.group(1)
        host = urllib.parse.urlparse(u).netloc
        if is_asset_host(host):
            return local_for_asset(u)
        return u
    html = URL_RE.sub(repl, html)
    return html

def page_to_path(route):
    if route == "/":
        return "/index.html"
    return route.rstrip("/") + "/index.html"

def run_pages():
    for route in PAGES:
        url = SITE + route
        data, ctype = fetch(url)
        if data is None:
            print(f"  !! page failed: {route}")
            continue
        html = data.decode("utf-8", "replace")
        html = strip_and_rewrite_html(html)
        save(page_to_path(route), html.encode("utf-8"))
        print(f"  page: {route} -> {page_to_path(route)}")

if __name__ == "__main__":
    print("== pages ==")
    run_pages()
    print(f"== assets (queue={len(queue)}) ==")
    run_assets()
    print("DONE")
