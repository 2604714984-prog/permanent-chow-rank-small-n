# Internal proof audit — perm4 computation-free revision

Date: 2026-10-19. Scope: the manuscript `main.tex` in this directory.

## Conclusion

The current written argument closes the three computational dependencies identified in the earlier investigation. No unresolved mathematical step was found in the internal review described below. This is not external peer review, a novelty-priority certification, or a formal proof-assistant verification.

The review deliberately separates (a) symbolic mathematical arguments, (b) optional computational regression tests, and (c) technical PDF preparation. A computational PASS is never used to discharge a written lemma.

## Dependency and edge-case review

| Obligation | Review outcome |
|---|---|
| Fixed linear flattening | K(h) is defined on a fixed source and target and is linear in h; the derivative-image restriction is used only to compute its rank. |
| Row-space containment | Proved using the apolar pairing D'D(h)=DD'(h), not ordinary unnormalized monomial-matrix symmetry. |
| Full Koszul kernel | Mixed-partial equations are integrated by g=(1/3) sum x_a q_a. Injectivity and surjectivity are both proved. |
| Base permanent prolongation | A fixed derivative and a remaining quadratic determine a unique cubic; forbidden coefficients cannot cancel. Transpositions connect all six matchings. |
| Independent Chow term | Only four squarefree cubics survive; outside variables and repeats are excluded. |
| Dependent Chow term | The 93-minors vanish on the dense independent-factor locus, hence everywhere. Rank does not increase under specialization. |
| Missing derivative: no z | Every bad cubic is killed by an allowed derivative. |
| Missing derivative: z²u | Differentiation by u is allowed and produces forbidden z². |
| Missing derivative: z times boundary factor | Differentiating by the other factor leaves a forbidden row/column pair. |
| Missing derivative: z times two interior variables in a common row/column | This is the nontrivial exception. A rectangle companion cubic is forced; that companion is killed by a non-z boundary derivative. |
| Repeated interior variable | Multiplicity 2 is retained and invertible in characteristic zero; it is not silently treated as squarefree. |
| Missing matching equality | Only one of nine transposition edges can be absent. A displayed three-swap path recovers it, so no exhaustive-table premise is needed. |
| Kernel at z | Uses exactness for q tensor z minus an E-valued tensor; its cubic lies in D plus K z³, giving q congruent to 3c z². |
| Nonzero square class | Every nonzero square has a nonzero square coefficient; E has none. Thus [v²] is nonzero for every v≠0. |
| Row-column scaling | Weights are 0 at the selected corner, 1 on its row/column, and 2 in the interior. Each rectangle is homogeneous. |
| Equivariance | Both quotient spaces are fixed, and the induced transformations are invertible for t≠0. |
| Specialization direction | The special rank 99 is less than or equal to the rank for nonzero t. Only polynomial minors are used; there is no analytic or invertibility assumption at t=0. |
| Kernel collapse under a limit | Avoided: the proof compares ranks rather than transporting a proposed kernel vector. |
| Minimum quadratic rank | A nonzero off-diagonal symmetric zero-diagonal block has rank at least two, so its two-block principal matrix has rank at least four. |
| Rank-four classification | Equal-rank principal block gives image containment and a zero Schur complement; no numerical rank check is used. |
| Fixed-image uniqueness | A rank-two zero-diagonal symmetric matrix is unique up to scalar inside a fixed image, proved using disjoint supports. |
| Tensor-product image uniqueness | Contractions recover each factor, justifying the one-dimensional intersection bound. |
| Extension by q | Two independent kernel vectors would put a nonzero rank-at-most-two quadratic in E, impossible. |
| Subtraction inequality | Derived from the kernel of A-B and both image and row intersections; the source dimension is fixed. |
| Dependent factors in lower bound | They fall in the zero-intersection case, or a rank-four common quadratic forces independence. No generic-only assumption is used. |
| Seven or fewer terms | Removing one leaves at most six; no padding or separate seven-term hypothesis is required. |
| Upper bound | Sign-character cancellation proves Glynn directly over characteristic zero. |
| Field scope | The argument works over any algebraically closed characteristic-zero field; scalar extension gives the lower bound over any characteristic-zero field. |
| Border rank | Not proved or claimed. The subtraction argument uses an actual decomposition. |

## Optional checks actually run

A standard-library-only independent program reconstructs quotient derivative constraints directly from the rectangle basis. No historical helper is imported.

Over Q, the observed dimensions/ranks are respectively 16, 17, 4, 560 and 92 for the full permanent prolongation, the missing-corner prolongation, the single-term prolongation, the permanent Koszul image, and the single-term Koszul image. Over each of F_1000003 and F_1000033, all sixteen missing-coordinate prolongations have dimension 17. The six-node matching graph remains connected with eight edges. All forbidden cubic patterns in sizes 2, 3, 4 and 5 satisfy the displayed elimination rule. These extra-size tests do not establish a general-n Chow-rank equality.

For n=4, the 816 cubic monomials split into 692 directly forbidden monomials, 27 rectangle-companion exclusions, 96 matching monomials, and z³. This count is a diagnostic only, not an enumeration premise in the proof.

The supplement also verifies the integer Glynn expansion. The complete machine-readable receipt is `supplementary_results.json`.

## Alternative-route assessment

Han–Ju–Kim, arXiv:2503.12032, establishes tensor-rank results. It is not used to bound ordinary Chow rank in this manuscript. Indeed, the row-multihomogeneous component of one product of four column sums is the permanent itself. Projecting an arbitrary Chow term therefore does not produce one simple row tensor. A separate per-Chow-term bound would be required for a transfer; no such transfer is asserted.

The new scaling argument works within the original derivative-space framework. There is no need to replace the global lower-bound strategy once its uniform quotient-kernel lemma is proved directly.

## Historical and publication boundary

The initial branch note at commit 9dd3368a0973ac24a8f63b6ea818a89bda8e1139 correctly recorded that its then-current attempt had not solved the chart lemma. That text is historical. This revision supplies the missing argument instead of retroactively treating the initial attempt as complete.

Original perm4 sources, PDF and certificates are retained. Other n packages and frozen releases are not modified. In particular, the root HANDOFF identifies a newer perm5 r2 proof that does not use the historical 58-state route; this perm4 task does not re-audit or modify either perm5 version.

Author review remains distinct from the completed internal mathematical rewrite. arXiv upload remains paused.
