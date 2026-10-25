#!/usr/bin/env python3
"""Build script for the Gentle Productivity Manual.

Converts the Markdown chapters in docs/ into a small static HTML site in
site/ (local-first: no external assets beyond style.css, no accounts, no
network). Stdlib only.  Run:  python3 scripts/build.py [--out site] [--clean]
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

DEFAULT_DOCS_DIR = "docs"
DEFAULT_OUT_DIR = "site"

COPYRIGHT_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"
SITE_TITLE = "The Gentle Productivity Manual"
SITE_TAGLINE = "Working with low energy — an ADHD-friendly manual"


def slugify(text: str) -> str:
    text = text.strip().lower().replace(" ", "-")
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str) -> str:
    """Inline markdown: escape HTML, code, links, bold, italic."""
    text = esc(text)
    links = []

    def _stash_link(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00{len(links) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _stash_link, text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", text)

    def _restore_link(m):
        label, url = links[int(m.group(1))]
        return f'<a href="{url}">{label}</a>'

    text = re.sub(r"\x00(\d+)\x00", _restore_link, text)
    return text


def md_link_to_html(url: str) -> str:
    """Rewrite relative .md links to .html (keeping the #anchor)."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if parsed.scheme or not path.lower().endswith(".md"):
        return url
    new_path = path[: -len(".md")] + ".html"
    return new_path + (f"#{parsed.fragment}" if parsed.fragment else "")


def parse_blocks(md: str):
    """Yield (kind, payload) blocks: heading/para/list/quote/table/code/hr."""
    lines = md.replace("\r\n", "\n").split("\n")
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if not stripped:
            i += 1
            continue
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                body.append(esc(lines[i]))
                i += 1
            i += 1  # closing fence
            blocks.append(("code", (lang, "\n".join(body))))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            blocks.append(("heading", (len(m.group(1)), m.group(2).strip())))
            i += 1
            continue
        if re.match(r"^(---+|\*\*\*+)$", stripped) and indent == 0:
            blocks.append(("hr", None))
            i += 1
            continue
        if stripped.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            blocks.append(("quote", " ".join(q for q in quote if q)))
            continue
        if stripped.startswith("|") and i + 1 < n and re.match(
            r"^\|?[\s:|-]+\|?$", lines[i + 1].strip()
        ) and "-" in lines[i + 1]:
            header = [c.strip() for c in stripped.strip("|").split("|")]
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(
                    [c.strip() for c in lines[i].strip().strip("|").split("|")]
                )
                i += 1
            blocks.append(("table", (header, rows)))
            continue
        is_ul = bool(re.match(r"^[-*]\s+", stripped))
        is_ol = bool(re.match(r"^\d+[.)]\s+", stripped))
        if is_ul or is_ol:
            items = []

            def _flush():
                if items:
                    blocks.append(("list", items.copy()))
                    items.clear()

            while i < n and lines[i].strip():
                s = lines[i].strip()
                child = bool((len(lines[i]) - len(lines[i].lstrip())) >= 2)
                cont = None
                if re.match(r"^[-*]\s+", s):
                    kind = "ul"
                elif re.match(r"^\d+[.)]\s+", s):
                    kind = "ol"
                elif child and items:
                    items[-1] = (items[-1][0], items[-1][1] + " " + s)
                    i += 1
                    continue
                else:
                    break
                cont = re.sub(r"^(?:[-*]|\d+[.)])\s+", "", s)
                # flush when list type or nesting context changes
                if items and (items[-1][0] != kind) and not child and kind == "ol":
                    _flush()
                items.append((kind, cont))
                i += 1
            _flush()
            continue
        para = [stripped]
        i += 1
        while i < n:
            s = lines[i].strip()
            if (
                not s
                or s.startswith("```")
                or s.startswith(">")
                or s.startswith("|")
                or s.startswith("#")
                or re.match(r"^[-*]\s+", s)
                or re.match(r"^\d+[.)]\s+", s)
                or re.match(r"^(---+|\*\*\*+)$", s)
            ):
                break
            para.append(s)
            i += 1
        blocks.append(("para", " ".join(para)))
    return blocks


def render_blocks(blocks) -> str:
    out = []
    for kind, payload in blocks:
        if kind == "heading":
            level, text = payload
            attrs = f' id="{slugify(text)}"' if level <= 4 else ""
            out.append(f"<h{level}{attrs}>{inline(text)}</h{level}>")
        elif kind == "para":
            out.append(f"<p>{inline(payload)}</p>")
        elif kind == "quote":
            out.append(f"<blockquote><p>{inline(payload)}</p></blockquote>")
        elif kind == "code":
            lang, body = payload
            lang_attr = f' data-lang="{esc(lang)}"' if lang else ""
            out.append(f"<pre><code{lang_attr}>{body}</code></pre>")
        elif kind == "hr":
            out.append("<hr>")
        elif kind == "list":
            if not payload:
                continue
            tag = "ul" if payload[0][0] == "ul" else "ol"
            lis = "\n".join(f"<li>{inline(text)}</li>" for _, text in payload)
            out.append(f"<{tag}>\n{lis}\n</{tag}>")
        elif kind == "table":
            header, rows = payload
            th = "".join(f"<th>{inline(c)}</th>" for c in header)
            trs = []
            for row in rows:
                tds = "".join(f"<td>{inline(c)}</td>" for c in row)
                trs.append(f"<tr>{tds}</tr>")
            out.append(
                "<table><thead><tr>" + th + "</tr></thead><tbody>"
                + "".join(trs) + "</tbody></table>"
            )
    return "\n".join(out)


def first_heading(md: str) -> str:
    for line in md.split("\n"):
        m = re.match(r"^#\s+(.*)$", line.strip())
        if m:
            return m.group(1).strip()
    return "Untitled"


def rewrite_internal_links(html: str) -> str:
    return re.sub(
        r'href="([^"]+\.md[^"]*)"',
        lambda m: f'href="{md_link_to_html(m.group(1))}"',
        html,
    )


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title} — {site_title}</title>
<meta name="author" content="Asdale Dynamics, LLC">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
  <p class="brand"><a href="index.html">{site_title}</a></p>
  <p class="tagline">{tagline}</p>
</header>
<div class="layout">
  <nav class="sidebar" aria-label="Chapters">
    <h2>Chapters</h2>
    <ol>
{nav_items}
    </ol>
  </nav>
  <main>
{content}
  <nav class="pager">
{pager}
  </nav>
  <footer>
    <p>Local-first and account-free. {copyright}</p>
  </footer>
</main>
</div>
</body>
</html>
"""


def build(docs_dir: Path, out_dir: Path):
    doc_files = sorted(docs_dir.glob("*.md"))
    if not doc_files:
        raise SystemExit(f"No .md files found in {docs_dir}")
    pages = []
    for path in doc_files:
        md = path.read_text(encoding="utf-8")
        title = first_heading(md)
        body = render_blocks(parse_blocks(md))
        pages.append((path.stem, title, body))

    out_dir.mkdir(parents=True, exist_ok=True)
    style_source = Path(__file__).resolve().parent / "style-source.css"
    if style_source.is_file():
        shutil.copyfile(style_source, out_dir / "style.css")
    for i, (name, title, body) in enumerate(pages):
        nav_items = "\n".join(
            f'      <li><a href="{n}.html">{t}</a></li>' for n, t, _ in pages
        )
        pager_parts = []
        if i > 0:
            pager_parts.append(
                f'<a class="prev" href="{pages[i - 1][0]}.html">'
                f"&larr; {pages[i - 1][1]}</a>"
            )
        if i < len(pages) - 1:
            pager_parts.append(
                f'<a class="next" href="{pages[i + 1][0]}.html">'
                f"{pages[i + 1][1]} &rarr;</a>"
            )
        html = rewrite_internal_links(
            PAGE_TEMPLATE.format(
                page_title=esc(title),
                site_title=esc(SITE_TITLE),
                tagline=esc(SITE_TAGLINE),
                nav_items=nav_items,
                content=body,
                pager="\n".join(pager_parts),
                copyright=esc(COPYRIGHT_LINE),
            )
        )
        (out_dir / f"{name}.html").write_text(html, encoding="utf-8")

    # index.html = landing page built from the first chapter
    nav_items = "\n".join(
        f'      <li><a href="{n}.html">{t}</a></li>' for n, t, _ in pages
    )
    pager = (
        f'<a class="next" href="{pages[1][0]}.html">{pages[1][1]} &rarr;</a>'
        if len(pages) > 1
        else ""
    )
    (out_dir / "index.html").write_text(
        rewrite_internal_links(
            PAGE_TEMPLATE.format(
                page_title=esc("Start Here"),
                site_title=esc(SITE_TITLE),
                tagline=esc(SITE_TAGLINE),
                nav_items=nav_items,
                content=pages[0][2],
                pager=pager,
                copyright=esc(COPYRIGHT_LINE),
            )
        ),
        encoding="utf-8",
    )
    return [(name, title) for name, title, _ in pages]


def main() -> int:
    cli = argparse.ArgumentParser(description="Build the static manual site.")
    cli.add_argument("--docs", default=DEFAULT_DOCS_DIR, type=Path)
    cli.add_argument("--out", default=DEFAULT_OUT_DIR, type=Path)
    cli.add_argument("--clean", action="store_true", help="wipe out dir first")
    args = cli.parse_args()
    if args.clean and args.out.exists():
        shutil.rmtree(args.out)
    built = build(args.docs, args.out)
    print(f"Built {len(built)} chapter pages + index.html into {args.out}/")
    for name, title in built:
        print(f"  {name}.html  {title}")
    print("  index.html  Start Here")
    return 0


if __name__ == "__main__":
    sys.exit(main())
