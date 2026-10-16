#!/usr/bin/env python3
"""Exact integration diagnostic on the known optimal Glynn decompositions.

Compute the row-polarized quadratic/cubic image spans directly. This checks
that the proposed global inequalities are sharp on actual decompositions;
it is not a proof that no shorter arbitrary decomposition exists.
"""
from fractions import Fraction
from itertools import product
from math import factorial, comb
from pathlib import Path
import argparse
import json


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:
            continue
        a[r],a[p] = a[p],a[r]
        value = a[r][j]
        a[r] = [x/value for x in a[r]]
        for i in range(r+1,len(a)):
            value = a[i][j]
            a[i] = [x-value*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def exponents(n,degree):
    if n==1:
        yield (degree,)
        return
    for first in range(degree+1):
        for rest in exponents(n-1,degree-first):
            yield (first,)+rest


def image_span(n,degree):
    signs = [(1,)+z for z in product((-1,1),repeat=n-1)]
    monomials = list(exponents(n,degree))
    matrix = []
    for powers in monomials:
        scale = factorial(degree)
        for power in powers:
            scale //= factorial(power)
        matrix.append([scale*product_sign(point,powers) for point in signs])
    dimension = rank(matrix)
    # All squarefree row monomials must belong to the actual image span.
    for i,powers in enumerate(monomials):
        if max(powers)<=1:
            augmented = [row+[int(j==i)] for j,row in enumerate(matrix)]
            if rank(augmented)!=dimension:
                raise RuntimeError(("missing permanent derivative",n,degree,powers))
    return dimension


def product_sign(point,powers):
    value = 1
    for sign,power in zip(point,powers):
        value *= sign**power
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    records = []
    for n,expected in [(5,(11,15)),(6,(16,26))]:
        r2,r3 = image_span(n,2),image_span(n,3)
        if (r2,r3)!=expected:
            raise RuntimeError((n,r2,r3))
        f_dimension = comb(n,2)*r2
        u_dimension = comb(n,3)*r3
        h2 = f_dimension-comb(n,2)**2
        h3 = u_dimension-comb(n,3)**2
        if n==5 and (h2,h3)!=(10,50):
            raise RuntimeError((n,h2,h3))
        if n==6 and h3!=120:
            raise RuntimeError((n,h3))
        records.append({"n":n,"Glynn_terms":2**(n-1),
                        "row_quadratic_span":r2,"row_cubic_span":r3,
                        "F_dimension":f_dimension,"U_dimension":u_dimension,
                        "h2":h2,"h3":h3,"individual_middle_defect":0,
                        "global_bound_is_sharp":True})
    payload = {"status":"PASS","scope":"integration diagnostic on actual known decompositions",
               "records":records}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps(payload,sort_keys=True))


if __name__ == "__main__":
    main()
