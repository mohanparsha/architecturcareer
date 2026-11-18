# -*- coding: utf-8 -*-
"""Build iks-life-skills/cards/index.html from cards_data.py.

Usage, from anywhere:  python _tools/iks-cards/build.py [pages]
(pages = the A4 page count printed in the header; default 34, checked by verify.py)
The repository root is found from this file's own location.
Validates every card (60 to 110 words, ends in a question) and every run plan (minutes add up).
"""
import html, io, os, re, sys
import cards_data as D

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))  # this file lives in <repo>/_tools/iks-cards/
OUT = os.path.join(REPO, "iks-life-skills", "cards", "index.html")
PAGES = sys.argv[1] if len(sys.argv) > 1 else "34"  # A4 pages in Edge; verify.py fails if the PDF disagrees
VERSION = "1.0"
DATE = "November 2026"
TITLE = "IKS Life Skills: scenario cards and facilitator notes"
URL = "https://mohanparsha.github.io/architecturcareer/iks-life-skills/cards/"
CREDIT = "IKS Life Skills cards, v%s · Architect U'r Career · CC BY-NC-SA 4.0" % VERSION
MID = " · "


def sq(text):
    """Straight single quotes to typographic ones. Opening after a space or bracket, closing otherwise."""
    out = []
    for i, ch in enumerate(text):
        if ch == "'":
            prev = text[i - 1] if i else " "
            out.append("\u2018" if prev in " \n\t([>" else "\u2019")
        else:
            out.append(ch)
    return "".join(out)


def esc(text):
    return sq(html.escape(text, quote=False))


def words(text):
    return len(text.split())


# ---------------------------------------------------------------- validate
problems = []
total = 0
per_week = {}
for w in D.WEEKS:
    n = 0
    for s in w["sets"]:
        for c in s["cards"]:
            n += 1
            wc = words(c["body"]) + words(c["q"])
            c["wc"] = wc
            if not (60 <= wc <= 110):
                problems.append("week %d card %d (%s): %d words" % (w["n"], n, c["title"], wc))
            if not c["q"].rstrip().endswith("?"):
                problems.append("week %d card %d (%s): does not end in a question" % (w["n"], n, c["title"]))
            if '"' in c["body"] + c["q"] + c["title"]:
                problems.append("week %d card %d: double quote in text" % (w["n"], n))
    per_week[w["n"]] = n
    total += n
    note = w["note"]
    mins = sum(m for m, _ in note["run"])
    if mins != note["slot"]:
        problems.append("week %d run plan adds to %d, slot is %d" % (w["n"], mins, note["slot"]))
if problems:
    print("PROBLEMS:\n  " + "\n  ".join(problems))
print("cards per week:", per_week, "total:", total)

# ---------------------------------------------------------------- pieces
CSS = r"""
:root{--ink:#14181f;--muted:#4a5565;--line:#d5d9d0;--paper:#ffffff;--bg:#f3f4ef;--accent:#065f46;--soft:#eaf3ee}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
main{display:block;max-width:1040px;margin:0 auto;padding:28px 16px 64px}
h1,h2,h3,h4,p,ul,ol{margin:0}
a{color:var(--accent)}
.print-only{display:none}
.pk-kicker{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.pk-head h1{font-size:clamp(28px,5vw,40px);line-height:1.15;margin:6px 0 10px;letter-spacing:-.01em}
.pk-ver{font-weight:600;color:var(--ink)}
.pk-lede{margin-top:10px;max-width:760px;color:var(--muted);font-size:17px}
.pk-head .auc-note{margin:16px 0 0;max-width:none}
.pk-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.pk-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 18px;border-radius:8px;border:2px solid var(--accent);font:600 15px/1.2 inherit;font-family:inherit;cursor:pointer;text-decoration:none}
.pk-btn-main{background:var(--accent);color:#fff}
.pk-btn-main:hover{background:#044a37}
.pk-btn-ghost{background:#fff;color:var(--accent)}
.pk-btn-ghost:hover{background:var(--soft)}
.pk-toc{margin:22px 0 0;padding:14px 16px;background:var(--paper);border:1px solid var(--line);border-radius:10px}
.pk-toc h2{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:8px}
.pk-toc ol{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:2px 18px}
.pk-toc a{display:block;padding:5px 0;text-decoration:none;color:var(--ink)}
.pk-toc a:hover{text-decoration:underline}
.pk-toc a b{color:var(--accent)}
.pk-toc small{color:var(--muted);font-size:13px}
.pk-panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:22px 22px 24px;margin-top:26px}
.pk-panel h2{font-size:26px;line-height:1.2;margin:2px 0 12px}
.pk-panel h3{font-size:16px;margin:16px 0 6px}
.pk-panel ul,.pk-panel ol{padding-left:20px}
.pk-panel li{margin:3px 0}
.pk-open-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 32px}
.pk-open-grid h3{margin-top:4px}
.pk-source{font-size:14px;color:var(--muted);overflow-wrap:anywhere}
.pk-week{margin-top:44px}
.pk-week-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:10px}
.pk-week-head h2{margin:2px 0 0}
.pk-aim{margin-top:12px;font-size:17px}
.pk-run{list-style:none;padding:0 !important}
.pk-run li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:10px;margin:4px 0}
.pk-min{font-weight:700;color:var(--accent);white-space:nowrap}
.pk-slot{font-weight:400;color:var(--muted)}
.pk-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 28px}
.pk-link,.pk-copies,.pk-extra{margin-top:12px}
.pk-safe{margin-top:12px;padding:10px 14px;border:1px solid var(--ink);border-left-width:5px;border-radius:6px}
.pk-set-title{font-size:18px;margin:26px 0 0;line-height:1.3}
.pk-set-title small{display:block;font-size:14px;font-weight:400;color:var(--muted)}
.sheet{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:18px 20px 20px;display:flex;flex-direction:column}
.card.card-blank{display:none}
.card-id{display:flex;justify-content:space-between;gap:10px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}
.card h4{font-size:21px;line-height:1.2;margin:8px 0 2px}
.card-tag{font-size:14px;font-style:italic;color:var(--muted)}
.card-body{margin-top:10px}
.card-q{margin-top:10px;font-weight:700}
.pk-map table{border-collapse:collapse;width:100%;font-size:15px}
.pk-map th,.pk-map td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
.pk-map th{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.pk-map td:first-child{white-space:nowrap;font-weight:700}
.pk-map p{margin-top:12px}
@media screen and (max-width:760px){
  .pk-open-grid,.pk-two,.sheet{grid-template-columns:minmax(0,1fr)}
  .pk-panel{padding:18px 16px 20px}
  .pk-panel h2{font-size:22px}
  .pk-map table,.pk-map tbody,.pk-map tr,.pk-map td{display:block;width:100%}
  .pk-map thead{position:absolute;left:-9999px}
  .pk-map tr{padding:10px 0;border-bottom:1px solid var(--line)}
  .pk-map td{border:0;padding:2px 0;white-space:normal !important}
  .pk-map td[data-h]:before{content:attr(data-h) ": ";font-weight:700}
}

@page{size:A4 portrait;margin:10mm}
@media print{
  html,body{background:#fff !important;color:#000}
  body{font:11pt/1.38 Arial,Helvetica,"Liberation Sans",Arimo,Roboto,sans-serif}
  main{max-width:none;margin:0;padding:0}
  a,a:visited{color:#000;text-decoration:none}
  .screen-only{display:none !important}
  .print-only{display:block}
  .pk-kicker,.pk-min,.card-id,.pk-toc a b{color:#000}
  .pk-panel{border:0;border-radius:0;padding:0;margin:0;background:none}
  .pk-head h1{font-size:21pt;margin:1mm 0 1.5mm}
  .pk-ver{font-size:11pt}
  .pk-lede{font-size:11pt;color:#000;max-width:none;margin-top:1.5mm}
  .pk-head .auc-note{background:#fff;border:1pt solid #000;border-left-width:3pt;color:#000;margin-top:3mm;padding:2mm 3mm;font:11pt/1.35 Arial,Helvetica,"Liberation Sans",Arimo,Roboto,sans-serif}
  .pk-head .auc-note strong{color:#000}
  .pk-open{margin-top:4mm;break-after:page;page-break-after:always}
  .pk-open h2{font-size:15pt;margin:0 0 1mm}
  .pk-open-grid{gap:2mm 7mm;font-size:10.5pt}
  .pk-open-grid h3{margin-top:1mm}
  .pk-panel h3{font-size:11.5pt;margin:3mm 0 1mm}
  .pk-panel ul,.pk-panel ol{padding-left:4.5mm}
  .pk-panel li{margin:.6mm 0}
  .pk-source{font-size:10pt;color:#000}
  .pk-week{margin:0}
  .pk-note{break-after:page;page-break-after:always}
  .pk-note h2{font-size:17pt;margin:.5mm 0 0}
  .pk-aim{font-size:11pt;margin-top:2.5mm}
  .pk-run li{grid-template-columns:15mm minmax(0,1fr);gap:2mm;margin:.5mm 0}
  .pk-slot{color:#000}
  .pk-two{gap:0 7mm}
  .pk-link,.pk-copies,.pk-extra{margin-top:2.5mm}
  .pk-safe{margin-top:3mm;padding:2mm 3mm;border:1pt solid #000;border-left-width:3pt;border-radius:0}
  .pk-credit{margin-top:3mm;padding-top:1.5mm;border-top:.75pt solid #000;font-size:9pt}
  .sheet{grid-template-columns:1fr 1fr;grid-template-rows:7mm minmax(0,1fr) minmax(0,1fr);gap:0;height:272mm;margin:0;break-after:page;page-break-after:always;break-inside:avoid;page-break-inside:avoid}
  .sheet-cap{grid-column:1 / -1;display:flex;justify-content:space-between;align-items:flex-start;font-size:9.5pt}
  .card{border:0;border-top:1pt dashed #000;border-left:1pt dashed #000;border-radius:0;background:none;padding:6mm 6.5mm 3.5mm;min-height:0;overflow:hidden;break-inside:avoid;page-break-inside:avoid}
  .card.pos-2,.card.pos-4{border-right:1pt dashed #000}
  .card.pos-3,.card.pos-4{border-bottom:1pt dashed #000}
  .card.card-blank{display:flex}
  .card-in{flex:1 1 auto;min-height:0}
  .card-id{font-size:11pt;letter-spacing:.03em}
  .card h4{font-size:15pt;line-height:1.15;margin:2.5mm 0 .5mm}
  .card-tag{font-size:11pt;color:#000}
  .card-body{font-size:12pt;line-height:1.33;margin-top:2.5mm}
  .card-q{font-size:12pt;line-height:1.33;margin-top:2mm}
  .card-credit{display:block;font-size:7.5pt;margin-top:1.5mm;white-space:nowrap}
  .blank-line{border-bottom:.75pt solid #000;height:7.6mm}
  .blank-label{font-size:11pt;font-weight:700;margin-top:3mm}
  .blank-rule{font-size:11pt;font-style:italic;margin-top:3mm}
  .pk-map{break-before:auto}
  .pk-map h2{font-size:15pt;margin:0 0 2mm}
  .pk-map table{font-size:10pt}
  .pk-map th,.pk-map td{padding:1.4mm 2mm;border-bottom:.75pt solid #000}
  .pk-map th{color:#000;font-size:9pt}
  .pk-map p{margin-top:2.5mm;font-size:10pt}
  .auc-foot{margin-top:5mm;padding:3mm 0 0;text-align:left;font-size:9pt}
  .auc-foot p{max-width:none}
  body[data-print-only] .pk-head,
  body[data-print-only] .pk-open,
  body[data-print-only] .pk-map,
  body[data-print-only] .auc-foot,
  body[data-print-only] .pk-week:not(.is-print-target){display:none !important}
}
"""

JS = r"""
(function () {
  'use strict';
  var body = document.body;
  function clear() {
    body.removeAttribute('data-print-only');
    var t = document.querySelector('.is-print-target');
    if (t) { t.classList.remove('is-print-target'); }
  }
  document.addEventListener('click', function (e) {
    var b = e.target && e.target.closest ? e.target.closest('button[data-print]') : null;
    if (!b) { return; }
    clear();
    var v = b.getAttribute('data-print');
    if (v !== 'all') {
      var s = document.getElementById(v);
      if (s) { s.classList.add('is-print-target'); body.setAttribute('data-print-only', v); }
    }
    window.print();
  });
  window.addEventListener('afterprint', clear);
})();
"""


def card_html(wn, num, tier, c, pos):
    short_tier = tier.split(" (")[0]
    return (
        '<article class="card pos-%d" id="w%d-c%d">\n'
        '<div class="card-in">\n'
        '<p class="card-id"><span>Week %d%sCard %d</span><span>%s</span></p>\n'
        '<h4>%s</h4>\n'
        '<p class="card-tag">%s</p>\n'
        '<p class="card-body">%s</p>\n'
        '<p class="card-q">%s</p>\n'
        '</div>\n'
        '<p class="card-credit print-only">%s</p>\n'
        '</article>\n'
    ) % (pos, wn, num, wn, MID, num, short_tier, esc(c["title"]), esc(c["tag"]), esc(c["body"]), esc(c["q"]), CREDIT)


def blank_html(wn, tier, pos):
    short_tier = tier.split(" (")[0]
    lines = '<div class="blank-line"></div>\n'
    return (
        '<article class="card card-blank pos-%d print-only" aria-hidden="true">\n'
        '<div class="card-in">\n'
        '<p class="card-id"><span>Week %d%syour own card</span><span>%s</span></p>\n'
        '<p class="blank-label">Title</p>\n%s'
        '<p class="blank-label">What happens</p>\n%s'
        '<p class="blank-label">Question</p>\n%s'
        '<p class="blank-rule">Keep it made up and about someone else. End on a question with more than one good answer.</p>\n'
        '</div>\n'
        '<p class="card-credit print-only">%s</p>\n'
        '</article>\n'
    ) % (pos, wn, MID, short_tier, lines, lines * 6, lines * 2, CREDIT)


def rng(a, b):
    return "card %d" % a if a == b else "cards %d to %d" % (a, b)


def week_html(w):
    wn, note = w["n"], w["note"]
    o = []
    o.append('<section class="pk-week" id="week-%d">\n' % wn)
    o.append('<div class="pk-note pk-panel">\n')
    o.append('<div class="pk-week-head">\n<div>\n<p class="pk-kicker">Week %d%sfacilitator note</p>\n<h2>Week %d: %s</h2>\n</div>\n'
             '<button type="button" class="pk-btn pk-btn-ghost screen-only" data-print="week-%d">Print week %d only</button>\n</div>\n'
             % (wn, MID, wn, esc(w["theme"]), wn, wn))
    o.append('<p class="pk-aim"><b>Aim.</b> %s</p>\n' % esc(note["aim"]))
    o.append('<h3>What the curriculum asks for, and what is here</h3>\n<ul>\n')
    for a in note["asks"]:
        o.append('<li>%s</li>\n' % sq(a))
    o.append('</ul>\n')
    o.append('<h3>Running the cards in one period <span class="pk-slot">(%s)</span></h3>\n<ol class="pk-run">\n' % esc(note["slot_label"]))
    for m, t in note["run"]:
        o.append('<li><span class="pk-min">%d min</span><span>%s</span></li>\n' % (m, esc(t)))
    o.append('</ol>\n')
    o.append('<p class="pk-copies"><b>Copies.</b> %s</p>\n' % esc(note["copies"]))
    o.append('<div class="pk-two">\n<div>\n<h3>Follow-up questions</h3>\n<ul>\n')
    for f in note["followups"]:
        o.append('<li>%s</li>\n' % esc(f))
    o.append('</ul>\n</div>\n<div>\n<h3>What a thoughtful response tends to do</h3>\n<ul>\n')
    for f in note["thoughtful"]:
        o.append('<li>%s</li>\n' % esc(f))
    o.append('</ul>\n</div>\n</div>\n')
    for title, text in note["extra"]:
        o.append('<p class="pk-extra"><b>%s.</b> %s</p>\n' % (esc(title), esc(text)))
    o.append('<p class="pk-link"><b>Link to the story.</b> %s</p>\n' % esc(note["link"]))
    o.append('<p class="pk-safe"><b>Safeguarding.</b> %s</p>\n' % esc(note["safeguarding"]))
    o.append('<p class="pk-credit print-only">%s, version %s, %s%sKrishna Mohan Parsha, Architect U\'r Career%sCC BY-NC-SA 4.0%s%s</p>\n'
             % (TITLE, VERSION, DATE, MID, MID, MID, URL.replace("https://", "")))
    o.append('</div>\n')
    num = 0
    for s in w["sets"]:
        first = num + 1
        last = num + len(s["cards"])
        o.append('<div class="pk-set">\n')
        o.append('<h3 class="pk-set-title screen-only">%s: %s<small>Week %d, %s</small></h3>\n' % (esc(s["tier"]), esc(s["name"]), wn, rng(first, last)))
        cards = s["cards"]
        for i in range(0, len(cards), 4):
            chunk = cards[i:i + 4]
            a, b = first + i, first + i + len(chunk) - 1
            o.append('<div class="sheet">\n')
            o.append('<p class="sheet-cap print-only"><span>IKS Life Skills cards%sWeek %d%s%s%s%s</span><span>Cut along the dashed lines</span></p>\n'
                     % (MID, wn, MID, esc(s["tier"]), MID, rng(a, b)))
            for j, c in enumerate(chunk):
                num += 1
                o.append(card_html(wn, num, s["tier"], c, j + 1))
            for j in range(len(chunk), 4):
                o.append(blank_html(wn, s["tier"], j + 1))
            o.append('</div>\n')
        o.append('</div>\n')
    o.append('</section>\n')
    return "".join(o)


def toc_html():
    o = ['<nav class="pk-toc screen-only" aria-label="Contents of this pack">\n<h2>In this pack</h2>\n<ol>\n']
    o.append('<li><a href="#how-to-use"><b>Before you start</b><br><small>Print, group, ground rules, safeguarding</small></a></li>\n')
    for w in D.WEEKS:
        o.append('<li><a href="#week-%d"><b>Week %d</b> %s<br><small>%d cards</small></a></li>\n' % (w["n"], w["n"], esc(w["theme"]), per_week[w["n"]]))
    o.append('<li><a href="#what-is-covered"><b>What is covered</b><br><small>Week by week, tier by tier</small></a></li>\n')
    o.append('</ol>\n</nav>\n')
    return "".join(o)


def map_html():
    o = ['<section class="pk-map pk-panel" id="what-is-covered">\n<h2>What is covered</h2>\n<table>\n<thead><tr><th>Week</th><th>Theme</th><th>Cards in this pack</th></tr></thead>\n<tbody>\n']
    for w in D.WEEKS:
        num = 0
        parts = []
        for s in w["sets"]:
            a, b = num + 1, num + len(s["cards"])
            num = b
            parts.append("%s, %s: %s" % (s["tier"].split(" (")[0], rng(a, b), s["name"]))
        o.append('<tr><td>Week %d</td><td data-h="Theme">%s</td><td data-h="Cards">%s</td></tr>\n' % (w["n"], esc(w["theme"]), "<br>".join(esc(p) for p in parts)))
    o.append('</tbody>\n</table>\n')
    o.append('<p><b>%d cards in all.</b> Each week&rsquo;s facilitator note says what the curriculum asks the teacher to prepare and how the cards answer it. '
             'In Weeks 8 and 12 the curriculum asks for no scenario cards, and the cards are an addition.</p>\n' % total)
    o.append('<p><b>Not covered in version %s.</b> Tier 3 (Class 11 and above) is a teach-back tier in which students design their own materials, so no Tier 3 cards are supplied. '
             'The Tier 2 simulations in Weeks 2, 3, 4, 5, 7 and 8 work from briefs, case files or a single task rather than cards, and are not supplied either.</p>\n' % VERSION)
    o.append('</section>\n')
    return "".join(o)


pages_txt = (MID + "%s A4 pages" % PAGES) if PAGES else ""
DESC = "Printable scenario cards and facilitator notes for the 12-week IKS Life Skills curriculum, Classes 9 to 12: %d cards on A4, four to a page." % total
assert len(DESC) < 160, len(DESC)

HEAD = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>%(title)s | Architect U'r Career</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="article">
<meta property="og:title" content="%(title)s | Architect U'r Career">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="https://mohanparsha.github.io/architecturcareer/auc-logo.png">
<meta name="twitter:card" content="summary">
<link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
<link rel="stylesheet" href="../../assets/auc-guide.css">
<style>%(css)s</style>
</head>
<body>
<!-- auc:bar -->
<a class="auc-skip" href="#auc-main">Skip to content</a>
<nav class="auc-bar" aria-label="Architect U'r Career">
  <a class="auc-bar-home" href="../../">Architect U'r Career</a>
  <span class="auc-bar-sep" aria-hidden="true">/</span>
  <a href="../">IKS Life Skills Curriculum</a>
  <span class="auc-bar-sep" aria-hidden="true">/</span>
  <span class="auc-bar-here">Scenario cards</span>
  <span class="auc-bar-right">
    <span class="auc-bar-rev">Last reviewed: November 2026</span>
    <a href="../../#guides">All guides</a>
    <a href="../../about/">How this site is maintained</a>
  </span>
</nav>
<!-- /auc:bar -->
<main id="auc-main">
<header class="pk-head">
<p class="pk-kicker">IKS Life Skills Curriculum%(mid)sprintable facilitator pack</p>
<h1>%(title)s</h1>
<p class="pk-ver">Version %(version)s, %(date)s%(mid)s%(total)d cards%(mid)s12 facilitator notes%(pages)s</p>
<p class="pk-lede">The <a href="../">12-week IKS Life Skills curriculum</a> for Classes 9 to 12 asks the teacher to prepare scenario cards before most sessions. This pack supplies them, with a one-page note on running each week&rsquo;s cards.</p>
<div class="auc-note"><strong>These cards are original material written for this curriculum.</strong> They are an independent work and are not published, endorsed or approved by UGC, NCERT, CBSE or any government body.</div>
<div class="pk-actions screen-only">
<button type="button" class="pk-btn pk-btn-main" data-print="all">Print this pack</button>
<a class="pk-btn pk-btn-ghost" href="../">Open the curriculum</a>
</div>
</header>
"""

OPEN = """<section class="pk-open pk-panel" id="how-to-use">
<h2>Before you start</h2>
<div class="pk-open-grid">
<div>
<h3>Print and cut</h3>
<ul>
<li>Use <b>Print this pack</b> for everything, or the button beside a week for that week alone. Choose A4, portrait, 100 per cent scale and default margins, and print on one side only.</li>
<li>Black and white is enough: nothing depends on colour and nothing is shaded.</li>
<li>Cards come four to a page. Cut once across and once down, along the dashed lines.</li>
<li>Every card carries its week, card number, tier and title, so a mixed pile can be sorted again.</li>
<li>Spare spaces on a page are blank cards for a scenario of your own. Each week&rsquo;s note says how many copies to make.</li>
</ul>
</div>
<div>
<h3>Group the students</h3>
<ul>
<li>Use the group size the curriculum gives for the week. The note repeats it.</li>
<li>Form groups by counting off or by seating row, not by friendship or marks, and change them every week or two.</li>
<li>Give each group a reader, a timekeeper, a note-taker and a reporter, and rotate the jobs so that the same voices do not always lead.</li>
<li>In a large class, run two circuits with a second set of cards instead of making the groups bigger.</li>
</ul>
</div>
<div>
<h3>Ground rules for discussion</h3>
<p>Read these aloud in the first week and keep them on the wall.</p>
<ol>
<li>We talk about the people on the card, not about people in this room.</li>
<li>Nobody has to share anything about their own life, family or home. Anyone may say &lsquo;pass&rsquo;.</li>
<li>One person speaks at a time. We disagree with ideas, not with people.</li>
<li>No names and no stories about classmates or teachers, here or afterwards.</li>
<li>The cards have no single right answer. Reasons matter more than verdicts.</li>
<li>If a card is upsetting, anyone may ask quietly for a different one or step out, without giving a reason.</li>
</ol>
</div>
<div>
<h3>Safeguarding, for the teacher</h3>
<ul>
<li>Every card is fiction: the people and events are made up, and real towns only give a setting.</li>
<li>Never stage an incident or mislead students. Every role-play is announced, uses volunteers and lets anyone opt out without losing marks; private brief cards are a game rule the whole class is told about.</li>
<li>Never ask students about their own family, income, caste, religion, health or relationships, never let a card be turned on a real student, and never record students on audio or video.</li>
<li>If a student discloses something worrying: listen calmly, do not ask for details in front of others, do not promise secrecy, follow the school&rsquo;s child protection policy and tell its designated person the same day. Find out who that is before Week 1.</li>
<li><b>Child Helpline: 1098.</b> It runs under the Government of India&rsquo;s Mission Vatsalya scheme (Ministry of Women and Child Development) and is linked to the emergency number 112.</li>
</ul>
<p class="pk-source">Source for the helpline: Ministry of Women and Child Development, &lsquo;Child Helpline 1098&rsquo;, <a href="https://wcd.gov.in/child/child-helpline" target="_blank" rel="noopener">wcd.gov.in/child/child-helpline</a>, checked on 18 November 2026.</p>
</div>
</div>
</section>
"""

FOOT = """</main>
<!-- auc:foot -->
<footer class="auc-foot">
  <p><strong>%(title)s</strong>, version %(version)s, last reviewed November 2026. Written by <a href="../../">Krishna Mohan Parsha</a> as part of Architect U'r Career, a personal initiative. The views are my own and not those of my employer.</p>
  <p>Free to use, share and adapt for non-commercial teaching and learning, with credit, under <a rel="license noopener" href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">CC BY-NC-SA 4.0</a>. <a href="https://github.com/mohanparsha/architecturcareer/issues/new?title=Correction%%3A%%20iks-life-skills%%2Fcards" target="_blank" rel="noopener">Found an error? Tell me.</a> <a href="../../about/#changelog">What changed</a>. <a href="../../about/">How this site is maintained</a>.</p>
</footer>
<!-- /auc:foot -->
<script>%(js)s</script>
<script src="../../assets/auc-guide.js" defer></script>
<script data-goatcounter="https://km-auc.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
"""

vals = dict(title=TITLE, desc=DESC, url=URL, css=CSS, js=JS, version=VERSION, date=DATE, total=total, pages=pages_txt, mid=MID)
doc = HEAD % vals + toc_html() + OPEN + "".join(week_html(w) for w in D.WEEKS) + map_html() + FOOT % vals

EM = chr(0x2014)
EN = chr(0x2013)
assert EM not in doc, "em dash in output"
assert EN not in doc, "en dash in output"
assert "&mdash;" not in doc and "&ndash;" not in doc
if problems:
    print("NOT WRITTEN: fix the problems above")
    sys.exit(1)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
print("wrote", OUT, len(doc.encode("utf-8")), "bytes")
wcs = sorted((c["wc"], w["n"], c["title"]) for w in D.WEEKS for s in w["sets"] for c in s["cards"])
print("shortest:", wcs[:3])
print("longest:", wcs[-5:])
