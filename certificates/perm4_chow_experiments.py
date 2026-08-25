"""Reproducible checks for the Chow/product rank of perm_4.

This script verifies:
  1. Glynn's formula gives a Chow decomposition of perm_4 with 8 terms.
  2. The symmetric Koszul flattening P_{2,2}^{wedge 1} gives
     rank(flattening(perm_4)) = 560.
  3. The same flattening has rank 92 on a generic completely decomposable
     quartic l1*l2*l3*l4, so border Chow rank >= ceil(560/92) = 7.

The rank computations are done over a large prime field. Since the matrices have
integer entries, a rank found modulo p is a certificate that the characteristic
zero rank is at least that value. The single-product rank 92 is also checked by
direct evaluation on x0*x1*x2*x3.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations, product
from math import ceil

MOD = 1_000_003
N = 16
D = 4


def multiset_basis(deg: int):
    return list(combinations_with_replacement(range(N), deg))


def wedge_add(a: int, tup: tuple[int, ...]):
    if a in tup:
        return 0, None
    inversions = sum(1 for x in tup if a > x)
    sign = MOD - 1 if inversions % 2 else 1
    return sign, tuple(sorted((a,) + tup))


def perm4_poly():
    poly = defaultdict(int)
    for sigma in permutations(range(4)):
        mon = tuple(sorted(4 * row + sigma[row] for row in range(4)))
        poly[mon] += 1
    return dict(poly)


def chow_monomial_poly():
    return {(0, 1, 2, 3): 1}


def deriv_coeff(mon: tuple[int, ...], der: tuple[int, ...]):
    cm = Counter(mon)
    cd = Counter(der)
    for i, r in cd.items():
        if r > cm.get(i, 0):
            return 0, None
    coeff = 1
    rest = []
    for i, c in cm.items():
        r = cd.get(i, 0)
        for t in range(r):
            coeff *= c - t
        rest += [i] * (c - r)
    return coeff % MOD, tuple(sorted(rest))


def koszul_columns(poly, k: int, p: int):
    """Columns for P_{k,d-k}^{wedge p}: S^k V* x Lambda^p V -> S^{d-k-1} V x Lambda^{p+1} V."""
    bp = list(combinations(range(N), p))
    bp1 = list(combinations(range(N), p + 1))
    sk = multiset_basis(k)
    sleft = multiset_basis(D - k - 1)
    row_index = {
        (s, w): idx
        for idx, (s, w) in enumerate((s, w) for s in sleft for w in bp1)
    }

    derivs = {der: defaultdict(int) for der in sk}
    for mon, c in poly.items():
        for der in sk:
            coeff, rest = deriv_coeff(mon, der)
            if coeff:
                derivs[der][rest] = (derivs[der][rest] + c * coeff) % MOD

    for der in sk:
        dct = derivs[der]
        for wedge in bp:
            col = {}
            for rest, c in dct.items():
                for idx, a in enumerate(rest):
                    left = list(rest)
                    left.pop(idx)
                    left = tuple(left)
                    sign, wedge2 = wedge_add(a, wedge)
                    if sign:
                        row = row_index[(left, wedge2)]
                        col[row] = (col.get(row, 0) + sign * c) % MOD
            yield {r: v for r, v in col.items() if v}


def sparse_rank_mod(columns):
    pivots = {}
    rank = 0
    for col in columns:
        col = dict(col)
        while col:
            piv = min(col)
            val = col[piv] % MOD
            if not val:
                del col[piv]
                continue
            if piv not in pivots:
                inv = pow(val, MOD - 2, MOD)
                for r in list(col):
                    nv = col[r] * inv % MOD
                    if nv:
                        col[r] = nv
                    else:
                        del col[r]
                pivots[piv] = col
                rank += 1
                break
            basis = pivots[piv]
            factor = val
            for r, bv in basis.items():
                nv = (col.get(r, 0) - factor * bv) % MOD
                if nv:
                    col[r] = nv
                elif r in col:
                    del col[r]
    return rank


def glynn_coefficients():
    coeffs = defaultdict(float)
    for eps_tail in product([1, -1], repeat=3):
        eps = (1,) + eps_tail
        weight = 1
        for e in eps:
            weight *= e
        weight /= 8
        for cols in product(range(4), repeat=4):
            # The product over columns j of sum_i eps_i*x_{i,j}.
            mon = tuple(sorted(4 * row + col for col, row in enumerate(cols)))
            coeff = weight
            for row in cols:
                coeff *= eps[row]
            coeffs[mon] += coeff
    return coeffs


def verify_glynn():
    target = perm4_poly()
    coeffs = glynn_coefficients()
    support = set(target) | set(coeffs)
    return max(abs(coeffs.get(m, 0.0) - target.get(m, 0)) for m in support)


def main():
    glynn_error = verify_glynn()
    rank_perm = sparse_rank_mod(koszul_columns(perm4_poly(), k=2, p=1))
    rank_term = sparse_rank_mod(koszul_columns(chow_monomial_poly(), k=2, p=1))
    print(f"Glynn max coefficient error: {glynn_error:g}")
    print(f"rank P_{{2,2}}^wedge1(perm_4): {rank_perm}")
    print(f"rank P_{{2,2}}^wedge1(x0*x1*x2*x3): {rank_term}")
    print(f"certified Chow-rank lower bound: ceil({rank_perm}/{rank_term}) = {ceil(rank_perm / rank_term)}")


if __name__ == "__main__":
    main()
