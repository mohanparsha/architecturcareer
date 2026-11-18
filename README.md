# Architect U'r Career

Free guides for careers in security, cloud and AI, by Krishna Mohan Parsha.
Published at https://mohanparsha.github.io/architecturcareer/

A personal initiative. The views are my own and not those of my employer.

## What is here

| Path | Guides |
|---|---|
| Start a security career | `network-concepts/`, `cybersecurity-roadmap/`, `devops-devsecops-roadmap/`, `secure-sdlc/` |
| Secure and govern AI | `ai-knowledge-map/`, `agentic-ai-runtime/`, `ai-security/`, `data-intelligence-layer/` |
| Teach it | `iks-life-skills/` (with `iks-life-skills/cards/`), `thinking-skills/`, `os-unit-1/` |

`about/` says how the site is maintained and records what changed. `assets/` holds the header strip,
footer and keyboard support that every guide shares. The `.html` files in the root are redirects from
the addresses the guides had before November 2026.

## Found an error?

Open an issue: https://github.com/mohanparsha/architecturcareer/issues/new
Say which page, what is wrong, and where you checked it.

## Licence

The teaching material is licensed CC BY-NC-SA 4.0: copy, share and adapt it for non-commercial
teaching and learning, with credit. The logo and photographs are not covered. See `LICENSE`.

## Maintaining it

Folders that start with `_` are not published by GitHub Pages.

- `_tools/GUIDE_SHELL.md`: the header, footer and house rules every guide follows.
- `python _tools/check_page.py --all`: checks every guide against those rules.
- `python _tools/check_site.py`: checks every internal link, anchor and redirect on the site.
- `python _tools/shot.py <slug>/index.html <folder>`: renders a page at desktop and phone width.
- `python _tools/build_about.py`: rebuilds `about/index.html` from `_tools/changes/*.md`.
- `python _tools/make_stubs.py`: rewrites the redirects at the old addresses.
