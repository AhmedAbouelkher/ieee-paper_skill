# IEEEtran Class & Conference Template Specification

## Overview
The official IEEE conference template is maintained by IEEE and updated regularly (baseline: `IEEE-conference-template-062824.tex` / `IEEEtran.cls` v1.8b). All margins, column widths, line spaces, and fonts are prescribed; they must not be redefined or altered.

## Document Class Options

### Standard Conference Declaration
```latex
\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
```
- `conference`: Configures 2-column format, specific margins, running heads, and typography according to IEEE Conference specifications.
- `\IEEEoverridecommandlockouts`: Required when using `\thanks{}` in the title for financial sponsorship or grant acknowledgment footnotes. If no funding footnote is needed, this command can be omitted.

### Other Useful IEEEtran Options
- `a4paper` vs default `letterpaper`: Most IEEE conferences specify US Letter (`8.5 x 11 in`), but European conferences may specify `\documentclass[conference,a4paper]{IEEEtran}`. Check venue author guidelines.
- `draftcls`: For review drafts needing double spacing and wide margins (rarely used for final conference papers).

## Title and Metadata Rules

### Title Constraints
```latex
\title{Paper Title Here\thanks{Identify applicable funding agency here. If none, delete this.}}
```
- **CRITICAL**: Do NOT use symbols, special characters, math formulas, footnotes, or acronyms in the paper title.
- **No Sub-titles**: IEEE Xplore does not index or capture subtitles; do not use `\\` to create subtitles.
- **Capitalization**: Title Case according to IEEE standards. If the phrase "that uses" can accurately replace the word "using", capitalize "Using"; if not, keep "using" lower-cased.

### Abstract & Keywords Constraints
```latex
\begin{abstract}
Concise paragraph summarizing background, methodology, quantitative results, and conclusions.
\end{abstract}

\begin{IEEEkeywords}
keyword 1, keyword 2, keyword 3, keyword 4.
\end{IEEEkeywords}
```
- **No Math or Symbols**: Mathematical notation, LaTeX math mode (`$...$`), and symbols are strictly forbidden in both abstract and keywords.
- **No Citations or Footnotes**: Abstracts must be fully self-contained.
- **No Undefined Acronyms**: If an acronym appears in the abstract, define it upon first use in the abstract AND define it again upon first use in the main body text.
- **Keyword Count**: Typically 4 to 6 index terms, comma-separated, ending with a period.

## Author Blocks and Affiliations

IEEEtran provides multiple layout methods for author blocks depending on author count and affiliations.

### Pattern 1: 1 to 3 Authors (Side-by-Side Columns)
```latex
\author{
\IEEEauthorblockN{1\textsuperscript{st} Given Name Surname}
\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
\textit{name of organization (of Aff.)}\\
City, Country \\
email address or ORCID}
\and
\IEEEauthorblockN{2\textsuperscript{nd} Given Name Surname}
\IEEEauthorblockA{\textit{dept. name of organization (of Aff.)} \\
\textit{name of organization (of Aff.)}\\
City, Country \\
email address or ORCID}
}
```

### Pattern 2: 4 to 6 Authors (Two Rows of Side-by-Side)
```latex
\author{
\IEEEauthorblockN{First Author}
\IEEEauthorblockA{\textit{Department} \\ \textit{Institution}\\ City, Country \\ email}
\and
\IEEEauthorblockN{Second Author}
\IEEEauthorblockA{\textit{Department} \\ \textit{Institution}\\ City, Country \\ email}
\and
\IEEEauthorblockN{Third Author}
\IEEEauthorblockA{\textit{Department} \\ \textit{Institution}\\ City, Country \\ email}
\and
\IEEEauthorblockN{Fourth Author}
\IEEEauthorblockA{\textit{Department} \\ \textit{Institution}\\ City, Country \\ email}
}
```

### Pattern 3: Many Authors or Shared Affiliations (Marked Affiliations)
When authors share departments or exceed 4--6 across distinct institutions, use `\IEEEauthorrefmark`:
```latex
\author{
\IEEEauthorblockN{
  First Author\IEEEauthorrefmark{1},
  Second Author\IEEEauthorrefmark{2},
  Third Author\IEEEauthorrefmark{1}, and
  Fourth Author\IEEEauthorrefmark{3}
}
\IEEEauthorblockA{\IEEEauthorrefmark{1}Department of Electrical Engineering, University A, City, Country}
\IEEEauthorblockA{\IEEEauthorrefmark{2}Department of Computer Science, University B, City, Country}
\IEEEauthorblockA{\IEEEauthorrefmark{3}Research & Development Division, Company C, City, Country}
\IEEEauthorblockA{Emails: \IEEEauthorrefmark{1}\{first, third\}@univ-a.edu, \IEEEauthorrefmark{2}second@univ-b.edu, \IEEEauthorrefmark{3}fourth@company-c.com}
}
```

### Mandatory Author Formatting Rules
1. Sequence: Names list from left to right, moving down to the next row.
2. Grouping: Do not group authors strictly by affiliation if it alters the intellectual author order.
3. Succinct Affiliations: Do not duplicate or over-specify departments within the same organization.

## Section Headings Hierarchy

IEEEtran defines clear structural levels:
1. Primary Headings (`\section{...}`): Roman numerals (I, II, III, IV), small caps, centered.
2. Secondary Headings (`\subsection{...}`): Capital letters (A, B, C), italic, flush left.
3. Tertiary Headings (`\subsubsection{...}`): Numbers (1, 2, 3), indented, italic, run-in with text followed by a colon.
4. Component Headings (`\section*{Acknowledgment}`, `\section*{References}`): Unnumbered, centered, small caps.

## Content and Section Strategy

### Mathematical Models
- **Justification & Output Impact**: Include only equations that have direct bearing on model outputs, loss functions, or experimental evaluations. Prune ornamental textbook formulas.
- **Attribution**: When adopting a formula, cite the original source once upon introduction; avoid repeating citations across subsequent steps.

### Discussion and Conclusion (The Four Pillars)
Every IEEE submission should address four vital components across its Discussion and Conclusion:
1. **Key Findings**: Succinct summary of core quantitative achievements with exact metrics.
2. **Broader Implications**: Significance and impact on the overarching scientific or engineering field.
3. **Benefits vs. Shortcomings**: Candid assessment of the system's advantages alongside operational bottlenecks, assumptions, and threats to validity.
4. **Future Research Directions**: Explicit, actionable next steps rather than generic platitudes.
