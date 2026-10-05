---
name: ieee-paper
description: Author, format, validate, and compile IEEE conference papers using LaTeX based on the official IEEEtran template (06/28/2024 revision). Use when drafting IEEE papers, preparing conference submissions, configuring IEEEtran document layouts, generating IEEE-compliant figures, or linting papers against IEEE desk-rejection rules.
---

# IEEE Conference Paper Authoring

## Overview

Produce publication-grade IEEE conference papers using LaTeX adhering strictly to the official IEEEtran specification (baseline template `IEEE-conference-template-062824.tex` / `IEEEtran.cls`). This skill covers the full research-to-submission lifecycle: evidence compilation, visual schematic design, LaTeX typesetting, deterministic IEEE rule validation, and PDF compilation.

## When to Use This Skill

Apply this skill when:
- Authoring new IEEE conference papers or technical workshop papers.
- Migrating research drafts or generic LaTeX documents to the IEEE two-column layout.
- Designing IEEE publication figures with compliant 3.5 in (single) or 7.16 in (double) column widths.
- Verifying IEEE manuscripts against desk-rejection hazards (residual template text, improper caption placement, title/abstract math).
- Diagnosing LaTeX compilation errors, overfull hboxes, or undefined citations in IEEE papers.

---

## The IEEE Paper Lifecycle

```
[Phase 1: Evidence]   --> research-lookup & paper-lookup (60+ verified sources)
[Phase 2: Schematics] --> scientific-schematics (3.5 in / 7.16 in, 8pt labels)
[Phase 3: Scaffold]   --> assets/paper_scaffold.tex (clean IEEEtran skeleton)
[Phase 4: Drafting]   --> IMRAD structure & mathematical typesetting
[Phase 5: Validation] --> scripts/validate_ieee_paper.py (desk-rejection check)
[Phase 6: Compiling]  --> scripts/compile_paper.py (pdflatex + bibtex diagnostic)
```

---

## Quick Start: Scaffold a New Paper

To initialize a new IEEE conference paper in the current workspace:

```bash
# Copy the clean scaffold and class file to your project root
cp .cursor/skills/ieee-paper/assets/IEEEtran.cls ./
cp .cursor/skills/ieee-paper/assets/paper_scaffold.tex ./main.tex
cp .cursor/skills/ieee-paper/assets/references.bib ./references.bib
```

---

## Non-Negotiable IEEE Rules

Before submitting, every paper must comply with these core IEEE directives:

1. **Zero Template Boilerplate**: IEEE desk-rejects papers containing residual template instructions (e.g., *"This document is a model and instructions for LaTeX"*, *"Identify applicable funding agency here"*). Purge all guidance text.
2. **Title & Abstract Constraints**:
   - Strictly NO math mode (`$...$`), symbols, citations, or footnotes in title or abstract.
   - Do NOT use subtitles (`\\` in `\title`). IEEE Xplore does not index subtitles.
3. **Caption Orientation**:
   - Table captions must appear **ABOVE** tables (`\caption{...}` before `\begin{tabular}`).
   - Figure captions must appear **BELOW** figures (`\caption{...}` after `\includegraphics`).
   - `\label{...}` must NEVER precede `\caption{...}`.
4. **Equation Typography**:
   - Strictly avoid `\begin{eqnarray}` (use `align` or `IEEEeqnarray`).
   - Reference equations as `\eqref{eq}` (not `Eq.~\eqref{eq}`) unless beginning a sentence.
   - Punctuate displayed equations with commas or periods matching sentence grammar.
5. **Citations & Bibliography**:
   - In-text references use `[1]` or `\cite{ref}` (not `Ref. [1]`).
   - List all author names if under 6 authors; only use *et al.* for 6 or more authors.
   - Capitalize only the first word of article and conference titles.
6. **Strict Equation Justification & Attribution**:
   - Zero Orphan Equations: Every equation must have a demonstrable impact on final outputs or decisions. Unreferenced or decorative formulas must be eliminated.
   - Targeted Attribution: When adopting formulas, cite the source once at introduction without repeating citations across derivation steps.

---

## Detailed Step-by-Step Workflow

### Step 1: Research and Evidence Gathering
- Run academic queries using `research-lookup` and `paper-lookup` to assemble foundational and state-of-the-art references.
- Construct a claim-to-source mapping using `scientific-writing` principles to ensure every technical claim is grounded in verified literature.

### Step 2: Visual Elements and Schematics
Generate publication-quality figures matching IEEE column geometry:
- **Single Column**: Width exactly 3.5 in (88.9 mm, 21 picas / `\columnwidth`).
- **Double Column (Full Width)**: Width exactly 7.16 in (181.9 mm, 43 picas / `\textwidth`).
- **Typography**: Minimum 8pt sans-serif or Times labels; Okabe-Ito colorblind-safe palette.

Using `scientific-schematics`:
```bash
# Single-column system architecture
python scripts/generate_schematic.py \
  "IEEE conference single-column diagram (width 3.5 in): Block diagram showing Sensor -> Edge Processor -> Cloud Gateway. 8pt clean labels. White background." \
  -o figures/fig1.png --doc-type conference
```
*See [figures_and_tables.md](references/figures_and_tables.md) for full geometry and float rules.*

### Step 3: Authoring and Typesetting

Structure your manuscript using the clean skeleton in `assets/paper_scaffold.tex`:
- **Document Class**: `\documentclass[conference]{IEEEtran}` with `\IEEEoverridecommandlockouts` for funding footnotes (`\thanks{}`).
- **Author Blocks**:
  - 1--3 Authors: Side-by-side using `\and`.
  - 4--6 Authors: Two rows of side-by-side author columns.
  - Multi-institution: Use `\IEEEauthorrefmark{1}`.
- **Section Hierarchy**:
  - `\section{Introduction}`
  - `\section{Related Work}`
  - `\section{Methodology}` (justified equations impacting outputs, single citation at introduction)
  - `\section{Experimental Evaluation}`
  - `\section{Discussion and Limitations}` (four pillars: key findings, field implications, benefits vs. shortcomings)
  - `\section{Conclusion}` (core takeaways, concrete future research directions)
  - `\section*{Acknowledgment}`

*See [ieee_template_spec.md](references/ieee_template_spec.md) and [mathematical_typesetting.md](references/mathematical_typesetting.md).*

### Step 4: Validate Paper Compliance

Run the deterministic IEEE compliance linter:

```bash
python3 .cursor/skills/ieee-paper/scripts/validate_ieee_paper.py main.tex
```

For automated pipelines or CI checks:
```bash
python3 .cursor/skills/ieee-paper/scripts/validate_ieee_paper.py main.tex --strict --json
```

The validator automatically audits:
- Template instructional boilerplate residue (`IEEE-TPL-001`)
- Math in title or abstract (`IEEE-TIT-001`, `IEEE-ABS-001`)
- Table caption below tabular (`IEEE-FLT-002`)
- Figure caption above graphic (`IEEE-FLT-004`)
- Counter error: `\label` placed before `\caption` (`IEEE-FLT-005`)
- Deprecated `eqnarray` environments (`IEEE-MTH-001`)
- Orphan equations and unlabeled numbered math (`IEEE-MTH-002`, `IEEE-MTH-003`)
- Citations placed directly inside equation environments (`IEEE-REF-004`)
- Redundant citation and equation grammar (`IEEE-REF-001` to `003`)
- Common editorial mistakes ("data is", missing decimal zero, "Acknowledgement")

*See [common_mistakes_checklist.md](references/common_mistakes_checklist.md).*

### Step 5: Compilation and Diagnostics

Compile the paper through the complete four-pass pipeline:

```bash
python3 .cursor/skills/ieee-paper/scripts/compile_paper.py main.tex
```

To clean intermediate build files (`.aux`, `.bbl`, `.blg`, `.log`, `.out`):
```bash
python3 .cursor/skills/ieee-paper/scripts/compile_paper.py main.tex --clean
```

The script verifies:
- Clean PDF generation
- Overfull `\hbox` / `\vbox` warnings (reporting line numbers and overflow pt)
- Undefined citations and cross-references
- Output page count against venue limits

---

## Reference Guides

For deep dives into IEEE styling specifications, consult the following modular references:
- **[ieee_template_spec.md](references/ieee_template_spec.md)**: Class options, author blocks, and title/abstract constraints.
- **[figures_and_tables.md](references/figures_and_tables.md)**: Column widths, caption positioning, axis labeling, and schematic integration.
- **[mathematical_typesetting.md](references/mathematical_typesetting.md)**: Equations, AMS environments, punctuation, upright operators, and constants.
- **[references_and_citations.md](references/references_and_citations.md)**: IEEE citation grammar, 6-author rule, sentence casing, and BibTeX schemas.
- **[common_mistakes_checklist.md](references/common_mistakes_checklist.md)**: Complete pre-submission editorial and desk-rejection checklist.

---

## Bundled Assets and Scripts

- `assets/IEEEtran.cls`: Official IEEE document class (v1.8b).
- `assets/IEEE-conference-template-062824.tex`: Upstream reference template with IEEE guidance.
- `assets/paper_scaffold.tex`: Clean, production-ready LaTeX scaffold completely stripped of template boilerplate.
- `assets/references.bib`: IEEEtran-compliant BibTeX starter bibliography.
- `scripts/validate_ieee_paper.py`: Zero-dependency Python linter for IEEE compliance.
- `scripts/compile_paper.py`: Automated multi-pass PDF compiler with overfull box diagnostics.
