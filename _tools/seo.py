"""Write each guide's search title, description and structured data from _tools/site_meta.py.

Run from the repository root:  python _tools/seo.py
Safe to run again. It touches only <title>, the description, og: and twitter: title and
description tags, and one JSON-LD block between <!-- auc:ld --> markers in each guide's <head>.
The home page gets a WebSite block beside its existing Person block.
"""
import html, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_meta as M  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EM = chr(0x2014)


def ld_block(obj):
    body = json.dumps(obj, ensure_ascii=False, indent=2)
    return "<!-- auc:ld -->\n<script type=\"application/ld+json\">\n%s\n</script>\n<!-- /auc:ld -->" % body


def set_meta(s, attr, key, value, path):
    """Replace the content of <meta {attr}="{key}" content="..."> exactly once, or add it if missing."""
    esc = html.escape(value, quote=True)
    pat = re.compile(r'(<meta\s+%s="%s"\s+content=")[^"]*(")' % (attr, re.escape(key)))
    n = len(pat.findall(s))
    if n > 1:
        sys.exit("%s: %d tags for %s=%s" % (path, n, attr, key))
    if n == 1:
        return pat.sub(lambda m: m.group(1) + esc + m.group(2), s)
    return s.replace("</title>", '</title>\n<meta %s="%s" content="%s">' % (attr, key, esc), 1)


def guide_ld(g):
    return {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": g["name"],
        "headline": g["seo_title"],
        "description": g["description"],
        "url": M.url(g["slug"]),
        "inLanguage": "en-GB",
        "learningResourceType": g["type"],
        "educationalLevel": g["level"],
        "audience": {"@type": "EducationalAudience", "educationalRole": g["audience"]},
        "teaches": g["learn"],
        "isAccessibleForFree": True,
        "license": M.LICENCE_URL,
        "version": g["version"],
        "dateModified": M.REVIEWED,
        "author": {"@type": "Person", "name": M.AUTHOR, "url": M.SITE},
        "isPartOf": {"@type": "WebSite", "name": M.SITE_NAME, "url": M.SITE},
    }


def write_guide(g):
    path = os.path.join(ROOT, g["slug"], "index.html")
    s0 = io.open(path, encoding="utf-8", newline="").read()
    s = s0
    title = "%s | %s" % (g["seo_title"], M.SITE_NAME)
    s, n = re.subn(r"<title>.*?</title>", "<title>%s</title>" % html.escape(title, quote=False), s, count=1, flags=re.S)
    if n != 1:
        sys.exit(path + ": no <title>")
    s = set_meta(s, "name", "description", g["description"], path)
    s = set_meta(s, "property", "og:title", title, path)
    s = set_meta(s, "property", "og:description", g["description"], path)
    if 'name="twitter:title"' in s:
        s = set_meta(s, "name", "twitter:title", title, path)
    if 'name="twitter:description"' in s:
        s = set_meta(s, "name", "twitter:description", g["description"], path)
    # one structured-data block: drop any earlier hand-written block, then insert ours before </head>
    s = re.sub(r"\s*<!-- auc:ld -->.*?<!-- /auc:ld -->", "", s, flags=re.S)
    s = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", s, flags=re.S)
    s = s.replace("</head>", ld_block(guide_ld(g)) + "\n</head>", 1)
    if EM in s:
        sys.exit(path + ": contains an em dash")
    if s != s0:
        io.open(path, "w", encoding="utf-8", newline="").write(s)
        return True
    return False


def write_home():
    path = os.path.join(ROOT, "index.html")
    s0 = io.open(path, encoding="utf-8", newline="").read()
    site = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": M.SITE_NAME,
        "url": M.SITE,
        "inLanguage": "en-GB",
        "description": "Free guides for careers in security, cloud and AI, arranged as three learning paths, by %s." % M.AUTHOR,
        "license": M.LICENCE_URL,
        "author": {"@type": "Person", "name": M.AUTHOR, "url": M.SITE},
        "hasPart": [{"@type": "LearningResource", "name": g["name"], "url": M.url(g["slug"])} for g in M.GUIDES],
    }
    s = re.sub(r"\s*<!-- auc:ld -->.*?<!-- /auc:ld -->", "", s0, flags=re.S)
    s = s.replace("</head>", ld_block(site) + "\n</head>", 1)
    if s != s0:
        io.open(path, "w", encoding="utf-8", newline="").write(s)
        return True
    return False


if __name__ == "__main__":
    changed = [g["slug"] for g in M.GUIDES if write_guide(g)]
    if write_home():
        changed.append("home")
    print("pages changed:", len(changed), changed)
