"""Prove the old addresses still work: serve the site locally, open each old address in Edge,
and check where the reader lands. Run from the repository root:  python _tools/test_redirects.py
Starts a temporary server on 127.0.0.1 and stops it when done. Exit code 0 means all passed.
"""
import functools, http.server, os, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_stubs import MOVED  # noqa: E402


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    handler = functools.partial(Quiet, directory=ROOT)
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = "http://127.0.0.1:%d/" % port
        fails = 0
        with sync_playwright() as p:
            b = p.chromium.launch(channel="msedge", headless=True)
            pg = b.new_page()
            for old, (target, name) in sorted(MOVED.items()):
                pg.goto(base + old, wait_until="load")
                pg.wait_for_timeout(900)
                want = base + target
                got = pg.url
                frag = target.split("#")[1] if "#" in target else None
                visible = True
                if frag:
                    visible = pg.evaluate("""(id) => { const e = document.getElementById(id); if (!e) return false;
                        const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top < innerHeight && r.bottom > 0; }""", frag)
                has_bar = pg.locator(".auc-bar").count() == 1
                ok = got == want and has_bar and visible
                fails += 0 if ok else 1
                print("%s %-46s -> %s%s" % ("PASS" if ok else "FAIL", old, got.replace(base, "/"),
                                              "" if ok else "   (wanted /%s, strip=%s, anchor on screen=%s)" % (target, has_bar, visible)))
            # an old address with a fragment keeps the fragment
            pg.goto(base + "cybersecurity-roadmap.html#x", wait_until="load"); pg.wait_for_timeout(700)
            ok = pg.url == base + "cybersecurity-roadmap/#x"
            fails += 0 if ok else 1
            print("%s fragment is carried across a redirect -> %s" % ("PASS" if ok else "FAIL", pg.url.replace(base, "/")))
            # the retired page explains itself and does not redirect
            pg.goto(base + "llm-deep-dive_v3.0.html", wait_until="load"); pg.wait_for_timeout(700)
            ok = pg.url.endswith("llm-deep-dive_v3.0.html") and "retired" in pg.inner_text("h1").lower()
            fails += 0 if ok else 1
            print("%s retired page stays put and says so" % ("PASS" if ok else "FAIL"))
            # control: an address that never existed is a 404
            r = pg.goto(base + "never-existed.html")
            ok = r.status == 404
            fails += 0 if ok else 1
            print("%s control: unknown address returns %d" % ("PASS" if ok else "FAIL", r.status))
            # home page links: every guide card opens a page with the strip
            pg.goto(base, wait_until="load")
            hrefs = pg.eval_on_selector_all("a.resource-card", "els => els.map(e => e.getAttribute('href'))")
            for h in hrefs:
                r = pg.goto(base + h, wait_until="load")
                ok = r.status == 200 and pg.locator(".auc-bar").count() == 1 and pg.locator(".auc-foot").count() == 1
                fails += 0 if ok else 1
                print("%s home card %-28s status %d" % ("PASS" if ok else "FAIL", h, r.status))
            ok = len(hrefs) == 12
            fails += 0 if ok else 1
            print("%s home page has 12 cards (11 guides and the card pack): %d" % ("PASS" if ok else "FAIL", len(hrefs)))
            b.close()
        httpd.shutdown()
    print("RESULT:", "PASS" if not fails else "FAIL (%d)" % fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
