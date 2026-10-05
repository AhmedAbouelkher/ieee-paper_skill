# IEEE Editorial and Common Mistakes Checklist

## Pre-Submission Verification Checklist

This checklist codifies the explicit editorial requirements from IEEE Conference Publishing. Every IEEE conference submission should pass these checks prior to camera-ready generation.

### 1. Template Text Removal (Desk-Rejection Hazard)
- [ ] **Zero Template Boilerplate**: IEEE explicitly rejects papers containing leftover template instructional text. Ensure phrases like *"This document is a model and instructions for LaTeX"*, *"Identify applicable funding agency here"*, or *"Please observe the conference page limits"* are completely eradicated.
- [ ] **No Template Sample Figures or Tables**: Replace all placeholder figures (`fig1.png`) and mock tables with genuine experimental data.
- [ ] **Clean Title & Abstract**: Verify no footnotes, subtitle tags, or math notation exist in title or abstract.

### 2. Grammar, Vocabulary, and Diction
- [ ] **"Data" is Plural**:
  - Correct: `The collected telemetry data are evaluated...`
  - Incorrect: `The collected telemetry data is evaluated...`
- [ ] **Precision in Word Choice**:
  - `affect` (verb: to influence) vs. `effect` (noun: result, or verb: to bring about)
  - `complement` (to complete or pair with) vs. `compliment` (praise)
  - `discrete` (distinct, detached) vs. `discreet` (careful, prudent)
  - `principal` (primary, chief) vs. `principle` (fundamental doctrine or law)
  - `imply` (speaker suggests) vs. `infer` (listener concludes)
- [ ] **Avoid "Essentially"**: Do not use "essentially" to mean "approximately" or "effectively". State exact tolerances or values.
- [ ] **Graph Terminology**: A small graph inside a larger coordinate plot is an **"inset"**, not an "insert".
- [ ] **Latin Abbreviations**:
  - `et al.` (no period after `et`, followed by period after `al.`)
  - `i.e.,` (means "that is", always followed by a comma in American English)
  - `e.g.,` (means "for example", always followed by a comma in American English)
- [ ] **Prefix "non"**: Join without a hyphen in standard technical terms:
  - Correct: `nonlinear`, `nonvolatile`, `nonnegative`, `nonconvex`
  - Incorrect: `non-linear`, `non-volatile`

### 3. Units and Scientific Constants
- [ ] **No Mixed Unit Systems**: Use SI (MKS) as primary units throughout. Do not mix SI and CGS in balancing equations (e.g., mixing amperes with oersteds).
- [ ] **Leading Zeroes**: Always place a zero before a decimal point:
  - Correct: `0.25 ms`, `0.05`
  - Incorrect: `.25 ms`, `.05`
- [ ] **Volume Units**: Use `\text{cm}^3$`, never `cc`.
- [ ] **No Mixed Unit Abbreviations**:
  - Correct: `\text{Wb/m}^2$` or `webers per square meter`
  - Incorrect: `webers/m^2`
- [ ] **Units in Prose**: Spell out units in body text when not following numbers:
  - Correct: `separated by a few henries`, `a current of 5~A`
  - Incorrect: `separated by a few H`
- [ ] **Vacuum Permeability**: $\mu_0$ has subscript zero ($0$), not letter 'o': write `\mu_0`.

### 4. Punctuation and Typography
- [ ] **Equation Punctuation**: Every displayed equation must end with a comma or period matching sentence grammar.
- [ ] **Quotation Punctuation (American English)**: Commas and periods go inside quotation marks only when quoting titles or full thoughts; otherwise outside.
- [ ] **Parentheses Punctuation**: Sentence ends outside closing parenthesis `(like this).` unless the whole sentence is parenthetical `(Like this.)`.
- [ ] **Minus Signs**: Use math minus `$-$` rather than text hyphen `-` for negative numbers: `$-15^\circ\text{C}$`.
- [ ] **Spelling of Acknowledgment**: Use American spelling **"Acknowledgment"** (without an 'e' after the 'g'). Avoid stilted phrasing: write `A. B. thanks...` rather than `One of us (A. B.) thanks...`.

### 5. Floats, Equations, and Cross-References
- [ ] Table captions are ABOVE tables.
- [ ] Figure captions are BELOW figures.
- [ ] `\label{...}` is placed AFTER or inside `\caption{...}`, never before.
- [ ] **Strict Equation Impact**: Every displayed equation directly impacts outputs, decision thresholds, or evaluation metrics. No decorative formulas.
- [ ] **Zero Orphan Equations**: Every equation is labeled, referenced with `\eqref{...}`, and explained in prose.
- [ ] **Disciplined Equation Attribution**: Adapted equations cite foundational sources once upon introduction; no citations inside equation displays and no redundant citation repetition.
- [ ] In-text references use `Fig.~\ref{...}`, `Table~\ref{...}`, and `\eqref{...}`.
- [ ] In-text citations use `[1]` or `\cite{...}`, never `Ref. [1]`.

### 6. Discussion and Conclusion Completeness
- [ ] **Key Findings**: Clear summary of quantitative results with specific performance metrics.
- [ ] **Field Implications**: Articulation of broader significance and consequences for the research domain.
- [ ] **Balanced Assessment**: Explicit analysis of both methodology benefits and shortcomings/limitations.
- [ ] **Future Directions**: Concrete, actionable areas identified for future investigation.
