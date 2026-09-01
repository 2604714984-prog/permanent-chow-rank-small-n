# Closure of the 2026-08-21 `perm_6` rank-32 proof audit

## Outcome

The audit found a real defect in the local proof, not a failure of the final
arithmetic. The defect is repaired in
[`n6_exact_ordinary_chow_rank_32.md`](n6_exact_ordinary_chow_rank_32.md).
The synchronized reviewer files are
[`n6_exact_ordinary_chow_rank_32.tex`](n6_exact_ordinary_chow_rank_32.tex)
and [`n6_exact_ordinary_chow_rank_32.pdf`](n6_exact_ordinary_chow_rank_32.pdf).
The repaired internal theorem is

\[
\operatorname{ChowRank}(\operatorname{perm}_6)=32
\]

over an algebraically closed field of characteristic zero. It remains an
ordinary-rank statement and has not received named external peer review or
proof-assistant formalization.

## The defect that was found

For

\[
T_s=x_1x_2x_3x_4x_5(x_1+\cdots+x_s),
\]

the old source proof passed from six formal factor labels to the actual
quadratic and cubic derivative spaces without proving that the spaces agree.
Exact rational differentiation shows that they do not always agree:

\[
\begin{array}{c|cc|cc}
s&\dim F&\dim U&
\dim(\text{formal pair-product span})&
\dim(\text{formal triple-product span})\\ \hline
1&11&14&11&14\\
2&11&14&12&17\\
3&13&18&13&19\\
4&14&20&14&20\\
5&15&20&15&20.
\end{array}
\]

Thus the formal squarefree symbol table cannot be pushed directly to the
actual \(s=2,3\) derivative spaces. The new frozen payload records these
mismatches, and a regression test requires them to remain false.

## Repair

The repaired proof uses the formal squarefree table only for six independent
factors, where the identification is valid. For factor-span dimension five it
works directly with the actual polynomial:

- exact differentiation gives middle ranks \(14,14,18,20,20\);
- for \(s=3\), the actual middle space contains nine squarefree cubics, with
  minimum coordinate incidence five;
- for \(s=4,5\), it contains all ten squarefree cubics, with minimum
  coordinate incidence six;
- the diagonal-torus specialization of a nonzero direction supplies the
  corresponding directional rank floor;
- the general kernel-preimage bound handles quotient ranks two through four;
- an elementary essential-variable argument strengthens the one-dimensional
  kernel case for \(s=1,2\); and
- the full quotient is injective because
  \(E_2^{(1)}=E_3\) and a nonzero permanent cubic has at least nine essential
  variables.

The resulting sufficient adjusted rows are

\[
\begin{array}{c|c}
s&\operatorname{rank}\beta_{P,R}+(20-\dim U)/2\\ \hline
4,5&(0,5,8,13,15,20)\\
3&(1,5,7,12,14,19)\\
1,2&(3,9,9,10,16,17).
\end{array}
\]

Every entry is at least \(10d/3\), so the half-defect lemma survives with no
use of the false identification.

## Audit-comment traceability

| Audit issue | Resolution | Evidence |
|---|---|---|
| Geometric degeneration was asserted but not shown | The proof now states the diagonal one-parameter degeneration and uses it only for the middle-rank floor, where semicontinuity has the required direction | theorem Section 4.1; exact positive-partition replay |
| Normal-form reduction was not justified | The unique relation among six factors spanning a five-space is normalized by its support size \(s=1,\ldots,5\) | theorem Section 4.3 |
| Formal and actual local spaces were conflated | Confirmed as a genuine error for \(s=2,3\); removed from the proof and frozen as a negative regression | normal-form table above; `test_rejected_formal_actual_shortcut_stays_rejected` |
| Kernel-preimage estimate was missing | Polarization gives kernel \(\operatorname{Sym}^3(\ker P)\), followed by the elementary inverse-image dimension bound | theorem equation (3.1) |
| Local quotient-symbol rows were merely replayed | Six-independent rows are derived from all 45,696 torus-fixed coordinate pairs; five-span rows are derived from actual derivative matrices plus written directional arguments | theorem Sections 3 and 4; exact script and JSON |
| Global filtration said ranks “add” without a dimension argument | The repaired proof introduces \(H_i\), projects to \(W_i/W_{i-1}\), and proves the increment inequality before summing | theorem equation (7.1) |
| Replay could be mistaken for border-rank evidence | Every artifact states ordinary rank only | theorem Sections 1 and 8; frozen `scope` field |

## Reproduction

```text
python scripts/n6_exact_ordinary_chow_rank_32.py \
  --verify-json data/n6_exact_ordinary_chow_rank_32.json
python -m unittest tests.test_n6_exact_ordinary_chow_rank_32 -v
```

The first command derives the finite tables from their underlying objects; it
does not compare a second hard-coded copy of the old local rows.
