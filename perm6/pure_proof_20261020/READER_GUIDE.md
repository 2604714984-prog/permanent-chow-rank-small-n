# Understanding the computation-free perm6 proof

## 1. The result and the real task

The theorem is about ordinary Chow rank. A summand is a product of six linear forms, and each form may involve all 36 matrix variables. It is not restricted to one assigned row or column. The goal is to show that 32 such summands suffice and that 31 or fewer cannot suffice.

The upper bound is Glynn's identity. The difficulty is the lower bound. The new manuscript keeps the earlier proof's global strategy but replaces every computer-dependent local endpoint.

The most important part to read is Section 5, particularly its five-dimensional factor-span case. This is where a new argument removes the need to know the five exact dependent-factor rank profiles.

## 2. What the permanent's derivatives remember

Write `E2` for the space of degree-two derivatives of the permanent and `E3` for its degree-three derivatives. These are spaces of remaining degree, not the order of differentiation: for a sextic, obtaining a quadratic means differentiating four times.

The rectangle permanents form a 225-dimensional basis of `E2`. The three-by-three subpermanents form a 400-dimensional basis of `E3`. Their monomial supports make the dimensions transparent.

A cubic whose every derivative lies in `E2` must belong to `E3`. A repeated row or column would leave a forbidden quadratic after differentiation. On a fixed three-by-three block, the rectangle coefficient relations force all six matching coefficients to agree. Thus the cubic is a sum of subpermanents.

Two further facts limit what a single Chow term can share with the permanent. Every nonzero quadratic in `E2` has rank at least four. Also, if at most six linear variables support a quadratic subspace, its intersection with `E2` has dimension at most three; with at most five variables, the dimension is at most one.

The latter bound has a short graph proof. Row-column scaling reduces to a coordinate subspace, represented by edges of a bipartite graph. Supported rectangle permanents are four-cycles. Two distinct four-cycles already need at least six edges. At exactly six edges their union is a complete two-by-three graph and has three cycles. This replaces the labelled-graph enumeration.

## 3. The local estimate

For one Chow term `T`, let `L` be the span of its six factors, `U` its actual cubic derivative space, and `u = dim U`. Always `u <= 20`. The quantity `20-u` records how much middle rank the term loses through dependencies among its factors.

Take any quotient of `L` with dimension `d`. Differentiate cubics in `U`, keep the first factor only modulo that quotient, and remove the quadratic directions already belonging to `E2`. The resulting linear map is called `beta` in the paper.

The local target is

\[
 \operatorname{rank}\beta+\frac{20-u}{2}\ge\frac{10}{3}d.
\]

It says that a term either contributes enough genuinely new derivative information or has a sufficiently large middle-rank deficit to compensate. It must hold for every quotient, not just a generic one.

For factor spans of dimension at most four, the small-complement kernel argument and a simple scalar inequality suffice. The monomial rank floors are obtained from the divisor formula

\[
 \binom{\ell}{3}+(\ell-1)\#\{i:\alpha_i\ge2\}
                  +\#\{i:\alpha_i\ge3\},
\]

where the positive exponents sum to six. No partition enumeration is required.

For six independent factors, the actual derivative spaces are squarefree. A cubic is indexed by three vertices. Its polarization has three vertex-edge entries, and different triples have disjoint output supports. Therefore one can count surviving columns exactly. With at most three killed edges, a union bound handles quotient dimensions up to three; dimensions four and five require only short edge-count arguments. At dimension six the actual symbol is injective by the permanent's cubic structure. A generic three-edge quotient need not be injective, and the manuscript explicitly keeps that distinction.

## 4. The main simplification: complete a small squarefree space

The remaining factor span has dimension five. After choosing independent factors as coordinates, the term is one of

\[
 T_s=x_1x_2x_3x_4x_5(x_1+\cdots+x_s),\qquad1\le s\le5.
\]

Quotient dimensions three, four and five are already controlled by the small-complement argument. Only dimensions one and two need additional work.

Let `H` be the full ten-dimensional squarefree cubic space on the five coordinates. The corresponding quotient-symbol rank is at least five for a one-dimensional quotient and at least seven for a two-dimensional quotient. These bounds follow from one formula counting killed triples; no table of 352 cases is needed.

The actual derivative space need not contain all of `H`. Instead find an explicit `U0` contained in both, and set

\[
 m=10-\dim U_0.
\]

Restricting a linear map from `H` to `U0` loses at most `m` in rank. Thus it is enough to show that `(20-u)/2` pays for those missing directions.

For `s=1,4,5`, all ten squarefree cubics are actual derivatives, so `m=0`.

For `s=2`, seven are explicit derivatives, so `m=3`. Factor the polynomial into a binary cubic and a squarefree cubic on the other three variables. The derivative space splits by bidegree. Its dimension is at most

\[
 1\cdot1+2\cdot3+2\cdot3+1\cdot1=14.
\]

Therefore `(20-u)/2 >= 3`, exactly what is needed.

For `s=3`, nine squarefree cubics are explicit derivatives, so `m=1`. Factor the polynomial into a quartic on three variables and a quadratic on the other two. Bidegrees give the upper bound

\[
 u\le3\cdot1+6\cdot2+3\cdot1=18.
\]

Therefore `(20-u)/2 >= 1`.

The common conclusion is

\[
 \operatorname{rank}\beta+\frac{20-u}{2}
 \ge a_d-m+\frac{20-u}{2}\ge a_d,
 \qquad a_1=5,\quad a_2=7.
\]

Both values exceed `10d/3` for the required dimensions. This closes the local estimate without computing any of the five exact normal-form ranks.

An important detail: the completed squarefree space is only a comparison space. Both maps are viewed in the same ambient quadratic quotient. The paper never identifies a formal product span with the actual derivative space. That is crucial in the second and third normal forms, where those spaces have different dimensions.

## 5. Why the local estimate forces 32 terms

Suppose an actual decomposition has `N` terms. Let `Delta` be the sum of their middle-rank deficits, and let `400+h` be the dimension of the sum of their actual cubic derivative spaces.

The symmetric middle-catalecticant inequality gives

\[
 h\le10N-200-\Delta/2.
\]

Independently, add the factor spans one at a time. At each step project away the previously introduced variables. The resulting new-variable dimensions add to 36 because the permanent uses every matrix variable. Applying the local estimate at each step gives

\[
 h\ge120-\Delta/2.
\]

This summation is justified by projecting each new image before counting its dimension; it does not assume that different terms have independent derivative images.

The same defect occurs in both inequalities. Cancelling it gives `120 <= 10N-200`, hence `N >= 32`. Together with Glynn's explicit 32-term sum, this proves the equality.

## 6. What the optional tests do

The program checks that the formulas agree with direct rational linear algebra, including nongeneric coordinate-boundary quotients and rank-four killed quadratic lines. It checks the actual derivative spaces rather than larger formal spans, verifies the permanent prolongation, and expands Glynn's identity over the integers.

It also checks the actual Glynn decomposition globally: the sum of cubic derivative images has dimension 520, so `h=120`, and every term has middle rank 20, so `Delta=0`. Both global inequalities are equalities in this example. The quotient derivative map is reconstructed separately, not merely assigned the expected rank by subtraction.

These checks can reveal mistakes, but they are not proof premises. The manuscript proves all parameter cases in writing. It has received an internal review, not external peer review or formal proof-assistant certification.
