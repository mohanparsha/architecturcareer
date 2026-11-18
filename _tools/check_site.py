"""Check every internal link, anchor, image and redirect on the published site.

Run from the repository root:  python _tools/check_site.py
Exit code 0 means no broken internal link. Anchors that a page creates with JavaScript cannot
be seen in the file, so a missing anchor is reported as a warning unless it is in STRICT_ANCHORS.
External links are listed with --external (they are fetched; LinkedIn and font hosts are skipped).
"""
import io, os, re, sys, urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRICT_ANCHORS = {"guides", "resources", "changelog", "glossary", "soft-skills", "ugc-jeevan-kaushal", "auc-main"}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "//")


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.in_script = [], set(), False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        for key in ("href", "src"):
            v = a.get(key)
            if v and tag in ("a", "link", "img", "script", "source", "iframe"):
                self.refs.append((tag, v, self.getpos()[0]))
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "refresh":
            m = re.search(r"url=(.+)$", a.get("content") or "", re.I)
            if m:
                self.refs.append(("meta-refresh", m.group(1).strip(), self.getpos()[0]))


def pages():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_"))]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def parse(path):
    p = Links()
    text = io.open(path, encoding="utf-8", errors="replace").read()
    p.feed(text)
    # ids that scripts create from template strings in the same file, e.g. id="${x}" or id: 'glossary'
    p.ids.update(re.findall(r"""\bid=\\?["']([A-Za-z][\w-]*)""", text))
    return p


def main():
    cache, errors, warnings, external = {}, [], [], set()
    all_pages = sorted(pages())
    for path in all_pages:
        cache[path] = parse(path)
    for path in all_pages:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        for tag, ref, line in cache[path].refs:
            if "${" in ref or "{{" in ref or ref.startswith("#") and len(ref) == 1:
                continue
            if ref.startswith(SKIP_SCHEMES):
                if ref.startswith("http"):
                    external.add(ref)
                continue
            target, _, frag = ref.partition("#")
            target = target.split("?")[0]
            if target == "":
                tpath = path
            else:
                tpath = os.path.normpath(os.path.join(os.path.dirname(path), target.replace("/", os.sep)))
                if os.path.isdir(tpath):
                    tpath = os.path.join(tpath, "index.html")
            if not tpath.startswith(ROOT):
                errors.append("%s:%d  %s points outside the site: %s" % (rel, line, tag, ref))
                continue
            if not os.path.isfile(tpath):
                errors.append("%s:%d  broken %s: %s" % (rel, line, tag, ref))
                continue
            if target and target.endswith("/") is False and os.path.isdir(os.path.join(os.path.dirname(path), target)):
                warnings.append("%s:%d  folder link without trailing slash: %s" % (rel, line, ref))
            if frag and tpath.endswith(".html"):
                if tpath not in cache:
                    cache[tpath] = parse(tpath)
                if frag not in cache[tpath].ids:
                    msg = "%s:%d  anchor #%s not found in %s" % (rel, line, frag, os.path.relpath(tpath, ROOT).replace("\\", "/"))
                    (errors if frag in STRICT_ANCHORS else warnings).append(msg)
    print("pages checked: %d" % len(all_pages))
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("internal links: %s (%d error(s), %d warning(s))" % ("OK" if not errors else "BROKEN", len(errors), len(warnings)))
    if "--external" in sys.argv:
        bad = 0
        for u in sorted(external):
            if any(h in u for h in ("linkedin.com", "fonts.googleapis.com", "fonts.gstatic.com", "gc.zgo.at", "goatcounter.com/count")):
                continue
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (link check)"})
                code = urllib.request.urlopen(req, timeout=25).status
            except Exception as ex:  # noqa: BLE001
                code = getattr(ex, "code", None) or type(ex).__name__
            if code != 200:
                bad += 1
                print("EXT  %s  %s" % (code, u))
        print("external links not returning 200: %d of %d (a site may refuse automated checks: open those by hand)" % (bad, len(external)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
