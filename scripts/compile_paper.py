#!/usr/bin/env python3
"""
compile_paper.py - Deterministic compiler and diagnostic runner for IEEE LaTeX papers.

Orchestrates full compilation pipeline:
pdflatex -> bibtex -> pdflatex -> pdflatex
Parses log file for overfull boxes, undefined citations/references, and page count.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEMP_EXTENSIONS = [".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".synctex.gz"]

def check_latex_binaries():
    has_pdflatex = shutil.which("pdflatex") is not None
    has_bibtex = shutil.which("bibtex") is not None
    return has_pdflatex, has_bibtex

def run_cmd(cmd: list, cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
        return proc.returncode, proc.stdout
    except Exception as e:
        return -1, str(e)

def parse_latex_log(log_path: Path) -> dict:
    if not log_path.exists():
        return {"overfull_boxes": [], "undefined_citations": [], "undefined_references": [], "pages": 0}

    log_content = log_path.read_text(encoding="utf-8", errors="replace")

    overfull_boxes = []
    for match in re.finditer(r"Overfull \\hbox \(([0-9.]+pt too wide\) in paragraph at lines ([0-9]+--[0-9]+|[0-9]+))", log_content):
        overfull_boxes.append({
            "type": "hbox",
            "detail": match.group(1),
            "line": match.group(2)
        })

    for match in re.finditer(r"Overfull \\vbox \(([0-9.]+pt too high\) has occurred while \\output is active)", log_content):
        overfull_boxes.append({
            "type": "vbox",
            "detail": match.group(1),
            "line": "output"
        })

    undefined_citations = []
    for match in re.finditer(r"LaTeX Warning: Citation [`']([^']+)['`] on page [0-9]+ undefined", log_content):
        undefined_citations.append(match.group(1))

    undefined_references = []
    for match in re.finditer(r"LaTeX Warning: Reference [`']([^']+)['`] on page [0-9]+ undefined", log_content):
        undefined_references.append(match.group(1))

    # Determine page count
    pages = 0
    page_match = re.search(r"Output written on .*? \((\d+) pages?,", log_content)
    if page_match:
        pages = int(page_match.group(1))

    return {
        "overfull_boxes": overfull_boxes,
        "undefined_citations": list(set(undefined_citations)),
        "undefined_references": list(set(undefined_references)),
        "pages": pages
    }

def clean_artifacts(tex_path: Path):
    stem = tex_path.stem
    parent = tex_path.parent
    for ext in TEMP_EXTENSIONS:
        f = parent / f"{stem}{ext}"
        if f.exists():
            f.unlink()

def main():
    parser = argparse.ArgumentParser(description="Compile and diagnose an IEEE LaTeX conference paper.")
    parser.add_argument("tex_file", type=Path, help="Path to main .tex paper file")
    parser.add_argument("--clean", action="store_true", help="Remove intermediate artifacts after compilation")
    parser.add_argument("--dry-run", action="store_true", help="Verify toolchain without executing compilation")
    parser.add_argument("--json", action="store_true", help="Emit JSON diagnostic output")
    args = parser.parse_args()

    tex_file = args.tex_file.resolve()
    if not tex_file.exists():
        print(f"Error: {tex_file} not found.", file=sys.stderr)
        sys.exit(2)

    has_pdflatex, has_bibtex = check_latex_binaries()
    if not has_pdflatex:
        err = "Error: 'pdflatex' executable not found on PATH. Install TeX Live or MacTeX."
        if args.json:
            print(json.dumps({"success": False, "error": err}))
        else:
            print(err, file=sys.stderr)
        sys.exit(3)

    if args.dry_run:
        msg = f"Ready to compile {tex_file.name} using pdflatex (bibtex: {'available' if has_bibtex else 'missing'})."
        if args.json:
            print(json.dumps({"success": True, "dry_run": True, "message": msg}))
        else:
            print(msg)
        sys.exit(0)

    work_dir = tex_file.parent
    stem = tex_file.stem
    pdf_path = work_dir / f"{stem}.pdf"
    log_path = work_dir / f"{stem}.log"

    # Step 1: pdflatex pass 1
    rc, out = run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file.name], cwd=work_dir)
    compile_success = (rc == 0 or pdf_path.exists())

    # Step 2: bibtex (if bibtex exists and aux mentions bibdata)
    aux_path = work_dir / f"{stem}.aux"
    if has_bibtex and aux_path.exists():
        aux_text = aux_path.read_text(encoding="utf-8", errors="replace")
        if r"\bibdata" in aux_text:
            run_cmd(["bibtex", stem], cwd=work_dir)

    # Step 3 & 4: pdflatex resolve passes
    run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file.name], cwd=work_dir)
    rc_final, out_final = run_cmd(["pdflatex", "-interaction=nonstopmode", tex_file.name], cwd=work_dir)

    diagnostics = parse_latex_log(log_path)
    success = pdf_path.exists() and len(diagnostics["undefined_references"]) == 0

    if args.clean:
        clean_artifacts(tex_file)

    if args.json:
        result = {
            "success": success,
            "pdf_generated": pdf_path.exists(),
            "pdf_path": str(pdf_path) if pdf_path.exists() else None,
            "pages": diagnostics["pages"],
            "overfull_boxes": diagnostics["overfull_boxes"],
            "undefined_citations": diagnostics["undefined_citations"],
            "undefined_references": diagnostics["undefined_references"],
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\n--- IEEE LaTeX Compilation Report: {tex_file.name} ---")
        if pdf_path.exists():
            print(f"Status: PDF GENERATED -> {pdf_path}")
            print(f"Total Pages: {diagnostics['pages']}")
        else:
            print("Status: COMPILATION FAILED")

        if diagnostics["overfull_boxes"]:
            print(f"\n[Warning] Overfull Boxes Detected ({len(diagnostics['overfull_boxes'])}):")
            for box in diagnostics["overfull_boxes"][:5]:
                print(f"  - {box['type'].upper()} {box['detail']} at lines {box['line']}")
            if len(diagnostics["overfull_boxes"]) > 5:
                print(f"  ... and {len(diagnostics['overfull_boxes']) - 5} more.")

        if diagnostics["undefined_citations"]:
            print(f"\n[Warning] Undefined Citations ({len(diagnostics['undefined_citations'])}):")
            for cit in diagnostics["undefined_citations"]:
                print(f"  - {cit}")

        if diagnostics["undefined_references"]:
            print(f"\n[Warning] Undefined References ({len(diagnostics['undefined_references'])}):")
            for ref in diagnostics["undefined_references"]:
                print(f"  - {ref}")

        print("\nDone.")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
