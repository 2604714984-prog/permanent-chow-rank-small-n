#!/usr/bin/env python3
"""Adversarial finite-field diagnostic, NOT a characteristic-zero certificate.

Enumerate every quotient row space of F_3^4 and every projective rank-four
quadric in each actual quadratic derivative space of T_s, s=1,...,4.
No first verifier, second verifier, or reference payload is imported.
"""
from itertools import combinations, product
from math import factorial
import json
import time
import argparse
from pathlib import Path

P = 3


def rref(matrix):
    a = [[int(x)%P for x in row] for row in matrix]
    if not a:
        return [], []
    pivots = []
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        if a[r][j] == 2:
            a[r] = [(2*x)%P for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                scale = a[i][j]
                a[i] = [(x-scale*y)%P for x,y in zip(a[i],a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    return a[:r],pivots


def rank(matrix):
    return len(rref(matrix)[1])


def powers(degree):
    return [e for e in product(range(degree+1), repeat=4) if sum(e)==degree]


QUADRATICS = powers(2)
CUBICS = powers(3)


def derivative_basis(s, order):
    sources = [tuple(1+int(i==j) for i in range(4)) for j in range(s)]
    targets = powers(5-order)
    columns = []
    for direction in powers(order):
        column = []
        for target in targets:
            value = 0
            for source in sources:
                if all(a-b == c for a,b,c in zip(source,direction,target)):
                    scale = 1
                    for a,b in zip(source,direction):
                        scale *= factorial(a)//factorial(a-b)
                    value += scale
            column.append(value%P)
        columns.append(column)
    return rref(columns)[0]


def quotient_maps(d):
    for pivots in combinations(range(4), d):
        positions = [(i,j) for i,pivot in enumerate(pivots)
                     for j in range(pivot+1,4) if j not in pivots]
        for values in product(range(P), repeat=len(positions)):
            matrix = [[int(j==pivot) for j in range(4)] for pivot in pivots]
            for (i,j),value in zip(positions,values):
                matrix[i][j] = value
            yield matrix


def quadratic_rank(q):
    matrix = [[0]*4 for _ in range(4)]
    for e,value in zip(QUADRATICS,q):
        indices = [i for i in range(4) for _ in range(e[i])]
        i,j = indices
        matrix[i][j] = value if i==j else (2*value)%P
        matrix[j][i] = matrix[i][j]
    return rank(matrix)


def projective_vectors(n):
    for pivot in range(n):
        for tail in product(range(P), repeat=n-pivot-1):
            yield (0,)*pivot+(1,)+tail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    records = []
    total_pairs = 0
    last_update = started
    for support in range(1,5):
        U = derivative_basis(support,2)
        F = derivative_basis(support,3)
        u = len(U)
        if u != [7,7,9,10][support-1] or len(F)!=u:
            raise RuntimeError(("field profile changed",support,len(F),u))
        derivative = []
        for variable in range(4):
            matrix = []
            for target in QUADRATICS:
                source = tuple(a+int(i==variable) for i,a in enumerate(target))
                index = CUBICS.index(source)
                matrix.append([(source[variable]*column[index])%P for column in U])
            derivative.append(matrix)
        maps = []
        for d in range(5):
            for quotient in quotient_maps(d):
                matrix = [[sum(row[v]*derivative[v][q][j] for v in range(4))%P
                           for j in range(u)] for row in quotient for q in range(10)]
                maps.append((d,matrix))
        if len(maps)!=212:
            raise RuntimeError(("quotient count",len(maps)))
        minima = [u]*5
        for d,matrix in maps:
            value = rank(matrix)
            if 2*value+10-u < 4*d:
                raise RuntimeError(("R=0 counterexample",support,d,matrix,value))
            minima[d] = min(minima[d],value)
            total_pairs += 1
        quadrics = 0
        for coefficients in projective_vectors(len(F)):
            q = [sum(c*column[i] for c,column in zip(coefficients,F))%P for i in range(10)]
            if quadratic_rank(q)!=4:
                continue
            quadrics += 1
            pivot = next(i for i,x in enumerate(q) if x)
            inverse = pow(q[pivot],-1,P)
            q = [(x*inverse)%P for x in q]
            for d,matrix in maps:
                reduced = [[(matrix[10*b+i][j]-q[i]*matrix[10*b+pivot][j])%P
                            for j in range(u)] for b in range(d) for i in range(10) if i!=pivot]
                value = rank(reduced)
                if 2*value+10-u < 4*d:
                    raise RuntimeError(("COUNTEREXAMPLE",support,d,q,matrix,value))
                minima[d] = min(minima[d],value)
                total_pairs += 1
            now = time.monotonic()
            if now-last_update >=30:
                print(json.dumps({"support":support,"quadrics":quadrics,
                                  "pairs":total_pairs,"elapsed_seconds":round(now-started,2)}),flush=True)
                last_update = now
        records.append({"support":support,"middle_rank":u,
                        "projective_rank_four_quadrics":quadrics,
                        "quotient_row_spaces":len(maps),"minimum_symbol_ranks_by_d":minima})
        print(json.dumps(records[-1]),flush=True)
    payload = {"field":"F_3","scope":"diagnostic only; does not prove a characteristic-zero theorem",
               "status":"PASS","records":records,"total_quotient_quadric_pairs":total_pairs,
               "elapsed_seconds":round(time.monotonic()-started,3)}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print("QUINTIC_NONCOORDINATE_STRESS_PASS",flush=True)


if __name__ == "__main__":
    main()
