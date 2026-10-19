# Computation-Free Proof of the Chow Rank of the Four-by-Four Permanent

**Revision date:** October 19, 2026  
**Scope:** Ordinary Chow rank over fields of characteristic zero.

## Result

This revision proves
\[
\operatorname{ChowRank}(\operatorname{perm}_4)=8
\]
without using matrix-rank computations, finite enumeration, or computer-generated certificates as premises.

The original lower-bound strategy is retained. The computational dependencies are replaced by:
1. A direct classification of the cubic prolongation of the permanent's quadratic derivative space, giving flattening rank 560.
2. A direct classification of the prolongation associated with one Chow term, giving the rank bound 92.
3. A missing-derivative lemma at the coordinate z = x_00, followed by explicit row-column scaling and rank specialization proving the uniform quotient-kernel rank 99.
4. A low-rank quadratic classification and an extension argument yielding the lower bound 559, contradicting the upper bound 552 for six Chow terms.

The upper bound is verified directly from Glynn's eight-term identity.

## Files

- `main.tex` — complete standalone mathematical manuscript.
- `AUDIT.md` — internal dependency and edge-case review.
- `verify_supplementary.py` — optional exact regression checks.
- `supplementary_results.json` — frozen output from those optional checks.
- `HANDOFF.md` — status, scope and reproduction instructions.

## Reproduction

Run from the repository root:

```sh
python -B perm4/pure_proof_20261019/verify_supplementary.py
```

Compile the manuscript twice with shell escape disabled:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The supplementary script is a regression check only. Its outputs are not premises of the written proof.

## Status and limitations

This is an AI-assisted research revision that has received an internal review. It is not external peer review or formal proof-assistant certification. The theorem concerns ordinary Chow rank only; it makes no claim about border Chow rank or a general formula for arbitrary matrix size.

The previous computation-assisted manuscript, PDF, and certificate package are retained unchanged as historical evidence. The new manuscript is the computation-free revision.