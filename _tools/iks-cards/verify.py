# -*- coding: utf-8 -*-
"""Check iks-life-skills/cards/index.html: static rules, screen render at 1280 and 375, and the print PDF.

Usage, from anywhere:  python _tools/iks-cards/verify.py <output-folder>

Writes screenshots and two PDFs (the whole pack, and Week 9 printed on its own) to the output folder,
which should be outside the repository. Needs Playwright with Microsoft Edge, and PyMuPDF (fitz).
Exit code 0 means every check passed. The repository root is found from this file's own location.
"""
import io, os, re, sys
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(REPO, "iks-life-skills", "cards", "index.html")
URL = "file:///" + PAGE.replace("\\", "/").replace(" ", "%20")
if len(sys.argv) < 2:
    sys.exit(__doc__)
OUT = os.path.abspath(sys.argv[1])
os.makedirs(OUT, exist_ok=True)
MM = 96 / 25.4
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- static checks
s = io.open(PAGE, encoding="utf-8").read()
EM, EN = chr(0x2014), chr(0x2013)
check("no em dash", EM not in s and "&mdash;" not in s and "&#8212;" not in s and "&#x2014;" not in s.lower())
check("no en dash", EN not in s and "&ndash;" not in s)
check("title", "<title>IKS Life Skills: scenario cards and facilitator notes | Architect U'r Career</title>" in s)
check("one strip", s.count('class="auc-bar"') == 1)
check("one footer", s.count('class="auc-foot"') == 1)
check("one skip link", s.count('class="auc-skip"') == 1)
check("auc-main", s.count('id="auc-main"') == 1)
check("stylesheet two levels up", 'href="../../assets/auc-guide.css"' in s and 'href="../assets/' not in s)
check("script two levels up", 'src="../../assets/auc-guide.js"' in s and 'src="../assets/' not in s)
check("one GoatCounter", len(re.findall(r"gc\.zgo\.at/count\.js", s)) == 1)
check("canonical", 'rel="canonical" href="https://mohanparsha.github.io/architecturcareer/iks-life-skills/cards/"' in s)
check("og:url", 'property="og:url" content="https://mohanparsha.github.io/architecturcareer/iks-life-skills/cards/"' in s)
check("og tags", all(('property="%s"' % t) in s for t in ("og:title", "og:description", "og:image", "og:type")))
check("description", 'name="description"' in s)
check("viewport", 'name="viewport"' in s)
check("licence link", "creativecommons.org/licenses/by-nc-sa/4.0/" in s)
check("no All rights reserved", "All rights reserved" not in s)
check("brand", "Architecting U'r Career" not in s)
check("Last reviewed", "Last reviewed" in s)
check("lang en-GB", '<html lang="en-GB">' in s)
check("crumb to curriculum", '<a href="../">IKS Life Skills Curriculum</a>' in s)
check("home link two levels up", '<a class="auc-bar-home" href="../../">' in s)
check("about link two levels up", 'href="../../about/"' in s)
check("version shown twice and agreeing", "Version 1.0, November 2026" in s and "version 1.0, last reviewed November 2026" in s)
check("independence statement", "These cards are original material written for this curriculum.</strong> They are an independent work and are not published, endorsed or approved by UGC, NCERT, CBSE or any government body." in s)
check("print button is a button", re.search(r'<button type="button"[^>]*data-print="all">Print this pack</button>', s) is not None)
ext = re.findall(r'<a [^>]*href="https?://[^"]+"[^>]*>', s)
bad = [a for a in ext if 'target="_blank"' not in a or "noopener" not in a]
check("outbound links target=_blank rel=noopener (%d links)" % len(ext), not bad, str(bad))
print("external resources:", re.findall(r'<(?:script|link|img)[^>]+(?:src|href)="(https?:[^"]+)"', s))
m_pages = re.search(r"(\d+) A4 pages", s)
claimed_pages = int(m_pages.group(1)) if m_pages else None
m_cards = re.search(r"November 2026 · (\d+) cards", s)
claimed_cards = int(m_cards.group(1)) if m_cards else None

# ---------------------------------------------------------------- browser checks
with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w, h, mobile in ((1280, 900, False), (375, 812, True)):
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
        ctx.route("**/gc.zgo.at/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=""))
        pg = ctx.new_page()
        errs, failed = [], []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(800)
        info = pg.evaluate("""() => ({
            scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
            scrollHeight: document.documentElement.scrollHeight,
            bar: document.querySelectorAll('.auc-bar').length, foot: document.querySelectorAll('.auc-foot').length,
            barTop: document.querySelector('.auc-bar').getBoundingClientRect().top,
            cards: document.querySelectorAll('.card:not(.card-blank)').length,
            blanksVisible: Array.from(document.querySelectorAll('.card-blank')).filter(e => e.offsetParent !== null).length,
            buttons: document.querySelectorAll('button[data-print]').length
        })""")
        print("width %d: %s" % (w, info))
        check("width %d: no horizontal overflow" % w, info["scrollWidth"] <= info["innerWidth"] + 1, "%d > %d" % (info["scrollWidth"], info["innerWidth"]))
        check("width %d: no console errors" % w, not errs, str(errs))
        check("width %d: no failed requests" % w, not [f for f in failed if "zgo.at" not in f], str(failed))
        check("width %d: strip at the top, one strip, one footer" % w, info["barTop"] == 0 and info["bar"] == 1 and info["foot"] == 1)
        check("width %d: blank cards hidden on screen" % w, info["blanksVisible"] == 0)
        check("width %d: card count matches the header (%s)" % (w, claimed_cards), info["cards"] == claimed_cards, str(info["cards"]))
        pg.screenshot(path=os.path.join(OUT, "cards-%d-top.png" % w), clip={"x": 0, "y": 0, "width": w, "height": min(3600, info["scrollHeight"])}, full_page=True)
        for anchor, name, height in (("week-1", "week1", 4200), ("week-9", "week9", 3400)):
            y = pg.evaluate("(id) => document.getElementById(id).getBoundingClientRect().top + scrollY", anchor)
            pg.screenshot(path=os.path.join(OUT, "cards-%d-%s.png" % (w, name)), clip={"x": 0, "y": y - 10, "width": w, "height": height}, full_page=True)
        y = pg.evaluate("() => document.getElementById('what-is-covered').getBoundingClientRect().top + scrollY")
        pg.screenshot(path=os.path.join(OUT, "cards-%d-end.png" % w), clip={"x": 0, "y": y - 40, "width": w, "height": info["scrollHeight"] - y + 40}, full_page=True)
        if w == 1280:
            pg.evaluate("() => { window.__p = []; window.print = () => window.__p.push(document.body.getAttribute('data-print-only') || 'all'); }")
            pg.click('button[data-print="all"]')
            pg.click('button[data-print="week-3"]')
            pg.focus('button[data-print="week-9"]')
            pg.keyboard.press("Enter")
            calls = pg.evaluate("() => window.__p")
            check("print buttons call window.print with the right scope", calls == ["all", "week-3", "week-9"], str(calls))
            pg.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
            left = pg.evaluate("() => [document.body.getAttribute('data-print-only'), document.querySelectorAll('.is-print-target').length]")
            check("print scope cleared after printing", left == [None, 0], str(left))
        ctx.close()

    # ---------------------------------------------------------------- print layout
    ctx = b.new_context(viewport={"width": round(190 * MM), "height": round(277 * MM)}, device_scale_factor=1)
    ctx.route("**/gc.zgo.at/**", lambda r: r.fulfill(status=200, content_type="application/javascript", body=""))
    pg = ctx.new_page()
    pg.goto(URL, wait_until="load")
    pg.emulate_media(media="print")
    pg.wait_for_timeout(500)
    m = pg.evaluate("""() => {
        const mm = 96 / 25.4, page = 277 * mm;
        const out = {page: page, cards: [], notes: [], sheets: [], blanks: 0};
        document.querySelectorAll('.sheet').forEach(sh => out.sheets.push({h: Math.round(sh.getBoundingClientRect().height), n: sh.querySelectorAll('.card').length}));
        document.querySelectorAll('.card').forEach(c => {
            if (c.classList.contains('card-blank')) { out.blanks++; }
            const inn = c.querySelector('.card-in'), cr = c.querySelector('.card-credit');
            const last = inn.lastElementChild.getBoundingClientRect().bottom;
            const limit = cr.getBoundingClientRect().top;
            out.cards.push({id: c.id || 'blank', h: Math.round(c.getBoundingClientRect().height), spare: Math.round(limit - last),
                            clipped: c.scrollHeight > c.clientHeight + 1, creditInside: cr.getBoundingClientRect().bottom <= c.getBoundingClientRect().bottom + 0.5,
                            dashed: getComputedStyle(c).borderTopStyle === 'dashed' && getComputedStyle(c).borderLeftStyle === 'dashed'});
        });
        const head = document.querySelector('.pk-head'), open = document.querySelector('.pk-open');
        out.opening = Math.round(open.getBoundingClientRect().bottom - head.getBoundingClientRect().top);
        document.querySelectorAll('.pk-note').forEach(n => out.notes.push({id: n.parentElement.id, h: Math.round(n.getBoundingClientRect().height)}));
        const map = document.querySelector('.pk-map'), foot = document.querySelector('.auc-foot');
        out.mapAndFoot = Math.round(foot.getBoundingClientRect().bottom - map.getBoundingClientRect().top);
        out.fills = Array.from(document.querySelectorAll('main *, .auc-foot, .auc-foot *')).filter(e => {
            const bg = getComputedStyle(e).backgroundColor;
            return e.offsetParent !== null && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'rgb(255, 255, 255)';
        }).map(e => (e.className || e.tagName) + ' ' + getComputedStyle(e).backgroundColor).slice(0, 10);
        out.minFontPt = Math.min.apply(null, Array.from(document.querySelectorAll('.card:not(.card-blank) .card-in *')).map(e => parseFloat(getComputedStyle(e).fontSize) * 0.75));
        out.stripHidden = getComputedStyle(document.querySelector('.auc-bar')).display === 'none';
        out.footShown = getComputedStyle(document.querySelector('.auc-foot')).display !== 'none';
        return out;
    }""")
    page_px = m["page"]
    real = [c for c in m["cards"] if c["id"] != "blank"]
    print("print layout: page content height %.0f px; %d sheets; %d written cards, %d blank; card heights %s" % (
        page_px, len(m["sheets"]), len(real), m["blanks"], sorted(set(c["h"] for c in m["cards"]))))
    print("  least spare space inside a written card (px):", [(c["id"], c["spare"]) for c in sorted(real, key=lambda c: c["spare"])[:6]])
    check("print: every sheet holds four cards", all(sh["n"] == 4 for sh in m["sheets"]), str([sh["n"] for sh in m["sheets"]]))
    check("print: every sheet fits one page", all(sh["h"] <= page_px for sh in m["sheets"]))
    clipped = [c["id"] for c in m["cards"] if c["clipped"] or c["spare"] < 0 or not c["creditInside"]]
    check("print: no card clipped or overflowing", not clipped, str(clipped))
    check("print: every written card keeps at least 25 px spare", min(c["spare"] for c in real) >= 25, str(min(c["spare"] for c in real)))
    check("print: dashed cut lines on every card", all(c["dashed"] for c in m["cards"]))
    check("print: smallest type inside a written card is at least 11 pt", m["minFontPt"] >= 10.99, "%.2f" % m["minFontPt"])
    check("print: opening fits one page (%d px)" % m["opening"], m["opening"] <= page_px)
    for n in m["notes"]:
        check("print: note %s fits one page (%d px)" % (n["id"], n["h"]), n["h"] <= page_px)
    check("print: coverage table and footer fit one page (%d px)" % m["mapAndFoot"], m["mapAndFoot"] <= page_px)
    check("print: no background fills", not m["fills"], str(m["fills"]))
    check("print: strip hidden, licence footer shown", m["stripHidden"] and m["footShown"])

    pdf = os.path.join(OUT, "iks-cards-pack.pdf")
    pg.pdf(path=pdf, format="A4", prefer_css_page_size=True, print_background=False)
    pg.evaluate("() => { document.getElementById('week-9').classList.add('is-print-target'); document.body.setAttribute('data-print-only', 'week-9'); }")
    pdf9 = os.path.join(OUT, "iks-cards-week9-only.pdf")
    pg.pdf(path=pdf9, format="A4", prefer_css_page_size=True, print_background=False)
    ctx.close()
    b.close()

import fitz


def kinds_of(path):
    d = fitz.open(path)
    kinds = []
    for pgx in d:
        t = pgx.get_text()
        ncards = len(re.findall(r"Week \d+ · Card \d+", t, re.I)) + len(re.findall("your own card", t, re.I))
        if not t.strip():
            kind = "BLANK"
        elif "Cut along the dashed lines" in t:
            kind = "cards:%d" % ncards
        elif "facilitator note" in t.lower() and "Aim." in t:
            kind = "note"
        elif "Before you start" in t:
            kind = "opening"
        elif "What is covered" in t:
            kind = "coverage"
        else:
            kind = "OTHER"
        kinds.append(kind)
    size = tuple(round(x) for x in d[0].rect)[2:]
    d.close()
    return kinds, size


kinds, size = kinds_of(pdf)
print("PDF %s: %d pages, page size %s pt" % (os.path.basename(pdf), len(kinds), size))
print("  pages:", " | ".join("%d %s" % (i + 1, k) for i, k in enumerate(kinds)))
check("PDF: A4", size == (595, 842), str(size))
check("PDF: page count matches the header (%s)" % claimed_pages, len(kinds) == claimed_pages, str(len(kinds)))
check("PDF: no blank or unexpected page", not [k for k in kinds if k in ("BLANK", "OTHER")])
check("PDF: every card page has four cards", all(k == "cards:4" for k in kinds if k.startswith("cards")))
check("PDF: 1 opening, 12 notes, 1 coverage page", kinds.count("opening") == 1 and kinds.count("note") == 12 and kinds.count("coverage") == 1)
kinds9, _ = kinds_of(pdf9)
print("PDF %s: %d pages: %s" % (os.path.basename(pdf9), len(kinds9), " | ".join(kinds9)))
check("PDF: Week 9 alone prints its note and card sheets only", kinds9[0] == "note" and all(k == "cards:4" for k in kinds9[1:]) and len(kinds9) >= 2)

print("")
print("RESULT: %s" % ("PASS, every check passed" if not FAILS else "FAIL: " + "; ".join(FAILS)))
sys.exit(1 if FAILS else 0)
