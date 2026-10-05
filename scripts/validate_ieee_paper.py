#!/usr/bin/env python3
"""
validate_ieee_paper.py - Deterministic static linter for IEEE Conference LaTeX papers.

Checks compliance with official IEEEtran (06/28/2024) conference standards:
- Purging of IEEE template instructional boilerplate
- Correct float caption positioning (table captions above, figure captions below)
- Label order (ensuring \\label is not placed before \\caption)
- Prohibited math/citations in title and abstract
- Prohibition of \\begin{eqnarray}
- Orphan equation detection (unreferenced math or missing labels) and citation inside math
- IEEE citation and referencing grammar (Fig. vs Figure, [X] vs Ref. [X], \\eqref vs Eq.)
- Editorial pitfalls (plurality of data, leading zeroes, acknowledgment spelling)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Phrases from official IEEE-conference-template-062824.tex that must be removed
TEMPLATE_RESIDUE_PATTERNS = [
    r"This document is a model and instructions for",
    r"component,\s*formatting,\s*style,\s*styling,\s*insert",
    r"Identify applicable funding agency here",
    r"Before you begin to format your paper",
    r"Keep your text and graphic files separate until",
    r"The class file is designed for, but not limited to, six authors",
    r"Identify the Headings",
    r"IEEE conference templates contain guidance text",
    r"Please ensure that all template text is removed",
    r"Failure to remove the template text from your paper",
    r"Please observe the conference page limits",
    r"All margins,\s*column widths,\s*line spaces",
    r"An excellent style manual for science writers is",
    r"Example of a figure caption",
    r"Sample of a Table footnote",
    r"1\textsuperscript{st} Given Name Surname",
]

class Issue:
    def __init__(self, severity: str, line_no: int, code: str, message: str, suggestion: str = ""):
        self.severity = severity  # "ERROR" or "WARNING"
        self.line_no = line_no
        self.code = code
        self.message = message
        self.suggestion = suggestion

    def to_dict(self):
        return {
            "severity": self.severity,
            "line": self.line_no,
            "code": self.code,
            "message": self.message,
            "suggestion": self.suggestion,
        }

def find_line_number(text: str, match_index: int) -> int:
    return text[:match_index].count("\n") + 1

def strip_latex_comments(content: str) -> str:
    # Keep newlines intact to preserve accurate line counts
    lines = content.splitlines(keepends=True)
    stripped = []
    for line in lines:
        # Match % that is not escaped by backslash
        idx = 0
        in_comment = False
        while idx < len(line):
            if line[idx] == "%" and (idx == 0 or line[idx - 1] != "\\"):
                stripped.append(line[:idx] + "\n")
                in_comment = True
                break
            idx += 1
        if not in_comment:
            stripped.append(line)
    return "".join(stripped)

def check_template_residue(raw_content: str, issues: list):
    for pattern in TEMPLATE_RESIDUE_PATTERNS:
        for match in re.finditer(pattern, raw_content, re.IGNORECASE):
            line = find_line_number(raw_content, match.start())
            issues.append(Issue(
                severity="ERROR",
                line_no=line,
                code="IEEE-TPL-001",
                message=f"Residual IEEE template text detected: '{match.group()}'",
                suggestion="Purge all template instructions and boilerplate prior to submission."
            ))

def check_title_and_abstract(content: str, issues: list):
    # Check title
    title_match = re.search(r"\\title(?:\[[^\]]*\])?\{([^}]+)\}", content, re.DOTALL)
    if title_match:
        title_text = title_match.group(1)
        line = find_line_number(content, title_match.start())
        if "$" in title_text or r"\(" in title_text or r"\[" in title_text:
            issues.append(Issue(
                severity="ERROR",
                line_no=line,
                code="IEEE-TIT-001",
                message="Math notation detected in \\title.",
                suggestion="IEEE prohibits math symbols or LaTeX math mode in paper titles."
            ))
        if r"\\" in title_text:
            issues.append(Issue(
                severity="WARNING",
                line_no=line,
                code="IEEE-TIT-002",
                message="Line break (\\\\) in \\title suggests a sub-title.",
                suggestion="IEEE Xplore does not capture subtitles. Combine into a single concise title."
            ))

    # Check abstract
    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1)
        line = find_line_number(content, abstract_match.start())
        if "$" in abstract_text or r"\(" in abstract_text:
            issues.append(Issue(
                severity="ERROR",
                line_no=line,
                code="IEEE-ABS-001",
                message="Math mode notation detected inside abstract environment.",
                suggestion="IEEE forbids mathematical formulas and special symbols in the abstract."
            ))
        if r"\cite" in abstract_text:
            issues.append(Issue(
                severity="ERROR",
                line_no=line,
                code="IEEE-ABS-002",
                message="Citation \\cite detected inside abstract.",
                suggestion="Abstracts must be self-contained; eliminate citations."
            ))
        if r"\footnote" in abstract_text:
            issues.append(Issue(
                severity="ERROR",
                line_no=line,
                code="IEEE-ABS-003",
                message="Footnote \\footnote detected inside abstract.",
                suggestion="Footnotes are strictly forbidden inside the abstract."
            ))

def check_environments_and_math(content: str, issues: list):
    # Check eqnarray
    for match in re.finditer(r"\\begin\{(eqnarray\*?)\}", content):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="ERROR",
            line_no=line,
            code="IEEE-MTH-001",
            message=f"Deprecated \\begin{{{match.group(1)}}} environment used.",
            suggestion="Use \\begin{align} (from amsmath) or \\begin{IEEEeqnarray} instead."
        ))

    # Check numbered math environments for orphan equations and proper cross-referencing
    math_env_pat = re.compile(
        r"\\begin\{(equation|align|IEEEeqnarray)\*?\}(.*?)\\end\{\1\*?\}", re.DOTALL
    )
    for match in math_env_pat.finditer(content):
        env_full = match.group(0)
        env_type, body = match.group(1), match.group(2)
        line = find_line_number(content, match.start())

        # Check for citation placed directly inside math display
        if r"\cite" in body:
            issues.append(Issue(
                severity="WARNING",
                line_no=line,
                code="IEEE-REF-004",
                message="Citation \\cite found inside displayed equation.",
                suggestion="Attribute formulas in introductory prose once; avoid placing \\cite directly in equation displays."
            ))

        # Check for label and cross-referencing (orphan equation check)
        is_starred = env_full.startswith(r"\begin{" + env_type + "*")
        labels = re.findall(r"\\label\{([^}]+)\}", body)
        if not labels and not is_starred:
            issues.append(Issue(
                severity="WARNING",
                line_no=line,
                code="IEEE-MTH-003",
                message=f"Numbered \\begin{{{env_type}}} lacks a \\label.",
                suggestion="Every numbered equation must have a strict reason to exist, be labeled, and impact outputs. If not impactful, eliminate it."
            ))
        for lbl in labels:
            ref_pat = re.compile(r"\\(?:eq)?ref\{" + re.escape(lbl) + r"\}")
            if not ref_pat.search(content):
                issues.append(Issue(
                    severity="WARNING",
                    line_no=line,
                    code="IEEE-MTH-002",
                    message=f"Orphan equation detected: '\\label{{{lbl}}}' is never referenced in text.",
                    suggestion="Verify that this equation directly impacts paper outputs and reference it with \\eqref{...}, or eliminate it."
                ))

def check_floats_and_captions(content: str, issues: list):
    # Check table environments: caption must be BEFORE tabular
    for table_match in re.finditer(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", content, re.DOTALL):
        block = table_match.group(1)
        line = find_line_number(content, table_match.start())
        cap_pos = block.find(r"\caption")
        tab_pos = block.find(r"\begin{tabular")
        if tab_pos != -1:
            if cap_pos == -1:
                issues.append(Issue(
                    severity="WARNING",
                    line_no=line,
                    code="IEEE-FLT-001",
                    message="Table float has no \\caption.",
                    suggestion="Add a table \\caption above the tabular environment."
                ))
            elif cap_pos > tab_pos:
                issues.append(Issue(
                    severity="ERROR",
                    line_no=line + block[:cap_pos].count("\n"),
                    code="IEEE-FLT-002",
                    message="Table \\caption is placed BELOW \\begin{tabular}.",
                    suggestion="In IEEE format, table captions MUST appear ABOVE the table."
                ))

    # Check figure environments: caption must be AFTER includegraphics
    for fig_match in re.finditer(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", content, re.DOTALL):
        block = fig_match.group(1)
        line = find_line_number(content, fig_match.start())
        cap_pos = block.find(r"\caption")
        img_pos = block.find(r"\includegraphics")
        if img_pos != -1:
            if cap_pos == -1:
                issues.append(Issue(
                    severity="WARNING",
                    line_no=line,
                    code="IEEE-FLT-003",
                    message="Figure float has no \\caption.",
                    suggestion="Add a figure \\caption below the graphic."
                ))
            elif cap_pos < img_pos:
                issues.append(Issue(
                    severity="ERROR",
                    line_no=line + block[:cap_pos].count("\n"),
                    code="IEEE-FLT-004",
                    message="Figure \\caption is placed ABOVE \\includegraphics.",
                    suggestion="In IEEE format, figure captions MUST appear BELOW the graphic."
                ))

    # Check label placed before caption (counter increment error)
    label_before_cap = re.compile(r"(\\label\{[^}]+\}\s*\\caption)", re.DOTALL)
    for match in label_before_cap.finditer(content):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="ERROR",
            line_no=line,
            code="IEEE-FLT-005",
            message="\\label command placed before \\caption command.",
            suggestion="Always place \\label inside or AFTER \\caption to avoid referencing incorrect counters."
        ))

def check_referencing_grammar(content: str, issues: list):
    # Check "Figure \ref" or "Figure~\ref" -> should be "Fig.~\ref"
    for match in re.finditer(r"\bFigure~?\\ref\{", content):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-REF-001",
            message="Use 'Fig.~\\ref{...}' instead of 'Figure \\ref{...}'.",
            suggestion="IEEE standard requires 'Fig.~\\ref{...}' even at sentence beginnings."
        ))

    # Check "Ref. \cite" or "Ref.~\cite"
    for match in re.finditer(r"\b(?:Ref\.|reference)~?\\cite\{", content, re.IGNORECASE):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-REF-002",
            message="Redundant 'Ref.' or 'reference' before \\cite.",
            suggestion="Refer simply to '[1]' or '\\cite{...}' without 'Ref.' unless beginning a sentence."
        ))

    # Check "Eq. \eqref" or "equation \eqref"
    for match in re.finditer(r"\b(?:Eq\.|equation)~?\\eqref\{", content, re.IGNORECASE):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-REF-003",
            message="Redundant 'Eq.' or 'equation' before \\eqref.",
            suggestion="Use simply '\\eqref{...}' (e.g. 'as shown in (1)') unless at sentence start."
        ))

def check_editorial_pitfalls(content: str, issues: list):
    # Check misspelled Acknowledgment
    for match in re.finditer(r"\\section\*?\{Acknowledgement\}", content, re.IGNORECASE):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-EDT-001",
            message="British spelling 'Acknowledgement' detected.",
            suggestion="Use American IEEE spelling 'Acknowledgment' (without the 'e' after 'g')."
        ))

    # Check "the data is / was"
    for match in re.finditer(r"\bthe\s+data\s+(?:is|was)\b", content, re.IGNORECASE):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-EDT-002",
            message="Singular verb applied to 'data' ('data is/was').",
            suggestion="In IEEE scientific writing, 'data' is strictly plural: use 'data are' or 'data were'."
        ))

    # Check decimal without leading zero in text (e.g., " .25 " or "=.25")
    for match in re.finditer(r"(?:[=\s(,])(\.\d+)\b", content):
        line = find_line_number(content, match.start())
        issues.append(Issue(
            severity="WARNING",
            line_no=line,
            code="IEEE-EDT-003",
            message=f"Missing leading zero in decimal: '{match.group(1)}'.",
            suggestion=f"Prepend zero to decimal: '0{match.group(1)}'."
        ))

def validate_latex_file(file_path: Path) -> list:
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)

    raw_text = file_path.read_text(encoding="utf-8", errors="replace")
    clean_text = strip_latex_comments(raw_text)

    issues = []
    # 1. Template residue check (on raw text to catch comments if needed, but primarily text)
    check_template_residue(raw_text, issues)
    # 2. Structural & grammar checks on clean LaTeX
    check_title_and_abstract(clean_text, issues)
    check_environments_and_math(clean_text, issues)
    check_floats_and_captions(clean_text, issues)
    check_referencing_grammar(clean_text, issues)
    check_editorial_pitfalls(clean_text, issues)

    issues.sort(key=lambda x: (x.line_no, x.severity != "ERROR"))
    return issues

def main():
    parser = argparse.ArgumentParser(
        description="Validate LaTeX paper compliance with IEEE Conference standards."
    )
    parser.add_argument("file", type=Path, help="Path to .tex paper to validate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    issues = validate_latex_file(args.file)
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARNING"]

    if args.json:
        result = {
            "file": str(args.file),
            "errors_count": len(errors),
            "warnings_count": len(warnings),
            "passed": len(errors) == 0 and (not args.strict or len(warnings) == 0),
            "issues": [i.to_dict() for i in issues],
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n--- IEEE Conference Validation: {args.file} ---")
        if not issues:
            print("Status: PASSED (Clean, no IEEE specification issues found)\n")
        else:
            for issue in issues:
                tag = f"[{issue.severity}]"
                print(f"{tag:9} Line {issue.line_no:4d} | ({issue.code}) {issue.message}")
                if issue.suggestion:
                    print(f"          Fix: {issue.suggestion}")
            print(f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors or (args.strict and warnings):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
