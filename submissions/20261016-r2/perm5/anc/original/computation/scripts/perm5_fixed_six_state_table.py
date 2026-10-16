#!/usr/bin/env python3
"""Generate and verification the 58-state fixed-six routing table for perm_5.

This is a deliberately small, definition-level verification.  It reconstructs the
Petersen-product minimum-shadow table, generates the 58 integer states from the
closed inequalities in the paper, assigns each state to exactly one written
exclusion route, and emits JSON, CSV, and LaTeX tables.

The script checks the finite arithmetic and the route partition.  It does not
replace the geometric or rank arguments attached to the routes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from functools import lru_cache
from pathlib import Path

PETERSEN_COMPLEMENT_NEIGHBORHOODS = (10, 7, 5, 4, 4, 2, 1, 1, 0, 0, 0)
LAYER_DIFFERENCES = tuple(
    PETERSEN_COMPLEMENT_NEIGHBORHOODS[i - 1]
    - PETERSEN_COMPLEMENT_NEIGHBORHOODS[i]
    for i in range(1, 11)
)
EXPECTED_SHADOWS = (
    0, 9, 15, 18, 18, 24, 27, 27, 30, 30, 30, 35,
    35, 36, 36, 36, 36, 42, 45, 45, 48, 48, 48, 52,
)
P_UPPER = {
    9: 35,
    10: 50,
    11: 55,
    12: 61,
    # If W is enlarged by one quadratic quotient direction, the target of
    # the polarization map loses a 25-dimensional summand.  Thus
    # p_{d+1} <= p_d + 25.  Starting from p_12 <= 61 gives these bounds.
    13: 86,
    14: 111,
    15: 136,
}
ROUTE_LABELS = {
    "A": "Petersen equality at (19,9,45)",
    "B": "global prolongation / double quotient",
    "C": "d=9 equality geometry",
    "D": "p_11 <= 55 endpoint",
    "E": "coarse p_12 <= 80 endpoint",
    "F": "sharp p_12 <= 61 endpoint",
    "G": "flag-annihilator gap for d=11,12",
    "H": "three terminal orbits for d=10",
}
EXPECTED_ROUTE_COUNTS = {
    "A": 1,
    "B": 38,
    "C": 1,
    "D": 2,
    "E": 1,
    "F": 1,
    "G": 5,
    "H": 9,
}


@lru_cache(maxsize=None)
def tail(layer: int, remaining: int, cap: int) -> int:
    if layer == 10:
        return 0 if remaining == 0 else -10**9
    return max(
        LAYER_DIFFERENCES[layer]
        * PETERSEN_COMPLEMENT_NEIGHBORHOODS[value]
        + tail(layer + 1, remaining - value, value)
        for value in range(min(cap, remaining) + 1)
    )


def shadow_lower(size: int) -> int:
    if size == 0:
        return 0
    complement_upper = max(
        LAYER_DIFFERENCES[0]
        * PETERSEN_COMPLEMENT_NEIGHBORHOODS[first]
        + tail(1, size - first, first)
        for first in range(1, min(10, size) + 1)
    )
    return 100 - complement_upper


def route_for(s: int, d: int, t: int) -> str:
    """The mutually exclusive routing order stated in the revised paper."""
    if (s, d, t) == (19, 9, 45):
        return "A"
    # Seventeen d=9 states violate p >= t+d-s together with p_9 <= 35.
    # The remaining twenty-one B states are precisely s=19,d>=10.
    if (d == 9 and (s, t) != (22, 48)) or (s == 19 and d >= 10):
        return "B"
    if (s, d, t) == (22, 9, 48):
        return "C"
    if s == 20 and d == 11:
        return "D"
    if (s, d, t) == (20, 12, 48):
        return "E"
    if (s, d, t) == (21, 12, 48):
        return "F"
    if d == 10 and s in (20, 21, 22):
        return "H"
    return "G"


def build_states(shadows: tuple[int, ...]) -> list[dict[str, object]]:
    states: list[dict[str, object]] = []
    for s in range(19, 23):
        m_s = shadows[s]
        for d in range(9, 61 - m_s):
            for t in range(m_s, 61 - d):
                route = route_for(s, d, t)
                p_required = t + d - s
                p_upper = P_UPPER.get(d)
                residual_lower = None
                residual_margin = None
                if p_upper is not None:
                    residual_lower = (
                        2400 + (25 * d - p_upper) - (25 * s - m_s)
                    )
                    residual_margin = residual_lower - 2160
                states.append(
                    {
                        "s": s,
                        "d": d,
                        "t": t,
                        "h": t + d,
                        "m_s": m_s,
                        "p_required": p_required,
                        "p_upper": p_upper,
                        "p_gap": None if p_upper is None else p_required - p_upper,
                        "residual_K_lower_with_displayed_p_bound": residual_lower,
                        "margin_over_9_times_240": residual_margin,
                        "route": route,
                        "route_description": ROUTE_LABELS[route],
                    }
                )
    return states


def write_csv(path: Path, states: list[dict[str, object]]) -> None:
    fieldnames = list(states[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(states)


def tex_value(value: object) -> str:
    return "--" if value is None else str(value)


def write_tex(path: Path, states: list[dict[str, object]]) -> None:
    lines = [
        "% Generated by scripts/perm5_fixed_six_state_table.py; do not edit.",
        "\\begingroup",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3.1pt}",
        "\\renewcommand{\\arraystretch}{1.02}",
        "\\begin{longtable}{rrrrrrrcl}",
        "\\caption{The complete fixed-six state universe and its unique exclusion route. "
        "The columns $p_d^{\\rm up}$ and $K_{\\rm low}$ show the displayed global "
        "prolongation bound and its substitution in the double-quotient inequality; "
        "for $d=13,14,15$ the bound follows from $p_{d+1}\\le p_d+25$.}"
        "\\label{tab:all-58-states}\\\\",
        "\\toprule",
        "$s$&$d$&$t$&$h$&$m_s$&$t+d-s$&$p_d^{\\rm up}$&$K_{\\rm low}$&route\\\\",
        "\\midrule",
        "\\endfirsthead",
        "\\toprule",
        "$s$&$d$&$t$&$h$&$m_s$&$t+d-s$&$p_d^{\\rm up}$&$K_{\\rm low}$&route\\\\",
        "\\midrule",
        "\\endhead",
    ]
    for row in states:
        lines.append(
            "{s}&{d}&{t}&{h}&{m_s}&{p_required}&{p_upper}&{k_low}&{route}\\\\".format(
                s=row["s"], d=row["d"], t=row["t"], h=row["h"],
                m_s=row["m_s"], p_required=row["p_required"],
                p_upper=tex_value(row["p_upper"]),
                k_low=tex_value(row["residual_K_lower_with_displayed_p_bound"]),
                route=row["route"],
            )
        )
    lines.extend(["\\bottomrule", "\\end{longtable}", "\\endgroup", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    shadows = tuple(shadow_lower(size) for size in range(24))
    if shadows != EXPECTED_SHADOWS:
        raise RuntimeError(("shadow table mismatch", shadows))
    states = build_states(shadows)
    if len(states) != 58:
        raise RuntimeError(("state count", len(states)))

    observed_counts = {
        route: sum(row["route"] == route for row in states)
        for route in ROUTE_LABELS
    }
    if observed_counts != EXPECTED_ROUTE_COUNTS:
        raise RuntimeError(("route counts", observed_counts))
    if any(row["route"] not in ROUTE_LABELS for row in states):
        raise RuntimeError("unrouted state")

    # Definition-level checks for the two transparent global subfamilies.
    d9_global = [row for row in states if row["route"] == "B" and row["d"] == 9]
    if len(d9_global) != 17 or not all(int(row["p_gap"]) > 0 for row in d9_global):
        raise RuntimeError("d=9 p-gap verification failed")
    s19_global = [
        row for row in states
        if row["route"] == "B" and row["s"] == 19 and row["d"] >= 10
    ]
    if len(s19_global) != 21 or not all(
        int(row["margin_over_9_times_240"]) > 0 for row in s19_global
    ):
        raise RuntimeError("s=19 double-quotient margins failed")

    json_path = args.output_dir / "perm5_fixed_six_state_table.json"
    csv_path = args.output_dir / "perm5_fixed_six_state_table.csv"
    tex_path = args.output_dir / "perm5_fixed_six_state_table.tex"
    payload = {
        "status": "PASS",
        "claim_type": "definition-level exact verification of the 58-state universe and route partition",
        "petersen_product_minimum_shadows_0_to_23": list(shadows),
        "route_labels": ROUTE_LABELS,
        "route_counts": observed_counts,
        "state_count": len(states),
        "states": states,
        "strict_scope": (
            "This file checks integer generation and unique routing.  The geometric equality "
            "cases, prolongation bounds, flag-annihilator estimates, and terminal-orbit "
            "contradictions are proved in the manuscript and checked by their dedicated "
            "exact certificates."
        ),
    }
    json_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    json_path.write_text(json_text, encoding="utf-8")
    write_csv(csv_path, states)
    write_tex(tex_path, states)

    summary = {
        "status": "PASS",
        "state_count": len(states),
        "route_counts": observed_counts,
        "json_sha256": hashlib.sha256(json_path.read_bytes()).hexdigest().upper(),
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest().upper(),
        "tex_sha256": hashlib.sha256(tex_path.read_bytes()).hexdigest().upper(),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
