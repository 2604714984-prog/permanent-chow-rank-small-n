#!/usr/bin/env python3
"""Audit-only PDF preflight. Needs PyMuPDF, pypdf and Pillow, not reader replay.

Inspects font descriptor metadata only. Does not extract or distribute fonts.
Renders previews outside the repository and compares them with the reviewed draft.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import fitz
from PIL import Image, ImageChops
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT.parent / "r2 accepted source extraction"
OUT = ROOT.parent / "final-r2-pdf-preview"
AUDIT = Path(__file__).resolve().parent


def font_records(reader: PdfReader) -> list[dict]:
    records = {}
    for page in reader.pages:
        resources = page.get("/Resources", {}).get_object()
        for _, reference in resources.get("/Font", {}).get_object().items():
            font = reference.get_object()
            descendants = font.get("/DescendantFonts")
            target = descendants[0].get_object() if descendants else font
            descriptor = target.get("/FontDescriptor")
            descriptor = descriptor.get_object() if descriptor else {}
            key = str(font.get("/BaseFont"))
            records[key] = {"name": key, "subtype": str(font.get("/Subtype")),
                            "embedded": any(field in descriptor for field in ("/FontFile", "/FontFile2", "/FontFile3"))}
    return sorted(records.values(), key=lambda x: x["name"])


def main() -> None:
    OUT.mkdir(exist_ok=True)
    results = []
    for n in (5, 6):
        path = WORK / f"perm{n}" / "main.pdf"
        doc = fitz.open(path)
        reader = PdfReader(path)
        fonts = font_records(reader)
        changed = []
        pages = []
        for page in doc:
            number = page.number + 1
            words = page.get_text("words")
            outside = [word[:4] for word in words if not (page.rect.x0 <= word[0] <= word[2] <= page.rect.x1 and page.rect.y0 <= word[1] <= word[3] <= page.rect.y1)]
            image_path = OUT / f"perm{n}_page{number:02d}.png"
            page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False).save(image_path)
            old = ROOT.parent / "preview-r2" / image_path.name
            same = old.exists() and Image.open(old).size == Image.open(image_path).size and ImageChops.difference(Image.open(old).convert("RGB"), Image.open(image_path).convert("RGB")).getbbox() is None
            if not same:
                changed.append(number)
            pages.append({"page": number, "words": len(words), "words_outside_page": len(outside),
                          "embedded_images": len(page.get_images()), "matches_reviewed_draft_render": same})
        source = (WORK / f"perm{n}" / "main.tex").read_text(encoding="utf-8")
        packages = re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", source)
        tex_log = (WORK / f"perm{n}" / "main.log").read_text(encoding="utf-8", errors="replace")
        warnings = [line for line in tex_log.splitlines() if re.search(r"Warning|Overfull|Underfull|undefined|Rerun to", line)]
        entry = {"n": n, "pages": len(doc), "pdf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                 "pdf_bytes": path.stat().st_size, "all_fonts_embedded": all(f["embedded"] for f in fonts),
                 "font_descriptor_metadata": fonts, "embedded_files": doc.embfile_count(),
                 "declared_packages": packages, "bibliography": "inline thebibliography; no bibtex/biber input",
                 "figures": "no external figures", "final_tex_warnings": warnings,
                 "changed_pages_from_reviewed_draft": changed, "page_checks": pages,
                 "source_uses_shell_escape": bool(re.search(r"\\write18\b", source))}
        if not entry["all_fonts_embedded"] or entry["embedded_files"] or any(p["words_outside_page"] or not p["words"] for p in pages):
            raise RuntimeError("PDF preflight failure")
        results.append(entry)
    report = {"status": "PASS", "renderer": "PyMuPDF "+fitz.VersionBind,
              "PDF_descriptor_reader": "pypdf", "font_files_extracted": False, "results": results}
    (AUDIT / "pdf_preflight.json").write_bytes((json.dumps(report, indent=2, sort_keys=True)+"\n").encode())
    print(json.dumps([{k: v for k, v in r.items() if k not in ("font_descriptor_metadata", "page_checks")} for r in results], indent=2))


if __name__ == "__main__":
    main()
