import re, glob

for p in glob.glob("site/**/*.html", recursive=True):
    s = open(p, encoding="utf-8").read()
    o = s

    # Remove the entire <div id="__framer-badge-container">...</div> (balanced)
    key = '<div id="__framer-badge-container">'
    i = s.find(key)
    if i != -1:
        tail = s[i:]
        depth = 0
        end = None
        for m in re.finditer(r'<div\b|</div>', tail):
            depth += 1 if m.group() != '</div>' else -1
            if depth == 0:
                end = m.end()
                break
        if end:
            s = s[:i] + s[i + end:]

    # CSS fallback: force-hide the badge container if any remnant remains
    if "__framer-badge-container" in s and "/*hide-badge*/" not in s:
        s = s.replace("</head>",
                      '<style>/*hide-badge*/#__framer-badge-container,.__framer-badge{display:none!important}</style></head>')

    if s != o:
        open(p, "w", encoding="utf-8").write(s)
        print("cleaned badge:", p)

print("BADGE HTML DONE")
