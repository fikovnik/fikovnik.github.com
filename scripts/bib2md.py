# /// script
# requires-python = ">=3.10"
# dependencies = ["bibtexparser<2"]
# ///
"""Generate the Zola publications page from a BibTeX file.

Usage: uv run scripts/bib2md.py <input.bib> <output.md>

Each entry needs: title, author, year, venue. Optional: doi, status
(e.g. "under review"), artifact/url. A `[pdf]` link is emitted automatically
when `<bibdir>/<key>.pdf` exists (PDFs are named after the BibTeX key).
"""

import sys
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import splitname

# Preserved page header. Everything below the marker is generated.
HEADER = """+++
title = "Publications"
template = "prose.html"
aliases = ["/research/"]

[extra]
title = "Publications"
+++

[BibTeX](/publications/publications.bib) :: [Google Scholar](https://scholar.google.com/citations?user=r_GmitIAAAAJ&hl=en) :: [DBLP](https://dblp.org/pid/05/10588.html).

<!-- Generated from publications.bib by scripts/bib2md.py — do not edit by hand. Run `make publications`. -->
"""


def format_author(name: str) -> str:
    """Render a single BibTeX author name as "F. Last"."""
    parts = splitname(name.strip())
    last = " ".join(parts.get("von", []) + parts.get("last", [])).strip()
    first = parts.get("first", [])
    initial = f"{first[0][0]}. " if first and first[0] else ""
    return f"{initial}{last}".strip()


def format_authors(field: str) -> str:
    authors = [a.strip() for a in field.replace("\n", " ").split(" and ") if a.strip()]
    return ", ".join(format_author(a) for a in authors)


def clean(text: str) -> str:
    """Drop BibTeX brace-protection and collapse whitespace."""
    return " ".join(text.replace("{", "").replace("}", "").split())


def sort_key(entry):
    year = int(entry.get("year", "0") or "0")
    in_submission = 0 if entry.get("status") else 1  # in-submission first within a year
    return (-year, in_submission, entry.get("ID", ""))


def render_entry(entry, bibdir: Path) -> str:
    key = entry["ID"]
    title = clean(entry.get("title", ""))
    venue = clean(entry.get("venue", ""))
    year = entry.get("year", "")

    head = f"**{title}**, {venue}, {year}"
    if status := entry.get("status"):
        head += f" _({clean(status)})_"

    links = []
    if (bibdir / f"{key}.pdf").exists():
        links.append(f"[pdf](/publications/{key}.pdf)")  # locally hosted copy wins
    elif pdf := entry.get("pdf"):
        links.append(f"[pdf]({pdf.strip()})")  # else an external free PDF
    if doi := entry.get("doi"):
        links.append(f"[doi](https://doi.org/{doi.strip()})")
    if artifact := (entry.get("artifact") or entry.get("url")):
        links.append(f"[artifact]({artifact.strip()})")
    if links:
        head += " · " + " · ".join(links)

    authors = format_authors(entry.get("author", ""))
    return f"- {head}  \n  {authors}"


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: bib2md.py <input.bib> <output.md>")
    bib_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    bibdir = bib_path.parent

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    db = bibtexparser.loads(bib_path.read_text(encoding="utf-8"), parser=parser)

    entries = sorted(db.entries, key=sort_key)
    body = "\n\n".join(render_entry(e, bibdir) for e in entries)
    out_path.write_text(f"{HEADER}\n{body}\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(entries)} publications)")


if __name__ == "__main__":
    main()
