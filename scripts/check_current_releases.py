#!/usr/bin/env python3
"""Check current and archived file inventories; this does not prove a theorem.

Read-only. Never creates or repairs an expected hash. Standard library only.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def check_manifest(root: Path, *, exact_paths: set[str] | None = None) -> int:
    manifest = root / 'MANIFEST.sha256'
    if not manifest.is_file():
        raise RuntimeError(f'Missing inventory: {manifest}')
    seen: set[str] = set()
    for line_number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        match = re.fullmatch(r'([0-9a-fA-F]{64})\s+\*?(.+)', line)
        if match is None:
            raise RuntimeError(f'Invalid inventory line {manifest}:{line_number}')
        expected, relative = match.groups()
        target = (root / relative).resolve()
        if relative in seen or not target.is_relative_to(root.resolve()):
            raise RuntimeError(f'Duplicate or escaping inventory path: {relative}')
        seen.add(relative)
        if not target.is_file():
            raise RuntimeError(f'Missing inventoried file: {target}')
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise RuntimeError(f'Checksum mismatch: {target}')
    if not seen:
        raise RuntimeError(f'Empty inventory: {manifest}')
    if exact_paths is not None and seen != exact_paths:
        raise RuntimeError(f'Current inventory coverage mismatch in {root}: missing={sorted(exact_paths-seen)}, extra={sorted(seen-exact_paths)}')
    return len(seen)

def check_release(root: Path, n: int) -> dict[str, int]:
    paper = root / 'paper'
    expected = {
        'README.md',
        'paper/source/main.tex',
        f'paper/perm{n}_chow_rank_{2**(n-1)}.pdf',
        'paper/AUDIT.md',
        'paper/BUILD.json',
        'paper/verify_supplementary.py',
        'paper/supplementary_results.json',
    }
    files = check_manifest(root, exact_paths=expected)
    receipt = json.loads((paper / 'BUILD.json').read_text(encoding='utf-8'))
    for path_key, hash_key in [('canonical_source', 'source_sha256'), ('canonical_pdf', 'pdf_sha256')]:
        target = (paper / receipt[path_key]).resolve()
        if not target.is_relative_to(paper.resolve()):
            raise RuntimeError('Build receipt path escapes paper directory')
        if hashlib.sha256(target.read_bytes()).hexdigest() != receipt[hash_key]:
            raise RuntimeError(f'Build receipt mismatch: {target}')
    if not receipt.get('mathematical_source_unchanged') or not receipt.get('source_only'):
        raise RuntimeError('Unexpected source or build acceptance status')
    if receipt.get('shell_escape') is not False:
        raise RuntimeError('Unexpected shell-escape setting')
    archive_files = check_manifest(root / 'archive' / 'computation-assisted')
    return {'n': n, 'current_files': files, 'archived_original_files': archive_files}

def main() -> int:
    results = [check_release(ROOT / f'perm{n}', n) for n in (4, 5, 6)]
    print(json.dumps({'status': 'RELEASE_INTEGRITY_PASS', 'proof_certification': False, 'packages': results}, indent=2))
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(f'RELEASE_INTEGRITY_FAIL: {exc}', file=sys.stderr)
        raise SystemExit(1)
