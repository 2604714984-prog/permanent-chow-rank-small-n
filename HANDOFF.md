# perm5 / perm6 arXiv preparation handoff

Updated: 2026-10-16, Asia/Shanghai.

## Current deliverables

- [Current source manuscripts and standalone ancillary packages](submissions/20261016/).
- [Two arXiv source ZIPs and two preview PDFs](dist/).
- [Acceptance report](audit/20261016/REPORT.md).
- [Internal mathematical dependency review](audit/20261016/MATHEMATICAL_REVIEW.md).

The fixed starting public head was
`a3d161b0e86d6cd1f7926aa34e3cb4ee0b69f0e2` (September 1, 2026).
The original `perm5/` and `perm6/` files, manifests, and expected certificate
hashes remain unchanged. Each submission independently contains its original
public package under `anc/original/`.

## Important scientific change

The active perm5 manuscript is now a seven-page short proof using rectangular
catalecticant image spans and a local quintic half-defect estimate. It does
not rely on the abbreviated September 58-state/terminal-orbit argument.
Four normal-form matrices, explicit printed minors, and all 352 coordinate
symbols are checked by two implementations. Review the current source,
not only the unchanged old `perm5/paper/` PDF.

The active perm6 manuscript retains the symmetric middle-catalecticant
argument. It expands written reductions, fixes equation tags and reproduction
paths, and explicitly handles every characteristic-zero field.

Theorems concern ordinary Chow rank, not border rank or a general-n formula.
The review recorded here is an assistant-conducted internal mathematical
audit. No named independent human review, external peer review, or personal
author approval of the new perm5 proof is recorded.

## Reproduce

From this repository:

```sh
python -B submissions/20261016/perm5/anc/verify_submission.py
python -B submissions/20261016/perm6/anc/verify_submission.py
python -B scripts/build_arxiv_submissions.py
```

From either independently extracted source ZIP:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
python -B anc/verify_submission.py
```

Each source package has a separately frozen `anc/SOURCE_MANIFEST.sha256`.
The builder verifies that inventory and never edits expected hashes.
Submission revisions must be explicit new scientific revisions; do not
rewrite original expected hashes to force a PASS.

## Acceptance and next action

Both public original entry points and both freshly extracted full submission
entry points pass. Normal and optimized Python runs pass; missing/altered
input tests fail closed. Both extracted sources compile locally with
PDFLaTeX/TeX Live 2023 without shell escape or final warnings. Actual arXiv
processor preview and author confirmation of the mathematical contents are
still to be performed during a real submission.

No arXiv upload or announcement was performed. No GitHub Actions workflow
was dispatched. The unrelated private v15 LF/CRLF receipt transport issue
was neither altered nor declared repaired; the public original inventories
pass independently and the new proof does not depend on those receipts.

Keep the two paper submissions separate. The ZIP root contains `main.tex`
and `anc/`; preview PDFs are separate files. The author still controls final
metadata, license selection, and the actual submission. See the report for
the precise limits of the internal review and the archived computation logs.
