# perm4 pure-proof investigation — 2026-10-19

## Scope and status

This is a research note, not a replacement for the theorem or its existing certificate. The target is to remove computer-assisted steps from the proof of
\[
\operatorname{ChowRank}(\operatorname{perm}_4)=8.
\]
The present proof remains valid with its exact certificate package. This investigation establishes elementary structural proofs for the two base flattening ranks and isolates the remaining obstruction. It does **not** yet establish a fully computation-free proof.

## 1. Base rank 560: a direct prolongation classification

Let
\[
E=\operatorname{Span}\{x_{ia}x_{jb}+x_{ib}x_{ja}:i<j,\ a<b\},
\qquad \dim E=36.
\]
The relevant map has domain \(E\otimes V\), of dimension \(36\cdot16=576\). Its kernel is identified with the first prolongation
\[
E^{(1)}=\{g\in\operatorname{Sym}^3V: \partial_{ij}g\in E\text{ for all }i,j\}.
\]

**Claim.** \(E^{(1)}\) is exactly the span of the sixteen 3-by-3 subpermanents.

**Proof.** If a cubic monomial has two variables in a common row or a common column (including a repeated variable), differentiating with respect to the remaining factor produces a quadratic monomial unsupported in \(E\). The coefficient cannot cancel with a different cubic monomial, since the differentiated variable and remaining quadratic monomial determine the original cubic monomial. Hence only squarefree monomials whose variables occupy distinct rows and distinct columns can occur.

Fix a 3-row set \(I\) and 3-column set \(J\). The allowed monomials supported on \(I\times J\) are the six perfect-matching monomials. The condition \(\partial_{ij}g\in E\) says that coefficients of two matchings differing by a transposition are equal. Transpositions connect \(S_3\), so all six coefficients agree. Thus this support contributes one scalar multiple of \(\operatorname{perm}(X_{I,J})\). Distinct \((I,J)\) have disjoint monomial supports, yielding exactly \(\binom43^2=16\) independent cubics. Therefore
\[
\operatorname{rank}K(\operatorname{perm}_4)=576-16=560.
\]
This replaces the rank-560 modular-minor step with a direct monomial argument.

## 2. Base rank 92: direct classification for one Chow term

For four independent factors, a linear change of coordinates sends the term to \(T=x_0x_1x_2x_3\). Its quadratic derivative space is
\[
F_T=\operatorname{Span}\{x_ix_j:0\le i<j\le3\},\quad \dim F_T=6.
\]
The first prolongation \(F_T^{(1)}\) consists exactly of the squarefree cubics in \(x_0,x_1,x_2,x_3\): a repeated variable yields a square in a derivative, and any variable outside these four yields a derivative not in \(F_T\). There are \(\binom43=4\) such cubics. Hence
\[
\operatorname{rank}K(T)=6\cdot16-4=92.
\]
For dependent factors, approximate the factor tuple by tuples of independent factors. The locus of matrices of rank at most 92 is Zariski closed (it is cut out by the 93-by-93 minors), so the limiting flattening also has rank at most 92. This replaces the modular rank calculation for a single Chow term.

## 3. The remaining bottleneck: the chart lemma

The lower-bound argument still needs, for every nonzero \(v\in V\),
\[
\ker\psi_v=\operatorname{Span}([v^2]),\qquad
\psi_v:\operatorname{Sym}^2V/E\to\operatorname{coker}\delta(E\otimes V),
\quad [q]\mapsto[\delta(q\otimes v)].
\]
Equivalently, \(\operatorname{rank}\psi_v=99\). The existing proof establishes this through a selected \(659\times659\) minor with exact identity
\[
\det\mathcal M(v)=-32768\,v_{00}^{99},
\]
proved by rational Schur-complement calculations and simultaneous triangularization of fifteen 99-by-99 coefficient matrices.

The current investigation has **not** derived this identity from a short invariant argument. The exact computation is not merely an approximate numerical experiment: the rational reconstruction and triangularization are already rigorous. What remains is to replace the certificate by a structural explanation or a smaller transparent combinatorial certificate.

## 4. Equivalent formulation that may help remove the chart calculation

For \(q\notin E\), define
\[
\theta_q:V\to\operatorname{coker}\delta(E\otimes V),\qquad
v\mapsto[\delta(q\otimes v)].
\]
The chart lemma implies \(\dim\ker\theta_q\le1\), and hence \(\operatorname{rank}\theta_q\ge15\). This is precisely the extension estimate needed by the rank-8 lower bound:
\[
\operatorname{rank}\delta((E+\langle q\rangle)\otimes V)\ge560+15=575.
\]
A direct proof of \(\dim\ker\theta_q\le1\), using the explicit rectangle basis of \(E\) and the low-rank classification, would eliminate the 99-dimensional chart calculation from the main proof.

The condition \(v\in\ker\theta_q\) can be expressed as the existence of a cubic \(g\) whose derivatives satisfy
\[
\partial_a g-v_aq\in E\quad\text{for every coordinate }a.
\]
Thus the unresolved problem is a constrained cubic-prolongation classification. The evident solution is \(q\equiv v^2\pmod E\); the goal is to prove it is the only one.

## 5. Alternative global strategy

A different proof would need a stronger or combined flattening/rank invariant that rules out seven terms without the extension estimate. The current rank 560 versus per-term bound 92 only yields \(\operatorname{ChowRank}\ge7\), so this cannot be achieved by that single inequality alone. No replacement invariant has been established in this investigation; changing the whole proof is currently less concrete than attacking the chart lemma.

## 6. Conclusion and next research target

- **Established without matrix-rank computation:** the structural derivations of ranks 560 and 92 above.
- **Still certificate-dependent:** the rank-99 chart lemma and the resulting rank-575 extension bound.
- **Not changed:** the published proof, PDF, and existing verification scripts.

The next mathematically meaningful target is to prove directly that \(\ker\theta_q\) has dimension at most one. Until that is proved, the result should be described as a partially de-computationalized proof, not a fully pure proof. The existing exact certificate must remain in place as the rigorous fallback.
