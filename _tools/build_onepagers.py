"""Build one A4 summary per guide, for printing and for sharing in class groups.

Run from the repository root:  python _tools/build_onepagers.py
Reads _tools/site_meta.py and writes, under print/:
  <slug>.pdf     A4, one page, for printing
  <slug>.png     the same page as an image, for WhatsApp and similar
  thumbs/<slug>.jpg   small preview for the index page
  architect-ur-career-one-pagers.pdf   all of them in one file
  index.html     the page that lists them
Each QR code opens the guide with ?campaign=onepager, so GoatCounter can count scans.
Then it proves the output: every QR code is decoded from its image and compared with the
address it should hold, and every page is checked to fit A4 without overflow.
Needs: segno (QR codes), Playwright with Edge, Pillow, pypdf, OpenCV (cv2) for the decode check.
"""
import html, io, os, shutil, sys, tempfile

import segno
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_meta as M  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print")
EM, EN = chr(0x2014), chr(0x2013)
A4_W, A4_H = 794, 1123  # CSS pixels at 96 per inch
e = lambda t: html.escape(t, quote=True)  # noqa: E731

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 15mm 16mm 12mm; display: flex; flex-direction: column;
        font-family: "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif; color: #0b1220; overflow: hidden; }
.top { display: flex; justify-content: space-between; align-items: baseline; gap: 6mm;
       border-bottom: 3px solid #047857; padding-bottom: 3mm; font-size: 10.5pt; }
.brand { font-weight: 700; letter-spacing: .01em; }
.pathlabel { color: #334155; text-align: right; }
h1 { font-size: 27pt; line-height: 1.12; margin: 9mm 0 3mm; letter-spacing: -.01em; }
.what { font-size: 14pt; line-height: 1.4; color: #1f2937; margin: 0 0 5mm; }
.who { background: #ecfdf5; border-left: 5px solid #047857; padding: 3mm 4mm; font-size: 12pt; line-height: 1.4; margin: 0 0 7mm; }
.who b { color: #065f46; }
h2 { font-size: 11pt; letter-spacing: .07em; text-transform: uppercase; color: #047857; margin: 0 0 3.5mm; }
ol { list-style: none; padding: 0; margin: 0; counter-reset: n; }
ol li { counter-increment: n; position: relative; padding-left: 11mm; margin: 0 0 4.2mm; font-size: 12.8pt; line-height: 1.45; }
ol li::before { content: counter(n); position: absolute; left: 0; top: .3mm; width: 7.2mm; height: 7.2mm; border-radius: 50%;
                background: #047857; color: #fff; font-weight: 700; font-size: 10.5pt; display: flex; align-items: center; justify-content: center; }
.scan { margin-top: auto; display: flex; gap: 7mm; align-items: center; border: 1.5px solid #cbd5e1; border-radius: 4mm; padding: 4.5mm 5mm; }
.qr { flex: 0 0 42mm; width: 42mm; height: 42mm; }
.qr svg { width: 42mm; height: 42mm; display: block; }
.t1 { font-size: 15pt; font-weight: 700; margin: 0 0 1.5mm; }
.t2 { font-size: 11pt; color: #334155; margin: 0 0 2.5mm; line-height: 1.4; }
.url { font-family: Consolas, "Cascadia Mono", "Courier New", monospace; font-size: 10pt; color: #0b1220; overflow-wrap: anywhere; }
.next { font-size: 10.5pt; color: #334155; margin: 4mm 0 0; line-height: 1.4; }
.next b { color: #0b1220; }
.nw { white-space: nowrap; }
.foot { margin-top: 4mm; border-top: 1px solid #cbd5e1; padding-top: 2.5mm; font-size: 8.6pt; color: #475569; line-height: 1.45; }
"""


def short(u):
    return u.replace("https://", "")


def qr_svg(data):
    buf = io.BytesIO()
    segno.make(data, error="m").save(buf, kind="svg", xmldecl=False, svgns=True, omitsize=True, scale=1, border=4, dark="#0b1220", light="#ffffff")
    return buf.getvalue().decode("utf-8")


def qr_target(g):
    return "%s?campaign=%s" % (M.url(g["slug"]), M.ONEPAGER_CAMPAIGN)


def next_line(g):
    if g["slug"] == "iks-life-skills":
        return "<b>Goes with:</b> the printable scenario cards and facilitator notes, at <span class=\"nw\">%s</span>" % e(short(M.url(g["slug"]) + "cards/"))
    n = M.next_on_path(g)
    if n:
        return "<b>Next on this path:</b> %s, at <span class=\"nw\">%s</span>" % (e(n["name"]), e(short(M.url(n["slug"]))))
    return "<b>Last guide on this path.</b> All eleven guides, in three paths: %s" % e(short(M.SITE))


def page_html(g):
    steps = max(x["step"] for x in M.GUIDES if x["path"] == g["path"])
    items = "\n".join("<li>%s</li>" % e(t) for t in g["learn"])
    return """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>%(name)s: one-page summary</title><style>%(css)s</style></head>
<body><div class="page">
  <div class="top"><span class="brand">%(site)s</span><span class="pathlabel">Path %(path)d: %(pathname)s &middot; guide %(step)d of %(steps)d</span></div>
  <h1>%(name)s</h1>
  <p class="what">%(what)s</p>
  <p class="who"><b>For:</b> %(who)s</p>
  <h2>What you will learn</h2>
  <ol>%(items)s</ol>
  <div class="scan">
    <div class="qr">%(qr)s</div>
    <div><p class="t1">Scan to open the guide</p>
      <p class="t2">Free, with no sign-up. Opens in any browser, on a phone too.</p>
      <p class="url">%(url)s</p></div>
  </div>
  <p class="next">%(next)s</p>
  <p class="foot">By %(author)s, as part of %(site)s, a personal initiative. Version %(version)s, last reviewed %(rev)s.
  Free to copy, share and adapt for non-commercial teaching and learning, with credit, under CC BY-NC-SA 4.0
  (creativecommons.org/licenses/by-nc-sa/4.0). Found an error? Tell me through the site.</p>
</div></body></html>""" % {
        "name": e(g["name"]), "css": CSS, "site": e(M.SITE_NAME), "path": g["path"], "pathname": e(M.PATHS[g["path"]]),
        "step": g["step"], "steps": steps, "what": e(g["what"]), "who": e(g["who"]), "items": items,
        "qr": qr_svg(qr_target(g)), "url": e(short(M.url(g["slug"]))), "next": next_line(g),
        "author": e(M.AUTHOR), "version": e(g["version"]), "rev": e(M.REVIEWED_TEXT),
    }


def index_html():
    rows = []
    for p, pname in M.PATHS.items():
        cards = []
        for g in sorted((x for x in M.GUIDES if x["path"] == p), key=lambda x: x["step"]):
            s = g["slug"]
            cards.append("""      <li class="op">
        <a class="op-thumb" href="%(s)s.png"><img src="thumbs/%(s)s.jpg" alt="One-page summary of %(n)s" width="300" height="424" loading="lazy"></a>
        <div><h3><a href="../%(s)s/">%(n)s</a></h3>
          <p>%(w)s</p>
          <p class="op-links"><a href="%(s)s.pdf">PDF, A4, to print</a> <a href="%(s)s.png">Image, to share</a></p></div>
      </li>""" % {"s": s, "n": e(g["name"]), "w": e(g["what"])})
        rows.append('    <h2>Path %d: %s</h2>\n    <ul class="ops">\n%s\n    </ul>' % (p, e(pname), "\n".join(cards)))
    return """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Printable one-page summaries | Architect U'r Career</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="One A4 page for each of the eleven guides, with a QR code, to print for a notice board or share in a class group. Free to copy and share.">
<link rel="canonical" href="%(site)sprint/">
<meta property="og:type" content="website">
<meta property="og:title" content="Printable one-page summaries | Architect U'r Career">
<meta property="og:description" content="One A4 page for each of the eleven guides, with a QR code, to print for a notice board or share in a class group.">
<meta property="og:url" content="%(site)sprint/">
<meta property="og:image" content="%(site)sauc-logo.png">
<meta name="twitter:card" content="summary">
<link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
<link rel="stylesheet" href="../assets/auc-guide.css">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #f6f8fb; color: #1f2937; font: 17px/1.65 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
  main { max-width: 62rem; margin: 0 auto; padding: 2.5rem 1rem 4rem; }
  h1 { font-size: 2rem; line-height: 1.2; color: #0b1220; margin: 0 0 .75rem; }
  h2 { font-size: 1.25rem; color: #0b1220; margin: 2.5rem 0 .9rem; }
  h3 { font-size: 1.05rem; margin: 0 0 .3rem; line-height: 1.3; }
  a { color: #047857; }
  .lede { max-width: 46rem; }
  .all { display: inline-block; margin: .4rem 0 0; padding: .6rem 1rem; background: #047857; color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600; }
  .all:hover { background: #065f46; }
  .ops { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%%, 27rem), 1fr)); gap: .9rem; }
  .op { display: grid; grid-template-columns: 7.5rem 1fr; gap: 1rem; background: #fff; border: 1px solid #dbe3ec; border-radius: 8px; padding: .9rem; margin: 0; }
  .op-thumb img { width: 7.5rem; height: auto; display: block; border: 1px solid #dbe3ec; border-radius: 4px; }
  .op p { margin: 0 0 .5rem; font-size: .93rem; line-height: 1.5; }
  .op-links { display: flex; flex-wrap: wrap; gap: .3rem 1rem; font-size: .9rem; font-weight: 600; }
  @media (max-width: 420px) { .op { grid-template-columns: 5.5rem 1fr; } .op-thumb img { width: 5.5rem; } }
</style>
</head>
<body>
<!-- auc:bar -->
<a class="auc-skip" href="#auc-main">Skip to content</a>
<nav class="auc-bar" aria-label="Architect U'r Career">
  <a class="auc-bar-home" href="../">Architect U'r Career</a>
  <span class="auc-bar-sep" aria-hidden="true">/</span>
  <span class="auc-bar-here">One-page summaries</span>
  <span class="auc-bar-right">
    <span class="auc-bar-rev">Last reviewed: %(rev)s</span>
    <a href="../#guides">All guides</a>
    <a href="../about/">How this site is maintained</a>
  </span>
</nav>
<!-- /auc:bar -->
<main id="auc-main">
  <h1>One-page summaries, to print or share</h1>
  <p class="lede">One A4 page for each guide: what it is, who it is for, five things it teaches, and a QR code that opens it. Print one for a notice board, or send the image to a class group. You may copy and share them freely for teaching and learning.</p>
  <p><a class="all" href="architect-ur-career-one-pagers.pdf">All eleven in one PDF</a></p>
%(rows)s
</main>
<!-- auc:foot -->
<footer class="auc-foot">
  <p><strong>One-page summaries</strong>, last reviewed %(rev)s. Written by <a href="../">Krishna Mohan Parsha</a> as part of Architect U'r Career, a personal initiative. The views are my own and not those of my employer.</p>
  <p>Free to use, share and adapt for non-commercial teaching and learning, with credit, under <a rel="license noopener" target="_blank" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. <a target="_blank" rel="noopener" href="https://github.com/mohanparsha/architecturcareer/issues/new?title=Correction%%3A%%20print">Found an error? Tell me.</a> <a href="../about/#changelog">What changed</a>. <a href="../about/">How this site is maintained</a>.</p>
</footer>
<!-- /auc:foot -->
<script src="../assets/auc-guide.js" defer></script>
<script data-goatcounter="https://km-auc.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
""" % {"site": M.SITE, "rev": e(M.REVIEWED_TEXT), "rows": "\n".join(rows)}


def main():
    os.makedirs(os.path.join(OUT, "thumbs"), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="auc-onepagers-")
    fails = []
    try:
        import cv2
        detector = cv2.QRCodeDetector()
        with sync_playwright() as p:
            b = p.chromium.launch(channel="msedge", headless=True)
            ctx = b.new_context(viewport={"width": A4_W, "height": A4_H}, device_scale_factor=2)
            pg = ctx.new_page()
            for g in M.GUIDES:
                s = g["slug"]
                doc = page_html(g)
                if EM in doc or (" " + EN + " ") in doc:
                    sys.exit(s + ": long dash in the one-pager text")
                src = os.path.join(tmp, s + ".html")
                io.open(src, "w", encoding="utf-8").write(doc)
                pg.goto("file:///" + src.replace("\\", "/"))
                pg.wait_for_timeout(150)
                fit = pg.evaluate("""() => { const p = document.querySelector('.page');
                    const kids = Array.from(p.querySelectorAll('*')); const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
                    const scan = document.querySelector('.scan').getBoundingClientRect(), ol = document.querySelector('ol').getBoundingClientRect();
                    return {pageH: p.getBoundingClientRect().height, bottom: Math.round(bottom), overflow: p.scrollHeight > p.clientHeight + 1, gap: Math.round(scan.top - ol.bottom)}; }""")
                if fit["overflow"] or fit["bottom"] > fit["pageH"] or fit["gap"] < 8:
                    fails.append("%s does not fit A4: %s" % (s, fit))
                pg.pdf(path=os.path.join(OUT, s + ".pdf"), format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
                png = os.path.join(OUT, s + ".png")
                pg.screenshot(path=png, full_page=False)
                im = Image.open(png).convert("RGB")
                im.quantize(colors=64, method=Image.Quantize.MEDIANCUT).save(png, optimize=True)
                th = im.copy()
                th.thumbnail((300, 424))
                th.save(os.path.join(OUT, "thumbs", s + ".jpg"), quality=82, optimize=True)
                # prove the QR code: decode it from the shared image
                data, _, _ = detector.detectAndDecode(cv2.imread(png))
                ok = data == qr_target(g)
                if not ok:
                    fails.append("%s QR decodes to %r, expected %r" % (s, data, qr_target(g)))
                pages = len(PdfReader(os.path.join(OUT, s + ".pdf")).pages)
                if pages != 1:
                    fails.append("%s PDF has %d pages" % (s, pages))
                print("%-26s fits=%s gap=%spx  QR=%s  pdf_pages=%d  png=%dKB" % (s, not fit["overflow"], fit["gap"], "ok" if ok else "FAIL",
                                                                                  pages, os.path.getsize(png) // 1024))
            b.close()
        w = PdfWriter()
        for g in M.GUIDES:
            w.append(os.path.join(OUT, g["slug"] + ".pdf"))
        with open(os.path.join(OUT, "architect-ur-career-one-pagers.pdf"), "wb") as f:
            w.write(f)
        io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n").write(index_html())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print("print/ total size: %d KB" % (total // 1024))
    if fails:
        print("FAIL\n  " + "\n  ".join(fails))
        sys.exit(1)
    print("RESULT: PASS, %d one-pagers, every QR code decoded to its guide" % len(M.GUIDES))


if __name__ == "__main__":
    main()
