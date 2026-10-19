# Final internal mathematical audit — perm5 computation-free proof

Date: 2026-10-19. Scope: the complete `main.tex` supplied with this directory.

## Conclusion and limit of the claim

The internal review found no remaining unproved computational endpoint or unfilled implication in the manuscript. The lower-bound chain is complete, including arbitrary dependent or repeated factors and arbitrary quotients of their actual factor spans. This is an internal review of AI-assisted mathematics, not external peer review, independent-human certification, or formal proof-assistant verification.

A test PASS establishes a successful exact regression run, not the theorem. The written proof is independent of every script and receipt in this directory. The theorem concerns ordinary Chow rank only.

## Source/version reconciliation

The starting research source was commit `4e408ab1c7589e3e767861859eade59239bc9ebc`, `perm5/pure_proof_20261019/main.tex`. Its mathematical parent is the active `20261016-r2` short proof, not the older 58-state proof. Repository main was read at `cb2fb4fc886abc9069f400a81c52bf91612b7606` before publication preparation. Later remote heads must be checked again before a push; unrelated intervening work is not overwritten.

The initial draft was mathematically promising but not a clean final deliverable. It retained the old date/title, a non-local `anc/verify_submission.py` instruction, stale ancillary wording, an incomplete explanation of partition minimization, and a larger-than-needed normal-form rank computation. The final source removes these dependencies/instructions, explicitly states specialization conventions, and replaces both numerical tables by formulas. Original release files and historical draft commits remain available.

## Dependency-by-dependency audit

| Obligation | Resolution in the written proof |
|---|---|
| Rank notion | Products have five arbitrary linear factors in the 25-variable space. No row-factor restriction is assumed. |
| Tensor-rank comparison | A single product of column sums projects to the permanent's row-multihomogeneous component; tensor-rank results are background only. |
| Differential pairing | Characteristic zero gives a perfect pairing, and commuting derivatives identify the two catalecticants as adjoints. |
| Actual images | `F_i` and `U_i` are actual derivative images throughout; formal pair/triple spans are used as equality only for independent factors, or to give an upper bound. |
| Permanent image dimensions | Distinct row/column supports give 100 quadratic and 100 cubic basis elements. |
| Prolongation equality | A fixed partial derivative and output monomial determine a unique cubic source, so forbidden coefficients cannot cancel. Transpositions connect the six matchings. The reverse inclusion is explicit. |
| Essential-variable support | All derivatives of a term lie in symmetric powers of its actual factor span. |
| One-parameter limits | The manuscript explains existence via Pluecker coordinates and fixedness under the diagonal action, rather than assuming every subspace is already coordinate. |
| Minimum quadratic rank | Explicit row/column weights give distinct rectangle characters and a nonzero projectively normalized rectangle limit. Rank four at the limit is a lower bound on the original rank. |
| Intersection specialization | `E2` is invariant, and intersection dimension is a kernel dimension which cannot drop at the special point. The inequality has the correct direction. |
| Coordinate intersection count | Distinct rectangles have disjoint quadratic supports; a surviving rectangle needs all four corners. Two distinct rectangles require at least six variables. |
| Small-complement kernel | All complementary derivatives of a kernel cubic lie in a line. Changing complementary coordinates leaves at most one nonzero derivative, putting its quadratic in at most `k+1 <= 3` variables. The contradiction uses rank at least four. |
| Kernel converse | A cubic on `ker P` has all complementary derivatives zero and is killed by the local symbol. |
| Divisor floor | Chosen independent coordinate factors survive the monomial degeneration. Distinct degree-two divisors give distinct nonzero second partials in characteristic zero. |
| No partition enumeration | The divisor number is `binom(ell,2)+#{alpha_i>=2}`; degree five and `ell<=4` force at least one square divisor. |
| Simultaneous local specialization | The independent-factor lemma holds for every quadratic subspace of dimension at most one. It does not require rank four for the limiting line. |
| Fixed quotient dimensions | `S tensor F + L tensor R` has dimension `10k+5r-kr`, which is constant during specialization. No kernel vector is transported through a possibly collapsing limit. |
| Triple count | A surviving component uniquely determines its triple. Two distinct complementary edges cannot both be killed by a single quadratic line. |
| Uniform comparison with 2d | The remaining expression factors as `(5-b)(b^2+2b-6)/6`; `b=0,1` are separately immediate. |
| Normal-form coverage | Four independent factors are chosen; the nonzero coefficients of the fifth are rescaled to one and permuted. A nonzero overall scalar does not affect any rank. |
| First two four-variable cases | Zero partials and one displayed derivative relation give `u<=7`; two actual cubics have no common nonzero annihilating direction. Their nonzero derivatives have rank at most three, so survive modulo `R`. |
| Third four-variable case | If the fourth directional coefficient is nonzero, three derivatives are independent modulo `x4 L`. Otherwise two independent derivatives are divisible by `x4`, and their span meets the rank-at-least-four line trivially. |
| Fourth four-variable case | Three derivatives containing a chosen nonzero directional coefficient are independent modulo its coordinate factor; removing a line loses at most one dimension. |
| Unneeded exact ranks | Neither `u=9` for the third form nor `u=10` for the fourth form is used. The universal ceiling `u<=10` suffices. |
| Dependent-factor exhaustion | For `ell<=4`, all `d>0` cases have `k<=2` except `(ell,d,k)=(4,1,3)`. `d=0` and `ell=5` are separately covered. |
| Single algebraic bound | The half-defect slack is bounded by `((ell-4)(ell-5)+2)/4 + 2k - binom(k+2,3)`, nonnegative in the stated range. |
| Rectangular inequality | Factoring through the direct sum of term ranks and bounding `im C intersect ker B` proves the inequality without assuming independent term images. |
| Containment of permanent images | Linearity of catalecticants gives `E2 subset F`, `E3 subset U`, not equality with the separate term spaces. |
| Kernel of the global polarization | Its kernel inside `U` is `U intersect E2^(1)=E3`; the last equality uses both prolongation and `E3 subset U`. |
| Factor spans cover V | `partial E2 = V` and `partial F subset sum L_i` prove `sum d_i=25`. |
| Filtration rank addition | Projection to the new first tensor-factor directions kills all earlier images. It is this projected rank, not a sum of unprojected ranks, which is accumulated. |
| Correct local quotient | `F_i/(F_i intersect E2)` injects into `F/E2`; composing this injection leaves the local rank unchanged. |
| Terminal nonnegativity | `h2`, `h3`, each `10-u_i`, and `Delta` are nonnegative. Thus `N<15` is impossible and `N=15` forces `h2=Delta=0`. |
| Endpoint contradiction | `F=E2` forces each ten-dimensional `F_i` into an intersection of dimension at most one. |
| Upper bound | Four independent sign sums kill every non-permutation monomial; all 120 permutation monomials have coefficient one. |
| General characteristic-zero field | Scalar extension gives the lower bound and the rational Glynn identity gives the upper bound over the original field. |
| Border rank | Not asserted. The global argument starts from an actual finite decomposition. |

## Additional non-computational endpoint check

There is a second way to close the N=15 endpoint. From h2=0, the global map b has target V tensor (F/E2)=0, so h3=rank b=0. But Delta=0 in the already-proved local-to-global bound forces h3>=50. This gives the same contradiction without reusing the individual ten-versus-one intersection at the last line. The manuscript retains the latter version because it exposes the structural obstruction.

The monomial degeneration was also checked factor by factor: each factor must be divided by its **own** least parameter power. Their normalized product differs from the invertibly transformed original only by a common scalar. The final source states this explicitly; it does not presume that one scalar normalizes all factors separately.

## Optional independent checks actually executed

The program is newly implemented using only integer arithmetic and `fractions.Fraction`; it imports no historical project helper. Its receipt records actual execution, hashes of the tested manuscript and verifier, the Python version, and elapsed time.

- The closed local formula agrees with exact rational rank for all 352 coordinate pairs; minima by quotient rank are `0,5,7,7,10,10`.
- All explicit normal-form derivative identities match; the optional full-rank diagnostics give `7,7,9,10` but these are not four premises of the final manuscript.
- The degree-two divisor formula agrees with direct differentiation for all 16 positive compositions of five; its symbolic proof does not enumerate them.
- There are 399 exact local quotient tests, including noncoordinate quotients and 159 tests with a nonzero quadratic line of rank at least four. All satisfy the half-defect bound.
- 252 tests verify the exact small-complement kernel identity, not only the numerical inequality.
- The full 25-variable cubic coefficient system gives `dim E2^(1)=100` over Q; explicit row/column weights and the six-variable union obstruction also pass.
- Forty rectangular matrix examples, including deliberately cancelling summands, satisfy the image-span inequality.
- All 50,000 terms in the integer sign expansion reproduce exactly the 120 permanent monomials.
- On the actual sixteen-term Glynn decomposition, the pair-image sum has dimension 110 and the cubic-image sum dimension 150. Thus `(h2,h3,Delta)=(10,50,0)`, and both global inequalities are equalities. The use of actual pair/triple images here is justified by independent column factors and complementary-column differentiation.

The tests also pass with Python optimization enabled; explicit failure checks are not disabled by `-O`. Finite examples do not prove statements quantified over all subspaces or all fields; those quantifiers are handled in the manuscript.

## Technical and publication boundary

The source builds on its own, without program execution or ancillary data. The final reading PDF has eight pages. The local final build has no undefined references, missing citations, overfull boxes, or underfull boxes. The standard epstopdf notice about disabled shell escape is harmless. All pages were rendered for visual inspection, and a text-box check found no content outside page bounds.

The source manifest identifies the mathematical text. Different TeX distributions can produce different PDF bytes; build receipts distinguish these outputs rather than claiming byte identity. Repository publication must retain frozen 20261016-r2 files, the older perm5 package, and every other n package unchanged. arXiv remains paused. No hosted CI or local Codex session is needed or used.
