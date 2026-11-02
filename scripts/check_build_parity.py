#!/usr/bin/env python3
"""check_build_parity.py - Compare the Sphinx and the ubCode (ubc) HTML builds of the docs.

Both builds are generated from the same sources (docs/), so their *content* must match.
Theme markup differs (furo vs. the ubc theme) and is ignored; what gets compared:

- the set of pages
- the needs in needs.json (id, type, title, status, tags, all link fields)
- the text of each page's main content
- needtables (columns and row count)
- needflow diagrams (the set of need IDs drawn)
- in-page toctrees (link targets) and the sidebar navigation (entry titles)

Differences caused by known ubc limitations are listed in KNOWN_DIFFERENCES. They are
normalized away and reported separately; once ubc fixes one, the script says so, and the
entry should be removed.

Usage:
    python scripts/check_build_parity.py [--sphinx docs/_build/html] [--ubc docs/_build/ubc]

Exit code 0 when both builds match, 1 otherwise.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Pages only one of the builders generates; not part of the documentation content
IGNORED_PAGES = {
    "genindex.html",  # Sphinx general index (empty for this project)
    "permalink.html",  # Sphinx-Needs permalink redirect page
    "search.html",  # each theme has its own search page
}

# Need fields compared in needs.json (link fields are added from ubproject.toml)
NEED_FIELDS = ["type", "title", "status", "tags"]


@dataclass
class KnownDifference:
    key: str
    description: str
    issue: str
    pattern: re.Pattern[str]  # how the difference shows up in the ubc output


KNOWN_DIFFERENCES = [
    KnownDifference(
        "octicon-titles",
        "Octicon roles in page titles are rendered as escaped SVG text in <title>, nav, prev/next and toctrees",
        "TODO: report to ubcode-pub",
        re.compile(r"&lt;svg\b"),
    ),
    KnownDifference(
        "card-header",
        "The '^^^' header separator of grid-item-card is not parsed, it ends up as card text",
        "TODO: report to ubcode-pub",
        re.compile(r"\^\^\^"),
    ),
    KnownDifference(
        "toctree-maxdepth",
        "toctree :maxdepth: is ignored, in-page toctrees list documents only (no sections)",
        "TODO: report to ubcode-pub",
        re.compile(r'<div class="toctree-wrapper">'),
    ),
    KnownDifference(
        "need-type-label",
        "Need headers show the directive name (e.g. 'req') instead of the type title ('Requirement')",
        "TODO: report to ubcode-pub",
        re.compile(r'<span class="ub-need-type">'),
    ),
    KnownDifference(
        "need-role-external",
        "The :need: role shows 'Title (ID)' for external needs (Sphinx-Needs shows the ID only)",
        "TODO: report to ubcode-pub",
        re.compile(r'<a class="ub-xref external"[^>]*>[^<]*\([^<)]*\)</a>'),
    ),
    KnownDifference(
        "external-needs-json",
        "External needs are written to needs.json (Sphinx-Needs leaves them out)",
        "TODO: report to ubcode-pub",
        re.compile(r"(?!)"),  # detected in needs.json, see compare_needs()
    ),
]


# ── HTML helpers ─────────────────────────────────────────────────────────────


def section(text: str, start: str, end: str) -> str:
    """The part of text from the first `start` up to the following `end`."""
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i)
    return text[i : j if j >= 0 else len(text)]


def strip_tags(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment))


def words(fragment: str) -> Counter[str]:
    return Counter(re.findall(r"\w+", strip_tags(fragment)))


def drop(pattern: str, text: str) -> str:
    return re.sub(pattern, " ", text, flags=re.S)


SVG = r"<svg\b.*?</svg>"
ESCAPED_SVG = r"&lt;svg\b.*?&lt;/svg&gt;"
MERMAID = r"<pre\s+class=\"mermaid\">.*?</pre>"
SCRIPT_STYLE = r"<(script|style)\b.*?</\1>"
TOCTREE = r'<div class="toctree-wrapper[^"]*">.*?</div>'


class Page:
    """The main content of one page of a build, plus its navigation."""

    def __init__(self, raw: str, builder: str, type_titles: dict[str, str]):
        self.raw = raw
        self.builder = builder
        if builder == "sphinx":
            self.main = section(raw, '<article role="main"', "</article>")
            self.sidebar = section(raw, '<div class="sidebar-tree">', "</aside>")
        else:
            self.main = section(raw, '<main class="ub-content"', "</main>")
            self.sidebar = section(raw, '<nav class="ub-nav"', "</aside>")
        self.type_titles = type_titles

    def text(self) -> Counter[str]:
        main = self.main
        if self.builder == "ubc":
            # need-type-label: show the type title, as Sphinx-Needs does
            main = re.sub(
                r'(<span class="ub-need-type">)([^<]*)(</span>)',
                lambda m: m.group(1) + self.type_titles.get(m.group(2), m.group(2)) + m.group(3),
                main,
            )
            # need-role-external: keep the ID only, as Sphinx-Needs does
            main = re.sub(r'(<a class="ub-xref external"[^>]*>)[^<]*\(([^<)]*)\)(</a>)', r"\1\2\3", main)
            # Theme markup: the collapsible need meta and the needflow legend, which
            # Sphinx-Needs draws inside the PlantUML image
            main = drop(r'<summary class="ub-need-meta-summary">.*?</summary>', main)
            main = drop(r'<table class="ub-needflow-legend">.*?</table>', main)
        for pattern in (SCRIPT_STYLE, TOCTREE, MERMAID, SVG, ESCAPED_SVG):
            main = drop(pattern, main)
        return words(main)

    def toctree_targets(self) -> list[str]:
        targets = []
        for block in re.findall(TOCTREE, self.main, re.S):
            if self.builder == "sphinx":
                # toctree-maxdepth: compare the documents (first level) only
                found = re.findall(r'<li class="toctree-l1[^"]*"><a[^>]*href="([^"]*)"', block)
            else:
                found = re.findall(r'<li><a[^>]*href="([^"]*)"', block)
            targets += [t.split("#")[0] for t in found]
        return targets

    def needtables(self) -> list[tuple[list[str], int]]:
        if self.builder == "sphinx":
            start = r'<table[^>]*class="[^"]*NEEDS_(?:DATATABLES|TABLE)'
        else:
            start = r'<table[^>]*class="[^"]*ub-needtable'
        tables = []
        for m in re.finditer(start, self.main):
            table = self.main[m.start() : self.main.find("</table>", m.start())]
            headers = [strip_tags(h).strip() for h in re.findall(r"<th\b[^>]*>(.*?)</th>", table, re.S)]
            rows = len(re.findall(r"<tr\b", table)) - 1
            tables.append((headers, rows))
        return tables

    def needflows(self, need_ids: set[str]) -> list[list[str]]:
        flows = []
        if self.builder == "sphinx":
            # A PlantUML image with the diagram source in its alt text, or a
            # "No needs passed the filters" paragraph
            for m in re.finditer(r'<(figure|p)\b[^>]*id="needflow-[^"]*"', self.main):
                element = self.main[m.start() : self.main.find("</figure>", m.start())]
                alt = re.search(r'<img[^>]*alt="([^"]*)"', element)
                if m.group(1) == "p" or not alt:
                    flows.append([])
                else:
                    source = html.unescape(alt.group(1))
                    flows.append(sorted(set(re.findall(r"\bas (\S+) \[\[", source)) & need_ids))
        else:
            for m in re.finditer(r'<div class="[^"]*\bub-needflow\b[^"]*">', self.main):
                block = section(self.main[m.start() :], "<div", "</svg>")
                texts = {html.unescape(t).strip() for t in re.findall(r"<text[^>]*>([^<]*)</text>", block)}
                if "ub-needs-empty" in self.main[m.start() : m.start() + 200]:
                    texts = set()
                flows.append(sorted(texts & need_ids))
        return flows

    def nav_titles(self) -> list[str]:
        if self.builder == "sphinx":
            links = re.findall(r'<li class="toctree-l\d[^"]*"><a[^>]*>(.*?)</a>', self.sidebar, re.S)
        else:
            links = re.findall(r'<a class="ub-nav-link[^"]*"[^>]*>(.*?)</a>', self.sidebar, re.S)
        titles = []
        for link in links:
            link = drop(SVG, drop(ESCAPED_SVG, link))  # octicon-titles
            titles.append(" ".join(strip_tags(link).split()))
        return titles


# ── Checks ───────────────────────────────────────────────────────────────────


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.known: Counter[str] = Counter()

    def fail(self, message: str) -> None:
        self.failures.append(message)


def load_config(path: Path) -> tuple[dict[str, str], list[str]]:
    """Need type titles by directive, and the names of all link fields."""
    config = tomllib.loads(path.read_text())
    needs = config.get("needs", {})
    type_titles = {t["directive"]: t["title"] for t in needs.get("types", [])}
    link_fields = ["links"] + [link["option"] for link in needs.get("extra_links", [])]
    return type_titles, sorted(set(link_fields))


def load_needs(build: Path) -> dict[str, dict]:
    data = json.loads((build / "needs.json").read_text())
    return data["versions"][data["current_version"]]["needs"]


def compare_needs(sphinx: Path, ubc: Path, link_fields: list[str], report: Report) -> set[str]:
    sphinx_needs = load_needs(sphinx)
    ubc_needs = load_needs(ubc)

    external = {i for i, n in ubc_needs.items() if n.get("external_url") and i not in sphinx_needs}
    if external:
        report.known["external-needs-json"] += len(external)
    ubc_needs = {i: n for i, n in ubc_needs.items() if i not in external}

    for need_id in sorted(set(sphinx_needs) - set(ubc_needs)):
        report.fail(f"needs.json: {need_id} only in the Sphinx build")
    for need_id in sorted(set(ubc_needs) - set(sphinx_needs)):
        report.fail(f"needs.json: {need_id} only in the ubc build")

    def value(need: dict, field: str):
        v = need.get(field)
        if isinstance(v, list):
            return sorted(v)
        return v if v not in ("", None) else None

    for need_id in sorted(set(sphinx_needs) & set(ubc_needs)):
        for field in NEED_FIELDS + link_fields:
            a, b = value(sphinx_needs[need_id], field), value(ubc_needs[need_id], field)
            if a != b and not (a in (None, []) and b in (None, [])):
                report.fail(f"needs.json: {need_id}.{field}: sphinx={a!r} ubc={b!r}")
    return set(sphinx_needs) | set(ubc_needs)


def html_pages(build: Path) -> set[str]:
    return {
        p.relative_to(build).as_posix()
        for p in build.rglob("*.html")
        if not any(part.startswith("_") for part in p.relative_to(build).parts)
    } - IGNORED_PAGES


def describe(counter: Counter[str], limit: int = 12) -> str:
    return " ".join(f"{w}×{n}" if n > 1 else w for w, n in counter.most_common(limit))


def compare_pages(sphinx: Path, ubc: Path, type_titles: dict[str, str], need_ids: set[str], report: Report) -> Counter[str]:
    sphinx_pages, ubc_pages = html_pages(sphinx), html_pages(ubc)
    for page in sorted(sphinx_pages - ubc_pages):
        report.fail(f"{page}: only in the Sphinx build")
    for page in sorted(ubc_pages - sphinx_pages):
        report.fail(f"{page}: only in the ubc build")

    pages = sorted(sphinx_pages & ubc_pages)
    stats: Counter[str] = Counter(pages=len(pages))
    for name in pages:
        a = Page((sphinx / name).read_text(errors="replace"), "sphinx", type_titles)
        b = Page((ubc / name).read_text(errors="replace"), "ubc", type_titles)

        for known in KNOWN_DIFFERENCES:
            report.known[known.key] += len(known.pattern.findall(b.raw))

        ta, tb = a.text(), b.text()
        if ta != tb:
            details = []
            if ta - tb:
                details.append(f"only in Sphinx: {describe(ta - tb)}")
            if tb - ta:
                details.append(f"only in ubc: {describe(tb - ta)}")
            report.fail(f"{name}: text differs ({'; '.join(details)})")

        if a.needtables() != b.needtables():
            report.fail(f"{name}: needtables differ: sphinx={a.needtables()} ubc={b.needtables()}")

        fa, fb = a.needflows(need_ids), b.needflows(need_ids)
        if fa != fb:
            report.fail(f"{name}: needflows differ: sphinx={fa} ubc={fb}")

        if a.toctree_targets() != b.toctree_targets():
            report.fail(f"{name}: toctree differs: sphinx={a.toctree_targets()} ubc={b.toctree_targets()}")

        if a.nav_titles() != b.nav_titles():
            report.fail(f"{name}: sidebar differs: sphinx={a.nav_titles()} ubc={b.nav_titles()}")

        # What was compared, so a check that silently finds nothing stands out
        stats["words"] += sum(ta.values())
        stats["needtables"] += len(a.needtables())
        stats["needflows"] += len(fa)
        stats["toctree links"] += len(a.toctree_targets())
        stats["sidebar entries"] += len(a.nav_titles())
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--sphinx", type=Path, default=PROJECT_ROOT / "docs/_build/html")
    parser.add_argument("--ubc", type=Path, default=PROJECT_ROOT / "docs/_build/ubc")
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "docs/ubproject.toml")
    args = parser.parse_args()

    for build in (args.sphinx, args.ubc):
        if not (build / "index.html").is_file():
            print(f"ERROR: no build found in {build}", file=sys.stderr)
            return 1

    report = Report()
    type_titles, link_fields = load_config(args.config)
    need_ids = compare_needs(args.sphinx, args.ubc, link_fields, report)
    stats = compare_pages(args.sphinx, args.ubc, type_titles, need_ids, report)

    print(f"Compared {len(need_ids)} needs and {', '.join(f'{n} {k}' for k, n in stats.items())}")
    print(f"  Sphinx: {args.sphinx}")
    print(f"  ubc:    {args.ubc}")

    print("\nKnown ubc differences (ignored):")
    for known in KNOWN_DIFFERENCES:
        count = report.known[known.key]
        if count:
            print(f"  - {known.key}: {known.description} [{count}×] ({known.issue})")
        else:
            print(f"  - {known.key}: no longer observed, remove it from KNOWN_DIFFERENCES")

    if report.failures:
        print(f"\nFAILED: {len(report.failures)} difference(s) between the builds:")
        for failure in report.failures:
            print(f"  - {failure if len(failure) <= 500 else failure[:500] + ' …'}")
        return 1

    print("\nOK: both builds have the same content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
