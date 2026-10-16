#!/usr/bin/env python3
"""Exact finite premises of the October perm5 proof; standard library only.

This does not certify the written geometric and global linear-algebra steps.
No historical generator or frozen result is imported or modified.
"""
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import comb
import json
from pathlib import Path
import argparse


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def derivative(poly, variable):
    result = {}
    for exponent, coefficient in poly.items():
        if exponent[variable]:
            target = list(exponent)
            target[variable] -= 1
            result[tuple(target)] = coefficient * exponent[variable]
    return result


def sparse_rank(columns):
    pivots = {}
    for raw in columns:
        column = {key: Fraction(value) for key, value in raw.items() if value}
        while column:
            lead = min(column)
            if lead not in pivots:
                scale = column[lead]
                pivots[lead] = {key: value / scale for key, value in column.items()}
                break
            scale = column[lead]
            for key, value in pivots[lead].items():
                column[key] = column.get(key, Fraction(0)) - scale * value
                if not column[key]:
                    del column[key]
    return len(pivots)


def determinant(matrix):
    a = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            answer = -answer
        value = a[j][j]
        answer *= value
        for i in range(j + 1, len(a)):
            scale = a[i][j] / value
            for k in range(j + 1, len(a)):
                a[i][k] -= scale * a[j][k]
    return answer


def normal_forms():
    rows = []
    expected = (7, 7, 9, 10)
    monomials = sorted({tuple(raw.count(i) for i in range(4))
                        for raw in combinations_with_replacement(range(4), 3)})
    directions = list(combinations_with_replacement(range(4), 2))
    for support in range(1, 5):
        poly = {}
        for i in range(support):
            exponent = [1] * 4
            exponent[i] += 1
            poly[tuple(exponent)] = 1
        columns = [derivative(derivative(poly, i), j) for i, j in directions]
        rank = sparse_rank(columns)
        require(rank == expected[support - 1], (support, rank))
        selected_columns = []
        for i, column in enumerate(columns):
            if sparse_rank([columns[j] for j in selected_columns] + [column]) > len(selected_columns):
                selected_columns.append(i)
        selected_rows = []
        dense_rows = [[columns[j].get(m, 0) for j in selected_columns] for m in monomials]
        for i, row in enumerate(dense_rows):
            if sparse_rank([dict(enumerate(dense_rows[j])) for j in selected_rows] +
                           [dict(enumerate(row))]) > len(selected_rows):
                selected_rows.append(i)
        minor = determinant([[dense_rows[i][j] for j in range(rank)] for i in selected_rows])
        require(bool(minor), (support, "zero pivot minor"))
        needed = ({1: [(0, 2, 3), (1, 2, 3)],
                   2: [(0, 2, 3), (1, 2, 3)],
                   3: [(0, 1, 3), (0, 2, 3), (1, 2, 3)],
                   4: list(combinations(range(4), 3))})[support]
        for triple in needed:
            monomial = tuple(int(i in triple) for i in range(4))
            require(sparse_rank(columns + [{monomial: 1}]) == rank,
                    (support, "missing required actual cubic", triple))
        rows.append({"support": support, "rank": rank,
                     "monomial_rows": monomials, "derivative_columns": directions,
                     "matrix": [[column.get(m, 0) for column in columns] for m in monomials],
                     "pivot_rows": selected_rows, "pivot_columns": selected_columns,
                     "nonzero_pivot_minor": str(minor), "required_squarefree_cubics": needed})
    return rows


def coordinate_symbols():
    vertices = tuple(range(5))
    edges = list(combinations(vertices, 2))
    triples = list(combinations(vertices, 3))
    minima = []
    count = 0
    for d in range(6):
        ranks = []
        for outside_tuple in combinations(vertices, d):
            outside = set(outside_tuple)
            inside = set(vertices) - outside
            for killed in [None, *edges]:
                count += 1
                rank = sum(any(v in outside and tuple(w for w in triple if w != v) != killed
                               for v in triple) for triple in triples)
                formula = 10 - comb(5-d, 3) - d * int(killed is not None and set(killed) <= inside)
                require(rank == formula, (d, outside_tuple, killed, rank, formula))
                ranks.append(rank)
        minima.append(min(ranks))
    require(count == 352 and minima == [0, 5, 7, 7, 10, 10], (count, minima))
    require(all(value >= 2*d for d, value in enumerate(minima)), minima)
    return {"cases": count, "minimum_ranks": minima}


def positive_partitions(total, length, maximum=None):
    if length == 0:
        if total == 0:
            yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(1, min(maximum, total-length+1)+1):
        for rest in positive_partitions(total-first, length-1, first):
            yield (first,) + rest


def low_span():
    floors = []
    rows = {}
    for ell in range(1, 5):
        ranks = []
        for partition in positive_partitions(5, ell):
            rank = sum(sum(exponent) == 2 for exponent in product(*(range(value+1) for value in partition)))
            ranks.append(rank)
        floor = min(ranks)
        floors.append(floor)
        ceiling = min(10, comb(ell+1, 2))
        entries = []
        for d in range(ell+1):
            k = ell-d
            if d == 0:
                bound = Fraction(10-ceiling, 2)
            elif ell == 4 and d == 1:
                bound = min(Fraction(1)+Fraction(10-7,2),
                            Fraction(2)+Fraction(10-9,2), Fraction(2))
            else:
                require(k <= 2, (ell, d, k))
                bound = min(Fraction(max(0, u-comb(k+2,3)))+Fraction(10-u,2)
                            for u in range(floor, ceiling+1))
            require(bound >= 2*d, (ell, d, bound))
            entries.append(str(bound))
        rows[str(ell)] = entries
    require(floors == [1,2,4,7], floors)
    return {"monomial_rank_floors": floors, "adjusted_local_lower_bounds": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = {"normal_forms": normal_forms(), "squarefree_symbols": coordinate_symbols(),
               "low_factor_span": low_span(),
               "scope": "finite premises only; written characteristic-zero arguments remain necessary"}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print("PERM5_SHORT_PROOF_FINITE_PASS profiles=4 coordinate_symbols=352 floors=1,2,4,7")


if __name__ == "__main__":
    main()
