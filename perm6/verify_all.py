#!/usr/bin/env python3
"""Replay every exact verifier in the public perm_6 proof package."""

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


def run(*arguments: str) -> None:
    subprocess.run([sys.executable, "-B", *arguments], cwd=COMPUTATION, check=True)


def main() -> int:
    run(
        str(SCRIPTS / "n6_exact_ordinary_chow_rank_32.py"),
        "--verify-json",
        str(COMPUTATION / "data" / "n6_exact_ordinary_chow_rank_32.json"),
    )
    run("-m", "unittest", "tests.test_n6_exact_ordinary_chow_rank_32", "-v")
    run(str(SCRIPTS / "n6_independent_finite_core_audit.py"))
    with tempfile.TemporaryDirectory(prefix="perm6-public-audit-") as temporary:
        output = Path(temporary) / "n6_dependent_normal_forms_independent.json"
        run(
            str(SCRIPTS / "n6_dependent_normal_forms_independent.py"),
            "--output",
            str(output),
        )
        observed = json.loads(output.read_text(encoding="utf-8"))
        expected = json.loads(
            (EVIDENCE / output.name).read_text(encoding="utf-8")
        )
        if observed != expected:
            raise RuntimeError("independent normal-form receipt mismatch")
    print("PERM6_PUBLIC_VERIFY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
