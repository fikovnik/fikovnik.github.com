# Publications + CV pages generated from BibTeX

Date: 2026-07-05
Status: approved (pending spec review)

## Goal

Rework the personal site (Zola + serene theme) so that:

1. `/publications` shows **only publications** — one flat chronological list,
   newest first — generated from a single BibTeX file that is also offered for
   download.
2. A new `/cv` page holds everything else that used to live on the publications
   page (theses, community service, program committees, reviewing, talks) plus a
   curated CV and a link to `CV.pdf`.
3. Adding a publication = add one entry to the `.bib` and run `make
   publications`.

Success criteria:

- `make publications` regenerates `content/publications/_index.md` from the
  `.bib` with no manual editing.
- `make build` / `make check` succeed; the committed generated markdown is what
  CI builds (CI is unchanged).
- `/publications` lists every publication (published + in-submission) in the
  requested format, newest first.
- `/cv` renders the curated CV and links `CV.pdf`.

## Non-goals

- No change to the deploy workflow (`.github/workflows/deploy.yml` keeps running
  `zola build` only).
- No new theme/template work unless strictly required (the pages stay
  `template = "prose.html"`).
- No citation-count / Scholar scraping.

## Constraints discovered

- CI runs `zola build` only — **no generation step runs in CI**. Therefore the
  generator's output (`content/publications/_index.md`) must be **committed**.
- Site is otherwise "Docker-only" (no local Zola). `uv`, `pandoc`, `pdftotext`
  are available locally; the generator uses `uv run` so no manual `pip install`
  is needed.
- PDFs already live in `static/publications/` and are served at
  `/publications/<file>`.

## Approach (chosen)

BibTeX (source of truth) → Python generator (`uv run`) → committed markdown page.
PDFs hosted locally where freely available, DOI link always where a DOI exists.

Alternatives considered and rejected: Zola template + committed JSON (more moving
parts, still needs a bib→json step); pandoc rendering (less control over the
exact line format). Both add complexity for no benefit here.

## Components

### 1. `static/publications/publications.bib` — source of truth

- Served at `/publications/publications.bib`; linked as **Download BibTeX** at the
  bottom of the publications page.
- Simple style, modeled on `Research/Publications/MPLR26/paper/jv.bib`: short
  keys, `@article` for journals (PACMPL etc.), `@inproceedings` for
  conferences/workshops, a `doi` on every published entry.
- Fields:
  - `title`, `author` (ALL authors), `year` — required.
  - `venue` — display abbreviation shown in the listing (`OOPSLA`, `PLDI`,
    `ECOOP`, `ISSTA`, `SLE`, `VMIL`, `MoreVMs`, `REP`, `MODELS`, `ICAC`, `SAC`,
    `SEKE`, `SEAMS`, `DISCOTEC`, `TAAS`, …). Required.
  - `doi` — present for published papers; omitted for in-submission papers.
  - `status` — optional; present only on in-submission papers. Value is the
    real status ("under review", "conditional accept", "to appear"). Rendered as
    a parenthetical label. (Open question for spec review: normalize all to
    "under review"?)
  - `artifact` / `url` — optional external link (Zenodo/artifact/author page),
    carried over where it already exists.
- Key naming: `<venue><yy>[a-z]`, e.g. `oopsla20`, `oopsla21a`, `vmil24`,
  `sle22`. Keys are lowercase and URL-safe.

Example:

```bibtex
@article{oopsla20,
  title  = {Designing Types for R, Empirically},
  author = {Turcotte, Alexi and Goel, Aviral and Křikava, Filip and Vitek, Jan},
  year   = {2020},
  venue  = {OOPSLA},
  doi    = {10.1145/3428264},
}

@article{oopsla26,
  title  = {Revisiting Row Polymorphism for Set-Theoretic Types},
  author = {Laurent, Mickael and Donat-Bouillud, Pierre and Křikava, Filip and Vitek, Jan},
  year   = {2026},
  venue  = {OOPSLA},
  status = {under review},
}
```

### 2. PDF hosting (by convention)

- Freely available PDFs are downloaded into `static/publications/<key>.pdf`.
- **Existing paper PDFs are renamed to their bib key** (e.g.
  `ISSTA18.pdf` → `issta18.pdf`, `SLE22.pdf` → `sle22.pdf`, `TAAS16.pdf` →
  `taas16.pdf`, `SSEN15.pdf`/`SEFSASb3.pdf` → their keys).
- The generator links a `[pdf]` **iff `static/publications/<key>.pdf` exists** —
  no `pdf` field in the bib. Paywalled papers with no local PDF get `[doi]` only.
- Thesis PDFs (`habilitation.pdf`, `phd.pdf`, `master.pdf`) are **not** part of
  the bib; they stay in `static/publications/` and are linked by hand from the
  CV page.

### 3. `scripts/bib2md.py` — generator

- Run as `uv run scripts/bib2md.py <bib> <out.md>`; deps declared inline
  (PEP 723): `bibtexparser`.
- Reads `static/publications/publications.bib`, writes
  `content/publications/_index.md` (front matter + intro prose preserved as a
  constant header in the script, then the generated list).
- Sort: `year` descending; within a year, in-submission (no doi) first, then
  stable by key. In-submission 2026 items therefore appear at the very top.
- Author rendering: normalize each author to `F. Last` (handle both
  `Last, First` and `First Last`, and accented names such as Křikava,
  Flückiger). All authors listed.
- For each entry emit:

  ```markdown
  - **{title}**, {venue}, {year}{ (status) if status}{ · [pdf](/publications/<key>.pdf) if exists}{ · [doi](https://doi.org/{doi}) if doi}{ · [artifact]({artifact}) if artifact}
    {A. Author, B. Author, C. Author}
  ```

  (`[doi]` resolves to ACM DL for ACM DOIs; label kept generic since ECOOP is
  LIPIcs and older venues are IEEE/HAL.)

### 4. `content/publications/_index.md` (generated)

- Front matter: `title = "Publications"`, `template = "prose.html"`,
  `aliases = ["/research/"]`.
- Body: the two existing intro paragraphs (research summary) + a "Download
  BibTeX" link + the generated chronological list. No thesis/committee/talks
  sections.
- This file is generated and committed; a comment marks it as generated.

### 5. `content/cv/_index.md` (new, hand-written)

`template = "prose.html"`, `title = "CV"`. Sections, sourced from `CV.pdf`, the
GACR summary, and the lists removed from the old publications page:

- Intro + **Download CV (PDF)** link → `/cv/cv.pdf` (copy of
  `Research/Grants/GACR27-std-types/CV.pdf` into `static/cv/cv.pdf`).
- **Employment** / positions.
- **Education**.
- **Awards** (10-Year Most Influential Paper SEAMS'25, Best Artifact ISSTA'18,
  Prof. Vlček Best MSc CTU'09).
- **Community service** (OOPSLA'27 general chair, OOPSLA steering from 2025,
  MoreVMs'25, REBASE from 2020, Curry-On 2017–2019, TTC 2015–2019, SPLASH'18 web
  co-chair, SC-CAMP from 2011).
- **Program committees** (existing list).
- **Theses** (habilitation / PhD / MSc — link existing PDFs).
- **Reviewing** (existing "Other" list).
- **Selected talks** (existing presentations list — moved here, not dropped).

### 6. Navigation + Makefile

- `config.toml`: add `{ name = "cv", path = "/cv", is_external = false }` to
  `[extra] sections`.
- `Makefile`: add
  ```make
  publications:
  	uv run scripts/bib2md.py static/publications/publications.bib content/publications/_index.md
  ```
  Local `serve` and `build` depend on `publications` so previews stay fresh; CI
  still calls `zola build` directly against the committed output.

## Data gathering plan

Build `publications.bib` by reconciling these sources (read-only research,
dispatched in parallel):

- **dblp** `https://dblp.org/pid/05/10588.html` — backbone; authoritative full
  list with DOIs and complete author lists (has a BibTeX export).
- **ACM DL** author page — DOIs and open-access PDFs where available.
- **PRL-PRG** `https://prl-prg.github.io/publications.html`.
- **janvitek.org** — open PDFs for the R/PL papers.
- **mlaurent.ovh/#publications** — Mickael Laurent's recent co-authored papers
  (VIMPL'25, row-polymorphism OOPSLA'26 submission).
- **`CV.pdf`** — recent + in-submission items (R4R/REP'25, MoreVMs'25, VIMPL'25,
  VMIL'24/'25, ECOOP'26, MPLR'26, OOPSLA'26, TOPLAS).

PDFs: fetch freely available ones into `static/publications/<key>.pdf`; DOI-only
where paywalled. **The `.bib` is the human-reviewable artifact** — mistakes are
caught and fixed there, then regenerated.

## Verification

1. `uv run scripts/bib2md.py …` produces `content/publications/_index.md`
   without error.
2. `make build` and `make check` succeed.
3. Manual review of rendered `/publications` (format, order, links resolve) and
   `/cv` (all moved sections present, CV.pdf downloads).
4. `.bib` reviewed by user for completeness/accuracy.

## Open questions for spec review

- Status labels: use accurate per-paper status ("under review" /
  "conditional accept") or normalize all in-submission items to
  "under review"?
- Keep "Selected talks" on the CV page, or drop talks entirely?
