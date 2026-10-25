#!/usr/bin/env python3
"""Test suite for the Gentle Productivity Manual.

Run:  python3 tests/run_tests.py
Every check is a positive/negative assertion printed as PASS/FAIL.
Exit code 0 = all tests pass. Local-only: no network access is used.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "scripts" / "build.py"

failures = []


def check(name: str, ok: bool, detail: str = "") -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        failures.append((name, detail))


def section(title: str) -> None:
    print(f"\n— {title} —")


def main() -> int:
    section("Repository layout")
    expected = [
        "docs/00-introduction.md",
        "docs/01-energy-accounting.md",
        "docs/02-task-slicing.md",
        "docs/03-body-doubling.md",
        "docs/04-guilt-free-rest.md",
        "docs/05-timers-without-shame.md",
        "docs/06-restart-rituals.md",
        "docs/07-ai-planning-helper.md",
        "docs/07-worksheets.md",
        "docs/08-glossary.md",
        "scripts/build.py",
        "build.sh",
        "README.md",
        "LICENSE",
    ]
    for rel in expected:
        check(f"file exists: {rel}", (ROOT / rel).is_file())

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    check(
        "LICENSE has exact copyright line",
        "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text,
    )
    check("LICENSE is MIT", "MIT License" in license_text)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check(
        "README credits Asdale Dynamics, LLC",
        "Asdale Dynamics, LLC" in readme,
    )

    section("Source documents")
    docs = sorted((ROOT / "docs").glob("*.md"))
    check("10 markdown chapters", len(docs) == 10, f"found {len(docs)}")
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        check(f"{doc.name} non-empty ({len(text)} chars)", len(text) > 200)
        h1s = re.findall(r"^# (.+)$", text, flags=re.M)
        check(f"{doc.name} has exactly one H1", len(h1s) == 1)

    section("Build sanity (in a temp dir, never touching site/)")
    tmp = Path(tempfile.mkdtemp(prefix="gpm-test-"))
    try:
        result = subprocess.run(
            [sys.executable, str(BUILD), "--docs", str(ROOT / "docs"),
             "--out", str(tmp / "site"), "--clean"],
            capture_output=True, text=True, cwd=ROOT, timeout=120,
        )
        check("build.py exits 0", result.returncode == 0, result.stderr[-500:])
        site = tmp / "site"

        names = sorted(p.stem for p in site.glob("*.html"))
        check(
            "11 HTML pages (10 chapters + index.html)",
            len(names) == 11 and "index" in names,
            f"got {names}",
        )

        style = (site / "style.css")
        check("style.css copied into site", style.is_file())
        if style.is_file():
            css = style.read_text(encoding="utf-8")
            check("stylesheet has no external url() references", "url(http" not in css)

        def page_text(name: str) -> str:
            return (site / f"{name}.html").read_text(encoding="utf-8")

        # pages are well-formed enough: one doctype, every page title set
        for name in names:
            html = page_text(name)
            check(f"{name} has doctype", html.lstrip().lower().startswith("<!doctype html>"))
            check(f"{name} has <title>", "<title>" in html)
            check(f"{name} copyright footer", "Copyright (c) 2026 Asdale Dynamics, LLC" in html)

        # single source of truth: no raw markdown syntax leaked through
        html_all = " ".join(page_text(n) for n in names)
        check("no leaked heading markers", not re.search(r"<p>\s*#{1,4} ", html_all))
        check("no leftover md links", '.md"' not in html_all)

        # anchor checking: every fragment link resolves to an id on its target page
        ids_by_page = {}
        for name in names:
            ids_by_page[name] = set(
                m.group(1) for m in re.finditer(r'\bid="([^"]+)"', page_text(name))
            )
        all_ids = set().union(*ids_by_page.values())
        missing = []
        for name in names:
            for href in re.findall(r'href="([^"]+)"', page_text(name)):
                parsed = urlparse(href)
                if parsed.scheme or not parsed.fragment:
                    continue
                target = unquote(parsed.path) or name
                frag = parsed.fragment
                target_name = target[: -len(".html")] if target.endswith(".html") else name
                if frag not in ids_by_page.get(target_name, set()):
                    missing.append((name, href))
        check("all fragment anchors resolve", not missing, str(missing[:5]))

        # internal page links resolve to files
        bad_links = []
        for name in names:
            for href in re.findall(r'href="([^"]+)"', page_text(name)):
                if urlparse(href).scheme in ("http", "https"):
                    bad_links.append((name, href))
        check("no external http(s) links", not bad_links, str(bad_links[:5]))

        missing_pages = []
        for name in names:
            for href in re.findall(r'href="([^"#?]+\.html)"', page_text(name)):
                target = unquote(href)
                if not (site / target).is_file():
                    missing_pages.append((name, href))
        check("all internal page links exist", not missing_pages, str(missing_pages[:5]))

        # worksheet anchors specifically
        for frag in [
            "worksheet-1-the-daily-energy-ledger",
            "worksheet-5-the-restart-ritual-card",
        ]:
            check(f"anchor present: {frag}", frag in all_ids)

        # key navigation exists on every chapter page
        for name in names:
            html = page_text(name)
            check(f"{name} has chapter nav", 'aria-label="Chapters"' in html)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    section("Local build in place (site/)")
    result = subprocess.run(
        ["bash", str(ROOT / "build.sh")],
        capture_output=True, text=True, cwd=ROOT, timeout=120,
    )
    check("build.sh exits 0", result.returncode == 0, result.stderr[-500:])
    check("site/index.html built", (ROOT / "site" / "index.html").is_file())

    section("Privacy / secrets scan")
    secret_patterns = [
        (r"sk-[A-Za-z0-9]{10,}", "OpenAI-style key"),
        (r"ghp_[A-Za-z0-9]{20,}", "GitHub token"),
        (r"AKIA[0-9A-Z]{12,}", "AWS access key"),
        (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
        (r"PASSWORD\s*=\s*[\"'][^\"']+[\"']", "hardcoded password"),
        (r"api[_-]?key\s*=\s*[\"'][^\"']+[\"']", "hardcoded api key"),
        (r"Bearer\s+[A-Za-z0-9_\-\.]{20,}", "bearer token"),
        (r"token\s*=\s*[\"'][A-Za-z0-9]{16,}[\"']", "hardcoded token"),
    ]
    scan_targets = list((ROOT).rglob("*"))
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    blob_files = [
        p for p in scan_targets
        if p.is_file() and not any(part in skip_dirs for part in p.parts)
    ]
    hits = []
    for path in blob_files:
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        for pattern, label in secret_patterns:
            if re.search(pattern, content):
                hits.append((str(path.relative_to(ROOT)), label))
    check("no secrets in repo files", not hits, str(hits))

    prose_targets = [
        p for p in blob_files
        if p.suffix == ".md" and "tests" not in p.parts and "site" not in p.parts
    ]
    condescending = [
        (r"just\s+do\s+it", "\"just do it\""),
        (r"everyone\s+can\s+do\s+this", "\"everyone can do this\""),
        (r"no\s+excuses", "\"no excuses\""),
        (r"you'?re\s+not\s+even\s+trying", "\"you're not even trying\""),
        (r"lazy\s+people", "\"lazy people\""),
    ]
    # Self-referential policy statements are allowed: the intro and README
    # mention these phrases specifically to promise we will NOT use them,
    # so each may appear at most once per file. Used anywhere else = fail.
    allowed = {"docs/00-introduction.md": 1, "README.md": 1}
    tone_counts = {}
    for path in prose_targets:
        content = path.read_text(encoding="utf-8")
        for pattern, label in condescending:
            if re.search(pattern, content, flags=re.I):
                tone_counts.setdefault(str(path.relative_to(ROOT)), []).append(label)
    tone_hits = []
    for rel, labels in tone_counts.items():
        cap = allowed.get(rel, 0)
        if len(labels) > cap:
            tone_hits.append((rel, f"{len(labels)}x {labels} (allowed {cap})"))
    check("no condescending stock phrases", not tone_hits, str(tone_hits))

    # glossary hook: chapters referenced in the glossary exist
    section("Cross-reference consistency")
    gloss = (ROOT / "docs" / "08-glossary.md").read_text(encoding="utf-8")
    md_refs = set(re.findall(r"\]\(([\w-]+\.md)", gloss))
    doc_names = {p.name for p in docs}
    check("glossary links point at real chapters", md_refs <= doc_names,
          str(md_refs - doc_names))

    worksheets = (ROOT / "docs" / "07-worksheets.md").read_text(encoding="utf-8")
    ws_count = len(re.findall(r"^## Worksheet \d", worksheets, flags=re.M))
    check("6 worksheets present", ws_count == 6, f"found {ws_count}")

    section("Summary")
    total = len(failures)
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for name, detail in failures:
            print(f"  FAIL: {name} {detail}")
        print(f"\n{'FAILED'}: {total} failing checks")
        return 1
    print("\nAll tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
