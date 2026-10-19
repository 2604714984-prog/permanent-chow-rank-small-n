# Chow Ranks of Small Permanents

Research manuscripts and reproducible evidence for the **ordinary Chow rank** of generic permanent polynomials over characteristic-zero fields.

## Start here

1. Read the current manuscript linked in the table below.
2. Read the corresponding internal audit and scope notes before interpreting a result.
3. Use the reproduction commands only for the checks they are documented to perform. A passing script is not a substitute for a mathematical proof or external peer review.

## Current results

| Polynomial | Claimed ordinary Chow rank | Current reading version | Source and review |
|---|---:|---|---|
| `perm_3` | 4 | [Manuscript PDF](perm3/paper/perm3_chow_rank_4.pdf) | [LaTeX source](perm3/paper/source/) · [Verification package](perm3/certificates/) |
| `perm_4` | 8 | [**Computation-free PDF (2026-10-19)**](perm4/pure_proof_20261019/main.pdf) | [LaTeX source](perm4/pure_proof_20261019/main.tex) · [English overview](perm4/pure_proof_20261019/README.md) · [Internal audit](perm4/pure_proof_20261019/AUDIT.md) · [Optional checks](perm4/pure_proof_20261019/verify_supplementary.py) |
| `perm_5` | 16 | [Manuscript PDF (20261016-r2)](dist/perm5_chow_rank_16_20261016-r2.pdf) | [Standalone source](submissions/20261016-r2/perm5/) · [Verification inputs](submissions/20261016-r2/perm5/anc/) |
| `perm_6` | 32 | [Manuscript PDF (20261016-r2)](dist/perm6_chow_rank_32_20261016-r2.pdf) | [Standalone source](submissions/20261016-r2/perm6/) · [Verification inputs](submissions/20261016-r2/perm6/anc/) |

## `perm_4`: current version and historical archive

The current reading version is the seven-page computation-free revision in [`perm4/pure_proof_20261019/`](perm4/pure_proof_20261019/). Its proof replaces the earlier rank computations with explicit prolongation classifications, a missing-derivative lemma, row-column scaling, and a rank-specialization argument. The supplementary script is an optional regression check and is **not** a premise of the theorem.

The earlier computation-assisted version remains preserved at [`perm4/paper/`](perm4/paper/) with its original certificates at [`perm4/certificates/`](perm4/certificates/). These files are historical evidence and are not the current reading version.

To replay the optional checks from the repository root:

```sh
python -B perm4/pure_proof_20261019/verify_supplementary.py
```

To compile the new manuscript, change to `perm4/pure_proof_20261019/` and run twice:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

## Reproduction and release records

- [Reproduction guide](REPRODUCING.md)
- [Current project handoff](HANDOFF.md)
- [20261016-r2 source and PDF checksums](dist/SHA256SUMS_20261016-r2)
- [20261016-r2 technical acceptance report](audit/20261016-r2/REPORT.md)
- [20261016-r2 mathematical review](audit/20261016-r2/MATHEMATICAL_REVIEW.md)
- [2026-10-18 package-integrity receipt](audit/20261018-submission/package_preflight.json)

## Scope and status

All four stated results concern **ordinary Chow rank**, not border Chow rank. No general formula for arbitrary matrix size is claimed. The `perm_4` revision has received an internal mathematical review; it has not received external peer review or formal proof-assistant certification.

The `perm_5` and `perm_6` release packages are frozen at **20261016-r2**. The arXiv workflow is paused; the PDFs linked here are local reading copies, not arXiv-generated previews.

## Language and archive policy

Reader-facing documentation for the current release is maintained in English. Historical source files, manuscripts, and evidence packages are retained rather than silently rewritten. The repository's original computation-assisted `perm_4` files remain unchanged.
