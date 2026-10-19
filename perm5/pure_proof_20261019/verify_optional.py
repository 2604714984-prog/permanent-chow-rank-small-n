#!/usr/bin/env python3
"""Independent, optional exact regression tests for the perm5 pure proof.

The written manuscript does not invoke this program or its output as a
premise. Tests cover explicit identities and examples; they are not a
formal verification of the theorem. Python 3.11+; standard library only.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product, permutations
from math import comb
from pathlib import Path
from random import Random
import hashlib
import json
import sys
import time

Mon = tuple[int, ...]
Poly = dict[Mon, int | Fraction]


def require(condition: bool, description: str) -> None:
    # Explicit checks remain enabled with python -O and -OO.
    if not condition:
        raise AssertionError(description)


def clean(p: Poly) -> Poly:
    return {m: c for m, c in p.items() if c}


def add(*polys: Poly) -> Poly:
    out: Poly = {}
    for p in polys:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return clean(out)


def scale(p: Poly, scalar: int | Fraction) -> Poly:
    return clean({m: scalar * c for m, c in p.items()})


def multiply(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            mon = tuple(sorted(ma + mb))
            out[mon] = out.get(mon, 0) + ca * cb
    return clean(out)


def factors_product(factors: list[list[int | Fraction]]) -> Poly:
    out: Poly = {(): 1}
    for vector in factors:
        out = multiply(out, {(i,): c for i, c in enumerate(vector) if c})
    return out


def derivative(p: Poly, variable: int) -> Poly:
    out: Poly = {}
    for m, c in p.items():
        multiplicity = m.count(variable)
        if multiplicity:
            remaining = list(m)
            remaining.remove(variable)
            key = tuple(remaining)
            out[key] = out.get(key, 0) + multiplicity * c
    return clean(out)


def partials(p: Poly, variables: int, order: int) -> list[Poly]:
    out = []
    for indices in combinations_with_replacement(range(variables), order):
        q = p
        for j in indices:
            q = derivative(q, j)
        out.append(q)
    return out


def mon_index(variables: int, degree: int) -> dict[Mon, int]:
    return {m: i for i, m in enumerate(combinations_with_replacement(range(variables), degree))}


def col_of(p: Poly, index: dict[Mon, int]) -> dict[int, Fraction]:
    return {index[m]: Fraction(c) for m, c in p.items() if c}


def independent_indices(columns) -> list[int]:
    """Exact sparse elimination from raw columns, not stored pivots."""
    pivots: dict[int, dict[int, Fraction]] = {}
    selected = []
    for number, source in enumerate(columns):
        col = {r: Fraction(v) for r, v in source.items() if v}
        while col:
            lead = min(col)
            value = col[lead]
            if lead not in pivots:
                pivots[lead] = {r: v / value for r, v in col.items()}
                selected.append(number)
                break
            for r, v in pivots[lead].items():
                new = col.get(r, 0) - value * v
                if new:
                    col[r] = new
                else:
                    col.pop(r, None)
    return selected


def rank(columns) -> int:
    return len(independent_indices(columns))


def poly_basis(polys: list[Poly], variables: int, degree: int) -> list[Poly]:
    index = mon_index(variables, degree)
    ids = independent_indices(col_of(p, index) for p in polys)
    return [polys[i] for i in ids]


def matrix_columns(rows: list[list[int | Fraction]]) -> list[dict[int, Fraction]]:
    return [{i: Fraction(row[j]) for i, row in enumerate(rows) if row[j]}
            for j in range(len(rows[0]) if rows else 0)]


def matrix_rank(rows: list[list[int | Fraction]]) -> int:
    return rank(matrix_columns(rows))


def nullspace(rows: list[list[int | Fraction]], ncols: int) -> list[list[Fraction]]:
    a = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        divisor = a[r][c]
        a[r] = [x / divisor for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                coefficient = a[i][c]
                a[i] = [x - coefficient * y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    result = []
    for free in (i for i in range(ncols) if i not in pivots):
        vector = [Fraction(0)] * ncols
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -a[row][free]
        result.append(vector)
    return result


def quadratic_rank(q: Poly, ell: int) -> int:
    # Hessian, so no division-by-two convention is involved.
    return matrix_rank([[derivative(derivative(q, i), j).get((), 0)
                         for j in range(ell)] for i in range(ell)])


def polarization_rank(U: list[Poly], P: list[list[int | Fraction]], ell: int,
                      q: Poly | None) -> int:
    d = len(P)
    if not d:
        return 0
    idx = mon_index(ell, 2)
    width = len(idx)
    killed = []
    if q:
        for a in range(d):
            killed.append({a * width + idx[m]: Fraction(c) for m, c in q.items()})
    cols = []
    for g in U:
        col = {}
        for a in range(d):
            dg = add(*(scale(derivative(g, j), P[a][j]) for j in range(ell)))
            col.update({a * width + idx[m]: Fraction(c) for m, c in dg.items()})
        cols.append(col)
    return rank(killed + cols) - len(killed)


def symmetric_cubes(vectors: list[list[Fraction]]) -> list[Poly]:
    return [factors_product([vectors[j] for j in inds])
            for inds in combinations_with_replacement(range(len(vectors)), 3)]


def test_coordinate_symbols() -> dict:
    U = [{I: 1} for I in combinations(range(5), 3)]
    edges = list(combinations(range(5), 2))
    minima = [10] * 6
    total = 0
    for bits in product((0, 1), repeat=5):
        B = {j for j, bit in enumerate(bits) if bit}
        outside = [j for j in range(5) if j not in B]
        P = [[int(i == j) for j in range(5)] for i in outside]
        d = len(P)
        for e in [None] + edges:
            q = {e: 1} if e is not None else None
            actual = polarization_rank(U, P, 5, q)
            expected = 10 - comb(len(B), 3) - d * int(e is not None and set(e) <= B)
            require(actual == expected, f'coordinate formula failed: B={B}, e={e}')
            require(actual >= 2 * d, 'coordinate half-defect inequality')
            minima[d] = min(minima[d], actual)
            total += 1
    require(total == 352, 'coordinate test coverage')
    return {'pairs': total, 'minimum_ranks_by_d': minima, 'formula_matches': True}


def test_normal_form_identities() -> dict:
    identity = [[int(i == j) for j in range(4)] for i in range(4)]
    result = []
    for s in range(1, 5):
        T = factors_product(identity + [[int(i < s) for i in range(4)]])
        H = {(i, j): derivative(derivative(T, i), j)
             for i, j in combinations_with_replacement(range(4), 2)}
        U = poly_basis(list(H.values()), 4, 3)
        F = poly_basis(partials(T, 4, 3), 4, 2)
        require(len(U) == len(F), 'adjoint catalecticant dimensions')
        for j in range(4):
            expected = {tuple(i for i in range(4) if i != j): 2} if j < s else {}
            require(H[j, j] == expected, f'diagonal identity s={s}, j={j}')
        if s == 1:
            require(H[0, 1] == {(0, 2, 3): 2}, 's=1 needed actual cubic')
            require(len(U) <= 7, 's=1 dimension ceiling')
        if s == 2:
            require(add(H[0, 0], H[1, 1], scale(H[0, 1], -1)) == {}, 's=2 derivative relation')
            require(len(U) <= 7, 's=2 dimension ceiling')
        # A retained diagnostic: exact u is not needed for s=3,4 in the proof.
        result.append({'s': s, 'u_observed': len(U), 'identities_match': True})
    return {'normal_forms': result, 's3_s4_exact_ranks_are_not_proof_inputs': True}


def positive_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
    else:
        for first in range(1, total - parts + 2):
            for tail in positive_compositions(total - first, parts - 1):
                yield (first,) + tail


def test_divisor_formula() -> dict:
    checks = []
    for ell in range(1, 6):
        values = []
        for alpha in positive_compositions(5, ell):
            T = {tuple(i for i, a in enumerate(alpha) for _ in range(a)): 1}
            u = len(poly_basis(partials(T, ell, 2), ell, 3))
            predicted = comb(ell, 2) + sum(a >= 2 for a in alpha)
            require(u == predicted, f'divisor formula {alpha}')
            if ell <= 4:
                require(u >= comb(ell, 2) + 1, 'divisor lower bound')
            values.append(u)
        checks.append({'ell': ell, 'compositions': len(values), 'minimum_u': min(values)})
    return {'formula_matches': True, 'by_factor_span': checks}


def unimodular(ell: int, rng: Random) -> list[list[int]]:
    a = [[int(i == j) for j in range(ell)] for i in range(ell)]
    if ell == 1:
        return a
    for _ in range(2 * ell + 2):
        i, j = rng.sample(range(ell), 2)
        c = rng.choice((-2, -1, 1, 2))
        a[i] = [x + c * y for x, y in zip(a[i], a[j])]
    require(matrix_rank(a) == ell, 'unimodular generator rank')
    return a


def test_nonnormal_quotients() -> dict:
    rng = Random(20261019)
    products = []
    for ell in range(1, 6):
        coordinates = [[int(i == j) for j in range(ell)] for i in range(ell)]
        if ell == 4:
            for s in range(1, 5):
                products.append((ell, coordinates + [[int(i < s) for i in range(ell)]]))
        for sample in range(3):
            remaining = []
            for _ in range(5 - ell):
                vector = [rng.randint(-2, 2) for _ in range(ell)]
                if not any(vector):
                    vector[0] = 1
                remaining.append(vector)
            products.append((ell, coordinates + remaining))
    checked = small_kernel_checks = nonzero_R_checks = 0
    observed_min_slack = None
    for number, (ell, factors) in enumerate(products):
        T = factors_product(factors)
        U = poly_basis(partials(T, ell, 2), ell, 3)
        F = poly_basis(partials(T, ell, 3), ell, 2)
        u = len(U)
        require(u == len(F) <= 10, 'actual derivative image rank')
        R_choices: list[Poly | None] = [None]
        if ell >= 4:
            for _ in range(20):
                q = add(*(scale(g, rng.randint(-2, 2)) for g in F))
                if q and quadratic_rank(q, ell) >= 4:
                    R_choices.append(q)
                    break
            require(len(R_choices) == 2, 'construct an admissible rank-four-or-higher R')
        for d in range(ell + 1):
            for sample in range(3):
                whole = unimodular(ell, rng)
                P = whole[:d]
                k = ell - d
                S = nullspace(P, ell)
                require(len(S) == k, 'quotient kernel dimension')
                if k <= 2:
                    idx = mon_index(ell, 3)
                    cubes = symmetric_cubes(S)
                    intersection = u + len(cubes) - rank([col_of(g, idx) for g in U + cubes])
                for q in R_choices:
                    r = polarization_rank(U, P, ell, q)
                    slack_twice = 2 * r + 10 - u - 4 * d
                    require(slack_twice >= 0,
                            f'local half-defect: product={number}, ell={ell}, d={d}, q={bool(q)}')
                    if k <= 2:
                        require(u - r == intersection, 'small-complement exact kernel identity')
                        small_kernel_checks += 1
                    if q:
                        nonzero_R_checks += 1
                    observed_min_slack = slack_twice if observed_min_slack is None else min(observed_min_slack, slack_twice)
                    checked += 1
    return {'products': len(products), 'exact_quotient_checks': checked,
            'nonzero_rank_at_least_four_R_checks': nonzero_R_checks,
            'small_complement_kernel_checks': small_kernel_checks,
            'minimum_twice_slack': observed_min_slack,
            'seed': 20261019, 'sampling_is_not_a_proof': True}


def test_permanent_prolongation() -> dict:
    n, N = 5, 25
    quadratics = list(combinations_with_replacement(range(N), 2))
    paired = {}
    rectangles = []
    for i, k in combinations(range(n), 2):
        for j, l in combinations(range(n), 2):
            a = tuple(sorted((n * i + j, n * k + l)))
            b = tuple(sorted((n * i + l, n * k + j)))
            paired[b] = a
            rectangles.append(frozenset(a + b))
    qb = [m for m in quadratics if m not in paired]
    qi = {m: i for i, m in enumerate(qb)}
    width = len(qb)
    def constraints():
        for mon in combinations_with_replacement(range(N), 3):
            col = {}
            for j in set(mon):
                rem = list(mon)
                rem.remove(j)
                residual = tuple(rem)
                mult = mon.count(j)
                if residual in paired:
                    col[j * width + qi[paired[residual]]] = -mult
                else:
                    col[j * width + qi[residual]] = mult
            yield col
    dimension = comb(N + 2, 3) - rank(constraints())
    require(dimension == 100, 'full permanent cubic prolongation dimension')
    weights = [2 ** i + 2 ** (5 + j) for i in range(n) for j in range(n)]
    require(len(set(weights)) == 25, 'variable weights distinct')
    rect_weights = []
    for b, a in paired.items():
        wa, wb = sum(weights[j] for j in a), sum(weights[j] for j in b)
        require(wa == wb, 'rectangle weights agree')
        rect_weights.append(wa)
    require(len(set(rect_weights)) == 100, 'rectangle characters distinct')
    min_union = min(len(a | b) for a, b in combinations(rectangles, 2))
    require(min_union == 6, 'two rectangles need six or more variables')
    return {'quadratic_dimension': 100, 'cubic_prolongation_dimension_over_Q': dimension,
            'distinct_variable_weights': 25, 'distinct_rectangle_weights': 100,
            'minimum_two_rectangle_union': min_union}


def test_rectangular_inequality() -> dict:
    rng = Random(19052026)
    total = 0
    for m, n, count in ((2, 3, 2), (3, 2, 4), (5, 4, 3), (3, 3, 5)):
        for _ in range(10):
            matrices = [[[rng.randint(-2, 2) for _ in range(n)] for _ in range(m)] for _ in range(count)]
            if total % 2 == 0:
                matrices[1] = [[-x for x in row] for row in matrices[0]]
            summed = [[sum(a[i][j] for a in matrices) for j in range(n)] for i in range(m)]
            image_span = rank([col for a in matrices for col in matrix_columns(a)])
            row_span = matrix_rank([row for a in matrices for row in a])
            bound = image_span + row_span - sum(matrix_rank(a) for a in matrices)
            require(matrix_rank(summed) >= bound, 'rectangular inequality including cancellation')
            total += 1
    return {'exact_examples_including_cancellation': total}


def test_glynn() -> dict:
    coeff = {}
    for tail in product((-1, 1), repeat=4):
        eps = (1,) + tail
        weight = 1
        for sign in eps:
            weight *= sign
        for rows in product(range(5), repeat=5):
            value = weight
            for r in rows:
                value *= eps[r]
            coeff[rows] = coeff.get(rows, 0) + value
    for rows, value in coeff.items():
        require(value == (16 if len(set(rows)) == 5 else 0), 'integer Glynn identity')
    return {'expanded_choices': 16 * 5 ** 5, 'row_choice_monomials': len(coeff),
            'nonzero_monomials': sum(bool(v) for v in coeff.values()),
            'unnormalized_permutation_coefficient': 16}



def test_glynn_image_spans() -> dict:
    """Check the global dimensions on the actual known 16-term decomposition.

    Column-factor supports are disjoint, so these five factors are independent.
    Differentiation in row 0 of complementary columns extracts the pair/triple
    products exactly. Hence the spans below are actual derivative images.
    """
    F, U = [], []
    for tail in product((-1, 1), repeat=4):
        eps = (1,) + tail
        factors = [{(5 * i + j,): eps[i] for i in range(5)} for j in range(5)]
        for pair in combinations(range(5), 2):
            F.append(multiply(factors[pair[0]], factors[pair[1]]))
        for triple in combinations(range(5), 3):
            U.append(multiply(multiply(factors[triple[0]], factors[triple[1]]), factors[triple[2]]))
    E2, E3 = [], []
    for rows in combinations(range(5), 2):
        for cols in combinations(range(5), 2):
            E2.append({tuple(sorted((5*rows[0]+cols[0], 5*rows[1]+cols[1]))): 1,
                       tuple(sorted((5*rows[0]+cols[1], 5*rows[1]+cols[0]))): 1})
    for rows in combinations(range(5), 3):
        for cols in combinations(range(5), 3):
            E3.append({tuple(sorted(5*r+c for r,c in zip(rows,p))): 1 for p in permutations(cols)})
    qidx, cidx = mon_index(25, 2), mon_index(25, 3)
    dimF = rank(col_of(g, qidx) for g in F)
    dimU = rank(col_of(g, cidx) for g in U)
    require((dimF,dimU) == (110,150), 'Glynn derivative-image dimensions')
    require(rank(col_of(g,qidx) for g in F+E2) == dimF, 'E2 lies in Glynn image sum')
    require(rank(col_of(g,cidx) for g in U+E3) == dimU, 'E3 lies in Glynn image sum')
    require(dimF+dimU-160 == 100, 'rectangular inequality equality at Glynn')
    h2,h3,Delta,N = dimF-100,dimU-100,0,16
    require(h3 == 50-Delta/2 and h2+Delta/2 == 10*N-150, 'global bound sharp at Glynn')
    return {'terms':N, 'actual_pair_image_sum_dimension':dimF,
            'actual_cubic_image_sum_dimension':dimU, 'h2':h2,'h3':h3,'Delta':Delta,
            'global_inequalities_are_equalities':True}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('verification_results.json'))
    args = parser.parse_args()
    start = time.monotonic()
    results = {'proof_dependency': False, 'arithmetic': 'exact integers and rational fractions',
               'tests': {}}
    tests = [test_coordinate_symbols, test_normal_form_identities, test_divisor_formula,
             test_nonnormal_quotients, test_permanent_prolongation,
             test_rectangular_inequality, test_glynn, test_glynn_image_spans]
    for test in tests:
        print(f'RUN {test.__name__}', flush=True)
        results['tests'][test.__name__] = test()
    source = Path(__file__).with_name('main.tex')
    results.update(status='OPTIONAL_EXACT_CHECKS_PASS',
                   source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   python_version=sys.version.split()[0],
                   elapsed_seconds=round(time.monotonic() - start, 3))
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(results, indent=2, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
