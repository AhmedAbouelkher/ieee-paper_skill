# IEEE Mathematical Typesetting Specification

## Equation Environments

### Strict Equation Justification Threshold
Every displayed equation in an IEEE conference paper must strictly justify its presence:
- **Direct Output Impact**: An equation must directly govern an output, decision threshold, optimization loss, or core evaluation metric. Ornamental or textbook background equations that do not alter the paper's final results must be eliminated or summarized in-text.
- **Explicit In-Text Linkage**: Explain in prose exactly why the formula matters to downstream findings and how its variables affect performance.
- **Zero Orphan Equations**: Every numbered equation must be introduced with context, have all symbols defined immediately, and be actively cited using `\eqref{...}`. Unreferenced formulas are flagged for elimination.

### Equation Attribution (Citing Sources Non-Repeatedly)
- **Attribute at Introduction**: When adopting or modifying a formula from literature, cite the foundational source once at the point of introduction (e.g., "adapted from [3]").
- **Avoid Citation Spam**: Do not repeat the same citation across intermediate derivation steps, sub-equations, or parameter definitions derived from that same source.
- **Original Contributions**: Do not attach external citations to original equations derived in this paper unless directly utilizing an external lemma or theorem.

### Preferred Environments
Use standard AMS-LaTeX or IEEEtran environments:
- Single-line: `\begin{equation} ... \end{equation}`
- Multi-line aligned: `\begin{align} ... \end{align}` or `\begin{IEEEeqnarray}{rCl}`

```latex
\begin{equation}
J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right)^2 + \frac{\lambda}{2m} \sum_{j=1}^{n} \theta_j^2,
\label{eq:cost_function}
\end{equation}
```

### FORBIDDEN: `eqnarray`
**Never use `\begin{eqnarray}`.** The `eqnarray` environment generates inconsistent, overly wide horizontal spacing around relation symbols ($=$, $\le$, etc.) that violates IEEE typographic standards. Use `align` from `amsmath` or `IEEEeqnarray` instead.

### Multi-line IEEEeqnarray Example
```latex
\begin{IEEEeqnarray}{rCl}
\mathcal{L}_{\mathrm{total}} & = & \mathcal{L}_{\mathrm{task}} + \alpha \mathcal{L}_{\mathrm{reg}} \nonumber \\
& & +\, \beta \sum_{l=1}^{L} \mathbb{D}_{\mathrm{KL}}(q_l \,\|\, p_l).
\label{eq:multiline_loss}
\end{IEEEeqnarray}
```

## Equation Numbering and Referencing

### Grammar and Punctuation
- Equations are grammatically part of the surrounding sentence. Always punctuate them with commas or periods:
  ```latex
  The discrete Fourier transform is given by
  \begin{equation}
  X[k] = \sum_{n=0}^{N-1} x[n] e^{-j 2\pi k n / N},
  \label{eq:dft}
  \end{equation}
  where $k = 0, \ldots, N-1$.
  ```

### Cross-Referencing Syntax
- Use **`\eqref{eq:label}`**, which automatically encloses the number in parentheses: `(1)`.
- **In-text syntax**: Refer simply to the number:
  - Correct: `as defined in \eqref{eq:dft}`
  - Incorrect: `as defined in Eq.~\eqref{eq:dft}`
  - Incorrect: `as defined in equation \eqref{eq:dft}`
- **Sentence-initial exception**: Only when beginning a sentence, spell out:
  - Correct: `Equation \eqref{eq:dft} defines the frequency transformation.`

### `subequations` Caveat
Be aware that `\begin{subequations}` increments the main equation counter even if individual sub-equations suppress display numbers. Avoid skipping numbers unintentionally.

## Symbol and Variable Typography

| Element | Typeface / Style | Example | LaTeX Code |
|---------|------------------|---------|------------|
| Roman Variables & Quantities | Italic Roman | $x$, $y$, $V$, $t$ | `$x, y, V, t$` |
| Roman Operators & Functions | Upright Roman | $\sin$, $\cos$, $\exp$, $\ln$ | `\sin, \cos, \exp, \ln` |
| Descriptive Subscripts | Upright Roman | $V_{\mathrm{in}}$, $T_{\mathrm{max}}$ | `$V_{\mathrm{in}}, T_{\mathrm{max}}$` |
| Variable Subscripts | Italic Roman | $x_i$, $a_k$ | `$x_i, a_k$` |
| Physical Constants | Standard constants | $\mu_0$, $\varepsilon_0$, $c$ | `\mu_0, \varepsilon_0, c` |
| Minus Sign | Math minus (en-dash) | $-5$, $a - b$ | `$-5$, $a - b$` (not hyphen `-`) |

### Common Traps
- **Vacuum Permeability**: $\mu_0$ has subscript zero ($0$), not lowercase letter `$o$`. Write `\mu_0`, not `\mu_o`.
- **Fractions in text**: Use the solidus ($/$) or $\exp(\cdot)$ for inline math rather than `\frac{}{}` to preserve uniform line spacing: `$a/b$` and `$\exp(-t/\tau)$`.
- **Vectors & Matrices**: Use bold italic for vectors/matrices ($\boldsymbol{x}$ or $\mathbf{x}$) consistently as defined by the domain.
