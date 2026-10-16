# perm6 submission verification

Run from the extracted submission root:

```sh
python -B anc/verify_submission.py
```

Python 3.11 or newer, standard library only. No data downloads or external
services are used. Fresh outputs go to temporary directories.

The entry point checks the release source inventory and the unchanged
September package inventory, independently expands Glynn's identity over
all 1,492,992 row choices, runs `original/verify_all.py`, and checks that the
frozen package inventory is still unchanged. The original entry executes
the primary exact payload comparison, nine regression tests, the independent
finite-core enumeration, and the independent actual-normal-form reconstruction.

The finite-core enumeration visits 2,391,496 labelled bipartite graphs and
45,696 coordinate squarefree-symbol cases. The independent normal-form
program computes actual derivative spaces, retaining the distinctions from
formal factor-product spans. The written proof supplies the specialization,
directional, kernel, symmetric image-span, and filtration arguments. A
computation PASS does not constitute an external mathematical review.

`original/` is the complete, unmodified public September perm6 package from
commit `a3d161b0e86d6cd1f7926aa34e3cb4ee0b69f0e2`. The October manuscript fixes
the working-directory instructions, expands several written reductions,
aligns equation tags with the section numbers, and explicitly explains
extension to every characteristic-zero field. No frozen result or expected
hash has been changed.

The only top-level TeX entry is `main.tex`. All non-typesetting material is
under `anc/`. Select PDFLaTeX when processing the upload. This package contains
no author login, license choice, endorsement, or arXiv submission action.
