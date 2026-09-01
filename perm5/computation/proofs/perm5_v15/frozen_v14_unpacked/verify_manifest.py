#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"


def fail(message: str) -> None:
    raise SystemExit("PACKAGE_VERIFY_FAIL: " + message)


payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
if payload.get("format") != "perm345-v14-repaired-reviewer-package-v1":
    fail("unknown format")
records = payload.get("files")
if not isinstance(records, list):
    fail("files must be a list")
expected = {"PACKAGE_MANIFEST.json"}
for record in records:
    name = record.get("path")
    if not isinstance(name, str) or not name or name.startswith(("/", "\\")) or ".." in Path(name).parts:
        fail(f"unsafe path {name!r}")
    if name in expected:
        fail(f"duplicate path {name}")
    expected.add(name)
    path = ROOT / name
    if not path.is_file():
        fail(f"missing {name}")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest().upper()
    if len(data) != record.get("bytes") or digest != record.get("sha256"):
        fail(f"identity mismatch {name}")
actual = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file()
}
if actual != expected:
    fail(f"file-set mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
print(f"PACKAGE_VERIFY_PASS files={len(actual)}")
