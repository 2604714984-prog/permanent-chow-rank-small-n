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

## Remaining review items
- Compile the revised TeX and check all references.
- Run the released standard-library verifier as an optional regression check,
  but do not cite its PASS as a proof premise.
- Carefully check the derivative coefficient identities, the specialization
  direction, and the use of the local estimate for all dependent-factor
  cases.
- Do not promote this draft to main or overwrite any frozen submission
  until these checks are complete.

No CI was dispatched. No historical release or certificate was modified.
