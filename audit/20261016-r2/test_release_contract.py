#!/usr/bin/env python3
"""Standard-library regression tests. Mutations use synthetic/temp fixtures only."""
from __future__ import annotations
import ast
import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("archive_builder", ROOT / "scripts/build_arxiv_submissions.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
RELEASE = "20261016-r2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SyntheticBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="synthetic_release_contract_")
        self.base = Path(self.temporary.name)
        self.source = self.base / "submissions" / RELEASE / "perm5"
        (self.source / "anc").mkdir(parents=True)
        (self.source / "main.tex").write_bytes(b"synthetic TeX fixture\n")
        (self.source / "anc/data.json").write_bytes(b'{"fixture":true}\n')
        self.manifest = self.source / "anc/SOURCE_MANIFEST.sha256"
        self.freeze_synthetic_inventory()
        self.patch = mock.patch.object(BUILDER, "ROOT", self.base)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.addCleanup(self.temporary.cleanup)

    def freeze_synthetic_inventory(self) -> None:
        files = sorted(p for p in self.source.rglob("*") if p.is_file() and p != self.manifest)
        self.manifest.write_bytes(("\n".join(digest(p)+" *"+p.relative_to(self.source).as_posix() for p in files)+"\n").encode())

    def build(self) -> bytes:
        with contextlib.redirect_stdout(io.StringIO()):
            BUILDER.build(5, self.base / "dist", RELEASE)
        return (self.base / "dist" / f"perm5_arxiv_{RELEASE}.zip").read_bytes()

    def test_repeated_build_is_identical(self) -> None:
        self.assertEqual(self.build(), self.build())

    def test_metadata_and_stored_payloads(self) -> None:
        with zipfile.ZipFile(io.BytesIO(self.build())) as z:
            self.assertEqual(z.namelist(), sorted(z.namelist()))
            for entry in z.infolist():
                self.assertEqual(entry.create_system, 3)
                self.assertEqual(entry.date_time, (2026, 10, 16, 0, 0, 0))
                self.assertEqual(entry.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(entry.external_attr, 0o100644 << 16)
                self.assertEqual(entry.compress_size, entry.file_size)
            self.assertIsNone(z.testzip())

    def test_does_not_call_a_compression_backend(self) -> None:
        expected = self.build()
        with mock.patch.object(zlib, "compressobj", side_effect=RuntimeError("compression backend must not be called")):
            self.assertEqual(self.build(), expected)

    def test_default_creator_platform_does_not_change_bytes(self) -> None:
        expected = self.build()
        original = zipfile.ZipInfo
        class DOSDefault(original):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.create_system = 0
        with mock.patch.object(zipfile, "ZipInfo", DOSDefault):
            self.assertEqual(self.build(), expected)

    def test_changed_payload_rejected_without_hash_rewrite(self) -> None:
        before = self.manifest.read_bytes()
        (self.source / "anc/data.json").write_bytes(b"changed fixture\n")
        with self.assertRaisesRegex(RuntimeError, "inventory mismatch"):
            self.build()
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_missing_payload_rejected(self) -> None:
        (self.source / "anc/data.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build()

    def test_duplicate_manifest_entry_rejected(self) -> None:
        data = self.manifest.read_bytes()
        self.manifest.write_bytes(data+data.splitlines(keepends=True)[0])
        with self.assertRaisesRegex(RuntimeError, "duplicate member"):
            self.build()

    def test_nested_tex_rejected(self) -> None:
        (self.source / "anc/historical.tex").write_bytes(b"synthetic obsolete manuscript\n")
        self.freeze_synthetic_inventory()
        with self.assertRaisesRegex(RuntimeError, "TeX source"):
            self.build()

    def test_root_noise_rejected(self) -> None:
        (self.source / "preview.pdf").write_bytes(b"synthetic fixture, not a PDF")
        self.freeze_synthetic_inventory()
        with self.assertRaisesRegex(RuntimeError, "top-level"):
            self.build()

    def test_parent_path_rejected(self) -> None:
        with self.manifest.open("ab") as stream:
            stream.write(("0"*64+" *../outside.txt\n").encode())
        with self.assertRaisesRegex(RuntimeError, "escapes submission root"):
            self.build()

    def test_missing_main_tex_rejected(self) -> None:
        self.manifest.write_bytes(b"\n".join(x for x in self.manifest.read_bytes().splitlines() if not x.endswith(b" *main.tex"))+b"\n")
        with self.assertRaisesRegex(RuntimeError, "missing main.tex"):
            self.build()

    def test_unknown_release_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown release"):
            BUILDER.build(5, self.base / "dist", "unregistered")


class PublishedReleaseTests(unittest.TestCase):
    def test_r2_actual_archives_rebuild_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory(prefix="r2_byte_rebuild_") as directory:
            out = Path(directory)
            for n in (5, 6):
                with contextlib.redirect_stdout(io.StringIO()):
                    BUILDER.build(n, out)  # The default must select the active release.
                name = f"perm{n}_arxiv_{RELEASE}.zip"
                self.assertEqual((out / name).read_bytes(), (ROOT / "dist" / name).read_bytes())

    def test_legacy_archives_rebuild_exact_payloads(self) -> None:
        # Legacy compressed bitstreams may differ between zlib and zlib-ng.
        with tempfile.TemporaryDirectory(prefix="legacy_payload_rebuild_") as directory:
            out = Path(directory)
            for n in (5, 6):
                with contextlib.redirect_stdout(io.StringIO()):
                    BUILDER.build(n, out, "20261016")
                name = f"perm{n}_arxiv_20261016.zip"
                with zipfile.ZipFile(out / name) as new, zipfile.ZipFile(ROOT / "dist" / name) as old:
                    self.assertEqual(new.namelist(), old.namelist())
                    for entry in old.namelist():
                        self.assertEqual(new.read(entry), old.read(entry))

    def test_frozen_expected_hashes_and_subsets(self) -> None:
        for n, expected_count in ((5, 9), (6, 7)):
            anc = ROOT / "submissions" / RELEASE / f"perm{n}" / "anc"
            spec = importlib.util.spec_from_file_location(f"perm{n}_submission", anc / "verify_submission.py")
            wrapper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wrapper)
            self.assertEqual((anc / "original/MANIFEST.sha256").read_bytes(), (ROOT / f"perm{n}/MANIFEST.sha256").read_bytes())
            count, _ = wrapper.frozen_inventory()
            self.assertEqual(count, expected_count)
            for name in wrapper.parse_manifest(anc / "COMPUTATION_INPUTS.sha256"):
                self.assertEqual((anc / "original" / name).read_bytes(), (ROOT / f"perm{n}" / name).read_bytes())

    def test_no_disappearing_python_assert_checks(self) -> None:
        for n in (5, 6):
            for source in (ROOT / "submissions" / RELEASE / f"perm{n}" / "anc").rglob("*.py"):
                self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source.read_text(encoding="utf-8")))), str(source))


if __name__ == "__main__":
    unittest.main(verbosity=2)
