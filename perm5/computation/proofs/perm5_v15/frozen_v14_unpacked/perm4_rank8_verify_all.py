"""Run the compact verification suite for ChowRank(perm_4)=8."""

from __future__ import annotations

import subprocess
import sys


CHECKS = [
    (
        [sys.executable, "perm4_chow_experiments.py"],
        [
            "Glynn max coefficient error: 0",
            "rank P_{2,2}^wedge1(perm_4): 560",
            "rank P_{2,2}^wedge1(x0*x1*x2*x3): 92",
        ],
    ),
    (
        [
            sys.executable,
            "perm4_quadratic_extension_chart_exact_verify.py",
        ],
        [
            "A_top_determinant=1",
            "full_minor_constant=-32768",
            "exact_nonzero_diagonals=0",
            "exact_simultaneously_strict_triangular=True",
            "exact_chart_minor=constant*v00^99",
        ],
    ),
    (
        [
            sys.executable,
            "perm4_quadratic_extension_full_minor_replay.py",
        ],
        [
            "selected_A=560 selected_Q=99",
            "failures=[]",
        ],
    ),
]


def main() -> None:
    for command, expected_fragments in CHECKS:
        completed = subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        output = completed.stdout + completed.stderr
        name = command[1]
        if completed.returncode:
            print(output)
            raise SystemExit(f"FAIL {name}: exit {completed.returncode}")
        missing = [
            fragment
            for fragment in expected_fragments
            if fragment not in output
        ]
        if missing:
            print(output)
            raise SystemExit(f"FAIL {name}: missing {missing}")
        print(f"PASS {name}")
    print("ALL_RANK8_CHECKS_PASS")


if __name__ == "__main__":
    main()
