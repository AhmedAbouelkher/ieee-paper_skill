# IEEE Figures and Tables Specification

## Column Dimensions and Geometry
IEEE conference papers operate strictly on a two-column grid. Visual assets must match column boundaries:

| float Scope | Width (in) | Width (mm) | Width (picas) | LaTeX Dimension |
|-------------|------------|------------|---------------|-----------------|
| Single Column | 3.50 in | 88.9 mm | 21.0 picas | `\columnwidth` or `\linewidth` |
| Double Column (Full Width) | 7.16 in | 181.9 mm | 43.0 picas | `\textwidth` |
| Column Separation (Gutter) | 0.16 in | 4.1 mm | 1.0 pica | `\columnsep` |

## Positioning Rules
- **Top or Bottom Only**: Place figures and tables at the top (`[t]`) or bottom (`[b]`) of columns. Avoid middle-of-column floats.
- **Float Specifiers**: Use `[htbp]` or `[!t]`.
- **Full-Width Floats**: Use `\begin{figure*}[t]` and `\begin{table*}[t]` to span both columns. Two-column floats always appear at the top of the next page unless placed early.
- **Order of Appearance**: Figures and tables must be cited in the narrative text before or immediately at their appearance.

## Captions and Cross-Referencing Rules

### 1. Table Captions (ABOVE)
Table titles MUST appear **above** the table:
```latex
\begin{table}[htbp]
\caption{System Performance Across Diverse Workloads}
\label{tab:performance}
\begin{center}
\begin{tabular}{|l|c|c|r|}
\hline
\textbf{Model} & \textbf{Latency (ms)} & \textbf{Throughput (req/s)} & \textbf{Accuracy (\%)} \\
\hline
Standard Baseline & 42.5 & 120 & 88.4 \\
Proposed Solution & \textbf{18.2} & \textbf{310} & \textbf{95.7} \\
\hline
\multicolumn{4}{l}{$^{\mathrm{a}}$Evaluated on NVIDIA Jetson AGX Orin 64GB.}
\end{tabular}
\end{center}
\end{table}
```
*Note*: Use superscript letters ($^{\mathrm{a}}$, $^{\mathrm{b}}$) for table footnotes, never numbers or asterisks.

### 2. Figure Captions (BELOW)
Figure captions MUST appear **below** the graphic:
```latex
\begin{figure}[htbp]
\centerline{\includegraphics[width=\columnwidth]{figures/architecture.png}}
\caption{End-to-end pipeline of the distributed streaming edge inference engine.}
\label{fig:architecture}
\end{figure}
```

### 3. Critical Label Placement Rule
`\LaTeX` increments counters during `\caption`. **Never place `\label` before `\caption`**, or the label will reference the enclosing section instead of the figure/table.
- Correct: `\caption{...}\label{fig:example}` or `\caption{...}` followed immediately by `\label{fig:example}`.
- Incorrect: `\label{fig:example}\caption{...}`.

### 4. Text Citation Grammar
- Refer to figures as **`Fig.~\ref{fig:example}`**, even at the beginning of a sentence (do NOT use "Figure 1" or "Figure~\ref{...}").
- Refer to tables as **`Table~\ref{tab:example}`**.

## Visual Design and Typography Standards

### Font and Sizing
- Label Font: Times New Roman or clean sans-serif (Helvetica/Arial), minimum 8 pt at print size.
- Clean Background: Pure white background; avoid drop shadows or decorative gradients.
- Colorblind Accessibility: Use the Okabe-Ito palette (black, orange, sky blue, bluish green, yellow, royal blue, vermilion, reddish purple). Ensure contrast holds in grayscale printing.

### Axis Label Conventions
- Always write the physical quantity and unit: `Magnetization (A/m)` or `Temperature (K)`.
- Never label axes with units alone (e.g., avoid `A/m` or `K`).
- Never use ratios for units: write `Velocity (m/s)`, NOT `Velocity/m/s`.
- Use parentheses `(...)` for units, not brackets unless nested.

## Generating Schematics via `scientific-schematics`

When generating figures for an IEEE conference paper with the AI schematic workflow:

```bash
# Generate 1-column figure (target: 3.5 inches, high-contrast, clean 8pt labels)
python scripts/generate_schematic.py \
  "IEEE conference single-column diagram (width 3.5 in): High-level system architecture showing edge sensor, gateway processor, and cloud aggregation. 8pt sans-serif labels. Horizontal flow left-to-right. White background. Okabe-Ito palette." \
  -o figures/system_arch.png --doc-type conference

# Generate 2-column wide figure (target: 7.16 inches)
python scripts/generate_schematic.py \
  "IEEE conference two-column full-width diagram (width 7.16 in): Detailed pipeline from raw telemetry ingestion through feature extraction, transformer encoder, and multi-task classification heads. White background, 8pt labels." \
  -o figures/full_pipeline.png --doc-type conference
```
