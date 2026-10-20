#!/usr/bin/env python3
"""Independent optional exact regression tests for the perm6 pure proof.

No project imports or frozen expected payloads. The written proof is independent
of this script. Finite samples below are NOT an all-parameter proof. Python 3.11+
and the standard library suffice. Run normally or with -O; no assert statements
are used for acceptance.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import comb
from pathlib import Path
import random
import sys


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def echelon(columns):
    pivots = {}
    for source in columns:
        col = {k: Fraction(v) for k, v in source.items() if v}
        while col:
            p = min(col)
            value = col[p]
            if p not in pivots:
                pivots[p] = {k: v/value for k, v in col.items()}
                break
            for k, v in pivots[p].items():
                new = col.get(k, Fraction(0)) - value*v
                if new:
                    col[k] = new
                else:
                    col.pop(k, None)
    return pivots


def reduce_col(source, pivots):
    col = {k: Fraction(v) for k, v in source.items() if v}
    for p in sorted(pivots):
        value = col.get(p, 0)
        if value:
            for k, v in pivots[p].items():
                new = col.get(k, Fraction(0)) - value*v
                if new:
                    col[k] = new
                else:
                    col.pop(k, None)
    return col


def rank(columns):
    return len(echelon(columns))


def add_poly(left, right, scale=1):
    out = dict(left)
    for mon, coeff in right.items():
        out[mon] = out.get(mon, 0) + scale*coeff
        if not out[mon]:
            out.pop(mon)
    return out


def multiply(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            mon = tuple(sorted(a+b))
            out[mon] = out.get(mon, 0) + ca*cb
    return {k: v for k, v in out.items() if v}


def poly_from_factors(factors):
    result = {(): 1}
    for vector in factors:
        result = multiply(result, {(i,): a for i, a in enumerate(vector) if a})
    return result


def derivative(poly, variable):
    out = {}
    for mon, coefficient in poly.items():
        multiplicity = mon.count(variable)
        if multiplicity:
            remaining = list(mon)
            remaining.remove(variable)
            out[tuple(remaining)] = coefficient*multiplicity
    return out


def derivatives(poly, ell, order):
    result = []
    for variables in combinations_with_replacement(range(ell), order):
        p = poly
        for a in variables:
            p = derivative(p, a)
        result.append(p)
    return result


def basis_of_polys(polys):
    return list(echelon(polys).values())


def symbol_rank(U, R, P, ell):
    rpivots = echelon(R)
    columns = []
    for cubic in U:
        col = {}
        for a in range(ell):
            q = reduce_col(derivative(cubic, a), rpivots)
            for i, row in enumerate(P):
                coefficient = row[a]
                if coefficient:
                    for mon, v in q.items():
                        key = (i, mon)
                        col[key] = col.get(key, 0) + coefficient*v
        columns.append({k: v for k, v in col.items() if v})
    return rank(columns)


def quadratic_rank(q, ell):
    return rank(derivative(q, a) for a in range(ell))


def random_quotient(ell, d, rng):
    rows = [[int(i == j) for j in range(ell)] for i in range(ell)]
    for _ in range(ell*2):
        if ell > 1:
            a, b = rng.sample(range(ell), 2)
            c = rng.choice((-2, -1, 1, 2))
            rows[a] = [x+c*y for x, y in zip(rows[a], rows[b])]
    rng.shuffle(rows)
    return rows[:d]


def check_coordinate_symbols():
    n = 6
    pairs = list(combinations(range(n), 2))
    triples = list(combinations(range(n), 3))
    minima = [[20]*7 for _ in range(4)]
    cases = 0
    for r in range(4):
        for mask in range(1 << n):
            B = {i for i in range(n) if (mask >> i) & 1}
            O = set(range(n))-B
            d = len(O)
            for size in range(r+1):
                for edge_tuple in combinations(pairs, size):
                    A = set(edge_tuple)
                    killed = 0
                    for I in triples:
                        if all(tuple(j for j in I if j != i) in A for i in I if i in O):
                            killed += 1
                    q = sum(set(e) <= B for e in A)
                    cross = sum(comb(sum(tuple(sorted((b,o))) in A for o in O),2) for b in B)
                    triangles = sum(all(e in A for e in combinations(I,2)) for I in combinations(sorted(O),3))
                    formula = comb(len(B),3)+d*q+cross+triangles
                    check(killed == formula, 'killed-column formula mismatch')
                    value = 20-killed
                    minima[r][d] = min(minima[r][d], value)
                    if d <= 5:
                        check(3*value >= 10*d, 'six-variable symbol bound failed')
                    cases += 1
    check(cases == 45696, 'coordinate domain count mismatch')
    check(minima[3] == [0,7,10,10,15,17,19], 'independent rank minima mismatch')
    cases5 = 0
    minima5 = [10]*6
    pairs5 = list(combinations(range(5),2))
    for mask in range(32):
        B = {i for i in range(5) if (mask >> i) & 1}
        O = set(range(5))-B
        for A in (set(), *({e} for e in pairs5)):
            surviving = sum(any(tuple(j for j in I if j != i) not in A for i in I if i in O)
                            for I in combinations(range(5),3))
            formula = 10-comb(len(B),3)-len(O)*int(bool(A) and set(next(iter(A))) <= B)
            check(surviving == formula, 'five-variable count mismatch')
            minima5[len(O)] = min(minima5[len(O)], surviving)
            cases5 += 1
    check(cases5 == 352 and minima5 == [0,5,7,7,10,10], 'five-variable minima mismatch')
    return {'six_variable_cases': cases, 'six_variable_minima': minima,
            'five_variable_cases': cases5, 'five_variable_minima': minima5}


def check_permanent_prolongation(n=6):
    N = n*n
    quadratics = list(combinations_with_replacement(range(N),2))
    relation = {}
    rectangles = []
    for i,k in combinations(range(n),2):
        for j,l in combinations(range(n),2):
            a = tuple(sorted((n*i+j,n*k+l)))
            b = tuple(sorted((n*i+l,n*k+j)))
            relation[b] = a
            rectangles.append({a: 1,b: 1})
    quotient_basis = {mon: i for i,mon in enumerate(q for q in quadratics if q not in relation)}
    def constraints():
        for mon in combinations_with_replacement(range(N),3):
            col = {}
            for a,multiplicity in Counter(mon).items():
                remaining = list(mon)
                remaining.remove(a)
                q = tuple(remaining)
                coefficient = multiplicity
                if q in relation:
                    q = relation[q]
                    coefficient = -coefficient
                col[(a, quotient_basis[q])] = coefficient
            yield col
    actual = comb(N+2,3)-rank(constraints())
    check(actual == comb(n,3)**2, 'permanent prolongation mismatch')
    return {'variables': N, 'cubic_monomials': comb(N+2,3),
            'quadratic_space_dimension': len(rectangles), 'prolongation_dimension': actual}


def compositions(total, length):
    if length == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total-length+2):
        for tail in compositions(total-first, length-1):
            yield (first,)+tail


def check_monomial_floor():
    counts = []
    for ell in range(1,7):
        values = []
        for alpha in compositions(6, ell):
            mon = tuple(i for i,a in enumerate(alpha) for _ in range(a))
            actual = rank(derivatives({mon: 1},ell,3))
            formula = comb(ell,3)+(ell-1)*sum(a >= 2 for a in alpha)+sum(a >= 3 for a in alpha)
            check(actual == formula, 'degree-three divisor formula mismatch')
            values.append(actual)
        counts.append({'ell':ell,'compositions':len(values),'minimum':min(values)})
    check([c['minimum'] for c in counts] == [1,2,4,8,14,20], 'monomial minima mismatch')
    return counts


def normal_form(s):
    factors = [[int(i==j) for i in range(5)] for j in range(5)]
    factors.append([int(i < s) for i in range(5)])
    return factors


def check_normal_forms():
    result = []
    for s in range(1,6):
        factors = normal_form(s)
        T = poly_from_factors(factors)
        U = basis_of_polys(derivatives(T,5,3))
        F = basis_of_polys(derivatives(T,5,4))
        upivots = echelon(U)
        sf = list(combinations(range(5),3))
        included = [I for I in sf if not reduce_col({I:1}, upivots)]
        expected_count = (10,7,9,10,10)[s-1]
        check(len(included) == expected_count, 'actual squarefree inclusions mismatch')
        m = 10-len(included)
        check(2*m <= 20-len(U), 'squarefree-defect budget failed')
        if s == 2:
            check(len(U) <= 14, 'binary cubic product upper bound failed')
        if s == 3:
            check(len(U) <= 18, 'ternary quartic product upper bound failed')
        for j in range(s):
            for k in range(5):
                if j == k:
                    continue
                p = derivative(derivative(derivative(T,j),j),k)
                expected = {tuple(i for i in range(5) if i not in (j,k)):2}
                check(p == expected, 'displayed squarefree derivative identity failed')
        formal_u = [poly_from_factors([factors[i] for i in choice]) for choice in combinations(range(6),3)]
        formal_f = [poly_from_factors([factors[i] for i in choice]) for choice in combinations(range(6),2)]
        result.append({'s':s,'actual_quadratic_dimension':len(F),'actual_middle_dimension':len(U),
                       'formal_pair_span':rank(formal_f),'formal_triple_span':rank(formal_u),
                       'squarefree_cubics':len(included),'missing_squarefree_directions':m,
                       'budget_twice':20-len(U)})
    check([(r['actual_quadratic_dimension'],r['actual_middle_dimension']) for r in result]
          == [(11,14),(11,14),(13,18),(14,20),(15,20)], 'normal-form regression mismatch')
    return result


def check_local_samples():
    rng = random.Random(20261020)
    families = []
    for ell in range(1,5):
        for alpha in compositions(6,ell):
            if tuple(sorted(alpha,reverse=True)) != alpha:
                continue
            factors = [[int(i==j) for i in range(ell)] for j,a in enumerate(alpha) for _ in range(a)]
            families.append((f'monomial-{alpha}',ell,factors))
        if ell >= 2:
            factors = [[int(i==j) for i in range(ell)] for j in range(ell)]
            for _ in range(6-ell):
                v = [rng.randrange(-2,3) for _ in range(ell)]
                if not any(v):
                    v[0] = 1
                factors.append(v)
            families.append((f'mixed-{ell}',ell,factors))
    for s in range(1,6):
        families.append((f'T{s}',5,normal_form(s)))
    cases = nonzero_R = kernel_cases = 0
    detail = []
    for name,ell,factors in families:
        T = poly_from_factors(factors)
        U = basis_of_polys(derivatives(T,ell,3))
        F = basis_of_polys(derivatives(T,ell,4))
        admissible = []
        if ell >= 4:
            for _ in range(25):
                q = {}
                for b in F:
                    q = add_poly(q,b,rng.randrange(-2,3))
                if quadratic_rank(q,ell) >= 4:
                    admissible = [q]
                    break
        options = [[]] + ([admissible] if admissible else [])
        for R in options:
            for d in range(ell+1):
                for trial in range(3):
                    P = random_quotient(ell,d,rng)
                    actual = symbol_rank(U,R,P,ell)
                    check(6*actual+3*(20-len(U)) >= 20*d,
                          f'half-defect failed: {name}, d={d}, rank={actual}, u={len(U)}')
                    if ell-d <= 2:
                        raw = symbol_rank(U,[],P,ell)
                        check(actual == raw, 'small-complement kernel identity failed')
                        kernel_cases += 1
                    cases += 1
                    nonzero_R += bool(R)
        detail.append({'family':name,'ell':ell,'u':len(U),'F_dimension':len(F),'nonzero_R_tested':bool(admissible)})
    ell = 6
    U = [{I:1} for I in combinations(range(6),3)]
    # Actual intersection for the coordinate K_{2,3} six-plane: every nonzero
    # member has rank at least four. Basis directions are permanent quadrics.
    rectangle = [{(a,3+b):1,(b,3+a):1} for a,b in combinations(range(3),2)]
    for r in range(4):
        for trial in range(6):
            C = random_quotient(3,r,rng)
            R = []
            for row in C:
                q = {}
                for coefficient,b in zip(row,rectangle):
                    q = add_poly(q,b,coefficient)
                R.append(q)
            check(rank(R) == r,'admissible rectangle space rank mismatch')
            for d in range(7):
                P = random_quotient(6,d,rng)
                actual = symbol_rank(U,R,P,6)
                check(3*actual >= 10*d, 'six-span admissible local estimate failed')
                cases += 1
                nonzero_R += bool(R)
    # Deliberate negative controls demonstrate why the restrictions matter.
    triangle = [{e:1} for e in combinations(range(3),2)]
    identity6 = [[int(i==j) for j in range(6)] for i in range(6)]
    bad_full_rank = symbol_rank(U,triangle,identity6,6)
    check(bad_full_rank == 19, 'negative triangle control did not expose rank 19')
    raw = symbol_rank([{(0,1,2):1}],[],[[0,0,1]],3)
    killed = symbol_rank([{(0,1,2):1}],[{(0,1):1}],[[0,0,1]],3)
    check(raw == 1 and killed == 0, 'negative rank-floor control failed')
    return {'exact_rational_local_examples':cases,'examples_with_nonzero_admissible_R':nonzero_R,
            'small_complement_kernel_identities':kernel_cases,'families':detail,
            'negative_controls':{'arbitrary_three_edge_full_symbol_rank':bad_full_rank,
                                 'rank_two_R_breaks_small_complement_identity':True}}


def check_glynn_and_global():
    n = 6
    eps_list = [(1,)+tail for tail in product((1,-1), repeat=5)]
    coefficients = Counter()
    expansions = 0
    for eps in eps_list:
        weight = 1
        for e in eps:
            weight *= e
        for rows in product(range(6),repeat=6):
            coefficient = weight
            for i in rows:
                coefficient *= eps[i]
            coefficients[rows] += coefficient
            expansions += 1
    for rows,value in coefficients.items():
        expected = 32 if len(set(rows)) == 6 else 0
        check(value == expected, 'integer Glynn expansion failed')
    def component_degree(k):
        return rank({rows:__import__('functools').reduce(lambda a,b:a*b,(eps[i] for i in rows),1)
                     for rows in product(range(6),repeat=k)} for eps in eps_list)
    cubic_component = component_degree(3)
    quadratic_component = component_degree(2)
    Udimension = comb(6,3)*cubic_component
    Fdimension = comb(6,2)*quadratic_component
    # Differentiate actual single-row Fourier-character cubics and reduce
    # their quadrics modulo the explicit rectangle relations. This checks the
    # global quotient map itself, not only a dimension-subtraction formula.
    def reduce_rectangle_quadratic(q):
        out = {}
        for mon, value in q.items():
            x, y = mon
            r,c = divmod(x,6); s,d = divmod(y,6)
            if r != s and c != d:
                low_row,high_row = sorted((r,s))
                low_col,high_col = sorted((c,d))
                target = (6*low_row+low_col,6*high_row+high_col)
                if mon != target:
                    value = -value
            else:
                target = mon
            out[target] = out.get(target,0)+value
        return {mon:v for mon,v in out.items() if v}
    columns = []
    actual_derivatives_checked = 0
    for J in combinations(range(6),3):
        for a in range(6):
            g = {tuple(6*a+c for c in J):1}
            for other in range(6):
                if other == a:
                    continue
                for singleton_column in J:
                    mon = tuple(sorted(6*(a if c == singleton_column else other)+c for c in J))
                    g[mon] = 1
            column = {}
            for variable in range(36):
                q = reduce_rectangle_quadratic(derivative(g,variable))
                r,c = divmod(variable,6)
                expected = {}
                if r == a and c in J:
                    remaining = [j for j in J if j != c]
                    expected = {(6*row+remaining[0],6*row+remaining[1]):1 for row in range(6)}
                check(q == expected, 'actual global quotient derivative mismatch')
                actual_derivatives_checked += 1
                for mon,v in q.items():
                    column[(variable,mon)] = v
            columns.append(column)
    h = rank(columns)
    check((cubic_component,quadratic_component,Udimension,Fdimension,h)==(26,16,520,240,120),
          'actual Glynn derivative-span check failed')
    check(h == Udimension-400 == 10*32-200, 'global equality check failed')
    return {'expanded_terms':expansions,'surviving_monomials':sum(bool(v) for v in coefficients.values()),
            'unscaled_coefficient':32,'single_column_triple_span':cubic_component,
            'single_column_pair_span':quadratic_component,'actual_middle_image_sum':Udimension,
            'actual_quadratic_image_sum':Fdimension,'h':h,'Delta':0,
            'independent_global_quotient_rank':h,'actual_quotient_derivatives_checked':actual_derivatives_checked,
            'both_global_bounds_are_equalities':True}


def check_small_span_bounds():
    cases = 0
    floors = {1:1,2:2,3:4,4:8}
    for ell,floor in floors.items():
        for u in range(floor,min(20,comb(ell+2,3))+1):
            for d in range(ell+1):
                if d == 0:
                    r = 0
                elif d == 1:
                    r = max(0,u-comb(ell+1,3)-1)
                else:
                    r = max(0,u-comb(ell-d+2,3))
                check(6*r+3*(20-u)>=20*d,'small-span algebraic inequality failed')
                cases += 1
    return {'integer_regression_cases':cases,'proof_uses_algebra_not_these_cases':True}



def check_structured_completions():
    """Check coordinate-boundary quotients, not just generic rational samples."""
    cases = kernels = dense_checks = 0
    details = []
    H = [{I:1} for I in combinations(range(5),3)]
    matching_lines = []
    for four in combinations(range(5),4):
        a,b,c,d = four
        matching_lines.extend([{(a,b):1,(c,d):1}, {(a,c):1,(b,d):1}, {(a,d):1,(b,c):1}])
    def concatenated_rank(U,R,P):
        # A second quotient-rank path: concatenate the killed target columns
        # before eliminating, instead of reducing each quadratic modulo R.
        cols = []
        for row in range(len(P)):
            for q in R:
                cols.append({(row,mon):v for mon,v in q.items()})
        killed_rank = rank(cols)
        for cubic in U:
            col = {}
            for a in range(5):
                for mon,v in derivative(cubic,a).items():
                    for row,coefficient_row in enumerate(P):
                        key = (row,mon)
                        col[key] = col.get(key,0)+v*coefficient_row[a]
            cols.append({k:v for k,v in col.items() if v})
        return rank(cols)-killed_rank
    for t in range(1,6):
        T = poly_from_factors(normal_form(t))
        U = basis_of_polys(derivatives(T,5,3))
        F = basis_of_polys(derivatives(T,5,4))
        up = echelon(U); fp = echelon(F)
        U0 = [q for q in H if not reduce_col(q,up)]
        m = 10-len(U0)
        lines = [q for q in matching_lines if not reduce_col(q,fp)]
        check(all(quadratic_rank(q,5) == 4 for q in lines), 'matching line not rank four')
        options = [[]]+[[q] for q in lines]
        minimum_margin = None
        for R in options:
            for mask in range(32):
                outside = [i for i in range(5) if not ((mask >> i)&1)]
                P = [[int(i==j) for j in range(5)] for i in outside]
                d = len(outside)
                actual = symbol_rank(U,R,P,5)
                margin = 6*actual+3*(20-len(U))-20*d
                check(margin >= 0,'structured half-defect failure')
                minimum_margin = margin if minimum_margin is None else min(margin,minimum_margin)
                if d in (1,2):
                    completed = symbol_rank(H,R,P,5)
                    restricted = symbol_rank(U0,R,P,5)
                    check(completed >= (5 if d == 1 else 7),'completed five-variable bound failed')
                    check(actual >= restricted >= completed-m,'source-restriction rank comparison failed')
                    check(2*m <= 20-len(U),'structured defect budget failed')
                if 5-d <= 2:
                    check(actual == symbol_rank(U,[],P,5),'structured small-complement kernel mismatch')
                    kernels += 1
                if mask in (0,3,7,15,31) and (not R or R == [lines[0]]):
                    independent = concatenated_rank(U,R,P)
                    check(actual == independent,'two quotient-rank algorithms disagree')
                    dense_checks += 1
                cases += 1
        details.append({'s':t,'rank_four_lines_in_actual_F':len(lines),
                        'quotient_cases':len(options)*32,'smallest_six_times_margin':minimum_margin})
    return {'coordinate_boundary_cases':cases,'small_complement_kernel_identities':kernels,
            'second_quotient_rank_algorithm_checks':dense_checks,'details':details}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('verification_results.json'))
    args = parser.parse_args()
    result = {'proof_dependency':False,'arithmetic':'integers and rational numbers; no floating-point ranks',
              'sampling_note':'Rational samples and finite enumerations are regression tests, not a universal proof.'}
    for name,operation in [('coordinate_symbols',check_coordinate_symbols),
                           ('permanent_prolongation',check_permanent_prolongation),
                           ('monomial_floors',check_monomial_floor),
                           ('normal_forms',check_normal_forms),
                           ('local_symbols',check_local_samples),
                           ('structured_completions',check_structured_completions),
                           ('small_span_bounds',check_small_span_bounds),
                           ('glynn_and_global',check_glynn_and_global)]:
        result[name] = operation()
        print(name+': PASS',flush=True)
    result['status'] = 'PERM6_OPTIONAL_CHECKS_PASS'
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'],flush=True)


if __name__ == '__main__':
    main()
