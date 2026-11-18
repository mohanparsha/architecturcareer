"""Check one guide page against the site's shared rules.

Usage (from the repository root):  python _tools/check_page.py <slug> [<slug> ...]
        or all guides:             python _tools/check_page.py --all

Exit code 0 means every listed page passed. The checks read the file only; use
_tools/shot.py to prove the page renders.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES = ["cybersecurity-roadmap", "devops-devsecops-roadmap", "secure-sdlc", "network-concepts", "os-unit-1",
          "agentic-ai-runtime", "ai-security", "ai-knowledge-map", "data-intelligence-layer", "thinking-skills",
          "iks-life-skills"]
EM, EN = chr(0x2014), chr(0x2013)


def check(slug):
    path = os.path.join(ROOT, slug, "index.html")
    s = io.open(path, encoding="utf-8").read()
    fails = []

    def need(cond, msg):
        if not cond:
            fails.append(msg)

    need(EM not in s, "contains %d em dash(es) (U+2014)" % s.count(EM))
    spaced_en = len(re.findall(r"\s" + EN + r"\s", s))
    need(spaced_en == 0, "contains %d spaced en dash(es) (U+2013 with spaces)" % spaced_en)
    need("&mdash;" not in s and "&#8212;" not in s and "&#x2014;" not in s.lower(), "contains an em dash entity")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    need(bool(t) and t.group(1).strip().endswith("| Architect U'r Career"), "title must end with \"| Architect U'r Career\"")
    need(s.count('class="auc-bar"') == 1, "shared header strip must appear exactly once")
    need(s.count('class="auc-foot"') == 1, "shared footer must appear exactly once")
    need(s.count('class="auc-skip"') == 1, "skip link must appear exactly once")
    need('id="auc-main"' in s, 'main content needs id="auc-main"')
    need('href="../assets/auc-guide.css"' in s, "missing ../assets/auc-guide.css")
    need('src="../assets/auc-guide.js"' in s, "missing ../assets/auc-guide.js")
    need(len(re.findall(r"gc\.zgo\.at/count\.js", s)) == 1, "GoatCounter snippet must appear exactly once")
    need('rel="canonical" href="https://mohanparsha.github.io/architecturcareer/%s/"' % slug in s, "missing or wrong canonical link")
    for tag in ("og:title", "og:description", "og:url", "og:image"):
        need(('property="%s"' % tag) in s, "missing %s" % tag)
    need('name="description"' in s, "missing meta description")
    need('name="viewport"' in s, "missing viewport meta")
    need("creativecommons.org/licenses/by-nc-sa/4.0/" in s, "missing licence link")
    need("All rights reserved" not in s and "All Rights Reserved" not in s, "still says All rights reserved")
    need("Architecting U'r Career" not in s, "old brand wording \"Architecting U'r Career\"")
    need("Last reviewed" in s, "missing \"Last reviewed\" date")
    need(re.search(r"<html[^>]*\blang=", s) is not None, "missing lang attribute on <html>")
    for old in ("network_glossary.html", "network_concepts_guide.html", "_v3.0.html", "_v2.5.html", "v2.6.html", "_3.0.html"):
        need(old not in s, "links to an old file name (%s)" % old)
    print(("PASS " if not fails else "FAIL ") + slug + ("" if not fails else "\n  - " + "\n  - ".join(fails)))
    return not fails


if __name__ == "__main__":
    args = sys.argv[1:]
    slugs = GUIDES if args == ["--all"] else args
    if not slugs:
        sys.exit(__doc__)
    ok = [check(x) for x in slugs]
    sys.exit(0 if all(ok) else 1)
