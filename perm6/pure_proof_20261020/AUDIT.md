# Internal mathematical audit — perm6 computation-free revision

Date: **2026-10-20**. Scope: `main.tex` in this directory.

## Disposition

The written argument closes the computational dependencies of the October 16 sextic proof. The review below identified no remaining unfilled mathematical implication in this revision. This is an AI-assisted internal review, not external peer review, a novelty-priority determination, or formal proof-assistant certification.

The review distinguishes symbolic arguments, finite regression tests, and technical document checks. A numerical rank or a PASS marker is not used to discharge a written lemma.

## Source boundary

The previous manuscript is the frozen `submissions/20261016-r2/perm6/main.tex`, Git blob `26fadadcde75415058928d87712ede553955e904`. The repository base inspected for this task is `fb03220dda763c3dc859042853a1f9e12a8c3e3e`. The new revision is separate and does not rewrite the frozen submission, original computation expectations, or other n results.

## Load-bearing dependency review

| Obligation | Mathematical check |
|---|---|
| Rank notion | Each linear factor may use all 36 variables. No row-separated tensor-rank bound is substituted for ordinary Chow rank. |
| Fixed catalecticants | All terms use the same source and target; addition of polynomials gives addition of maps. |
| Middle symmetry | Proved under the perfect differential pairing, not by assuming unnormalized monomial matrices are symmetric. |
| Permanent dimensions | Distinct row-column blocks have disjoint matching supports; the subpermanents give dimensions 225 and 400. |
| Prolongation equality | Forbidden cubic coefficients cannot cancel under a fixed derivative; transpositions equate all matching coefficients on each three-by-three block. |
| Quadratic rank floor | Row-column weights isolate a rectangle. Matrix rank cannot increase in the projective specialization. |
| Cubic essential-variable floor | The same argument reduces to a three-by-three permanent with nine independent first derivatives. |
| Small intersection | Intersection dimension can increase at the coordinate limit, so an upper bound at every such limit bounds the original space. |
| Six-edge graph endpoint | Two different four-cycles sharing two opposite edges would be the same cycle; at a six-edge union they share adjacent edges and form K2,3 or K3,2. |
| Generic one-parameter groups | Finitely many distinct characters admit integer weights separating them. A fixed subspace for distinct variable weights is coordinate. |
| Quotient families | Dimensions of source and quotient bundles are fixed; ranks can only decrease at specialization. Nonzero-orbit ranks are constant by equivariance. |
| Actual derivative spaces | The only universal assertion is containment in the formal triple-product span. Equality is used only for six independent factors. |
| Kernel-preimage bound | The unquotiented kernel is exactly the cubics on ker(P). Taking the inverse image of D tensor R adds at most d dim(R). |
| Small-complement lemma | A nonzero complementary derivative in a single quadratic line would make the cubic depend on at most k+1 variables. For k<=2 this violates quadratic rank at least four. |
| Full symbol | A kernel cubic belongs to E3 but is supported on at most six variables; the nine-essential-variable floor excludes it. |
| Monomial specialization | Independent coordinate factors are preserved; every limiting exponent is positive and the total remains six. Scalar normalizations are nonzero away from the limit. |
| Rank floors | Degree-three divisors are counted by the patterns 1+1+1, 2+1, and 3. The formula gives the required lower bounds without a partition table. |
| Killed-column formula | Zero, one, two and three outside vertices give the four displayed terms. Different triples have disjoint polarization coordinates. |
| Six-variable d<=3 | Every killed non-B triple supplies an outside-vertex/killed-edge factorization. The union bound is at most 3d; the excess factors as d(3-d)(12-d)/6. |
| Six-variable d=4 | An internal edge kills four triples and leaves only two edges, which kill at most one additional triple. Without it, at most three are killed. |
| Six-variable d=5 | There is no internal edge; three edges create at most three cross-edge pairs or one triangle. |
| Six-variable d=6 | An arbitrary three-edge quotient can have rank 19. The proof does not use the coordinate bound here; actual full-symbol injectivity gives rank 20. |
| Small factor spans | The absolute-value identity handles d=1. For d>=2 the strengthened kernel lemma and monomial floors suffice; no interval minimization is assumed. |
| Five-dimensional normal forms | Choosing five independent factors, rescaling nonzero coefficients, and absorbing a scalar gives Ts for s=1,...,5. This change of coordinates preserves ranks and support dimensions, not the displayed global rectangle basis. Only the invariant properties of R are used afterwards. |
| Explicit squarefree derivatives | The identity partial_j^2 partial_k Ts = 2 product_(i not in {j,k}) xi is proved by differentiation, with j<=s and j!=k. |
| The s=1 case | All ten squarefree cubic divisors of the monomial are actual derivatives. No exact middle rank is needed. |
| The s=2 upper bound | Bidegrees of binary cubic times disjoint squarefree cubic give u<=14. No claim that all formal triple products are derivatives is used. |
| The s=3 upper bound | Bidegrees of ternary quartic times a disjoint quadratic give u<=18 from ambient and derivative-order dimension bounds. |
| Squarefree-completion budget | The constructed missing dimensions are 0,3,1,0,0; they are bounded by half the middle-rank defect. Exact ranks 14,14,18,20,20 are unnecessary. |
| Common target in completion | Both actual and completed maps enter D tensor (Sym^2 L/R). The completed map kills only R intersect F_sf. The actual F/R embeds injectively in the same target. |
| Restricting the source | A codimension-m restriction reduces rank by at most m. No assertion of independence between actual and formal derivative images is made. |
| Remaining quotient dimensions | At factor span five, d=3,4,5 have kernel dimensions bounded using k<=2 and u>=14. |
| Symmetric image-span inequality | Factoring through the actual images and using the rank of a composition gives 2D minus the sum of individual ranks. Signs and cancellations are allowed. |
| Global quotient kernel | The map on the actual sum U has kernel U intersect E2^(1)=E3. E3 is contained in U by linearity. |
| All variables introduced | V=partial E2 is contained in partial F, which is contained in the sum of actual factor spans. Thus the filtration increments sum to 36. |
| Filtration increment | Projection kills previous images before the rank is counted; unprojected term images are not assumed independent. |
| Local/global quotient compatibility | Fi/(Fi intersect E2) injects into F/E2; the projected rank is exactly the local symbol rank. |
| Defect cancellation | Both bounds contain -Delta/2, including every dependent or repeated-factor term. Their comparison gives N>=32 without assuming Delta=0. |
| Upper bound | Sign cancellation leaves exactly the permutation monomials; the proof does not cite an expansion program. |
| Arbitrary characteristic-zero fields | Lower bound passes to the algebraic closure; the upper bound has rational coefficients. |
| Scope | No border-rank or general-n equality is inferred. |

## Independent cross-check of full-symbol injectivity

There is also a second short proof of this particular step. If a cubic's
first derivatives all lie in a space R of dimension at most three, its
first-catalecticant rank and hence its essential-variable dimension are at
most three. Every nonzero derivative then has quadratic rank at most three.
This is incompatible with the rank-four floor for nonzero quadrics in R.
Thus the full symbol is injective. The manuscript uses the permanent
prolongation/essential-variable proof instead; both give the same conclusion.

## Optional exact evidence actually reconstructed

The independent standard-library program imports no earlier proof module and reads no frozen result file. It reconstructs the following:

- All 45,696 coordinate six-variable symbols and all 352 five-variable coordinate symbols, comparing direct surviving-column counts with the closed formulas.
- The permanent prolongation on all 8,436 cubic monomials, with rational kernel dimension 400.
- All positive compositions of six, directly comparing monomial derivative ranks with the divisor formula.
- The five actual normal forms and their squarefree subspaces. It preserves the mismatches between actual and formal spans as regression checks.
- 528 rational local examples, including 261 with a nonzero admissible quadratic subspace; 222 small-complement kernel identities.
- 2,464 structured coordinate-boundary examples for the five normal forms, with 1,232 further kernel checks. Rank-four matching lines are required to lie in the actual quadratic derivative space.
- 50 checks using a second quotient-rank procedure, by concatenating killed target columns instead of reducing quadrics first.
- The integer Glynn expansion over 1,492,992 choices, leaving 720 permutation monomials.
- The actual Glynn image sums, with cubic dimension 520 and quadratic dimension 240; a separate reconstruction of 4,320 derivatives gives quotient rank 120, so both global inequalities are equalities for this decomposition.

The exact receipt is `verification_results.json`. These finite calculations are error-detection tests, not the all-parameter proof.

## Deliberate failure tests

An arbitrary coordinate triangle of killed quadratic edges gives full squarefree-symbol rank 19, not 20. The verifier requires this negative control to exhibit the failure; the manuscript uses actual permanent structure for the full symbol.

A rank-two quadratic line can kill a cubic with two-dimensional complementary kernel even though the cubic does not depend only on that kernel. The verifier also requires this counterexample. This tests the necessity of the rank-four hypothesis rather than silently assuming it away.

## Remaining boundary

No unresolved lemma was identified in this internal revision. Author responsibility, external referee assessment, and formal certification remain distinct from completion of the mathematical rewrite. arXiv remains paused. Technical source-only and cross-platform build checks are recorded separately, rather than being described as mathematical verification.
