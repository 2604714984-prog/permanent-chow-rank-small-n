#!/usr/bin/env python3
"""Direct integer expansion of Glynn's identity; no imported project code."""
from itertools import product
from math import factorial
import argparse


def verify(n):
    coefficients = {}
    choices = tuple(product(range(n), repeat=n))
    expanded = 0
    for tail in product((-1,1), repeat=n-1):
        signs = (1,)+tail
        prefactor = 1
        for value in signs:
            prefactor *= value
        for rows in choices:
            value = prefactor
            for row in rows:
                value *= signs[row]
            coefficients[rows] = coefficients.get(rows,0)+value
            expanded += 1
    scale = 2**(n-1)
    nonzero = 0
    for rows,value in coefficients.items():
        expected = scale if len(set(rows)) == n else 0
        if value != expected:
            raise RuntimeError((n,rows,value,expected))
        nonzero += int(bool(value))
    if nonzero != factorial(n) or expanded != scale*n**n:
        raise RuntimeError((n,nonzero,expanded))
    print(f"GLYNN_EXACT_PASS n={n} expanded_choices={expanded} permutation_monomials={nonzero}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n",type=int,choices=(5,6))
    verify(parser.parse_args().n)
