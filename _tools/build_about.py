"""Build about/index.html ("How this site is maintained") from the per-guide change files.

Run from the repository root:  python _tools/build_about.py
Reads _tools/changes/<slug>.md (first line: the version; then markdown bullets) and
_tools/known_issues.md (optional markdown bullets), and writes about/index.html.
To record a later correction: add a bullet to the guide's change file under a new dated
heading line of the form "## December 2026, version 4.2", then run this again.
"""
import html, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES = [
    ("cybersecurity-roadmap", "Cybersecurity Career Roadmap"),
    ("devops-devsecops-roadmap", "DevOps and DevSecOps Roadmap"),
    ("secure-sdlc", "Secure SDLC"),
    ("network-concepts", "Network Concepts Guide"),
    ("os-unit-1", "Operating Systems Unit 1"),
    ("ai-knowledge-map", "The AI Knowledge Map"),
    ("agentic-ai-runtime", "Agentic AI Runtime Architecture"),
    ("ai-security", "Securing AI Systems and Agents"),
    ("data-intelligence-layer", "Data Intelligence Layer"),
    ("thinking-skills", "Thinking Skills"),
    ("iks-life-skills", "IKS Life Skills Curriculum"),
    ("iks-life-skills-cards", "IKS Life Skills: scenario cards and facilitator notes"),
]
HREF = {"iks-life-skills-cards": "../iks-life-skills/cards/"}
EM = chr(0x2014)


def inline(text):
    """Escape, then allow `code`, **bold** and [text](url) from the change files."""
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return t


def bullets(lines):
    items, cur = [], None
    for ln in lines:
        if re.match(r"^\s*[-*]\s+", ln):
            if cur is not None:
                items.append(cur)
            cur = re.sub(r"^\s*[-*]\s+", "", ln).strip()
        elif ln.strip() and cur is not None and not ln.startswith("#"):
            cur += " " + ln.strip()
    if cur is not None:
        items.append(cur)
    return items


def guide_block(slug, name):
    path = os.path.join(ROOT, "_tools", "changes", slug + ".md")
    if not os.path.exists(path):
        return ""
    lines = io.open(path, encoding="utf-8").read().splitlines()
    head = next((l for l in lines if l.strip()), "").lstrip("# ").strip()
    version = re.search(r"\d+\.\d+", head)
    items = bullets(lines[1:] if lines else [])
    if not items:
        return ""
    href = HREF.get(slug, "../%s/" % slug)
    out = ['<section class="chg" id="chg-%s">' % slug,
           '<h3><a href="%s">%s</a> <span class="ver">version %s, November 2026</span></h3>' % (href, html.escape(name), version.group(0) if version else "updated"),
           "<ul>"]
    out += ["<li>%s</li>" % inline(i) for i in items]
    out += ["</ul>", "</section>"]
    return "\n".join(out)


def known_issues():
    path = os.path.join(ROOT, "_tools", "known_issues.md")
    if not os.path.exists(path):
        return ""
    items = bullets(io.open(path, encoding="utf-8").read().splitlines())
    if not items:
        return ""
    return ('<h2 id="known-issues">Known gaps</h2>\n<p>Things I know are not yet right or not yet checked. They are listed here so that you know too.</p>\n<ul>\n'
            + "\n".join("<li>%s</li>" % inline(i) for i in items) + "\n</ul>")


def main():
    tpl = io.open(os.path.join(ROOT, "_tools", "about_template.html"), encoding="utf-8").read()
    blocks = "\n".join(b for b in (guide_block(s, n) for s, n in GUIDES) if b)
    page = tpl.replace("<!-- CHANGELOG -->", blocks).replace("<!-- KNOWN_ISSUES -->", known_issues())
    if EM in page:
        sys.exit("em dash in the built page: fix the change file that contains it")
    os.makedirs(os.path.join(ROOT, "about"), exist_ok=True)
    io.open(os.path.join(ROOT, "about", "index.html"), "w", encoding="utf-8", newline="\n").write(page)
    print("about/index.html written; guides with a changelog:", blocks.count('class="chg"'))


if __name__ == "__main__":
    main()
