# `perm_5` v14 mathematical repair: one-intersection flags and binary cubics

## Status

This note repairs the two proof obligations identified in the external audit
of v13.  The first repair is a characteristic-zero degeneration argument whose
finite endpoint is certified by an exact standalone `F_3` computation.  It is
therefore a rigorous computer-assisted lemma, not a program-free lemma.  The
second repair is a purely algebraic characteristic-zero lemma.

The repaired argument must not be described as a purely combinatorial or
program-free proof.

## 1. Notation

Let

\[
V=A\otimes B,\qquad \dim A=\dim B=5,
\]

with coordinate variables \(x_{ia}=a_i\otimes b_a\).  Put

\[
E=\operatorname{im}C_{3,2}(\operatorname{perm}_5)
 =\langle x_{ia}x_{jb}+x_{ib}x_{ja}:i<j,\ a<b\rangle
 \subset \operatorname{Sym}^2V,
\]

and let

\[
\pi:\operatorname{Sym}^2V\longrightarrow
Q:=\operatorname{Sym}^2V/E
\]

be the quotient map.  For a ten-plane \(W\subset Q\), set

\[
p(W)=\dim\ker\Phi_W-100,
\]

where

\[
\Phi_W:\operatorname{Sym}^3V
\longrightarrow V\otimes(Q/W)
\]

is the polarized derivative map.  Thus

\[
\ker\Phi_W=(E+\widetilde W)^{(1)},
\qquad E^{(1)}=D,qquad \dim D=100.
\]

For a quintic Chow term \(T=\ell_1\cdots\ell_5\), write

\[
L_T=\langle\ell_1,\ldots,\ell_5\rangle,
\qquad
F_T=\langle\ell_i\ell_j:i<j\rangle.
\]

## 2. Universal one-dimensional-intersection flag theorem

### Theorem

Let the ground field have characteristic zero.  Suppose

\[
F=F_T,\qquad \dim F=10,\qquad \dim(E\cap F)=1.
\]

Put \(Z=\pi(F)\), so \(\dim Z=9\).  If

\[
Z\subset W\subset Q,\qquad \dim W=10,
\]

then

\[
\boxed{p(W)\le 26.}
\]

### Proof: closed incidence and preservation of the nine-dimensional image

Let \(d=\dim L_T\).  Since

\[
F\subset\operatorname{Sym}^2L_T,\qquad \dim F=10,
\]

we have \(d\in\{4,5\}\).

Let \(\mathbb T\subset \operatorname{GL}(A)\times\operatorname{GL}(B)\)
be the diagonal row-column torus.  For fixed \(d\), consider tuples

\[
(L,F',Z',W',[q])
\]

in

\[
\operatorname{Gr}(d,V)\times
\operatorname{Gr}(10,\operatorname{Sym}^2V)\times
\operatorname{Gr}(9,Q)\times
\operatorname{Gr}(10,Q)\times\mathbf P(E)
\]

satisfying

\[
F'\subset\operatorname{Sym}^2L,qquad
q\in F',\qquad
F'\subset\pi^{-1}(Z'),qquad
Z'\subset W'.                                      \tag{2.1}
\]

All four conditions are closed: they are vanishing conditions for natural
maps of universal bundles.  Hence the space \(\mathcal I_d\) of tuples
satisfying (2.1) is projective and \(\mathbb T\)-stable.

Choose \(0\ne q\in E\cap F\).  The original data give a point

\[
(L_T,F,Z,W,[q])\in\mathcal I_d.
\]

The closure of its \(\mathbb T\)-orbit is complete.  By the Borel fixed-point
theorem it contains a \(\mathbb T\)-fixed point

\[
(L_0,F_0,Z_0,W_0,[q_0]).
\]

The low-rank intersection theorem gives

\[
\dim(E\cap\operatorname{Sym}^2L_0)\le1.             \tag{2.2}
\]

Because \(0\ne q_0\in E\cap F_0\subset
E\cap\operatorname{Sym}^2L_0\), equation (2.2) implies

\[
E\cap F_0=\langle q_0\rangle.                       \tag{2.3}
\]

Consequently

\[
\dim\pi(F_0)=10-1=9.
\]

Condition (2.1) gives \(\pi(F_0)\subset Z_0\), and \(Z_0\) is a
nine-plane.  Therefore

\[
\boxed{Z_0=\pi(F_0).}                                \tag{2.4}
\]

This is the missing rank-preservation step.  In particular, no assumption
that quotient rank is a closed condition is being made: equality follows
from the closed incidence (2.1), the fixed Grassmann dimensions, and the
one-dimensional intersection bound (2.2).

### Proof: classification of the torus-fixed endpoint

The \(25\) coordinate lines \(kx_{ia}\) are the distinct weight spaces of
\(V\).  Hence the fixed \(d\)-plane \(L_0\) is a coordinate plane.  The
\(100\) generators

\[
x_{ia}x_{jb}+x_{ib}x_{ja}\qquad(i<j,\ a<b)
\]

are the distinct weight lines of \(E\).  Therefore \(q_0\) is one of these
rectangle permanents.  Its essential variable space is the four-plane

\[
\langle x_{ia},x_{ib},x_{ja},x_{jb}\rangle,
\]

which is contained in \(L_0\).

If \(d=4\), then \(L_0\) is exactly this coordinate rectangle.  Since
\(\dim F_0=\dim\operatorname{Sym}^2L_0=10\), we have

\[
F_0=\operatorname{Sym}^2L_0.
\]

Its quotient image is the coordinate nine-plane formed by the nine distinct
weights of the rectangle.

If \(d=5\), then \(L_0\) is the rectangle plus one coordinate cell.  Up to
row permutations, column permutations, and transpose, there are exactly two
possibilities:

1. the fifth cell shares a rectangle row or column (the attached orbit);
2. the fifth cell shares neither (the external orbit).

There are \(100\) coordinate rectangles.  Each has \(12\) attached and \(9\)
external choices for the fifth cell, hence the two orbit sizes are

\[
1200\quad\text{and}\quad900.                         \tag{2.5}
\]

By (2.2), \(\pi(\operatorname{Sym}^2L_0)\) has dimension \(14\).  Its
fourteen torus weights are one-dimensional.  Equations (2.3)--(2.4) show
that \(Z_0\) is a coordinate nine-subset of these fourteen weights.

The quotient \(Q\) has exactly \(225\) one-dimensional row-column weight
spaces: \(25\) squares, \(50\) same-row edges, \(50\) same-column edges,
and \(100\) rectangle crossing weights.  Since \(Z_0\subset W_0\), the
fixed ten-plane \(W_0\) consists of the nine weights of \(Z_0\) plus one
arbitrary additional quotient weight.  The additional weight is not assumed
to lie in the fourteen-weight universe.

### Proof: exact finite endpoint and return to characteristic zero

Use divided-power cubic coordinates.  For every coordinate subspace
\(W_0\subset Q\), the map \(\Phi_{W_0}\) is represented by an integral
matrix with entries in \(\{0,\pm1\}\).  Reduction modulo \(3\) can only
decrease matrix rank, hence

\[
\dim_{\mathbf Q}\ker\Phi_{W_0}
\le
\dim_{\mathbf F_3}\ker\Phi_{W_0}.                   \tag{2.6}
\]

The standalone verifier reconstructs every matrix from the polarized
derivative definition.  It also reconstructs the base permanent kernel and
finds dimension \(100\), equal to \(\dim_{\mathbf Q}D\).  Subtracting this
common base dimension from (2.6) is therefore legitimate.

The exact finite results are

\[
\begin{array}{c|c|c}
\text{factor-span dimension}&\text{flags checked}&\max p_{\mathbf F_3}(W_0)\\
\hline
4&100(225-9)=21{,}600&22\\
5,\ \text{attached}&\binom{14}{9}(225-9)=432{,}432&26\\
5,\ \text{external}&\binom{14}{9}(225-9)=432{,}432&22.
\end{array}                                           \tag{2.7}
\]

Thus \(p_{\mathbf Q}(W_0)\le26\).

Finally, \(\ker\Phi_W\) is the kernel of a morphism of vector bundles over
\(\operatorname{Gr}(10,Q)\).  Moreover \(p(tW)=p(W)\) for every
\(t\in\mathbb T\), because \(E\) and the polarized derivative map are
\(\mathbb T\)-equivariant.  Kernel dimension is upper semicontinuous, so
specialization of the torus orbit to the fixed point gives

\[
p(W)\le p(W_0)\le26.
\]

Extension of scalars and descent of matrix rank give the same statement over
every characteristic-zero ground field.  This proves the theorem.

## 3. Standalone finite certificate

The verifier is

```text
perm5_one_intersection_flag_standalone_exact.py
```

and the compact output is

```text
n5_one_intersection_flag_standalone_exact.json
```

The verifier uses only the Python standard library.  It imports no project
generator and reads no frozen result.  It reconstructs:

1. all \(225\) quadratic quotient weights;
2. all \(2925\) cubic monomials in \(25\) variables;
3. all \(1225\) cubic torus-weight blocks;
4. \(43825\) nonzero local truth-table entries;
5. the base kernel dimension \(100\);
6. the \(1200+900=2100\) coordinate five-planes containing a rectangle;
7. all \(21{,}600+864{,}864\) flags in (2.7).

The final output SHA-256 is

```text
B373461AB31F760C7A3DC2F83BFC61EAD73822C925FA8E81C5ACB015BD9705E0
```

This certificate is a logical premise of the repaired theorem.  It must be
packaged and replayed; it is not a redundant diagnostic.

## 4. Binary-cubic exclusion

### Lemma

Let \(U\) have basis \(z_1,\ldots,z_m\) over a characteristic-zero field and
let

\[
S_{\mathrm{sf}}^3U
=\langle z_i z_j z_k:i,j,k\ \text{distinct}\rangle.
\]

If \(0\ne f\in S_{\mathrm{sf}}^3U\), then the essential variable space of
\(f\) has dimension at least three.  Equivalently,

\[
S_{\mathrm{sf}}^3U\cap\operatorname{Sym}^3L=0
\qquad\text{for every }L\subset U\text{ with }\dim L\le2.
\]

### Proof

Squarefreeness gives

\[
\partial_{z_i}^2f=0\qquad(1\le i\le m).              \tag{4.1}
\]

Assume \(f\in\operatorname{Sym}^3L\), where \(\dim L\le2\).  The
restrictions of the coordinate covectors \(z_i^*\) span \(L^*\).

If \(\dim L=1\), write \(f=c\ell^3\).  Some restricted coordinate covector
\(\alpha\) is nonzero, and

\[
\partial_\alpha^2f=6c\alpha(\ell)^2\ell.
\]

Equation (4.1) forces \(c=0\).

If \(\dim L=2\), choose two coordinate covectors whose restrictions
\(\alpha,\beta\) form a basis of \(L^*\).  Choose coordinates \(u,v\) on
\(L\) so that \(\alpha=\partial_u\) and \(\beta=\partial_v\), and write

\[
f=a u^3+b u^2v+cuv^2+dv^3.
\]

Then (4.1) gives

\[
0=\partial_u^2f=6au+2bv,
\qquad
0=\partial_v^2f=2cu+6dv.
\]

Characteristic zero implies \(a=b=c=d=0\), again a contradiction.  Hence
no nonzero squarefree cubic has essential dimension at most two.

## 5. Consequence for the coupling lemma

In the \(k=2\) branch of the near-maximal coupling lemma, every component
\(q_i\) of the cubic relation lies in the same \(\operatorname{Sym}^3L\)
with \(\dim L=2\).  If the five factors of the corresponding Chow term are
independent, its cubic derivative space is squarefree in the factor basis,
so the lemma above forces \(q_i=0\).  Every nonzero component therefore comes
from a four-dimensional factor span.  For such a component
\(F_i=\operatorname{Sym}^2Y_i\); after the already established pure-cube
exclusion, the essential space of \(q_i\) is exactly \(L\subset Y_i\).
At least two components are nonzero, so two quadratic spaces contain the
common three-plane \(\operatorname{Sym}^2L\).  The quadratic relation kernel
then has dimension at least three, contradicting \(k=2\).

This supplies the missing proof obligation without changing the remainder of
the coupling argument.

## 6. Evidence classification after repair

| Statement | Classification |
|---|---|
| Low-rank classification and \(\dim(E\cap\operatorname{Sym}^2L)\le1\) | characteristic-zero proof |
| Closed incidence and quotient-rank preservation | characteristic-zero algebraic geometry |
| Coordinate endpoint maximum \(26\) | exact standalone finite certificate over \(\mathbf F_3\), used as a characteristic-zero upper bound |
| Binary-cubic exclusion | characteristic-zero proof |
| `ChowRank(perm_5)=16` | may be restored only after the complete v13 dependency chain is re-audited with this certificate included |
