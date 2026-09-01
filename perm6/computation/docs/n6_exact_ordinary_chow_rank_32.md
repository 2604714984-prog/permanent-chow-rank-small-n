# Exact ordinary Chow rank of the six-by-six permanent

## Status and scope

`EXACT ORDINARY-RANK THEOREM; POST-AUDIT LOCAL-SPACE REPAIR; EXACT FINITE REPLAY.`

Over an algebraically closed field of characteristic zero,

\[
\boxed{\operatorname{ChowRank}(\operatorname{perm}_6)=32.}
\]

This theorem concerns ordinary Chow rank. It makes no border-rank claim and
does not prove the conjectural formula for general \(n\).

Reviewer artifacts: [LaTeX source](n6_exact_ordinary_chow_rank_32.tex) and
[rendered PDF](n6_exact_ordinary_chow_rank_32.pdf).

The 2026-08-21 audit correctly observed that the earlier compact document did
not derive its local quotient-symbol rows. Reconstructing that derivation also
found a false shortcut in the longer source blueprint: for the five-variable
normal forms with support \(s=2,3\), the span of all formal squarefree
subproducts is larger than the actual derivative space. The proof below does
not use that shortcut. It works with the actual derivative spaces, replaces
the affected rows by weaker sufficient rows, and exposes every finite
calculation in the adjacent exact replay.

## 1. The permanent derivative tower

Let \(V=\langle x_{rc}:1\le r,c\le6\rangle\), and let
\(\mathcal D_j(f)\) denote the span of all derivatives of \(f\) whose
remaining degree is \(j\). Put

\[
E_j=\mathcal D_j(\operatorname{perm}_6).
\]

The \(3\times3\) and \(2\times2\) subpermanents are bases of \(E_3\) and
\(E_2\), respectively: distinct row-column blocks have disjoint matching
supports. Consequently

\[
\dim E_3=\binom63^2=400,
\qquad
\dim E_2=\binom62^2=225.                              \tag{1.1}
\]

Differentiating a rectangle permanent at one corner gives the opposite
variable, so

\[
\partial E_2=V.                                       \tag{1.2}
\]

Write

\[
E_2^{(1)}=\{g\in\operatorname{Sym}^3V:\partial g\subset E_2\}.
\]

Then

\[
\boxed{E_2^{(1)}=E_3.}                                \tag{1.3}
\]

The forward inclusion follows by differentiating a \(3\times3\)
subpermanent. Conversely, if every first derivative of a cubic \(g\) lies in
\(E_2\), row and column multiaffinity forces every monomial of \(g\) to be a
three-edge matching. Inside a fixed \(3\times3\) block, differentiating and
using the rectangle relations equates coefficients of matchings related by a
transposition. Transpositions connect all six matchings, so that block is a
scalar subpermanent. Summing over blocks proves (1.3).

Two rank floors will also be used. The row-column diagonal torus has distinct
weights on the subpermanent bases. A generic one-parameter subgroup therefore
degenerates every nonzero element to one basis element, while matrix and
first-catalectic ranks cannot increase in a limit. A rectangle permanent has
quadratic matrix rank four; the nine first derivatives of a \(3\times3\)
permanent are independent. Hence

\[
0\ne q\in E_2\Longrightarrow \operatorname{rank}(q)\ge4,
\qquad
0\ne g\in E_3\Longrightarrow \operatorname{essdim}(g)\ge9. \tag{1.4}
\]

## 2. Small intersections with permanent quadrics

If \(L\subset V\) has dimension at most six, then

\[
\dim(E_2\cap\operatorname{Sym}^2L)\le3,               \tag{2.1}
\]

and if \(\dim L\le5\), the right side improves to one.

For fixed \(a,q\), the locus in \(\operatorname{Gr}(a,V)\) where the
intersection has dimension at least \(q\) is closed, projective, and stable
under the connected row-column torus. If nonempty, the Borel fixed-point
theorem supplies a torus-fixed point. The variable weight spaces are
one-dimensional, so this point is a coordinate \(a\)-plane, represented by a
bipartite graph with \(a\) edges.

At such a point, the intersection has one independent rectangle permanent
for every four-cycle. Two distinct four-cycles use at least six edges. If
their union has exactly six edges, it is \(K_{2,3}\) or \(K_{3,2}\), which
has exactly three four-cycles. Thus a graph with at most five edges has at
most one four-cycle, and a graph with six edges has at most three. This proves
(2.1). The adjacent replay independently enumerates all row-permutation
reduced coordinate graphs with at most six edges.

## 3. Two local linear-algebra lemmas

Let \(L\) be an \(\ell\)-dimensional space. Polarization gives an injective
map

\[
\delta:\operatorname{Sym}^3L\longrightarrow
L\otimes\operatorname{Sym}^2L.
\]

If \(P:L\twoheadrightarrow D\) has rank \(d\), \(S=\ker P\), and
\(R\subset\operatorname{Sym}^2L\), then

\[
\ker((P\otimes1)\delta)=\operatorname{Sym}^3S.
\]

The inverse image of \(D\otimes R\) therefore has dimension at most

\[
\boxed{\binom{\ell-d+2}{3}+d\dim R.}                  \tag{3.1}
\]

This is only the dimension of the first kernel plus the dimension of the
target subspace; no transversality is assumed.

For the second lemma, let \(\widehat L=k^6\) with basis
\(z_1,\ldots,z_6\), and let \(\widehat F,\widehat U\) be the squarefree
quadratic and cubic spaces. On basis cubics,

\[
\delta(z_az_bz_c)=
z_a\otimes z_bz_c+z_b\otimes z_az_c+z_c\otimes z_az_b.
\]

For a rank-\(d\) quotient \(P\) and a subspace
\(R\subset\widehat F\) of dimension at most \(r\le3\), the following is a
universal lower-bound table for
\(\operatorname{rank}((P\otimes q_R)\delta)\):

\[
\begin{array}{c|rrrrrrr}
r\backslash d&0&1&2&3&4&5&6\\ \hline
0&0&10&16&19&20&20&20\\
1&0&9&14&16&16&20&20\\
2&0&8&12&13&16&19&20\\
3&0&7&10&10&15&17&19.
\end{array}                                             \tag{3.2}
\]

Indeed, the diagonal torus preserves the map. The closure of the orbit of
the pair \((\ker P,R)\) in the relevant product of Grassmannians contains a
fixed point, and rank can only fall in specialization. At a fixed point,
\(\ker P\) is a vertex set \(B\), and \(R\) is spanned by an edge set
\(A\) with at most \(r\) edges. Put \(O=[6]\setminus B\). Distinct source
cubics have disjoint output supports. The number of killed cubics is exactly

\[
\binom{|B|}{3}
+|O|e_A(B)
+\sum_{b\in B}\binom{\deg_A(b,O)}2
+\#\{\text{triangles of }A[O]\}.                       \tag{3.3}
\]

Inspecting edge sets of size at most three gives (3.2). The exact replay
checks all 45,696 coordinate pairs and records a minimizer for every entry.

## 4. The half-defect quotient-symbol lemma

Let

\[
T=\ell_1\cdots\ell_6\ne0,
\quad L=\langle\ell_1,\ldots,\ell_6\rangle,
\quad U=\mathcal D_3(T),
\quad F=\mathcal D_2(T),
\]

and put \(u=\dim U\) and \(R=F\cap E_2\). For every quotient
\(P:L\twoheadrightarrow D\) of rank \(d\), define the actual quotient
symbol

\[
\beta_{P,R}:U\xrightarrow{\delta}L\otimes F
\xrightarrow{P\otimes q_R}D\otimes(F/R).
\]

Then

\[
\boxed{
\operatorname{rank}\beta_{P,R}+\frac{20-u}{2}
\ge\frac{10}{3}d.}                                    \tag{4.1}
\]

The quotient is taken from the actual factor span. It may be an arbitrary
quotient of that span.

### 4.1. Factor-span dimension at most four

Let \(\ell=\dim L\le4\). Choose \(\ell\) independent factors as
coordinates. A generic diagonal one-parameter subgroup degenerates the other
factors to unique coordinate initials, so \(T\) specializes to

\[
x_1^{m_1}\cdots x_\ell^{m_\ell},
\qquad m_j\ge1,
\qquad\sum_jm_j=6.
\]

Middle catalectic rank cannot increase in specialization. Counting
degree-three divisors over the positive partitions of six gives

\[
\ell=1,2,3,4\quad\Longrightarrow\quad u\ge1,2,4,8.    \tag{4.2}
\]

By (2.1), \(\dim R\le1\). For \(0<d<\ell\), (3.1) gives

\[
\operatorname{rank}\beta_{P,R}\ge
\max\left\{0,u-\binom{\ell-d+2}{3}-d\right\}.         \tag{4.3}
\]

When \(d=\ell\), a kernel cubic has all first derivatives in \(E_2\), so
it lies in \(E_2^{(1)}=E_3\). But it belongs to
\(\operatorname{Sym}^3L\), whose essential-variable dimension is at most
six, contradicting (1.4). Thus the full symbol is injective. Minimizing over
the conservative range from (4.2) to
\(\min\{20,\binom{\ell+2}{3}\}\) gives the rows

\[
\begin{array}{c|c}
\ell&
\operatorname{rank}\beta_{P,R}+(20-u)/2,quad d=0,\ldots,\ell\\ \hline
4&(0,9/2,8,10,14)\\
3&(5,15/2,9,12)\\
2&(8,9,11)\\
1&(19/2,21/2).
\end{array}                                             \tag{4.4}
\]

Every entry dominates \(10d/3\).

### 4.2. Six independent factors

If \(\ell=6\), then \(u=20\), and the actual spaces identify with the
squarefree spaces in Section 3. Equation (2.1) gives \(\dim R\le3\), so the
last row of (3.2) applies. At \(d=6\), the preceding full-symbol argument
improves the last entry from 19 to 20. Thus a valid rank row is

\[
(0,7,10,10,15,17,20),                                  \tag{4.5}
\]

which again dominates \(10d/3\).

### 4.3. Five-dimensional factor span: actual derivative spaces

If \(\ell=5\), the unique factor relation puts \(T\), after changing and
rescaling coordinates, into exactly one of the forms

\[
T_s=x_1x_2x_3x_4x_5(x_1+\cdots+x_s),
\qquad1\le s\le5.                                      \tag{4.6}
\]

Here \(\dim R\le1\) by (2.1). Direct differentiation of the actual
polynomial gives

\[
\begin{array}{c|rrrrr}
s&1&2&3&4&5\\ \hline
\dim F&11&11&13&14&15\\
u&14&14&18&20&20.
\end{array}                                             \tag{4.7}
\]

For auditability, (4.7) is the exact rank of the matrix whose columns are
the order-four or order-three partial derivatives of the explicitly displayed
polynomial (4.6), in the ordinary monomial basis. The adjacent replay builds
these matrices over \(\mathbf Q\) and row-reduces them exactly.

For \(s=3\), \(U\) contains the nine squarefree cubics other than
\(x_1x_2x_3\). For \(s=4,5\), it contains all ten squarefree cubics. Call
these torus-stable subspaces \(H_s\). Under a nonzero rank-one quotient, the
diagonal torus specializes the defining functional to a coordinate
functional. Its rank on \(H_s\) is the number of displayed triples containing
that coordinate: at least five for \(s=3\), and six for \(s=4,5\).
Quotienting the quadratic target by \(R\) loses at most one rank. Combining
this rank-one bound, (3.1), and full-symbol injectivity gives the sufficient
adjusted rows

\[
\begin{array}{c|c|c}
s&u&\operatorname{rank}\beta_{P,R}+(20-u)/2\\ \hline
4,5&20&(0,5,8,13,15,20)\\
3&18&(1,5,7,12,14,19).
\end{array}                                             \tag{4.8}
\]

It remains to treat \(s=1,2\). In both cases \(u=14\). For
\(T_1=x_1^2x_2x_3x_4x_5\), the space \(U\) is spanned by the ten squarefree
cubics and the four cubics \(x_1^2x_j\), \(2\le j\le5\). If a direction
\(\lambda=\sum a_j\partial_{x_j}\) has \(a_j\ne0\) for some \(j\ge2\),
project modulo \(x_jL\). The six squarefree cubics divisible by \(x_j\) and
\(x_1^2x_j\) give seven independent quadrics. In the pure \(x_1\) direction,
the rank is ten.

For \(T_2=x_1x_2x_3x_4x_5(x_1+x_2)\), a basis of \(U\) consists of the
seven squarefree cubics containing at most one of \(x_1,x_2\), the six
cubics

\[
x_2^2x_j+2x_1x_2x_j,
\qquad
x_1x_2x_j+\tfrac12x_1^2x_j
\quad(3\le j\le5),
\]

and \(x_1x_2(x_1+x_2)\). If some \(a_j\ne0\), \(j\ge3\), seven basis
members divisible by \(x_j\) have independent images modulo \(x_jL\). If
\(\lambda=a_1\partial_{x_1}+a_2\partial_{x_2}\), the image contains the
three pair monomials on \(x_3,x_4,x_5\), one nonzero direction in each
\(\langle x_1x_j,x_2x_j\rangle\), and the nonzero quadratic

\[
a_2x_1^2+2(a_1+a_2)x_1x_2+a_1x_2^2.
\]

These seven directions have disjoint monomial supports. Thus every nonzero
directional map has rank at least seven; after quotienting by \(R\), every
positive-rank symbol has rank at least six.

For \(d=4\), let \(S=\ker P\) be a line and let \(v\) lie in the symbol
kernel. The four complementary derivatives of \(v\) span a subspace of
\(R\), hence have dimension at most one. If that span were nonzero, the full
essential-variable space of \(v\) would have dimension at most two and would
support a nonzero member of \(E_2\), contradicting the rank-four floor in
(1.4). Therefore \(v\in\operatorname{Sym}^3S\), and the kernel has dimension
at most one. At \(d=5\), the full symbol is injective. With (3.1), these facts
give

\[
\operatorname{rank}\beta_{P,R}+(20-u)/2
\ge(3,9,9,10,16,17).                                   \tag{4.9}
\]

The rows (4.8)--(4.9) dominate \(10d/3\), proving (4.1) in the final
factor-span dimension. Notice that the repaired proof never identifies the
formal squarefree subproduct span with the actual derivative space in the
\(s=2,3\) cases.

## 5. Symmetric image-span inequality

Let \(A_i:W^*\to W\) be symmetric linear maps, let
\(r_i=\operatorname{rank}A_i\), and put
\(D=\dim\sum_i\operatorname{im}A_i\). Then

\[
\operatorname{rank}\Bigl(\sum_iA_i\Bigr)
\ge2D-\sum_i r_i.                                      \tag{5.1}
\]

Choose \(B_i:k^{r_i}\to W\) onto \(\operatorname{im}A_i\). Symmetry gives
\(\ker A_i=(\operatorname{im}A_i)^\perp\), so the induced form on the rank
quotient is nondegenerate and
\(A_i=B_iJ_iB_i^*\) for an invertible symmetric \(J_i\). With
\(B=[B_1\ \cdots\ B_N]\) and block-diagonal \(J\), Sylvester's rank
inequality gives

\[
\operatorname{rank}(BJB^*)
\ge\operatorname{rank}(BJ)+\operatorname{rank}(B^*)-\sum_i r_i
=2D-\sum_i r_i.
\]

## 6. The global quotient derivative symbol

Suppose

\[
\operatorname{perm}_6=\sum_{i=1}^N T_i
\]

with no zero summands. Let

\[
A_i=C_{3,3}(T_i),
\quad U_i=\operatorname{im}A_i,
\quad u_i=\dim U_i,
\quad\delta_i=20-u_i,
\quad\Delta=\sum_i\delta_i.
\]

Put \(U=\sum_iU_i\) and \(\dim U=400+h\). The sum of the symmetric maps
\(A_i\) is the permanent middle catalecticant, with rank 400 and image
\(E_3\). Applying (5.1) gives

\[
400\ge2(400+h)-(20N-\Delta),
\]

or

\[
\boxed{h\le10N-200-\frac\Delta2.}                      \tag{6.1}
\]

Now put \(F_i=\mathcal D_2(T_i)\), \(F=\sum_iF_i\), and \(Q=F/E_2\).
Differentiating the decomposition twice gives \(E_2\subset F\). Blockwise
differentiation modulo \(E_2\) defines

\[
\widetilde\beta:\bigoplus_iU_i\longrightarrow V\otimes Q.
\]

For a tuple \((g_i)\), its image is zero precisely when every first
derivative of \(\sum_i g_i\) lies in \(E_2\). By (1.3), this is equivalent
to \(\sum_i g_i\in E_3\). Since \(E_3\subset U\), the image of
\(\widetilde\beta\) is an injective copy of \(U/E_3\), and hence

\[
\operatorname{rank}\widetilde\beta=h.                 \tag{6.2}
\]

## 7. Factor filtration and cancellation

Let \(L_i\) be the actual factor span of \(T_i\). From
\(E_2\subset F\), (1.2), and \(\partial F_i\subset L_i\),

\[
V=\partial E_2\subset\sum_iL_i.
\]

Thus the factor spans generate all 36 variables. Choose any ordering, put

\[
W_i=\sum_{j\le i}L_j,
\qquad
d_i=\dim(W_i/W_{i-1}),
\]

so \(\sum_i d_i=36\). Let \(Z_i\subset L_i\otimes Q\) be the image of the
\(i\)-th symbol block and \(H_i=\sum_{j\le i}Z_j\). Projection

\[
\pi_i:W_i\otimes Q\longrightarrow(W_i/W_{i-1})\otimes Q
\]

kills \(H_{i-1}\), and therefore

\[
\dim H_i-\dim H_{i-1}\ge\dim\pi_i(H_i)=\dim\pi_i(Z_i). \tag{7.1}
\]

On the current block, the first-factor map is the arbitrary quotient

\[
P_i:L_i\twoheadrightarrow L_i/(L_i\cap W_{i-1}),
\qquad\operatorname{rank}P_i=d_i.
\]

The natural map

\[
F_i/(F_i\cap E_2)\longrightarrow F/E_2=Q
\]

is injective. Hence \(\dim\pi_i(Z_i)\) is exactly the rank of the local
symbol in (4.1), with \(R_i=F_i\cap E_2\). Summing (7.1) and (4.1) gives

\[
\boxed{h\ge\sum_i\left(\frac{10}{3}d_i-\frac{\delta_i}{2}\right)
=120-\frac\Delta2.}                                    \tag{7.2}
\]

Comparing (6.1) and (7.2) cancels the complete individual middle-rank
defect:

\[
120-\frac\Delta2
\le10N-200-\frac\Delta2,
\]

so \(N\ge32\).

Glynn's identity supplies the matching upper bound:

\[
\operatorname{perm}_6=
\frac1{32}
\sum_{\epsilon_1=1,\ \epsilon_2,\ldots,\epsilon_6=\pm1}
\left(\prod_{r=1}^6\epsilon_r\right)
\prod_{c=1}^6\left(\sum_{r=1}^6\epsilon_rx_{rc}\right).
\]

Walsh cancellation leaves exactly the monomials using every row once. This
is a 32-term ordinary Chow decomposition, completing the proof.

## 8. Exact replay and audit boundary

```text
python scripts/n6_exact_ordinary_chow_rank_32.py \
  --verify-json data/n6_exact_ordinary_chow_rank_32.json
python -m unittest tests.test_n6_exact_ordinary_chow_rank_32 -v
```

The replay derives the finite coordinate-intersection maxima, all 45,696
coordinate cases behind (3.2), the actual derivative ranks and squarefree
subspaces in (4.7)--(4.8), the low-span monomial floors, and the final
cancellation. It also records the formal/actual mismatches at \(s=2,3\), so
the rejected shortcut cannot silently re-enter the proof.

The torus fixed-point reductions, prolongation identity, elementary
directional-shadow cases, symmetric image-span lemma, and global filtration
are written arguments, not conclusions inferred from the replay. The theorem
makes no statement about border Chow rank.
