# Computation-free proof of the Chow rank of perm5

Revision: **2026-10-19, final internal mathematical revision**.

The manuscript proves the **ordinary Chow rank** of the generic five-by-five permanent to be 16 over every characteristic-zero field. It does not claim border-rank equality or a general-size formula.

## Read first

- [Complete manuscript](main.tex) and [reading PDF](perm5_chow_rank_16_computation_free.pdf).
- [Internal mathematical audit](AUDIT.md), [Chinese reader guide](README.zh.md), and [handoff](HANDOFF.md).
- [Optional independent checks](verify_optional.py) and [actual exact-test receipt](verification_results.json).

The proof is self-contained: remove the program and its receipt, and all mathematical steps remain in the manuscript. This is internally reviewed, AI-assisted mathematics, not an external referee report or a formal proof-assistant certificate.

## What changed after the first draft

This final text develops the active October 16 short proof, **not** the historical 58-state/terminal-orbit proof. It removes all four former computational endpoints rather than merely labeling their programs optional:

| Former endpoint | Replacement in the written proof |
|---|---|
| Coordinate-symbol scan | A formula counting surviving squarefree triple columns, followed by a factored nonnegative polynomial |
| Four normal-form matrix ranks | Only zero-derivative identities and required actual cubic derivatives; exact ranks for the last two forms are not needed |
| Positive-partition floors | The uniform divisor count `binom(ell,2) + #{alpha_i >= 2}` |
| Finite interval minimizations | One displayed algebraic inequality, leaving only the explicitly treated four-dimensional one-direction case |

The global argument uses actual derivative-image sums, the adjoint catalecticants, and a filtration by factor spans. Its endpoint is

\[
 h_2+\Delta/2\le10N-150.
\]
For `N=15`, nonnegativity forces `h2=Delta=0`. Every ten-dimensional term image would then lie in a permanent/variable-space intersection of dimension at most one, a contradiction. Glynn's sixteen-term formula is proved by sign cancellation in the text.

## Rebuild

Only `main.tex` and an ordinary LaTeX distribution with the listed standard packages are needed:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. The named reading PDF is a copy of that output. No included project file, ancillary data, proof program, or network fetch is required by the source.

Optional checks use Python 3.11 or newer and its standard library:

```sh
python -B verify_optional.py --output verification_results.json
```

The tests include 352 coordinate symbols, 399 exact local quotient examples (159 with a nonzero admissible quadratic line), 252 small-complement kernel identities, the permanent prolongation, explicit normal forms, and Glynn's formula. They also check the global inequalities on the actual sixteen-term decomposition, where `(h2,h3,Delta)=(10,50,0)`. Sampling is a regression check, not a proof over all parameters.

`SOURCE_MANIFEST.sha256` records the mathematical source and companion text/programs. PDF bytes can differ between TeX distributions; the source hash identifies the mathematics. Local and workstation build receipts distinguish the PDF outputs rather than treating those bytes as interchangeable.

## Preservation policy

The released `submissions/20261016-r2/perm5/` files, their manifests, old computational packages, and the `perm3`, `perm4`, `perm6` results are not rewritten by this revision. The previous research-draft commits remain in Git history. No hosted CI, local Codex session, new scheduler, or arXiv upload is part of this delivery.
