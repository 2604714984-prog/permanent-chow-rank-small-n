"""Exact symmetry audit for the three terminal n=5 flag representatives.

This is a research diagnostic.  It asks whether the 50 elementary-shift
direction records in the active witness-forest certificate can be replaced by
only a few cases modulo the stabilizer of each terminal flag.  All operations
are finite set permutations over S_5 x S_5 and optional transpose.
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path

from perm5_witness_forest_independent_audit import (
    LOCAL_CERT,
    ORBIT0_CERT,
    TARGETS,
    TI,
    TRIPLES,
    all_valid_directions,
    parse_records,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_flag_direction_symmetry_exact.json"
PERMS = tuple(permutations(range(5)))


def act_subset(values: tuple[int, ...], permutation: tuple[int, ...]):
    return tuple(sorted(permutation[value] for value in values))


TRIPLE_MAPS = {
    permutation: tuple(TI[act_subset(triple, permutation)] for triple in TRIPLES)
    for permutation in PERMS
}


def act_family(
    family: int,
    row_permutation: tuple[int, ...],
    column_permutation: tuple[int, ...],
    transpose: bool,
):
    row_map = TRIPLE_MAPS[row_permutation]
    column_map = TRIPLE_MAPS[column_permutation]
    result = 0
    remaining = family
    while remaining:
        bit = remaining & -remaining
        position = bit.bit_length() - 1
        row, column = divmod(position, 10)
        new_row, new_column = row_map[row], column_map[column]
        if transpose:
            new_row, new_column = new_column, new_row
        result |= 1 << (10 * new_row + new_column)
        remaining ^= bit
    return result


def act_plane(
    plane: int,
    row_permutation: tuple[int, ...],
    column_permutation: tuple[int, ...],
    transpose: bool,
):
    result = 0
    remaining = plane
    while remaining:
        bit = remaining & -remaining
        position = bit.bit_length() - 1
        row, column = divmod(position, 5)
        new_row = row_permutation[row]
        new_column = column_permutation[column]
        if transpose:
            new_row, new_column = new_column, new_row
        result |= 1 << (5 * new_row + new_column)
        remaining ^= bit
    return result


def stabilizer(orbit: str):
    family, plane = TARGETS[orbit]
    result = []
    for row_permutation in PERMS:
        for column_permutation in PERMS:
            for transpose in (False, True):
                if act_plane(
                    plane, row_permutation, column_permutation, transpose
                ) != plane:
                    continue
                if act_family(
                    family, row_permutation, column_permutation, transpose
                ) == family:
                    result.append(
                        (row_permutation, column_permutation, transpose)
                    )
    return tuple(result)


def act_direction(direction, group_element):
    kind, low, high = direction
    row_permutation, column_permutation, transpose = group_element
    if kind == "row":
        image_kind = "column" if transpose else "row"
        permutation = row_permutation
    else:
        image_kind = "row" if transpose else "column"
        permutation = column_permutation
    return image_kind, permutation[low], permutation[high]


def direction_orbits(directions, group):
    unassigned = set(directions)
    result = []
    while unassigned:
        seed = min(unassigned)
        orbit = {act_direction(seed, element) for element in group}
        assert orbit <= set(directions)
        result.append(tuple(sorted(orbit)))
        unassigned -= orbit
    return tuple(result)


def main():
    records = parse_records(LOCAL_CERT) + parse_records(
        ORBIT0_CERT, orbit0=True
    )
    by_key = {
        (record["orbit"], record["kind"], record["low"], record["high"]): record
        for record in records
    }
    result = {
        "status": "PASS_EXACT_INTEGER_DIRECTION_SYMMETRY_AUDIT",
        "evidence_role": (
            "research diagnostic only; a stabilizer-orbit count does not prove "
            "the witness implications"
        ),
        "orbits": {},
    }
    for orbit in ("orbit0", "orbit1", "orbit13"):
        group = stabilizer(orbit)
        directions = all_valid_directions(orbit, orbit == "orbit0")
        classes = direction_orbits(directions, group)
        class_records = []
        for direction_class in classes:
            signatures = set()
            for kind, low, high in direction_class:
                record = by_key[(orbit, kind, low, high)]
                signatures.add(
                    (
                        len(record["s"]) + len(record["l"]),
                        tuple(sorted(len(component) for component in record["components"])),
                    )
                )
            class_records.append(
                {
                    "representative": list(direction_class[0]),
                    "size": len(direction_class),
                    "directions": [list(direction) for direction in direction_class],
                    "witness_signatures": [
                        [variables, list(components)]
                        for variables, components in sorted(signatures)
                    ],
                }
            )
        result["orbits"][orbit] = {
            "stabilizer_size": len(group),
            "valid_direction_count": len(directions),
            "direction_orbit_count": len(classes),
            "direction_orbits": class_records,
        }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
