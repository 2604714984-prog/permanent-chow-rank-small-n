# Internal mathematical audit of the October manuscripts

This is an assistant-conducted internal audit. It is not a named independent
human review, journal refereeing, or an external certification of the theorems.
The author's personal final reading of the new perm5 argument has not been
recorded by this workflow.

## perm5: replacement proof and dependency closure

The September public article abbreviates several nontrivial portions of the
fixed-six and terminal-orbit argument. Its five executable checks do not
reconstruct all of those portions. In particular, the state-table program
checks integer generation and route assignment; its `P_UPPER` values are
inputs, not a derivation of the global prolongation bounds. The terminal
independent program checks the orbit-zero endpoint, not the fourteen-profile
classification or the orbit-one and orbit-thirteen reductions. Those facts
must not be inferred from the public entry point's PASS marker.

Historical detailed text was consulted to locate the omitted interfaces. It
is not imported into the October theorem's dependency graph. The revised
seven-page manuscript instead proves the lower bound by the following short
argument, with all characteristic-zero steps written in the article.

1. The quadratic and cubic permanent derivative spaces `E2,E3` each have
   dimension 100, `partial E2=V`, and `E2^(1)=E3`. Disjoint matching supports
   give the bases; transposition connectivity gives the prolongation identity.
2. Row-column torus specialization gives a rank-four floor for nonzero
   permanent quadrics. The closed incidence of at most five-dimensional
   variable spaces degenerates to a coordinate graph with at most five edges,
   which supports at most one four-cycle. Thus each local quadratic
   intersection has dimension at most one.
3. For a quintic product, actual quadratic and cubic derivative dimensions
   agree: they are the ranks of transposed catalecticants. Their common value
   `u` is at most ten. The proof never replaces an actual derivative space
   by a larger formal product span in a dependent-factor case.
4. For a quotient with kernel of dimension `k<=2`, a kernel cubic whose
   complementary derivatives lie in a line of quadrics would, if any such
   derivative were nonzero, support that quadric on at most `k+1<=3`
   variables. This contradicts the rank-four floor. Therefore the kernel
   is precisely the actual cubic space intersected with `Sym^3(ker P)`.
5. Five independent factors reduce, after relaxing the intersection to any
   line, to coordinate quotient symbols. Distinct source triples have disjoint
   surviving supports. The killed-column formula gives ranks
   `(0,5,7,7,10,10)` for quotient ranks zero through five. The 352-case
   enumeration independently checks that formula; no preservation of a
   rank-four condition at the coordinate limit is assumed.
6. A four-dimensional span has exactly one relation among five factors. After
   changing and rescaling coordinates its forms are
   `x1*x2*x3*x4*(x1+...+xs)`, `s=1,...,4`. Actual middle ranks are
   `7,7,9,10`. The article displays nonzero minors `16,16,-16,16` and the
   upper-rank relations. The required squarefree cubic inclusions also have
   explicit derivative formulas in the appendix.
7. The remaining rank-one quotient cases use the actual cubics. In support
   three, the zero/nonzero coefficient of the fourth direction is treated
   separately. The zero case has a two-dimensional quadratic image divisible
   by one variable, so it cannot meet the rank-four intersection line.
   Together with elementary monomial floors, this proves
   `rank(beta)+(10-u)/2 >= 2*d` in every factor-span and quotient dimension.
8. The rectangular image-span inequality is proved by rank factorizations
   and Sylvester's inequality. For a hypothetical N-term decomposition it
   gives `h2+h3 <= 10*N-100-Delta`.
9. Addition followed by differentiated quotient has rank exactly `h3`,
   because its kernel after addition is `E3`. Filtering the actual factor
   spans kills previous blocks in the first tensor factor, giving
   `h3 >= 50-Delta/2`. The same individual actual ranks define `Delta` in
   both estimates.
10. Hence `h2+Delta/2 <= 10*N-150`. Length below fifteen is impossible.
    At length fifteen both nonnegative terms vanish. Then every ten-dimensional
    local quadratic derivative space lies in `E2`, contradicting the
    one-dimensional intersection bound. Thus length is at least sixteen.
11. Glynn's rational identity supplies sixteen products. Extension to an
    algebraic closure rules out shorter decompositions over any
    characteristic-zero field. No Nullstellensatz descent assertion is needed.

The new argument has no dependence on the earlier 58-state routing, global
prolongation constants, inverse compression, terminal local rings, private
receipts, or historical SAT material. The old proof package is preserved in
full for comparison, without asserting that the old abbreviated presentation
has thereby received a complete external review.

## perm6: retained proof chain

The ordinary-rank-32 lower bound keeps its symmetric middle-catalecticant
argument. The internal audit separately examined these interfaces:

| Interface | Review and finite boundary |
|---|---|
| Permanent derivative tower | Disjoint support bases, cubic prolongation by matching transpositions, and rank/essential-variable floors by torus specialization. |
| Small quadratic intersections | Closed Grassmannian incidence; coordinate limit has at most six graph edges. Two four-cycles need at least six edges, with extremal union K2,3 or K3,2 and at most three cycles. |
| Coordinate squarefree table | The diagonal factor torus preserves the source and quadratic spaces. Rank drops in the tautological quotient-bundle specialization. Exact coordinate calculations cover the relaxed dimension-at-most-three quadratic quotient. |
| Dependent normal forms | Actual polynomial derivatives give `(dim F,u)=(11,14),(11,14),(13,18),(14,20),(15,20)`. Formal/actual discrepancies remain regression tests. |
| Directional estimates | Squarefree input cubics projected modulo a chosen variable give distinct pair monomials. The two exceptional supports are handled by explicit independent output supports. These are written arguments, not extrapolations from sampled directions. |
| Exceptional four-dimensional quotient | Complementary derivatives in an at-most-one-dimensional intersection can be normalized to `(q,0,0,0)`; any nonzero q would use at most two variables and contradict the rank-four floor. |
| Symmetric image-span inequality | Factor each symmetric map through its image, then apply Sylvester. This yields `h <= 10*N-200-Delta/2`. |
| Filtration increment | Projection of the first tensor factor kills the preceding factor spans; `Fi/(Fi intersect E2)` injects into `F/E2`. The local symbol estimate therefore yields `h >= 120-Delta/2`. |
| Defect cancellation | Both inequalities use the same actual middle-rank defect. Cancellation forces N>=32, without assuming independent factors. |
| Upper bound and fields | Direct integer expansion of Glynn's formula; rational upper bound plus extension of a hypothetical shorter decomposition to an algebraic closure gives the equality over every characteristic-zero field. |

The revision spells out the elementary coordinate specialization, replaces
an implicit directional-specialization argument with a direct projection,
expands the exceptional kernel argument, and aligns equation tags with the
actual section numbering. No frozen finite result is changed.

## Adversarial and integration diagnostics

These diagnostics are supplemental and are not substituted for the written
characteristic-zero arguments:

- Over `F3`, all 212 quotient row spaces of a four-space were combined with
  every projective rank-four quadric in the actual quadratic derivative
  space of each quintic normal form. All 5,656,160 pairs satisfied the local
  half-defect bound. The exact output is `quintic_local_stress.json`.
- On the actual Glynn decompositions, direct rational image-span computations
  give `dim F=110, dim U=150, h2=10, h3=50` for perm5 and
  `dim F=240, dim U=520, h3=120` for perm6. The respective global bounds
  are sharp. See `glynn_global_consistency.json`.

The internal audit has identified no remaining gap in the revised written
chains. This judgment remains subject to the author's final reading and
independent external mathematical scrutiny. Executable checks alone do not
establish that judgment.
