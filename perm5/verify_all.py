#!/usr/bin/env python3
"""Run every finite computation used by the perm5 proof."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
COMPUTATION = ROOT / "computation"
SCRIPTS = COMPUTATION / "scripts"
EVIDENCE = COMPUTATION / "evidence"


def run(script: str, *arguments: str) -> None:
    subprocess.run(
        [sys.executable, "-B", str(SCRIPTS / script), *arguments],
        cwd=COMPUTATION,
        check=True,
    )


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="perm5_verification_") as name:
        output = Path(name)

        run(
            "perm5_one_intersection_independent_multifield.py",
            "--output",
            str(output / "one_intersection.json"),
        )

        run("perm5_fixed_six_state_table.py", "--output-dir", str(output))
        if load_json(output / "perm5_fixed_six_state_table.json") != load_json(
            EVIDENCE / "perm5_fixed_six_state_table.json"
        ):
            raise RuntimeError("fixed-six state table mismatch")

        run(
            "perm5_d11_d12_parent_table_independent.py",
            "--output",
            str(output / "parent_table.json"),
        )

        terminal = output / "perm5_terminal_independent_verification.json"
        run("perm5_terminal_independent_verification.py", "--output", str(terminal))
        if load_json(terminal) != load_json(
            EVIDENCE / "perm5_terminal_independent_verification.json"
        ):
            raise RuntimeError("terminal calculation mismatch")

        run(
            "perm5_glynn_upper_bound_independent.py",
            "--output",
            str(output / "glynn.json"),
        )

    print("PERM5_PROOF_VERIFICATION_PASS computations=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
