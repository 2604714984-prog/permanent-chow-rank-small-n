# Reading, building and checking the proof packages

## Current computation-free proofs

The canonical sources are `perm4/paper/source/main.tex`, `perm5/paper/source/main.tex` and `perm6/paper/source/main.tex`. Each source compiles by itself; it does not load a computational certificate. Run twice from the corresponding `source/` directory:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The canonical PDFs are named `perm4_chow_rank_8.pdf`, `perm5_chow_rank_16.pdf` and `perm6_chow_rank_32.pdf` in the respective `paper/` directories. Their page counts are 7, 8 and 7. `BUILD.json` records the source and PDF hashes and source-only compilation. A rebuild on another engine or date may have different PDF bytes; this is not a mathematical discrepancy.

From the repository root, check all three current inventories and the three archived original inventories:

```sh
python -B scripts/check_current_releases.py
```

This checks bytes and source/PDF bindings in the receipts; it does not certify a theorem.

## Optional exact regression checks

Use Python with its standard library. Acceptance was executed with Python 3.14.4; a separate minimum-version acceptance is not claimed. From the repository root:

```sh
python -B perm4/paper/verify_supplementary.py --output perm4-checks.local.json
python -B perm5/paper/verify_supplementary.py --output perm5-checks.local.json
python -B perm6/paper/verify_supplementary.py --output perm6-checks.local.json
python -B audit/20261020-computation-free/independent_checks.py --output independent-checks.local.json
```

The output names deliberately avoid the preserved result files. The checks also passed with optimization enabled. They test displayed formulas, actual derivative spaces and sample quotients; finite examples are not proofs of the universal statements. The manuscripts contain the all-parameter arguments.

## Original computation-assisted packages

The original programs and evidence remain unchanged, including their original relative file layouts and manifests. Their updated entry points from the repository root are:

```sh
python -B perm3/certificates/verify_all.py
python -m pip install -r perm4/archive/computation-assisted/certificates/requirements-replay.txt
python -B perm4/archive/computation-assisted/certificates/verify_all.py
python -B perm5/archive/computation-assisted/verify_all.py
python -B perm6/archive/computation-assisted/verify_all.py
```

The quartic historical replay uses the declared nonstandard dependency. The quintic and sextic historical programs use the standard library. These are checks for archived proofs, not prerequisites for the current computation-free manuscripts. Historic READMEs retain their original commands for provenance; use the relocated entry points above.

## Frozen October 16 submissions

The r1 and r2 submission directories and distributed archives remain unchanged. For the r2 computational subsets:

```sh
python -B submissions/20261016-r2/perm5/anc/verify_submission.py
python -B submissions/20261016-r2/perm6/anc/verify_submission.py
```

Each wrapper checks its own documented manifest base and permitted subset. An original full manifest inside `anc/original/` also lists historical manuscript files intentionally omitted from that ancillary subset; this is documented by its ORIGIN and README files and must not be confused with a missing current proof input.

To rebuild the historical r2 source archives without overwriting published files, supply an empty temporary output directory:

```sh
python -B scripts/build_arxiv_submissions.py --release 20261016-r2 --output-dir /path/to/temporary-output
```

The builder verifies frozen inventories and never changes expected hashes. The current computation-free sources are separate from these archived submission packages. arXiv remains paused. The repository workflow is manual-only and is not needed for any local command above.
