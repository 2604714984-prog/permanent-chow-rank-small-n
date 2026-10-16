# Standalone perm6 computational supplement (20261016-r2)

From the extracted source ZIP root:

```sh
python -B anc/verify_submission.py
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

Python 3.11+ and its standard library are sufficient. Verification creates
scratch outputs in temporary directories and does not rewrite frozen inputs.
Compilation needs the standard TeX distribution packages listed in main.tex;
there are no external figures, bibliography files, custom fonts or shell commands.

## Exact computational subset, not a changed historical certificate

`original/` contains 7 computational files copied byte for byte from
the public `perm6/` package, plus its complete, unchanged `MANIFEST.sha256`.
`COMPUTATION_INPUTS.sha256` consists of the original manifest lines for
`verify_all.py` and all `.py`, `.json`, `.csv` paths under `computation/`.
The wrapper verifies both the subset selection and every original expected hash.
It executes the original complete computation entry point, not a replacement.

The full historical manifest has 13 entries. Its other 6 entries
are historical manuscripts, rendered documents or explanatory prose, not
required computation inputs. They are deliberately not materialized here:
arXiv ancillary directories must not contain TeX manuscript sources.
They remain available unchanged in the original public package and the
archived `20261016` release. `ORIGIN.json` lists every inclusion and omission.
No missing historical document is reported as an inventoried computation.

The full original package, pinned at the audit starting commit:
https://github.com/2604714984-prog/permanent-chow-rank-small-n/tree/ff27dd3377e341ae89e4fd9017cf3d174f51d7c8/perm6

## Scope of the checks

`verify_prolongation_independent.py` reconstructs the whole cubic coefficient
system over exact rationals and confirms E2^(1)=E3 without importing the
historical verifier. The other programs check the finite premises described
in the manuscript and the exact Glynn expansion. Finite checks do not replace
the written torus-specialization, rank/quotient and filtration arguments.
PASS is a reproducibility statement, not peer review or author approval.

`SOURCE_MANIFEST.sha256` freezes this distinct revised submission. Historical
certificates and release manifests must not be edited to force a PASS.
