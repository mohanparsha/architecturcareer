"""Write sitemap.xml at the repository root from _tools/site_meta.py.

Run from the repository root:  python _tools/build_sitemap.py
It is published at <SITE>sitemap.xml. Submit that address in Google Search Console.

There is deliberately no robots.txt. Crawlers read robots.txt only at the root of a host
(https://mohanparsha.github.io/robots.txt), which this repository does not serve; a copy in
this folder would be ignored. If the site moves to its own domain, add one then.
"""
import io, os, sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_meta as M  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

entries = [(M.SITE + p["path"], p["changefreq"]) for p in M.OTHER_PAGES]
entries += [(M.url(g["slug"]), "quarterly") for g in M.GUIDES]
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, freq in entries:
    rel = loc[len(M.SITE):]
    if not os.path.isfile(os.path.join(ROOT, rel.replace("/", os.sep), "index.html") if rel else os.path.join(ROOT, "index.html")):
        sys.exit("sitemap entry has no page in the repository: " + loc)
    freq = "monthly" if freq == "quarterly" else freq  # sitemaps.org has no "quarterly"
    lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq></url>" % (escape(loc), M.REVIEWED, freq))
lines.append("</urlset>")
io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("sitemap.xml written with", len(entries), "addresses")
