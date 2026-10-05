# IEEE References and Citations Specification

## In-Text Citation Syntax

IEEE uses consecutive bracketed numbers for citations:
```latex
\usepackage{cite}
```

### Grammar and Placement
- Number citations consecutively in the order they appear in text: `\cite{b1}` yields `[1]`.
- **Punctuation follows brackets**:
  - Correct: `Recent benchmarks confirmed these findings [1], [2].`
  - Incorrect: `Recent benchmarks confirmed these findings. [1]`
- **Multiple citations**: Use commas inside `\cite{b1, b2, b3}`. With `\usepackage{cite}`, this compresses automatically to `[1]--[3]`.
- **Grammatical in-text citation**: Treat the bracketed number as the noun phrase:
  - Correct: `as demonstrated in [3]`
  - Incorrect: `as demonstrated in Ref. [3]`
  - Incorrect: `as demonstrated in reference [3]`
- **Sentence-initial exception**:
  - Correct: `Reference [3] introduced the sparse matrix factorization technique.`

### Attributing Mathematical Formulations
- **Cite at First Occurrence**: When introducing a theoretical model or adapted equation from prior work, cite the foundational source once in the introducing prose (e.g., `Following the formulation in [3], the objective function is defined as...`).
- **No Repeated Citations**: Do not repeatedly attach the same `\cite{...}` tag across consecutive equation steps, sub-equations, or immediate parameter definitions.
- **Novel Formulations**: Equations newly derived as contributions of this paper should not cite external works unless directly invoking a specific external lemma or theorem.

## Bibliography Formatting Rules

### Author Listing (The 6-Author Rule)
- **Fewer than 6 authors**: List ALL authors' names with initials and surname:
  `G. Eason, B. Noble, and I. N. Sneddon`
- **6 or more authors**: You may list the first author followed by *et al.*:
  `A. B. Researcher \textit{et al.}`
- Author name order: Given name initials followed by surname (e.g., `J. K. Author`, not `Author, J. K.`).

### Title Capitalization Rules
- **Journal Articles & Conference Papers**: Capitalize ONLY the first word of the title, plus proper nouns, acronyms, and chemical element symbols:
  - Correct: `Auto-encoding variational Bayes`
  - Correct: `Design of CMOS operational amplifiers with low power consumption`
  - Incorrect: `Design Of CMOS Operational Amplifiers With Low Power Consumption`
- **Books & Proceedings Series**: Use Title Case (capitalize all major words).
- **Journal Names**: Use standard IEEE abbreviations:
  - `IEEE Trans. Neural Netw. Learn. Syst.`
  - `IEEE Trans. Pattern Anal. Mach. Intell.`
  - `Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM)`

### Special Statuses
- Papers submitted but not yet published: Mark as `, unpublished.`
- Papers accepted for publication: Mark as `, in press.`
- Translated papers: Give English publication citation first, followed by original foreign-language citation in brackets.

## Standard IEEE BibTeX Entry Templates

```bibtex
@article{sample_article,
  author    = {A. B. Author and C. D. Researcher},
  title     = {Low-latency edge caching for interactive augmented reality},
  journal   = {IEEE Trans. Mobile Comput.},
  volume    = {21},
  number    = {4},
  pages     = {1340--1352},
  month     = {Apr.},
  year      = {2022},
  doi       = {10.1109/TMC.2021.1234567}
}

@inproceedings{sample_conf,
  author    = {E. F. Engineer and G. H. Scientist},
  title     = {Zero-shot classification in streaming graphs},
  booktitle = {Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)},
  address   = {Seattle, WA, USA},
  month     = {Jun.},
  year      = {2023},
  pages     = {4501--4510},
  doi       = {10.1109/CVPR.2023.00450}
}

@book{sample_book,
  author    = {J. Clerk Maxwell},
  title     = {A Treatise on Electricity and Magnetism},
  edition   = {3rd},
  volume    = {2},
  publisher = {Oxford: Clarendon},
  address   = {Oxford, UK},
  year      = {1892},
  pages     = {68--73}
}

@misc{sample_online,
  author       = {D. P. Kingma and M. Welling},
  title        = {Auto-encoding variational {Bayes}},
  year         = {2013},
  howpublished = {arXiv:1312.6114},
  note         = {[Online]. Available: https://arxiv.org/abs/1312.6114}
}
```

## Integrating with `paper-lookup` and `research-lookup`
When populating references from academic discovery skills:
1. Ensure DOIs are preserved and formatted as `10.xxxx/...`.
2. Normalize journal names to official IEEE abbreviations.
3. Convert all article and paper titles into sentence case (preserving curly braces around proper nouns in BibTeX: `{Bayes}`, `{CMOS}`, `{IEEE}`).
4. Verify author lists contain all authors when count < 6.
