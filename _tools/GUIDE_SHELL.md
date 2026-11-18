# Guide shell and house rules (every guide page follows this)

Site: Architect U'r Career, the personal give-back site of Krishna Mohan Parsha (CTO and Co-Founder, Rhinexa).
Published by GitHub Pages from this repository. Each guide lives at `<slug>/index.html` and is served at
`https://mohanparsha.github.io/architecturcareer/<slug>/`. Folders that start with `_` are not published.

## 1. In `<head>`

```html
<title>{Guide name} | Architect U'r Career</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{one plain sentence, under 160 characters, saying what the page contains}">
<link rel="canonical" href="https://mohanparsha.github.io/architecturcareer/{slug}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{Guide name} | Architect U'r Career">
<meta property="og:description" content="{same sentence}">
<meta property="og:url" content="https://mohanparsha.github.io/architecturcareer/{slug}/">
<meta property="og:image" content="https://mohanparsha.github.io/architecturcareer/auc-logo.png">
<meta name="twitter:card" content="summary">
<link rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
<link rel="stylesheet" href="../assets/auc-guide.css">
```

Replace any existing title, description, canonical, og and twitter tags: do not leave two of anything.
`<html>` carries `lang="en-GB"` (or the page's real language).

Do not hand-edit a guide's `<title>`, description, `og:`/`twitter:` title and description, or its
`<!-- auc:ld -->` structured-data block. They are generated from `_tools/site_meta.py` by `python _tools/seo.py`.
Change the record there and run the script.

## 2. First thing inside `<body>`

```html
<!-- auc:bar -->
<a class="auc-skip" href="#auc-main">Skip to content</a>
<nav class="auc-bar" aria-label="Architect U'r Career">
  <a class="auc-bar-home" href="../">Architect U'r Career</a>
  <span class="auc-bar-sep" aria-hidden="true">/</span>
  <span class="auc-bar-here">{Short guide name}</span>
  <span class="auc-bar-right">
    <span class="auc-bar-rev">Last reviewed: November 2026</span>
    <a href="../#guides">All guides</a>
    <a href="../about/">How this site is maintained</a>
  </span>
</nav>
<!-- /auc:bar -->
```

The strip is static (it scrolls away). If the page has its own fixed or sticky header, or a full-height
application layout, adjust the PAGE so the strip is visible at the top on load and nothing overlaps it.
Put `id="auc-main"` on the element that holds the page's main content.

## 3. Last things inside `<body>`

```html
<!-- auc:foot -->
<footer class="auc-foot">
  <p><strong>{Guide name}</strong>, version {N.N}, last reviewed November 2026. Written by <a href="../">Krishna Mohan Parsha</a> as part of Architect U'r Career, a personal initiative. The views are my own and not those of my employer.</p>
  <p>Free to use, share and adapt for non-commercial teaching and learning, with credit, under <a rel="license noopener" target="_blank" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. <a target="_blank" rel="noopener" href="https://github.com/mohanparsha/architecturcareer/issues/new?title=Correction%3A%20{slug}">Found an error? Tell me.</a> <a href="../about/#changelog">What changed</a>. <a href="../about/">How this site is maintained</a>.</p>
</footer>
<!-- /auc:foot -->
<script src="../assets/auc-guide.js" defer></script>
<script data-goatcounter="https://km-auc.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
```

This REPLACES the page's own footer and copyright line ("All rights reserved" goes). Exactly one GoatCounter
snippet per page. The version number and date appear on the page (here and in the page's own header if it
has one) and must agree with each other. The version is never in the file name.

## 4. House rules for every edit

1. **No em dash (U+2014) anywhere, and no spaced en dash.** A hook refuses any Write or Edit whose text
   contains U+2014. Before any other edit, remove every one from the file: rewrite with a comma, a colon,
   brackets or two sentences, whichever reads correctly in that sentence. A title "X (em dash) Y" becomes
   "X: Y". Number ranges may keep an unspaced en dash or use "to". Do this with a script whose rules you
   wrote for this file, then read a sample of 30 changed lines to confirm they read as natural English.
   Never a blind replace with a hyphen. Entities (`&mdash;`, `&#8212;`) count too. Box-drawing characters
   in CSS comments are not dashes and may stay.
2. **British English** in all text you write or touch (organise, behaviour, licence as a noun, programme).
   Product names and quoted titles keep their own spelling.
3. **Claim only what can be shown.** Every statistic carries a source link and a year, or it is removed.
   Every changeable fact (price, exam code, version, product status, free tier) is checked on the web today
   against the primary source. If you cannot verify a correct value, remove the claim or say plainly that
   it varies and link to the official page. Never write a number, date or name from memory.
4. **No superlatives the page cannot carry**: "definitive", "complete", "ultimate", "evidence-based" (with
   no evidence shown) are removed from titles and headings.
5. **Brand**: the site is "Architect U'r Career" (never "Architecting"). The author is Krishna Mohan Parsha,
   CTO and Co-Founder, Rhinexa (https://rhinexa.ai/, never rhinexa.com). No Rhinexa product is described
   or promoted in a guide.
6. **Links**: every outbound link is `target="_blank" rel="noopener"`. Links to other guides are relative:
   `../cybersecurity-roadmap/`, `../devops-devsecops-roadmap/`, `../secure-sdlc/`, `../network-concepts/`,
   `../os-unit-1/`, `../agentic-ai-runtime/`, `../ai-security/`, `../ai-knowledge-map/`,
   `../data-intelligence-layer/`, `../thinking-skills/`, `../iks-life-skills/`.
7. **Keyboard and phone**: `assets/auc-guide.js` makes every element that has an inline `onclick`
   focusable and operable with Enter and Space. Controls bound with `addEventListener` need the same done
   in the page (a real `<button>`, or `tabindex="0"` plus a key handler, or add the attribute
   `data-auc-click` and call `.click()` semantics). No information may be available on mouse hover only.
   Nothing may capture the arrow keys or the space bar away from normal scrolling.
8. **Do not add** any new third-party script, font host, tracker, form, cookie or storage use.
9. **Do not run git** (no add, commit, mv, rm, checkout, stash). The lead commits. Touch only the files
   your brief names.

## 5. Prove it before you report

From the repository root:

```
python _tools/check_page.py <slug>          must print PASS
python _tools/shot.py <slug>/index.html <your scratch folder>
```

Open both screenshots and look at them. No console errors, no horizontal overflow at 375 px, the strip at
the top, the footer at the bottom, no overlapping text. Click through every tab or panel you changed.

## 6. What to hand back

1. Write `_tools/changes/<slug>.md`: a short public changelog for this guide, as markdown bullets a reader
   would understand ("Corrected ...", "Removed ...", "Added ..."), most important first, at most 12 bullets,
   no em dashes, with the new version number on the first line.
2. In your final message: what you fixed (counts by kind), every finding from the review you did NOT fix
   and why, every fact you could not verify, anything you were unsure of, and the output of the two
   commands above. Be exact about what is verified and what is not. Do not claim a fix you did not test.
