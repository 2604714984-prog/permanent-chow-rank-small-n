#!/usr/bin/env python3
"""Replay the public perm_5 package's independent and optional full checks."""

from __future__ import annotations

import argparse
import json
import os
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


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_independent() -> None:
    with tempfile.TemporaryDirectory(prefix="perm5-public-audit-") as temporary:
        output = Path(temporary)
        run(str(SCRIPTS / "perm5_fixed_six_state_table.py"), "--output-dir", str(output))
        if load_json(output / "perm5_fixed_six_state_table.json") != load_json(
            EVIDENCE / "perm5_fixed_six_state_table.json"
        ):
            raise RuntimeError("fixed-six state-table receipt mismatch")

        terminal = output / "perm5_terminal_independent_audit.json"
        run(str(SCRIPTS / "perm5_terminal_independent_audit.py"), "--output", str(terminal))
        if load_json(terminal) != load_json(
            EVIDENCE / "perm5_terminal_independent_audit.json"
        ):
            raise RuntimeError("terminal independent-audit receipt mismatch")


def verify_full() -> None:
    if os.name != "nt":
        raise RuntimeError(
            "the historical frozen byte replay requires Windows because its "
            "manifest binds CRLF output bytes; use the independent checks on "
            "other platforms"
        )
    try:
        import sympy  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "install computation/requirements-replay.txt before --full"
        ) from exc
    if sympy.__version__ != "1.14.0":
        raise RuntimeError(f"expected SymPy 1.14.0, observed {sympy.__version__}")

    with tempfile.TemporaryDirectory(prefix="perm5-public-full-") as temporary:
        for mode in ("normal", "optimized"):
            receipt = Path(temporary) / f"replay_{mode}.json"
            run(
                str(SCRIPTS / "replay_perm5_v15_full.py"),
                "--mode",
                mode,
                "--receipt",
                str(receipt),
            )
            payload = load_json(receipt)
            if payload.get("status") != "PASS" or payload.get("mode") != mode:
                raise RuntimeError(f"full {mode} replay did not return PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full",
        action="store_true",
        help="also run the Windows-bound frozen normal and optimized replays",
    )
    args = parser.parse_args()
    verify_independent()
    if args.full:
        verify_full()
    print(f"PERM5_PUBLIC_VERIFY_PASS full={args.full}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
