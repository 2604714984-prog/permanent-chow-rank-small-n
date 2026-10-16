# Second-pass internal mathematical review — perm5 and perm6

Date: 2026-10-16. Starting commit: `ff27dd3377e341ae89e4fd9017cf3d174f51d7c8`.

Reviewed manuscripts: [perm5](../../submissions/20261016-r2/perm5/main.tex) and [perm6](../../submissions/20261016-r2/perm6/main.tex). This is an AI-assisted internal dependency audit, not external peer review, a proof-assistant formalization, or evidence of the author's final approval. No unfilled logical obligation was identified in the arguments reviewed below. That assessment is separate from the exact finite computations reported in `release_acceptance.json`.

## 1. Scope and proof objects

The statements concern ordinary Chow rank, with unrestricted homogeneous linear factors, over every field of characteristic zero. The proofs first work over an algebraic closure. A shorter decomposition over the original field would remain one over the closure, while the displayed upper bounds have rational coefficients. This correctly transfers equality back to every characteristic-zero field. Absorbing a scalar in one linear factor does not require taking a scalar root.

Neither manuscript proves border Chow rank, an arbitrary-n equality, or a theorem in positive characteristic. Tensor decompositions are a restricted class of product decompositions, so a tensor-rank lower bound cannot by itself establish the desired unrestricted Chow-rank lower bound. In particular the Han–Song reference is contextual rather than a substitute for the perm5 argument. Reference metadata and the withdrawn earlier work are treated separately in `REFERENCES_AND_ARXIV.md`.

Throughout, the relevant spaces are actual derivative images. A span of formal products of a dependent list of factors is not silently identified with an actual derivative space. The distinction is especially important in perm6, Remark 5.2.

## 2. Shared permanent geometry

For the spaces of 2-by-2 and 3-by-3 subpermanents, distinct row-column blocks have disjoint matching-monomial supports. Hence their dimensions are the squares of the corresponding binomial coefficients: perm5 has dimensions 100 and 100, while perm6 has dimensions 225 and 400. Differentiating a rectangle at one corner recovers its opposite variable, so the first derivatives of E2 span the full variable space.

The prolongation identity `E2^(1) = E3` is proved by coefficients: requiring every derivative of a cubic to lie in E2 forces matching monomials, and the rectangle relations equate the six matching coefficients inside each 3-by-3 block. Transpositions connect those six matchings. This is a written proof, not an inference from the dimension of one sampled matrix.

A new, separately implemented exact check reconstructs the entire coefficient system in `verify_prolongation_independent.py`. It uses rational weighted-graph equations, not the historical state tables or the primary verifier. Forbidden quadratic derivative monomials force coefficients to zero; rectangle relations give two-term equations. A surviving connected component is checked to be exactly the six equally weighted matchings of a 3-by-3 subpermanent.

| n | All cubic monomials | Forced-zero coefficients | Dimension of the surviving space |
|---|---:|---:|---:|
| 5 | 2,925 | 2,325 | 100 |
| 6 | 8,436 | 6,036 | 400 |

The row-column diagonal torus has distinct characters on the relevant subpermanent basis. Choosing a generic integral one-parameter subgroup isolates one nonzero basis term in a projective limit. Matrix rank, or first-derivative rank, cannot increase under specialization. The rank-four floor for nonzero quadrics in E2 follows from a single rectangle. In perm6 the analogous first-derivative calculation for a 3-by-3 permanent gives the nine-essential-variable floor for E3.

For a fixed dimension of L, the condition that `E2 intersect Sym^2 L` has dimension at least a specified value is a closed rank condition on a Grassmannian. It is stable under the row-column torus. Projectivity gives a fixed limit; distinct variable weights force that fixed subspace to be coordinate. A coordinate subspace is an edge set of the bipartite graph. Two distinct four-cycles use at least six edges; at six edges their union, when minimal, is K(2,3) or K(3,2), with exactly three four-cycles. This proves intersection bounds one for at most five variables and three for at most six. The rank/intersection semicontinuity directions used in the manuscripts are the required ones.

## 3. perm5: local bounds cover all factor spans

For a quintic product, put `F=D2(T)`, `U=D3(T)` and `u=dim F=dim U<=10`. Equality of the two dimensions is justified by transpose catalecticants under the natural differential pairing. With `R=F intersect E2`, the intersection bound gives `dim R<=1`, and every nonzero member of R has quadratic rank at least four.

Lemma 2.1 treats the projected polarization symbol when the kernel S of the first-factor quotient has dimension at most two. If all complementary derivatives of a kernel cubic lie in a nonzero line R, a change of complementary basis leaves only one possibly nonzero derivative. The cubic then uses S and at most one more variable. That derivative quadric has rank at most three, contradicting the rank-four floor. Thus the symbol kernel is precisely `U intersect Sym^3 S`. This argument does not assume that the factors are independent.

For five independent factors, the derivative spaces really are the squarefree pair and triple spaces. The factor-coordinate torus preserves them. Specializing the quotient kernel and R to coordinates gives the rank lower-bound row

```
d                         0  1  2  3   4   5
squarefree symbol rank    0  5  7  7  10  10
```

The finite domain has 352 cases. A specialized R need not retain the ambient rank-four floor; the squarefree counting bound deliberately uses only its dimension, so this loss creates no gap.

For a four-dimensional factor span, choosing four independent factors and normalizing the remaining linear relation gives the four displayed normal forms. Their actual derivative dimensions are 7, 7, 9 and 10. The manuscript's exact minors and column relations are checked by the short-proof verifier and its independent implementation. The rank-one quotient arguments use actual cubic members of U: in the first two cases a nonzero derivative supported on at most three variables cannot lie in R; in the other two cases projection modulo a variable produces the required independent pair monomials. They therefore address the rank-one case not supplied by the small-kernel estimate alone.

For smaller factor spans, one-parameter specialization of the product gives a monomial with positive exponents because an independent factor basis remains present. Catalecticant rank cannot rise at the limit. The positive-partition calculation gives the lower u-floors 1, 2 and 4, and 7 in factor dimension four. In characteristic zero the monomial derivative coefficients are nonzero, so counting its degree-two divisors is legitimate. Together with the kernel estimate and the four-dimensional rank-one cases this proves, for every quotient rank d,

```
rank(beta) + (10-u)/2 >= 2d.
```

No dependent-factor family is omitted: dimensions at most three use the general bound; dimension four uses the complete four-profile normal-form classification; dimension five uses the independent-factor case.

## 4. perm5: the endpoint N=15 is excluded explicitly

The rectangular image-span inequality is a Sylvester-rank argument. For the sum of the term catalecticants, let h2 and h3 be the excess dimensions of the sums of quadratic and cubic derivative spaces beyond 100, and let `Delta=sum(10-u_i)`. The manuscript obtains

```
h2 + h3 <= 10N - 100 - Delta.
```

After factoring the global quotient derivative map through U=sum(U_i), its kernel is exactly E3 by the prolongation identity, and therefore its rank is h3. On the original direct sum, the kernel consists of tuples whose sum lies in E3. A filtration by factor spans has increments whose sum is 25: this uses `E2 subset F` and `partial(E2)=V`. Projection kills the preceding filtration stage, so each new image increment is at least the current local symbol rank. The second-factor map `F_i/(F_i intersect E2) -> F/E2` is injective, as required. Summing the local inequality gives

```
h3 >= 50 - Delta/2,
h2 + Delta/2 <= 10N - 150.
```

Nonnegativity rules out N<=14. At N=15, both h2 and Delta must vanish. Then every F_i has dimension ten and lies inside E2, while it is supported on at most five variables. This contradicts the previously proved intersection bound of one. The endpoint is not left to numerical rounding or an unsupported strict inequality. The rational sixteen-term Glynn identity supplies the reverse bound.

## 5. perm6: quotient-symbol and dependent-factor cases

The squarefree symbol table, with rows indexed by the allowed relation dimension r and columns d=0,...,6, is

```
r=0: 0 10 16 19 20 20 20
r=1: 0  9 14 16 16 20 20
r=2: 0  8 12 13 16 19 20
r=3: 0  7 10 10 15 17 19
```

There are 45,696 parameterized cases `(r,B,A)`, not 45,696 distinct pairs after forgetting r. The count is `2^6 * (1 + 16 + 121 + 576)`. The r2 text makes the triple indexing explicit. The table values and all frozen certificates are unchanged. The independent verifier computes survival of each of the twenty source cubics without importing the primary implementation or reading its reference JSON.

For a factor span of dimension at most four, the general kernel-preimage bound uses `dim Sym^3 ker P + d dim R`. The positive-partition middle-rank floors are 1, 2, 4 and 8. For a full first-factor quotient, a kernel cubic would lie in E3 while using at most six variables, contradicting the nine-essential-variable floor. Minimizing the resulting bounds over the stated u-intervals yields the printed rows, each at least `10d/3` after adding `(20-u)/2`.

With six independent factors, u=20 and `dim R<=3`, not merely one. The last squarefree-table row, with the actual full-symbol injectivity improvement at d=6, gives `(0,7,10,10,15,17,20)` and the needed inequality.

With factor span five, the unique remaining relation is normalized to one of five forms `T_s=x1*x2*x3*x4*x5*(x1+...+x_s)`. This classification includes repeated factors. Exact differentiation gives the actual `(dim F,dim U)` pairs

```
s=1: (11,14)    s=2: (11,14)    s=3: (13,18)
s=4: (14,20)    s=5: (15,20).
```

For s=3 the displayed nine squarefree cubic members suffice; for s=4,5 all ten are present. For any nonzero direction, projection modulo a variable with nonzero directional coefficient exposes at least five, respectively six, independent pair monomials. Quotienting by R loses at most one dimension.

For s=1, a direction involving some x_j with j>=2 produces six independent pair monomials and one square after projection; the pure x1 direction has rank ten. For s=2, a direction involving j>=3 produces five pair monomials and two independent quadrics in x1,x2. A direction supported only on x1,x2 produces three independent pair monomials on x3,x4,x5, one nonzero image in each of three disjoint variable blocks, and a final nonzero quadratic in x1,x2. Thus the directional rank is at least seven in both cases, before quotienting by R.

At d=4, the quotient kernel is a line. The rank-four floor for a nonzero R rules out a kernel cubic with one nonzero complementary derivative: that derivative would use at most two variables. The symbol kernel therefore has dimension at most one. This is the load-bearing improvement for s=1,2, not a consequence of the coarse kernel-preimage estimate alone. At d=5 the full-symbol kernel is zero.

These arguments justify all cases of Proposition 5.1:

```
rank(beta) + (20-u)/2 >= (10/3)d.
```

The formal/actual dimension discrepancies are retained rather than normalized away: for T2 the formal pair/triple spans have dimensions 12/17, while the actual derivative spaces have dimensions 11/14; for T3 the formal triple span is 19 but the actual middle derivative space is 18. The replay explicitly tests these distinctions.

## 6. perm6: global cancellation

The middle catalecticants are symmetric for the natural bilinear differential pairing, not a Hermitian pairing. Factoring each through its image and applying Sylvester gives the symmetric image-span inequality without any positivity assumption. If the sum of the cubic derivative images has dimension `400+h` and `Delta=sum(20-u_i)`, it gives

```
h <= 10N - 200 - Delta/2.
```

After factoring through U=sum(U_i), the global projected derivative map again has kernel exactly E3; on the direct sum its kernel is the inverse image of E3 under addition. The factor-span increments sum to 36, and the injection of each actual quadratic quotient into the global quotient makes the filtered image-increment comparison valid. Summing Proposition 5.1 gives

```
h >= 120 - Delta/2.
```

The full individual defect cancels, giving N>=32. The rational thirty-two-term Glynn identity gives the matching upper bound. In particular the proof does not assume every summand has maximal middle rank.

## 7. What the executable evidence establishes

The original public programs, the two current standalone wrappers, the short-proof checks, the new full-cubic prolongation checker and the independent Glynn expansions were actually run. The Glynn programs cover 50,000 and 1,492,992 signed row choices, leaving respectively 120 and 720 permutation monomials. The perm6 independent graph enumeration covers 2,391,496 labelled edge sets.

The tests establish those finite algebraic premises and integrity properties; they do not mechanically certify projective specialization, the image-span arguments, or the global filtration reasoning. Those written steps were reviewed separately above. All nineteen Python files in the two active ancillary trees have no Python `assert` statements, and replay was additionally performed with inherited `PYTHONOPTIMIZE=0,1,2`.

The historical perm5 replay remains available and is also exercised for provenance. The current short proof does not inherit an unproved terminal-state claim from that historical route. The private perm5-v15 transport diagnosis in another repository is not evidence of a defect in these public packages; it was neither used as a theorem premise nor represented as repaired by this audit.
