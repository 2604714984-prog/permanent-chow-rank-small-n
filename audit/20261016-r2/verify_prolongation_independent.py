#!/usr/bin/env python3
"""Independent exact coefficient-graph check of E2^(1)=E3 for n=5,6.

Uses the whole cubic monomial space, not a stored state table or the primary
verifier. This finite linear-algebra check does not certify the torus,
quotient-symbol or global filtration proofs.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
import argparse
import json
from math import comb
from pathlib import Path


def require(test: bool, message: str) -> None:
    if not test:
        raise RuntimeError(message)


def check(n: int) -> dict:
    variables = tuple(range(n*n))
    quadratics = list(combinations_with_replacement(variables, 2))
    cubics = list(combinations_with_replacement(variables, 3))
    index = {monomial: i for i, monomial in enumerate(cubics)}
    rectangles = []
    for rows in combinations(range(n), 2):
        for cols in combinations(range(n), 2):
            rectangles.append((tuple(sorted((rows[0]*n+cols[0], rows[1]*n+cols[1]))),
                               tuple(sorted((rows[0]*n+cols[1], rows[1]*n+cols[0])))))
    allowed = {q for pair in rectangles for q in pair}
    require(len(allowed) == 2*comb(n, 2)**2, 'overlapping E2 supports')
    zero = set()
    graph = [[] for _ in cubics]
    equations = 0
    for v in variables:
        for q in quadratics:
            if q not in allowed:
                zero.add(index[tuple(sorted(q+(v,)))])
        for q, other in rectangles:
            i = index[tuple(sorted(q+(v,)))]
            j = index[tuple(sorted(other+(v,)))]
            a, b = q.count(v)+1, other.count(v)+1
            # a*c_i = b*c_j, so c_j = (a/b)*c_i.
            graph[i].append((j, Fraction(a, b)))
            graph[j].append((i, Fraction(b, a)))
            equations += 1
    seen = set()
    basis_supports = set()
    forced_count = 0
    for start in range(len(cubics)):
        if start in seen:
            continue
        values = {start: Fraction(1)}
        queue = [start]
        forced = False
        while queue:
            i = queue.pop()
            seen.add(i)
            forced |= i in zero
            for j, ratio in graph[i]:
                value = values[i]*ratio
                if j in values:
                    forced |= values[j] != value
                else:
                    values[j] = value
                    queue.append(j)
        if forced:
            forced_count += len(values)
            continue
        require(len(values) == 6, 'non-permanent component size')
        require(set(values.values()) == {Fraction(1)}, 'unequal matching coefficients')
        basis_supports.add(frozenset(cubics[i] for i in values))
    expected = set()
    for rows in combinations(range(n), 3):
        for cols in combinations(range(n), 3):
            expected.add(frozenset(tuple(sorted(r*n+c for r, c in zip(rows, sigma)))
                                  for sigma in permutations(cols)))
    require(basis_supports == expected, 'prolongation basis differs from E3')
    require(len(basis_supports) == comb(n, 3)**2, 'wrong prolongation dimension')
    require(forced_count + 6*len(basis_supports) == len(cubics), 'incomplete cubic coverage')
    require({v for pair in rectangles for q in pair for v in q} == set(variables),
            'first derivatives of E2 do not span V')
    return {'n': n, 'variables': len(variables), 'quadratic_monomials': len(quadratics),
            'cubic_monomials': len(cubics), 'rectangle_basis_dimension': len(rectangles),
            'two_term_derivative_equations': equations,
            'forced_zero_cubic_coefficients': forced_count,
            'prolongation_dimension': len(basis_supports),
            'basis_exactly_three_by_three_subpermanents': True,
            'E2_first_derivatives_span_V': True, 'status': 'PASS'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--n', type=int, choices=(5, 6), nargs='+', default=[5, 6])
    args = parser.parse_args()
    result = {'arithmetic': 'exact rational; standard library only',
              'results': [check(n) for n in args.n]}
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_bytes(text.encode('utf-8'))
    print(text, end='')


if __name__ == '__main__':
    main()
