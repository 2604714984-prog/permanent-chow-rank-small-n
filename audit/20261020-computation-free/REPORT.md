# Audit of the computation-free perm4, perm5 and perm6 proofs

Date: October 20, 2026. Repository baseline: `0a6d651f0f1de8ebe711c183b41d71576a036248`.

## Disposition

**All three manuscripts pass this internal mathematical audit.** The review identified no false implication, uncovered factor-span case, circular dependency, or remaining computer-generated premise in the three written arguments. Their mathematical sources are promoted without changing their bytes. The conclusions are ordinary Chow ranks 8, 16 and 32, respectively, over every field of characteristic zero.

This is an AI-assisted internal review of the complete written arguments, not an external referee report, a priority or novelty determination, or formal proof-assistant certification. Exact regression tests are reported separately; no finite test is used to establish an all-parameter lemma. The audit does not infer border Chow rank or a general-size formula.

| Result | Current paper | Source SHA-256 | Pages |
|---|---|---|---:|
| perm4: rank 8 | [PDF](../../perm4/paper/perm4_chow_rank_8.pdf), [source](../../perm4/paper/source/main.tex) | `263843c3a06f3f9d5d74c2eaa410afac107d8be0f7d806a97c0791fdbcafcca1` | 7 |
| perm5: rank 16 | [PDF](../../perm5/paper/perm5_chow_rank_16.pdf), [source](../../perm5/paper/source/main.tex) | `272fe8933808e7e58574a6588082005c0bd35a0dc6e1d1fc4b5939ccb47cd611` | 8 |
| perm6: rank 32 | [PDF](../../perm6/paper/perm6_chow_rank_32.pdf), [source](../../perm6/paper/source/main.tex) | `a13191fce613d530ebb1634b373597e178a8f843b15707f0d8f3d65bff1f4b40` | 7 |

The original source paths were `perm4/paper/source/main.tex`, `perm5/pure_proof_20261019/main.tex`, and `perm6/pure_proof_20261020/main.tex`. The latter two already existed on the baseline main branch. This review did not substitute the older October 16 computation-assisted papers for those new drafts.

## 1. Common obligations

The factors in each Chow term may involve every matrix variable. Tensor-rank results for separate row spaces are not imported as Chow-rank lower bounds. The row-multihomogeneous projection of one product of column sums is already the permanent, so that projection cannot justify such a transfer.

All catalecticants have fixed sources and targets and are linear in the input polynomial. Their adjoint relationships use the perfect differential pairing in characteristic zero. In particular, unnormalized monomial matrices are not silently assumed symmetric. Each term's derivative spaces are actual images, not formal spaces of products of factor positions.

The permanent derivative-space dimensions follow from disjoint row-set/column-set matching supports. The prolongation identity is proved by eliminating a forbidden cubic coefficient through a fixed derivative: its quadratic output has only one source monomial, so cancellation with a different source is impossible. Nonzero derivative multiplicities are retained. On an allowed three-by-three block, transpositions equate all six matching coefficients. The reverse inclusion is also checked.

Each use of diagonal specialization identifies a group preserving the relevant permanent or squarefree spaces. Subspaces have fixed Grassmannian dimensions; quotient ranks are compared in local bases of bundles of constant rank. Rank may decrease at specialization, while intersection or kernel dimension may increase. The proofs use these directions correctly. A rank hypothesis on a quadratic is not assumed to survive a torus limit when the argument actually needs a stronger statement valid for arbitrary limiting quadratics.

For arbitrary characteristic-zero fields, a shorter decomposition would persist over the algebraic closure, whereas the stated Glynn upper bounds are defined over the rationals. This supplies the claimed field scope. All lower-bound arguments start from actual finite decompositions and therefore make no border-rank assertion.

## 2. Quartic audit

### Kernel, prolongation and base ranks

The fixed Koszul map is linear in the quartic. Its restricted kernel consists exactly of cubic gradients: mixed-partial equalities integrate to `g = (1/3) sum x_a q_a`, and Euler's identity recovers each quadratic `q_a`. This proves both directions, including repeated monomial factors. The permanent prolongation has dimension 16, so the image rank is `16*36 - 16 = 560`.

For four independent factors, the six squarefree quadratics have the four squarefree cubics as prolongation, giving rank 92. Every 93-minor vanishes on the dense independent-factor locus, and therefore identically. Dependent and repeated factors satisfy the same upper bound; the proof does not assume generic factors in the final decomposition.

### Missing derivative and the uniform kernel

The missing-derivative classification covers all cubic types. Cubics without the selected corner, cubics `z^2 u`, and cubics containing a boundary variable are excluded by an allowed derivative. The remaining potentially missed type is `z u w` with interior `u,w` sharing a row or column, including `u=w`. Its rectangle companion has a forbidden derivative, forcing the original coefficient to vanish. The multiplicity two in the repeated-interior case is not discarded.

The six matching coefficients remain connected after omitting the comparison using the missing derivative. The explicit three-swap path recovers that comparison. Consequently the only new freedom is `z^3`.

At the coordinate vector, the gradient-kernel argument gives `ker psi_z = span([z^2])`. The row-column scaling with weights 0, 1 and 2 preserves the rectangle space and sends a vector with nonzero corner coefficient to that corner. The special rank 99 is no greater than the constant nonzero-orbit rank, while the nonzero square class supplies the uniform upper bound 99. No proposed kernel vector is pushed through a possibly collapsing limit.

### Low-rank structure and subtraction

For a rank-two symmetric zero-diagonal matrix, a factorization `ab^T + ba^T` gives disjoint supports. Within the same two-dimensional image, the zero diagonal leaves only the off-diagonal coefficient, establishing uniqueness up to scale. In the Hessian block argument, an equal-rank principal block implies image containment and a vanishing generalized Schur complement even when that principal block is singular. All remaining blocks are multiples of one rank-two block.

The resulting tensor-product image has uniquely recoverable factors, so a four-dimensional variable span contains at most one independent permanent quadratic. The extension estimate follows because two independent kernel directions would put a nonzero quadratic of rank at most two in the permanent space, whose minimum nonzero rank is four.

The row-and-column intersection rank inequality is independently derived from the kernel of `A-B`. If the derivative-space intersection is zero, the residual rank is at least 560. If its dimension is one, the common rank-four quadratic forces four independent factors; the horizontal and vertical concatenation bounds are 575 and 636. Thus the residual rank is at least `575 + 636 - 560 - 92 = 559`. Six terms have rank at most 552. This excludes every decomposition with at most seven terms. The direct sign-sum argument supplies the eight-term upper bound.

**Quartic conclusion:** no unfilled implication; the former large-minor computation is not a premise.

## 3. Quintic audit

### Local hypotheses and exhaustion

The two actual derivative images have the same rank `u <= 10` by adjointness. The permanent quadratic/cubic spaces each have dimension 100. Row-column specialization proves both minimum quadratic rank four and `dim(E2 intersect Sym^2 L) <= 1` for `dim L <= 5`: two different rectangles require at least six coordinates.

For a quotient of the factor span with kernel dimension `k <= 2`, complementary derivatives of a kernel cubic lie in a line. A change of complementary coordinates makes them `q,0,...,0`. The nonzero quadratic would then use at most `k+1 <= 3` variables, contradicting its rank-four floor. The exact kernel is therefore the cubics supported on the quotient kernel.

The divisor floor is not an unexplained partition minimum. Chosen independent coordinate factors persist under the monomial limit, and each other factor is normalized by its own lowest parameter power. With total degree five, all exponents positive, and at most four variables, the degree-two divisor count is at least `binom(ell,2)+1`.

For five independent factors, simultaneous specialization of the quotient kernel and a quadratic line is justified without preserving a rank-four condition. The stronger squarefree statement permits every line. Different cubic triples have disjoint output coordinates; the exact coordinate rank is `10 - binom(b,3) - d*1_(e subset B)`. The difference from `2d` is bounded by `(5-b)(b^2+2b-6)/6` for `b >= 2`, and the remaining two values are immediate.

The sole dependent-factor case not covered by the small-complement argument is a four-dimensional factor span with one new direction. All tuples reduce to the four support types `x1*x2*x3*x4*(x1+...+xs)`. For the first two types, displayed vanishing derivatives and one linear relation give `u <= 7`, and two actual cubics supply a nonzero derivative surviving the quotient. For the last two, explicit squarefree derivatives give at least two surviving directions. The proof never needs their exact catalecticant ranks.

Combining these statements gives `rank beta + (10-u)/2 >= 2d` for every actual factor span and every quotient. The small-complement slack formula is nonnegative throughout its stated domain. The cases `d=0`, five independent factors, small complements, and the single four-dimensional exception exhaust all possibilities.

### Global argument

The rectangular image-span inequality follows by factoring through a direct sum of spaces of the individual ranks. It allows cancellations; it does not assume independence of term images. Applied to the two adjoint catalecticants, it gives `h2+h3 <= 10N-100-Delta`.

The global polarization quotient has exact kernel `E3`, so its rank is `h3`. The factor spans cover all 25 variables because `partial E2 = V`. Projection to each newly introduced first-factor direction kills previous images. The local quotient injects into the global quadratic quotient, so the accumulated ranks are genuinely the local symbol ranks, not a sum of unprojected ranks. This yields `h3 >= 50-Delta/2`.

Thus `h2 + Delta/2 <= 10N-150`. Nonnegativity rules out `N<15`; at `N=15` it forces `h2=Delta=0`, placing a ten-dimensional individual quadratic image in an intersection of dimension at most one. Independently, that endpoint would make the global target zero and hence `h3=0`, contradicting `h3>=50`. Glynn supplies sixteen terms.

**Quintic conclusion:** no unfilled implication; neither the historical 58-state route nor a coordinate table nor four computed normal-form ranks is needed.

## 4. Sextic audit

### Permanent structure and squarefree bounds

The permanent spaces have dimensions 225 and 400. A projectively normalized row-column limit gives a rectangle or a three-by-three subpermanent. Their ranks establish minimum nonzero quadratic rank four and minimum cubic essential-variable dimension nine.

At most five coordinates contain at most one rectangle. With six coordinates, two distinct four-cycles must share adjacent edges, giving `K_(2,3)` or its transpose and exactly three possible cycles. This proves the intersection bound without a graph scan.

The degree-three monomial-divisor formula is `binom(ell,3) + (ell-1)r2 + r3`, giving the required middle-rank floors `1,2,4,8,14` for factor spans one through five. The kernel-preimage bound and the strengthened small-complement lemma use actual derivative images.

The squarefree killed-column formula separates triples with zero, one, two, and three outside vertices. The resulting bounds cover the six-independent-factor case for quotient ranks at most five. The full quotient is intentionally treated differently: three arbitrary killed edges can form a triangle and give rank 19, not 20. For the actual permanent intersection, a full-symbol kernel cubic would lie in `E3` while using at most six variables; the nine-variable floor excludes it. This is an essential hypothesis distinction, not a gap filled by a generic calculation.

### Five-dimensional factor span

This is the main replacement for the former normal-form rank certificate. In each form `x1*...*x5*(x1+...+xs)`, explicit derivatives produce a squarefree cubic subspace of dimensions `10,7,9,10,10`. Its missing dimensions are therefore `0,3,1,0,0`.

For support size two, the product splits into a binary cubic and a disjoint squarefree cubic. The bidegree decomposition gives the upper bound `u <= 14`. For support size three, a ternary quartic times a disjoint quadratic gives `u <= 18`. These upper bounds pay for the missing dimensions through `m <= (20-u)/2`; exact normal-form ranks are unnecessary.

Both the actual map and its squarefree completion enter the same target `D tensor (Sym^2 L/R)`. On squarefree quadratics the killed space is only `R intersect F_sf`, of dimension at most one. The completed rank is at least five or seven for one or two new directions. Restricting its source to codimension `m` loses at most `m` in rank. The actual source contains that restricted space and its target embeds into the common target. Consequently the middle-rank defect compensates the loss. This does not identify the larger formal factor-product space with the actual derivative space.

Together with the small-factor-span inequalities and full-symbol case, this proves `rank beta + (20-u)/2 >= 10d/3` for every factor span and every quotient.

### Global argument

Middle-catalecticant symmetry gives the image-span bound `h <= 10N-200-Delta/2`, with no restriction on signs or cancellations. The exact global polarization kernel and projected factor-span filtration introduce all 36 variables and give `h >= 120-Delta/2`. The identical defect cancels, forcing `N>=32`. The sign identity gives 32 terms over the rationals.

**Sextic conclusion:** no unfilled implication; the graph scan, coordinate symbol tables, partition minima, interval minimizations and five exact normal-form rank profiles are not premises.

## 5. Independent analytical consistency check

The global bounds are sharp on the actual Glynn decompositions, which can be checked without a rank program. Write the factor in column `c` as `L_(epsilon,c) = sum_r epsilon_r x_(r,c)`. The column factors are independent, so their pair and triple products are actual derivative images.

For a fixed pair of columns, the sign characters are the constant character and the `binom(n,2)` distinct two-row parity characters. Their coefficient vectors have disjoint monomial supports. Thus the pair-image sum has dimension `binom(n,2)*(1+binom(n,2))`.

For a fixed triple of columns, the characters are the `n` singleton and `binom(n,3)` three-row parity characters. Fixing the first sign does not identify two of these equal-parity subsets. Character orthogonality over the sign group and disjoint supports give cubic-image sum dimension `binom(n,3)*(n+binom(n,3))`.

For n=5 these dimensions are 110 and 150, hence `(h2,h3,Delta)=(10,50,0)`. For n=6 they are 240 and 520, hence `(h,Delta)=(120,0)`. The relevant global inequalities are equalities. This is an additional consistency argument, not a replacement for the lower-bound proofs.

### Additional independent structural checks

Two critical conclusions also admit shorter independent checks, which do not change the manuscripts.

For the quartic, the row-column torus argument independently proves both properties needed by the subtraction step: every nonzero rectangle-space quadratic has rank at least four, and a variable subspace of dimension at most four contains at most one independent such quadratic. The first follows by specializing a projectively normalized nonzero quadratic to one rectangle. For the second, specialize the variable subspace to a coordinate subspace; intersection dimension can only rise, and four selected coordinates support at most one complete rectangle. Thus the needed consequences of the explicit rank-four Hessian classification have an independent proof within the same coefficient geometry.

For the sextic full symbol, the actual quadratic intersection has dimension at most three and every nonzero member has rank at least four. A cubic whose first derivatives all lie in that intersection would have at most three essential variables, since the first derivative map would have rank at most three. Every nonzero derivative would then be a quadratic supported on at most three variables and would have rank at most three, a contradiction. This independently confirms full injectivity for the actual intersection while leaving the arbitrary triangle quotient counterexample intact.

## 6. Diagnostic computations and deliberate failures

A fresh [independent program](independent_checks.py) uses exact rational sparse elimination and polynomial differentiation. It imports no project module and reads no stored rank table. Its [result](independent_results.json) records:

- Independent rational reconstruction of all cubic coefficient constraints: prolongation dimensions 16, 100 and 400, on 816, 2,925 and 8,436 monomials. All sixteen quartic missing-coordinate systems have dimension 17.
- Quartic base rank 560 and quotient ranks 99 at four explicitly chosen vectors.
- 232 additional six-variable quotient tests with the actual three-dimensional intersection from a two-by-three coordinate rectangle. The full symbol has rank 20, in contrast to the arbitrary triangle quotient of rank 19.
- All 352 five-variable and 36,864 six-variable coordinate symbols with up to one and three killed edges, respectively; the closed formulas match direct surviving-column counts.
- Actual inclusion of all five selected sextic squarefree subspaces and their defect budgets.
- 744 quintic and 1,080 sextic exact local quotient examples, including dense noncoordinate quotients and nonzero admissible quadratic lines.

Two weakened assertions are deliberately rejected. A rank-two quadratic line can kill a cubic outside the cubics on the quotient kernel; the rank-four condition cannot be omitted. An arbitrary three-edge quadratic quotient at full six-dimensional rank has a triangle counterexample of rank 19. The program also retains strict differences between actual and formal cubic spans: for support size two they have dimensions 7 versus 9 in the quintic case, and 14 versus 17 in the sextic case.

All three supplied optional verifiers were replayed normally and with both Python optimization levels. The fresh program was also replayed normally and optimized. Optimization does not disable its explicit failure checks. Finite examples do not replace the universal arguments above.

## 7. Publication and preservation

The publication layout uses one canonical `permN/paper/` location for each current proof. The former computation-assisted packages are kept intact under each `permN/archive/computation-assisted/`. The frozen October 16 r1/r2 submissions and distributed files are not rebuilt or overwritten. Pre-canonical research directories are English navigation pointers; their exact earlier content remains at the baseline Git commit.

The audit found and repaired a pre-existing quartic archive defect: an explanatory README had replaced the manifest-bound original. The original README is restored from commit `7b8a9d2626df9c492e23ad8c1048b38279a78f86`, with SHA-256 `08ac09dd803c931f0966b52f8b95268a33a86cf9f1811ffc66675d169f490a0f`. The original expected hash is not changed. The new archive guide is separate. The quintic Chinese draft README is removed from the current tree, without rewriting history.

Only a packaging adjustment is made to the relocated quintic diagnostic: its source-hash lookup now reads `source/main.tex`. No mathematical source is edited. Fresh current-release inventories are distinct from historical inventories.

Each manuscript was built from its source alone in a fresh directory using two pdflatex passes with shell escape disabled. The resulting page counts are 7, 8 and 7; normalized extracted text agrees with the preceding published reading copies. Final logs have no unresolved references, missing characters, or overfull/underfull boxes. All 22 pages of the canonical rebuilt PDFs were rendered and visually inspected; no clipping, overlap or broken glyph was observed. Build hashes are recorded in each paper's `BUILD.json`; PDF byte identity across platforms or build timestamps is not claimed.

See [PRESERVATION.json](PRESERVATION.json) for exact move/recovery identities and protected files, and [ACCEPTANCE.json](ACCEPTANCE.json) for the final executable acceptance results. These receipts certify the stated operations, not external mathematical acceptance. No hosted CI is dispatched, no local Codex is used, and arXiv remains paused.

### Fresh checkout and byte-bound files

The staged publication was exported to a fresh directory with `core.autocrlf=true`. All 293 byte-bound files retained their exact Git blob identities, including the 213 protected historical files. Current inventory checks passed normally and optimized, and each current optional verifier passed from a different working directory. [CHECKOUT.json](CHECKOUT.json) records the pre-receipt tree identity and the precise scope. Windows CRLF is accepted by the whitespace review where original inventories intentionally bind those bytes; expected historical hashes are not regenerated to normalize line endings.
