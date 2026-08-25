"""Replay every exact certificate used by the public perm3/perm4 manuscript."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(*arguments: str) -> str:
    completed = subprocess.run(
        [sys.executable, *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    print(completed.stdout, end="")
    return completed.stdout


def main() -> None:
    actual = json.loads(run("perm3_exact_verification.py"))
    expected = json.loads(
        (ROOT / "perm3_exact_verification_v11.json").read_text(encoding="utf-8")
    )
    if actual != expected:
        raise AssertionError("perm3 exact output does not match the frozen certificate")

    run("perm4_rank8_independent_audit.py")
    run("perm4_rank8_verify_all.py")
    print("PERM34_ACTIVE_PROOF_REPLAY_PASS")


if __name__ == "__main__":
    main()
