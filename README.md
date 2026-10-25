# The Gentle Productivity Manual

An ADHD-friendly manual on **working with low energy** — a companion to our
(open-source) chore planner app. Plain English, step by step, never
condescending. Local-first: no accounts, no subscriptions, no network
required, nothing published anywhere you don't put it.

**By [Asdale Dynamics, LLC](https://dylanasdale.github.io)** — part of our
beginner-friendly, "explain it like a friend would" library.

## What's inside

Nine chapters, in any order you like:

| Chapter | What it teaches |
|---|---|
| [Introduction](docs/00-introduction.md) | Who this is for, the ground rules |
| [Energy Accounting](docs/01-energy-accounting.md) | Rate your battery, learn each task's personal energy price, spend on purpose |
| [Task Slicing](docs/02-task-slicing.md) | Cut big chores into 2–10 minute, decision-free slices |
| [Body Doubling](docs/03-body-doubling.md) | Why a second person (or a silent AI chat) makes starting easier |
| [Guilt-Free Rest](docs/04-guilt-free-rest.md) | Real rest vs. avoidance, and the Rest Protocol |
| [Timers Without Shame](docs/05-timers-without-shame.md) | Timers that measure time, not you |
| [Restart Rituals](docs/06-restart-rituals.md) | A 10-minute comeback procedure after crashes |
| [Your AI Planning Helper](docs/07-ai-planning-helper.md) | Copy-paste prompts that keep you in charge |
| [Worksheets](docs/07-worksheets.md) | 6 printable fill-in worksheets |
| [Glossary](docs/08-glossary.md) | Every term, defined in friend voice |

## How to run it (build the site)

Requirements: Python 3.8+ (standard library only). Nothing to install.

```bash
./build.sh            # builds the static site into ./site
# or explicitly:
python3 scripts/build.py --clean
```

Then open `site/index.html` in any browser — offline, no server needed.

Want another output folder? `./build.sh mysite` or
`python3 scripts/build.py --out /tmp/manual`.

## How to test it

```bash
python3 tests/run_tests.py
```

The suite checks: repo layout, the exact `LICENSE` copyright line, one-H1
per chapter, a clean build in a temp dir, internal link + anchor integrity,
no external-network references in the site, a secrets scan, a tone scan
(for condescending stock phrases), and cross-reference consistency between
worksheets, glossary, and chapters.

## Design principles

- **Local-first.** The site is plain HTML/CSS, built from `docs/`, and works
  from the filesystem. No JavaScript frameworks, no tracking, no external
  fonts, no accounts.
- **Never condescending.** No "just do it," no willpower lectures. The test
  suite even scans for those phrases and fails if one slips in.
- **Companion, not clinic.** Education only, never medical advice.
- **Print-friendly.** The worksheets are usable straight from paper;
  the site's print CSS keeps code blocks intact for paper use.

## Repository layout

```
docs/           Markdown chapters (the source of truth)
scripts/        build.py (markdown -> HTML) and the stylesheet source
tests/          run_tests.py — full local test suite
site/           Built static site (regenerate with ./build.sh)
build.sh        One-command build wrapper
LICENSE         MIT — Copyright (c) 2026 Asdale Dynamics, LLC
```

## Contributing and reuse

MIT licensed. Take the words, the worksheets, the build script, the prompts —
copy them, print them, reuse them. If you improve the manual, spelling
"guilt-free" with a hyphen is the only style rule we ask for.

_This manual is educational material from Asdale Dynamics, LLC and is not
medical, legal, or financial advice._
