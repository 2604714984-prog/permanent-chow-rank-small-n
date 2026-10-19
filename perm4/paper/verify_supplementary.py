#!/usr/bin/env python3
"""Optional exact cross-checks of the computation-free perm4 argument.

The manuscript does not cite this program as a premise. These checks are
independent regression tests, not a substitute for the written proof.
Standard library only; no imports from the historical certificate package.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
from math import comb
from pathlib import Path
import json
import time

PRIMES = (1000003, 1000033)


def rank_mod(columns, prime: int) -> int:
    """Sparse exact elimination over a prime field."""
    pivots: dict[int, dict[int, int]] = {}
    for source in columns:
        col = {r: v % prime for r, v in source.items() if v % prime}
        while col:
            lead = min(col)
            value = col[lead]
            if lead not in pivots:
                inverse = pow(value, -1, prime)
                pivots[lead] = {r: v * inverse % prime for r, v in col.items()}
                break
            for r, v in pivots[lead].items():
                updated = (col.get(r, 0) - value * v) % prime
                if updated:
                    col[r] = updated
                else:
                    col.pop(r, None)
    return len(pivots)



def rank_rational(columns) -> int:
    """Independent characteristic-zero sparse elimination."""
    pivots = {}
    for source in columns:
        col = {r: Fraction(v) for r, v in source.items() if v}
        while col:
            lead = min(col)
            value = col[lead]
            if lead not in pivots:
                pivots[lead] = {r: v/value for r, v in col.items()}
                break
            for r, v in pivots[lead].items():
                updated = col.get(r, Fraction(0)) - value*v
                if updated:
                    col[r] = updated
                else:
                    col.pop(r, None)
    return len(pivots)


def quad_quotient(n: int, kind: str = 'permanent'):
    """Explicit monomial coordinates of Sym^2(V)/F, including signs."""
    N = n * n
    quadratics = list(combinations_with_replacement(range(N), 2))
    relations = {}
    if kind == 'permanent':
        for i, k in combinations(range(n), 2):
            for j, l in combinations(range(n), 2):
                positive = tuple(sorted((n*i+j, n*k+l)))
                negative = tuple(sorted((n*i+l, n*k+j)))
                relations[negative] = positive
        excluded = set(relations)
    elif kind == 'chow4':
        excluded = set(combinations(range(4), 2))
    else:
        raise ValueError(kind)
    basis = [mon for mon in quadratics if mon not in excluded]
    index = {mon: i for i, mon in enumerate(basis)}
    result = {}
    for mon in quadratics:
        if mon in relations:
            result[mon] = (index[relations[mon]], -1)
        elif mon in index:
            result[mon] = (index[mon], 1)
        else:
            result[mon] = None
    return len(basis), result


def derivative_constraints(n: int, excluded_variable: int | None, kind='permanent'):
    """Columns for g -> (partial_a g mod F) for all nonexcluded a."""
    N = n*n
    width, quotient = quad_quotient(n, kind)
    for cubic in combinations_with_replacement(range(N), 3):
        col = {}
        for a, multiplicity in Counter(cubic).items():
            if a == excluded_variable:
                continue
            residual = list(cubic)
            residual.remove(a)
            image = quotient[tuple(residual)]
            if image is not None:
                qrow, coefficient = image
                col[a*width + qrow] = multiplicity * coefficient
        yield col


def E_quadratics(n: int):
    for i, k in combinations(range(n), 2):
        for j, l in combinations(range(n), 2):
            yield {
                tuple(sorted((n*i+j, n*k+l))): 1,
                tuple(sorted((n*i+l, n*k+j))): 1,
            }


def delta_column(quadratic, exterior, N: int, wedges):
    col = {}
    for (a, b), coefficient in quadratic.items():
        for differentiated, remaining in ((a, b), (b, a)):
            if differentiated == exterior:
                continue
            sign = 1 if differentiated < exterior else -1
            pair = tuple(sorted((differentiated, exterior)))
            row = remaining*comb(N, 2) + wedges[pair]
            col[row] = col.get(row, 0) + coefficient*sign
    return {r: v for r, v in col.items() if v}


def image_columns(n: int, kind='permanent'):
    N = n*n
    wedges = {p: k for k, p in enumerate(combinations(range(N), 2))}
    quadratics = E_quadratics(n) if kind == 'permanent' else ({p: 1} for p in combinations(range(4), 2))
    for q in quadratics:
        for a in range(N):
            yield delta_column(q, a, N, wedges)


def verify_matching_graph():
    """All six matching coefficients stay connected after omitting d/dx00."""
    nodes = list(permutations(range(3)))
    adjacency = {v: set() for v in nodes}
    removed = []
    for v in nodes:
        for a, b in combinations(range(3), 2):
            w = list(v)
            w[a], w[b] = w[b], w[a]
            w = tuple(w)
            remaining = next(k for k in range(3) if k not in (a,b))
            if remaining == 0 and v[remaining] == 0:
                if v < w:
                    removed.append((v,w))
            else:
                adjacency[v].add(w)
    seen, queue = set(), [nodes[0]]
    while queue:
        v = queue.pop()
        if v in seen:
            continue
        seen.add(v)
        queue.extend(adjacency[v] - seen)
    if len(seen) != 6 or len(removed) != 1:
        raise AssertionError('deleted-edge matching graph mismatch')
    return {'vertices': 6, 'remaining_edges': sum(map(len, adjacency.values()))//2,
            'removed_edges': len(removed), 'connected': True}


def verify_bad_monomial_rule(n: int):
    """Check the elementary elimination rule on every forbidden cubic."""
    N = n*n
    z = 0
    def bad_pair(a,b):
        return a//n == b//n or a % n == b % n
    def direct_kill(cubic):
        for a in set(cubic)-{z}:
            rest = list(cubic)
            rest.remove(a)
            if bad_pair(*rest):
                return True
        return False
    counts = {'directly_forbidden': 0, 'rectangle_companion': 0,
              'matching_monomials': 0, 'exception_z_cube': 0}
    for cubic in combinations_with_replacement(range(N), 3):
        if cubic == (z,z,z):
            counts['exception_z_cube'] += 1
            continue
        if all(not bad_pair(a,b) for a,b in combinations(cubic,2)):
            counts['matching_monomials'] += 1
            continue
        if direct_kill(cubic):
            counts['directly_forbidden'] += 1
            continue
        if cubic.count(z) != 1:
            raise AssertionError(('unexpected survivor',cubic))
        u,w = list(cubic)[1:]
        if not bad_pair(u,w) or 0 in (u//n,u%n,w//n,w%n):
            raise AssertionError(('survivor not interior',cubic))
        i,j = divmod(w,n)
        companion = tuple(sorted((u, j, n*i)))
        if not direct_kill(companion):
            raise AssertionError(('companion not killed',cubic,companion))
        counts['rectangle_companion'] += 1
    return counts


def verify_torus_weights(n: int):
    w = lambda a: int(a//n != 0)+int(a%n != 0)
    for q in E_quadratics(n):
        weights = {sum(w(a) for a in mon) for mon in q}
        if len(weights) != 1:
            raise AssertionError('E is not homogeneous for corner scaling')
    if w(0) != 0 or any(w(a) <= 0 for a in range(1,n*n)):
        raise AssertionError('corner degeneration does not isolate x00')
    return True


def verify_glynn():
    output = {}
    for signs in __import__('itertools').product((1,-1),repeat=3):
        eps = (1,)+signs
        weight = eps[0]*eps[1]*eps[2]*eps[3]
        for choices in __import__('itertools').product(range(4),repeat=4):
            mon = tuple(sorted(4*choices[j]+j for j in range(4)))
            coefficient = weight
            for i in choices:
                coefficient *= eps[i]
            output[mon] = output.get(mon,0)+coefficient
    target = {tuple(4*i+p[i] for i in range(4)) for p in permutations(range(4))}
    for mon, coefficient in output.items():
        if coefficient != (8 if mon in target else 0):
            raise AssertionError(('Glynn mismatch',mon,coefficient))
    return {'unscaled_permutation_coefficient': 8, 'nonzero_terms': 24,
            'expanded_terms': 8*4**4}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('supplementary_results.json'))
    args=parser.parse_args()
    started=time.monotonic()
    result={'proof_dependency': False,
            'description': 'Optional exact regression checks; proof is the written argument.',
            'matching_graph': verify_matching_graph(),
            'glynn': verify_glynn(), 'sizes': {}, 'prime_checks': []}
    for n in (2,3,4,5):
        result['sizes'][str(n)]={'forbidden_cubics':verify_bad_monomial_rule(n),
                                  'torus_preserves_E':verify_torus_weights(n)}
    for prime in PRIMES:
        entry={'prime':prime, 'n4_corners': []}
        n=4; N=16; cubics=comb(N+2,3)
        prolongation_dim=cubics-rank_mod(derivative_constraints(n,None),prime)
        if prolongation_dim != 16:
            raise AssertionError(('E prolongation dimension',prolongation_dim))
        entry['E_prolongation_dimension']=prolongation_dim
        for z in range(N):
            dim=cubics-rank_mod(derivative_constraints(n,z),prime)
            if dim != 17:
                raise AssertionError(('missing derivative dimension',z,dim))
            entry['n4_corners'].append({'coordinate':z,'partial_prolongation_dimension':dim})
        chow_kernel=cubics-rank_mod(derivative_constraints(n,None,'chow4'),prime)
        perm_rank=rank_mod(image_columns(n),prime)
        chow_rank=rank_mod(image_columns(n,'chow4'),prime)
        if (chow_kernel,perm_rank,chow_rank) != (4,560,92):
            raise AssertionError((chow_kernel,perm_rank,chow_rank))
        entry.update(chow_prolongation_dimension=chow_kernel,
                     permanent_koszul_rank=perm_rank,chow_koszul_rank=chow_rank)
        result['prime_checks'].append(entry)
    rational = {
        'E_prolongation_dimension': comb(18,3)-rank_rational(derivative_constraints(4,None)),
        'corner_partial_prolongation_dimension': comb(18,3)-rank_rational(derivative_constraints(4,0)),
        'chow_prolongation_dimension': comb(18,3)-rank_rational(derivative_constraints(4,None,'chow4')),
        'permanent_koszul_rank': rank_rational(image_columns(4)),
        'chow_koszul_rank': rank_rational(image_columns(4,'chow4')),
    }
    if tuple(rational.values()) != (16,17,4,560,92):
        raise AssertionError(('rational cross-check failed',rational))
    result['rational_checks'] = rational
    result['elapsed_seconds']=round(time.monotonic()-started,3)
    result['status']='SUPPLEMENTARY_CHECKS_PASS'
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
