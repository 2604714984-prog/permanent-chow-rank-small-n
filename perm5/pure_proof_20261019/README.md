# perm5 computation-free proof research (2026-10-19)

This branch develops a self-contained, no-computation rewrite of the active
short proof of
\[
\operatorname{ChowRank}(\operatorname{perm}_5)=16.
\]
It does not overwrite the released 20261016-r2 submission.

## Current changes

1. The 352 coordinate-pair scan in the five-independent-factor case is
   replaced by the exact count
   \[
   \operatorname{rank}\beta\ge
   10-\binom{5-d}{3}-d\,\mathbf 1_{\{A\subset B\}},
   \]
   where \(B\) is the coordinate kernel of the factor-span quotient and
   \(A\) is either absent or a single quadratic edge. The columns are
   indexed by triples and have disjoint supports, so the count is immediate.
2. The four rational derivative-matrix rank checks for
   \(T_s=x_1x_2x_3x_4(x_1+\cdots+x_s)\) are replaced by explicit formulas
   for the ten second derivatives. Distinct square-monomial pivots and one
   displayed relation yield ranks \(7,7,9,10\).
3. The lower bounds \(1,2,4,7\) for the cubic derivative-space dimensions
   are proved by specializing to the positive partitions
   \((5),(4,1),(3,1,1),(2,1,1,1)\).

## Acceptance boundary

This is a research draft, not yet the accepted public reading version. The
proof strategy otherwise remains the rectangular image-span inequality and
the local quotient-symbol estimate. The released version and its exact
certificates remain intact. Do not run CI for this branch.
