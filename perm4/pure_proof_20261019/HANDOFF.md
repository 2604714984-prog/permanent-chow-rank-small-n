# Handoff: Computation-Free `perm_4` Proof

Updated: October 19, 2026.

## Current reading order

1. [`main.pdf`](main.pdf) — seven-page reading copy.
2. [`main.tex`](main.tex) — complete standalone LaTeX manuscript used to build the PDF.
3. [`README.md`](README.md) — theorem, reproduction instructions, and scope.
4. [`AUDIT.md`](AUDIT.md) — internal dependency and edge-case review.
5. [`verify_supplementary.py`](verify_supplementary.py) and [`supplementary_results.json`](supplementary_results.json) — optional regression checks and their recorded output.

## Result and proof structure

The manuscript proves the ordinary Chow rank of the generic four-by-four permanent is eight over fields of characteristic zero.

The main new ingredient is the missing-derivative lemma at `z = x_00`, proved by excluding forbidden cubic monomials and recovering the missing matching-coefficient equality along a three-swap path. Explicit row-column scaling with weights 0, 1, and 2 then transfers the quotient-kernel rank statement to every nonzero vector by rank specialization. The proof combines this with the prolongation ranks 560 and 92, the low-rank quadratic classification, and the final contradiction `559 > 552`.

## Reproduction

From the repository root:

```sh
python -B perm4/pure_proof_20261019/verify_supplementary.py
```

To rebuild the PDF, run the following twice from this directory:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The supplementary program is a regression check only; its output is not a premise of the proof.

## Boundaries

- Ordinary Chow rank only; no border-rank claim.
- No general-n Chow-rank equality, and no claim about `perm_5`, `perm_6`, or `perm_7` from this manuscript.
- Internal review is not external peer review or formal proof-assistant certification.
- The original computation-assisted manuscript and certificates remain preserved in `perm4/paper/` and `perm4/certificates/`.
- No hosted CI run is required for this documentation/source synchronization; arXiv remains paused.
