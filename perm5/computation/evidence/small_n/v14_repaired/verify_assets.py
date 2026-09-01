#!/usr/bin/env python3
"""Fail-closed verifier for the v14 PDF and reviewer package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.json"
PDF_NAME = "perm345_chow_rank_v14_repaired_zh_ams.pdf"
ZIP_NAME = "perm345_reviewer_submission_v14_repaired_20260812.zip"
EXPECTED_ARTIFACTS = {PDF_NAME, ZIP_NAME}
SHA256_PATTERN = re.compile(r"[0-9A-Fa-f]{64}")


def fail(message: str) -> None:
    raise SystemExit("V14_ASSET_VERIFY_FAIL: " + message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate_artifacts(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        fail("artifacts must be a list")
    if len(artifacts) != len(EXPECTED_ARTIFACTS):
        fail("manifest must contain exactly the two release artifacts")

    by_name: dict[str, dict[str, object]] = {}
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            fail(f"artifact {index} must be an object")
        if set(artifact) != {"file", "bytes", "sha256"}:
            fail(f"artifact {index} has an unexpected schema")

        name = artifact.get("file")
        byte_count = artifact.get("bytes")
        digest = artifact.get("sha256")
        if not isinstance(name, str) or not name:
            fail(f"artifact {index} has an invalid file name")
        if name in by_name:
            fail(f"duplicate artifact {name}")
        if type(byte_count) is not int or byte_count <= 0:
            fail(f"artifact {name} has an invalid byte count")
        if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
            fail(f"artifact {name} has an invalid SHA-256")
        by_name[name] = artifact

    if set(by_name) != EXPECTED_ARTIFACTS:
        fail("artifact name set does not match the frozen release")
    return by_name


def run_inner(script: str, extracted: Path) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(
        [sys.executable, "-B", script],
        cwd=extracted,
        env=environment,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        fail("manifest root must be an object")
    if payload.get("format") != "perm345-v14-repaired-release-assets-v1":
        fail("unexpected manifest format")
    artifacts = validate_artifacts(payload)
    for name, artifact in artifacts.items():
        path = ROOT / name
        if not path.is_file():
            fail(f"missing {path.name}")
        if path.stat().st_size != artifact["bytes"]:
            fail(f"byte count mismatch for {path.name}")
        if sha256(path) != str(artifact["sha256"]).upper():
            fail(f"SHA-256 mismatch for {path.name}")

    zip_entries = payload.get("zip_entries")
    if type(zip_entries) is not int or zip_entries <= 0:
        fail("zip_entries must be a positive integer")

    zip_path = ROOT / ZIP_NAME
    with ZipFile(zip_path) as archive:
        entries = archive.infolist()
        if len(entries) != zip_entries:
            fail("ZIP entry count mismatch")
        names = set()
        for entry in entries:
            name = entry.filename.replace("\\", "/")
            parts = Path(name).parts
            if not name or name.startswith("/") or ".." in parts:
                fail(f"unsafe ZIP member {name!r}")
            if name in names:
                fail(f"duplicate ZIP member {name}")
            names.add(name)
            if entry.file_size >= 100_000_000:
                fail(f"unexpectedly large ZIP member {name}")
        required = {
            "PACKAGE_MANIFEST.json",
            "REVIEWER_README.md",
            "requirements-replay.txt",
            "verify_manifest.py",
            "replay_active_proof.py",
            "perm5_one_intersection_flag_standalone_exact.py",
            "n5_one_intersection_flag_standalone_exact.json",
            "latex/perm345_v14_repaired/n5_body.tex",
            "latex/perm345_v14_repaired/formal_computation_spec.tex",
        }
        missing = required - names
        if missing:
            fail(f"required ZIP entries missing: {sorted(missing)}")
        with tempfile.TemporaryDirectory(prefix="perm345_v14_asset_verify_") as temporary:
            extracted = Path(temporary)
            archive.extractall(extracted)
            run_inner("verify_manifest.py", extracted)
            if args.replay:
                run_inner("replay_active_proof.py", extracted)
                run_inner("verify_manifest.py", extracted)

    print(
        "PASS_V14_REPAIRED_RELEASE_ASSETS "
        f"files=2 zip_entries={zip_entries} replay={args.replay}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
