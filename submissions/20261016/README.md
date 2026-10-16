# October 16, 2026 arXiv preparation

These are two separate submissions, not a combined paper.

| Paper | Current source | Reproduction from this repository |
|---|---|---|
| perm5, ordinary Chow rank 16 | [perm5/main.tex](perm5/main.tex) | `python -B submissions/20261016/perm5/anc/verify_submission.py` |
| perm6, ordinary Chow rank 32 | [perm6/main.tex](perm6/main.tex) | `python -B submissions/20261016/perm6/anc/verify_submission.py` |

The original top-level `perm5/` and `perm6/` directories and all their frozen
expected hashes are unchanged. Each source submission also carries its own
complete original package as ancillary evidence, so it remains independent
after extraction.

## Mathematical changes

The perm5 manuscript has a new, self-contained lower-bound argument. It
replaces the abbreviated 58-state and terminal-orbit proof in the September
public article with a rectangular image-span inequality and a quintic local
half-defect estimate. The small finite premises have two implementations;
explicit minors and upper-rank relations are also printed in the article.
The historical proof has not been erased, silently repaired, or counted as
an independent review of the replacement argument.

The perm6 lower-bound architecture is retained. The revision expands the
coordinate-specialization and directional arguments, details the exceptional
kernel step, fixes equation numbering and reproduction paths, and spells out
the passage from an algebraic closure to any characteristic-zero field.

Both revisions concern ordinary Chow rank. They do not prove border Chow
rank or a general-n formula. Internal mathematical audit and executable
verification are separate from external human peer review, which is not
claimed.

## Upload and build

The release ZIPs are in [`../../dist/`](../../dist/) when built. Each has
`main.tex` at its root and scientific ancillary material under `anc/`.
Extract one ZIP into an empty directory and run:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
python -B anc/verify_submission.py
```

No graphics, custom class/style files, external bibliography, external fonts,
shell escape, or network access are required. Standard TeX Live packages are
used; the references are embedded with `thebibliography`. Preview PDFs are
distributed separately and must not be added alongside the top-level TeX
source in the upload ZIP.

arXiv's own processor preview must still be inspected during an actual
submission. These artifacts do not select a license, log in, endorse,
upload, or announce either paper. No external review has been completed by
the preparation workflow.

See [the audit report](../../audit/20261016/REPORT.md) and
[the project handoff](../../HANDOFF.md) for evidence and outstanding status.
