"""Replay the exact certificate accompanying the perm3 manuscript."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    completed = subprocess.run(
        [sys.executable, "perm3_exact_verification.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    print(completed.stdout, end="")
    actual = json.loads(completed.stdout)
    expected = json.loads(
        (ROOT / "perm3_exact_verification_v11.json").read_text(encoding="utf-8")
    )
    if actual != expected:
        raise AssertionError("perm3 exact output does not match the frozen certificate")
    print("PERM3_ACTIVE_PROOF_REPLAY_PASS")


if __name__ == "__main__":
    main()
