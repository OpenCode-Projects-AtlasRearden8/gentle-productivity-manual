# STATUS

Last updated: 2026-10-25

## What was built

**The Gentle Productivity Manual** — an ADHD-friendly manual on working with
low energy, positioned as a companion to the chore planner app. It is written,
built, and tested, and the entire repo is local-first (no accounts, no
network, no secrets).

### Content (source of truth: `docs/*.md`)

- `00-introduction.md` — who it's for, ground rules, how to use it
- `01-energy-accounting.md` — battery ratings, per-task energy pricing,
  spending plans, the 80% margin rule
- `02-task-slicing.md` — 2–10 minute decision-free slices, the
  "first slice only" rule, 2-minute versions
- `03-body-doubling.md` — human / remote / AI body doubling levels,
  etiquette, a ready-to-use ask script
- `04-guilt-free-rest.md` — what real rest is, the Rest Protocol,
  rest scheduling patterns
- `05-timers-without-shame.md` — "in, park, or pivot" timer frame,
  Park Breadcrumbs, timer types table
- `06-restart-rituals.md` — the 10-minute five-step comeback ritual,
  the three restart traps, amnesty logic, streak rebuilding
- `07-ai-planning-helper.md` — five copy-paste prompts (slicing clerk,
  energy clerk, rest menu, body double, restart clerk), privacy rules,
  what an AI helper should never be
- `07-worksheets.md` — 6 printable fill-in worksheets (energy ledger,
  slicing sheet, price list, rest menu, restart card, body-double ask)
- `08-glossary.md` — every term in friend voice

### Code

- `scripts/build.py` — stdlib-only Markdown → HTML static site generator
  (headings, lists, blockquotes, tables, fenced code, inline styling,
  heading anchors, internal `.md` → `.html` link rewriting, chapter nav,
  prev/next pager, index landing page)
- `scripts/style-source.css` — warm, high-contrast stylesheet with dark-mode
  support and print CSS for worksheets
- `build.sh` — one-command build wrapper
- `tests/run_tests.py` — full test suite (see verification below)

### Policy files

- `LICENSE` — MIT, with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — credits Asdale Dynamics, LLC; run and test instructions

## How to run it

```bash
./build.sh                 # build the static site into ./site
open site/index.html       # any browser, works offline from the filesystem
```

or explicitly: `python3 scripts/build.py --clean [--out some/dir]`
(Python 3.8+, standard library only — nothing to install).

## How to verify

```bash
python3 tests/run_tests.py
```

## Verification results (final run)

All checks pass (exit code 0):

- Repository layout: 14 required files present, LICENSE copyright line exact,
  README credit present
- Source documents: 10 chapters, all substantive, exactly one H1 each
- Build sanity: clean build in a temp dir → 11 HTML pages + style.css,
  every page has doctype/title/copyright footer, no leaked markdown syntax,
  no leftover `.md` links, all fragment anchors resolve (including both
  worksheet anchors referenced from other chapters), all internal page links
  exist, zero external http(s) links in the site
- Local build in place: `./build.sh` exits 0, `site/index.html` built
- Privacy scan: no secrets/key/token patterns in any repo file
- Tone scan: no condescending stock phrases in prose files (the two
  self-referential policy mentions in the intro/README are allowed by design)
- Cross-references: glossary links all resolve to real chapters,
  6 worksheets present
- All 11 generated pages parse as valid HTML

## Known gaps / not yet done

- The chore planner app itself is a separate project; this repo references it
  narratively (pre-sliced chore templates, battery entry, done-marking) and
  there is no integration or data exchange between the two yet.
- No search box in the generated site (chapter nav only); a small client-side
  search could be added without breaking the no-framework approach.
- No EPUB/PDF export — the site's print CSS is usable, but a proper PDF build
  script isn't included.
- The tone-scan is a lexicon check for a handful of stock condescending
  phrases; it is a smoke test, not a guarantee about tone in general.
- Worksheet fill-ins are `___` lines intended for printing or copying into a
  notebook; there is no editable/interactive form version.
- Anchors for headings inside tables or code blocks aren't linkable targets
  (only headings ≤ level 4 get ids) — no current link needs more.

## Licensing

MIT — Copyright (c) 2026 Asdale Dynamics, LLC. Educational material only;
never medical advice.
