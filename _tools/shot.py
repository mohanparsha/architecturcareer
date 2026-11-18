"""Render one page of the site in Edge and report what a reader would hit.

Usage (from the repository root):
    python _tools/shot.py <path-inside-repo> <output-folder>
    e.g. python _tools/shot.py secure-sdlc/index.html C:/some/scratch/folder

Writes <name>-1280.png and <name>-375.png (the top 4000 px of the page at each width) and
prints: console errors, failed requests, horizontal overflow, and how many controls the
keyboard can reach. Uses file:// so no server is needed.
"""
import os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rel, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
url = "file:///" + os.path.join(ROOT, rel).replace("\\", "/").replace(" ", "%20")
name = rel.replace("/index.html", "").replace("/", "_").replace(".html", "") or "home"

with sync_playwright() as p:
    b = p.chromium.launch(channel="msedge", headless=True)
    for w, h, mobile in ((1280, 900, False), (375, 812, True)):
        # is_mobile is left off on purpose: with it, Edge widens the layout viewport to fit wide content and hides real overflow
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=False, has_touch=mobile)
        pg = ctx.new_page()
        errs, failed = [], []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(1500)
        info = pg.evaluate("""() => ({
            scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
            scrollHeight: document.documentElement.scrollHeight,
            bar: document.querySelectorAll('.auc-bar').length, foot: document.querySelectorAll('.auc-foot').length,
            barTop: (document.querySelector('.auc-bar')||{getBoundingClientRect(){return {top:-1}}}).getBoundingClientRect().top,
            focusable: document.querySelectorAll('a[href],button,input,select,textarea,summary,[tabindex]:not([tabindex="-1"])').length,
            clickOnly: Array.from(document.querySelectorAll('[onclick]')).filter(e => !e.matches('a[href],button,input,select,textarea,summary,[tabindex]')).length
        })""")
        out = os.path.join(outdir, "%s-%d.png" % (name, w))
        pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": min(4000, info["scrollHeight"])}, full_page=True)
        print("width %d: %s" % (w, info))
        print("  overflow: %s" % ("NONE" if info["scrollWidth"] <= info["innerWidth"] + 1 else "HORIZONTAL OVERFLOW %d > %d" % (info["scrollWidth"], info["innerWidth"])))
        print("  console errors: %s" % (errs or "none"))
        print("  failed requests: %s" % ([f for f in failed if "goatcounter" not in f and "zgo.at" not in f] or "none"))
        print("  screenshot: %s" % out)
        ctx.close()
    b.close()
