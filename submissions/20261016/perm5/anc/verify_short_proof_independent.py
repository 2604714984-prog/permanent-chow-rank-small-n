#!/usr/bin/env python3
"""Second implementation: dense rational elimination and direct differentiation.

Does not import the first verifier or read its output. Its finite scope does
not replace the manuscript's arguments for arbitrary characteristic-zero data.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import factorial


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = a[r][j]
        a[r] = [x/v for x in a[r]]
        for i in range(r+1, len(a)):
            v = a[i][j]
            a[i] = [x-v*y for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def exponents(variables, degree):
    return [e for e in product(range(degree+1), repeat=variables) if sum(e) == degree]


def normal_form_checks():
    cubic = exponents(4,3)
    order_two = exponents(4,2)
    observed = []
    for s in range(1,5):
        monomials = [tuple(1+int(i==j) for i in range(4)) for j in range(s)]
        matrix = []
        for target in cubic:
            row = []
            for derivative in order_two:
                value = 0
                for source in monomials:
                    if all(a-b == c for a,b,c in zip(source,derivative,target)):
                        coefficient = 1
                        for a,b in zip(source,derivative):
                            coefficient *= factorial(a)//factorial(a-b)
                        value += coefficient
                row.append(value)
            matrix.append(row)
        dimension = rank(matrix)
        observed.append(dimension)
        needed = ({1:[(0,2,3),(1,2,3)],2:[(0,2,3),(1,2,3)],
                   3:[(0,1,3),(0,2,3),(1,2,3)],4:list(combinations(range(4),3))})[s]
        for triple in needed:
            monomial = tuple(int(i in triple) for i in range(4))
            augmented = [row+[int(e==monomial)] for e,row in zip(cubic,matrix)]
            require(rank(augmented)==dimension, (s,"actual cubic missing",triple))
    require(observed==[7,7,9,10], observed)


def squarefree_matrices():
    vertices = range(5)
    edges = list(combinations(vertices,2))
    triples = list(combinations(vertices,3))
    minima = [10]*6
    cases = 0
    for mask in range(32):
        outside = [i for i in vertices if mask>>i&1]
        for killed in [None,*edges]:
            output = [(v,e) for v in outside for e in edges if e != killed]
            matrix = [[int(v in t and tuple(x for x in t if x!=v)==e) for t in triples]
                      for v,e in output]
            value = rank(matrix)
            minima[len(outside)] = min(minima[len(outside)],value)
            cases += 1
    require(cases==352 and minima==[0,5,7,7,10,10], (cases,minima))


def monomial_floors():
    floors = []
    for ell in range(1,5):
        values = []
        for powers in product(range(1,6), repeat=ell):
            if sum(powers)!=5:
                continue
            count = sum(sum(e)==2 and all(a<=b for a,b in zip(e,powers))
                        for e in product(range(3), repeat=ell))
            values.append(count)
        floors.append(min(values))
    require(floors==[1,2,4,7], floors)


def main():
    normal_form_checks()
    squarefree_matrices()
    monomial_floors()
    print("PERM5_SHORT_PROOF_INDEPENDENT_PASS rational_matrices=4+352 floors=1,2,4,7")


if __name__ == "__main__":
    main()
