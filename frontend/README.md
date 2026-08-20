# rayoid — frontend

The rayoid site: a self-contained static site that runs fully offline.

## Run

```bash
python serve.py 8848        # or double-click start.bat (Windows)
```

Then open **http://127.0.0.1:8848/**.

> Must be served with `serve.py`. The `/docs` essays load their body content through a custom
> byte-range CMS protocol that `serve.py` implements; a plain `python -m http.server` leaves the
> doc pages blank.

## Pages

- **/** — homepage: who rayoid is, live stats, and the docs preview
- **/tracks** — the **Pathways** roadmap (Pulse Emergence → Current Expansion → Web Formation)
- **/docs** — five essays reading the project from signals to networks, plus each essay's detail page

## Layout

```
site/
├── index.html                 homepage
├── tracks/index.html
├── docs/index.html            essay index (CMS-driven)
├── docs/<slug>/index.html     5 essays
└── _assets/                   all local assets: JS modules, CSS, images, fonts, CMS data blocks
serve.py                       local server with CMS byte-range support
start.bat                      one-click launch
```

The essay content (titles, subtitles, bodies) lives in the binary CMS data blocks under
`_assets/.../cms/` and is hydrated into the pages at load time. The scripts in the repo-level
`tools/` directory were used to author and rebrand that content.
