#!/usr/bin/env python3
"""Characteristic-free graph audit of the full orbit-0 flag tangent space.

At S0=U0 tensor B3 and T0=R0 tensor B2, linearize partial(S) subset T.
Every nonzero scalar equation has one graph variable (an anchor) or two graph
variables with coefficients +1,-1 (an edge).  Hence the kernel is read from
the unanchored connected components over every field.
"""

from collections import defaultdict
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json


A3 = list(combinations(range(5), 3))
A2 = list(combinations(range(5), 2))
B3 = list(combinations(range(5), 3))
B2 = list(combinations(range(5), 2))
U0 = [(0, 1, 2), (0, 1, 3)]
UOUT = [x for x in A3 if x not in U0]
R0 = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3)]
ROUT = [x for x in A2 if x not in R0]


def m(x):
    return "".join(map(str, x))


vertices = []
index = {}

# S-graph variables: (U0 x B3) -> (UOUT x B3).
for ur in U0:
    for bc in B3:
        for vr in UOUT:
            for dc in B3:
                name = f"S_{m(ur)}x{m(bc)}__{m(vr)}x{m(dc)}"
                index[("S", ur, bc, vr, dc)] = len(vertices)
                vertices.append(name)

# T-graph variables: (R0 x B2) -> (ROUT x B2).
for rr in R0:
    for bc in B2:
        for tr in ROUT:
            for dc in B2:
                name = f"T_{m(rr)}x{m(bc)}__{m(tr)}x{m(dc)}"
                index[("T", rr, bc, tr, dc)] = len(vertices)
                vertices.append(name)

assert len(vertices) == 1600 + 2500


parent = list(range(len(vertices)))
size = [1] * len(vertices)
anchored_root = set()


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    a, b = find(a), find(b)
    if a == b:
        return a
    if size[a] < size[b]:
        a, b = b, a
    parent[b] = a
    size[a] += size[b]
    return a


one_term = 0
two_term = 0
equations_seen = set()
anchors = set()
edges = set()

# Equation indexed by a base cubic, a variable derivative, and an E/T target.
for ur in U0:
    for bc in B3:
        for i in range(5):
            for a in range(5):
                for tr in ROUT:
                    for dc in B2:
                        terms = []
                        # derivative of the S graph output
                        if i not in tr and a not in dc:
                            vr = tuple(sorted(tr + (i,)))
                            outc = tuple(sorted(dc + (a,)))
                            terms.append(index[("S", ur, bc, vr, outc)])
                        # T graph applied to derivative of the S base
                        if i in ur and a in bc:
                            rr = tuple(x for x in ur if x != i)
                            inc = tuple(x for x in bc if x != a)
                            terms.append(index[("T", rr, inc, tr, dc)])
                        if not terms:
                            continue
                        key = tuple(terms)
                        equations_seen.add(key)

for eq in equations_seen:
    if len(eq) == 1:
        one_term += 1
        anchors.add(eq[0])
    else:
        assert len(eq) == 2
        two_term += 1
        edge = tuple(sorted(eq))
        edges.add(edge)

for a, b in edges:
    union(a, b)

for a in anchors:
    anchored_root.add(find(a))

# Roots may have changed after union; recompute anchored roots.
anchored_root = {find(a) for a in anchors}
components = defaultdict(list)
for v in range(len(vertices)):
    components[find(v)].append(v)

unanchored = [vals for root, vals in components.items() if root not in anchored_root]
unanchored.sort(key=lambda vals: vertices[min(vals)])

key_by_vertex = [None] * len(vertices)
for key, value in index.items():
    key_by_vertex[value] = key


def permute_column_vertex(v, perm):
    key = key_by_vertex[v]
    if key[0] == "S":
        kind, ur, bc, vr, dc = key
        bc2 = tuple(sorted(perm[x] for x in bc))
        dc2 = tuple(sorted(perm[x] for x in dc))
        return index[(kind, ur, bc2, vr, dc2)]
    kind, rr, bc, tr, dc = key
    bc2 = tuple(sorted(perm[x] for x in bc))
    dc2 = tuple(sorted(perm[x] for x in dc))
    return index[(kind, rr, bc2, tr, dc2)]


column_perms = list(permutations(range(5)))
component_is_column_symmetric = []
for vals in unanchored:
    block = set(vals)
    component_is_column_symmetric.append(all(
        {permute_column_vertex(v, p) for v in vals} == block
        for p in column_perms
    ))


def compress_row_support(vals):
    s_moves = set()
    t_moves = set()
    bad_identity = []
    for v in vals:
        name = vertices[v]
        if name.startswith("S_"):
            left, right = name[2:].split("__")
            ur, bc = left.split("x")
            vr, dc = right.split("x")
            s_moves.add((ur, vr))
            if bc != dc:
                bad_identity.append(vertices[v])
        else:
            left, right = name[2:].split("__")
            rr, bc = left.split("x")
            tr, dc = right.split("x")
            t_moves.add((rr, tr))
            if bc != dc:
                bad_identity.append(vertices[v])
    return {
        "S_row_moves": [f"{a}->{b}" for a, b in sorted(s_moves)],
        "T_row_moves": [f"{a}->{b}" for a, b in sorted(t_moves)],
        "all_column_moves_are_identity": not bad_identity,
        "bad_column_moves": bad_identity,
    }


payload = {
    "status": "PASS_EXACT_INTEGER_ORBIT0_FULL_FLAG_TANGENT_AND_COLUMN_TRIVIALITY",
    "coefficient_ring": "integers; all nonzero coefficients are +/-1",
    "vertex_count": len(vertices),
    "distinct_one_term_equations": one_term,
    "distinct_two_term_equations": two_term,
    "connected_component_count": len(components),
    "anchored_component_count": len(components) - len(unanchored),
    "unanchored_component_count": len(unanchored),
    "kernel_dimension_over_every_field": len(unanchored),
    "column_permutation_group_order": len(column_perms),
    "every_unanchored_component_fixed_setwise_by_column_permutations": all(
        component_is_column_symmetric
    ),
    "unanchored_components": [
        {
            "size": len(vals),
            "row_support": compress_row_support(vals),
            "first_vertices": [vertices[v] for v in vals[:12]],
        }
        for vals in unanchored
    ],
}

assert len(unanchored) == 8
assert all(x["row_support"]["all_column_moves_are_identity"]
           for x in payload["unanchored_components"])
assert all(component_is_column_symmetric)
assert sorted(x["size"] for x in payload["unanchored_components"]) == [
    20, 20, 20, 20, 30, 30, 50, 50
]

out = Path("n5_s20_orbit0_fullflag_tangent_graph_integer_exact.json")
out.write_bytes((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"))
print(json.dumps({k: payload[k] for k in (
    "vertex_count", "distinct_one_term_equations",
    "distinct_two_term_equations", "connected_component_count",
    "unanchored_component_count", "kernel_dimension_over_every_field",
)}, sort_keys=True))
for c in payload["unanchored_components"]:
    print(c["size"], c["row_support"])
print("output", out)
print("sha256", hashlib.sha256(out.read_bytes()).hexdigest().upper())
