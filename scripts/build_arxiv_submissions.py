#!/usr/bin/env python3
"""Build deterministic source ZIPs from separately frozen release inventories.

This builder never rewrites an inventory, including historical certificates.
PDF previews are separate deliverables, not top-level source ZIP members.
"""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(n, output_directory):
    source = ROOT / "submissions" / "20261016" / f"perm{n}"
    manifest = source / "anc" / "SOURCE_MANIFEST.sha256"
    members = []
    for line in manifest.read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        relative = Path(name.removeprefix("*"))
        path = (source / relative).resolve()
        if not path.is_relative_to(source.resolve()):
            raise RuntimeError("inventory path escapes submission root")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest().lower() != expected.lower():
            raise RuntimeError(f"release inventory mismatch: {relative}")
        members.append((relative.as_posix(), data))
    members.append(("anc/SOURCE_MANIFEST.sha256", manifest.read_bytes()))
    names = [name for name,_ in members]
    if len(set(names)) != len(names) or "main.tex" not in names:
        raise RuntimeError("duplicate member or missing main.tex")
    if any(name != "main.tex" and not name.startswith("anc/") for name in names):
        raise RuntimeError("unexpected top-level submission member")
    output_directory.mkdir(parents=True, exist_ok=True)
    archive = output_directory / f"perm{n}_arxiv_20261016.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name,data in sorted(members):
            info = zipfile.ZipInfo(name, date_time=(2026,10,16,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(f"{archive.name} members={len(members)} sha256={hashlib.sha256(archive.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    for n in (5,6):
        build(n,args.output_dir)
