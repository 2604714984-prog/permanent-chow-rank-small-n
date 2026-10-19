# Internal audit — perm5 computation-free draft

Date: 2026-10-19. Branch: research/perm5-computation-free-20261019.

## Scope
This revision removes the finite 352-case coordinate scan and the four
small rational normal-form rank certificates from the active short proof.
It does not change the theorem, global image-span inequality, quotient-symbol
framework, or frozen release.

## Replacement arguments

- **Five independent factors.** At a coordinate degeneration, F is the
  squarefree quadratic space on five vertices and U the squarefree cubic
  space. The ten source columns correspond to triples. A column is zero iff
  its triple lies entirely in B=ker P, or it has exactly one vertex
  outside B and its complementary pair is the one-dimensional quotient
  edge A. Hence the number of zero columns is
  binom(5-d,3)+d*1_{A subset B}. Distinct triple columns have disjoint
  supports. This replaces the 352-case table.
- **Four-factor span.** The source lists all relevant second derivatives.
  For s=1, seven nonzero derivatives are distinct monomials. For s=2,
  two vanish, one relation is H11-H12+H22=0, and the remaining five
  nonzero derivatives have distinct square-monomial pivots. For s=3,
  six off-diagonal derivatives have distinct square pivots and three diagonal
  derivatives are distinct squarefree monomials. For s=4, the six
  off-diagonal derivatives have distinct square pivots and four diagonal
  derivatives are distinct squarefree monomials.
- **Small factor spans.** Specialization to a monomial with positive
  exponent partition gives minima 1,2,4,7 for the numbers of distinct
  degree-two divisors. Rank cannot increase under specialization.

## Checks completed in this revision
- The revised source compiled twice with MiKTeX using shell escape disabled.
  Output: 8-page PDF, 312,358 bytes. No undefined references or citation
  warnings remain. The only warnings are the benign no-shell-escape
  epstopdf warning and one underfull vertical box.
- The coordinate symbol formula was checked against its six values
  (d=0,\ldots,5); each nonzero triple column has a unique support.
- The four derivative ranks were rechecked by coefficient comparison:
  (7,7,9,10). In the (s=2) case the only relation among nonzero
  derivatives is (H_{11}-H_{12}+H_{22}=0); the remaining independence
  follows from the listed square monomials.
- The positive-partition floors (1,2,4,7) were checked directly.

## Remaining acceptance boundary
The mathematical replacements and TeX build have passed this internal review.
The full theorem has not been externally refereed or formally verified. The
released verifier may still be run as a regression check, but its PASS is not
needed as a proof premise. Do not promote this draft to main or overwrite any
frozen submission without author review.

No CI was dispatched. No historical release or certificate was modified.
