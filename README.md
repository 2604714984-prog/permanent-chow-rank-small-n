# Chow Ranks of Small Permanents

Research manuscripts and reproducible evidence for the **ordinary Chow rank** of generic permanent polynomials over fields of characteristic zero.

## Start here

Read the current manuscript first, then its scope notes and audit. Verification scripts check stated computations and artifacts; they do not replace mathematical proofs or external peer review.

## Current results

| Polynomial | Ordinary Chow rank | Current reading version | Source and review |
|---|---:|---|---|
| `perm_3` | 4 | [Manuscript PDF](perm3/paper/perm3_chow_rank_4.pdf) | [LaTeX source](perm3/paper/source/) · [Verification package](perm3/certificates/) |
| `perm_4` | 8 | [**Current computation-free PDF**](perm4/paper/perm4_chow_rank_8.pdf) | [LaTeX source](perm4/paper/source/main.tex) · [Reader guide](perm4/README.md) · [Internal audit](perm4/paper/AUDIT.md) · [Optional checks](perm4/paper/verify_supplementary.py) |
| `perm_5` | 16 | [**Current computation-free PDF**](perm5/pure_proof_20261019/perm5_chow_rank_16_computation_free.pdf) | [Self-contained source](perm5/pure_proof_20261019/main.tex) · [Reader guide](perm5/pure_proof_20261019/README.md) · [Internal audit](perm5/pure_proof_20261019/AUDIT.md) · [Optional checks](perm5/pure_proof_20261019/verify_optional.py) |
| `perm_6` | 32 | [**Current computation-free PDF**](perm6/pure_proof_20261020/perm6_chow_rank_32_computation_free.pdf) | [Self-contained source](perm6/pure_proof_20261020/main.tex) · [Reader guide](perm6/pure_proof_20261020/READER_GUIDE.md) · [Internal audit](perm6/pure_proof_20261020/AUDIT.md) · [Optional checks](perm6/pure_proof_20261020/verify_optional.py) |

## Current `perm_6` proof

The current reading version is the seven-page computation-free revision dated October 20, 2026, in [`perm6/pure_proof_20261020/`](perm6/pure_proof_20261020/). Direct four-cycle and surviving-triple arguments replace the graph and coordinate-symbol scans. A squarefree-completion argument bounds the loss from missing actual cubic directions by half the middle-rank defect, removing the need for all five exact normal-form rank profiles. Divisor counting and elementary inequalities replace the remaining finite tables.

The global inequalities are `120 - Delta/2 <= h <= 10*N - 200 - Delta/2`, so the defect cancels and `N >= 32`. Glynn's thirty-two-term upper bound is proved by sign cancellation. The source is self-contained, with no program output or ancillary data as a proof premise. [Internal audit](perm6/pure_proof_20261020/AUDIT.md), [exact test receipt](perm6/pure_proof_20261020/verification_results.json), [workstation acceptance](perm6/pure_proof_20261020/BUILD_ACCEPTANCE.json), and [handoff](perm6/pure_proof_20261020/HANDOFF.md) record the review and checks.

The frozen [20261016-r2 source](submissions/20261016-r2/perm6/) and [PDF](dist/perm6_chow_rank_32_20261016-r2.pdf), together with the earlier paper and computation package, remain unchanged. Internal review is not external peer review or formal certification.

## Current `perm_5` proof

The current reading version is the eight-page computation-free revision dated October 19, 2026, in [`perm5/pure_proof_20261019/`](perm5/pure_proof_20261019/). It develops the active October short proof, not the historical 58-state route. The local estimate is proved by a closed triple-column count, a uniform degree-two-divisor bound, and explicit derivatives; neither finite tables nor the four normal-form matrix ranks are premises.

The global argument uses actual derivative images and gives `h2 + Delta/2 <= 10*N - 150`. Its endpoint excludes fifteen terms; the sixteen-term upper bound is proved by sign cancellation. The source builds by itself without programs or ancillary inputs. [Optional exact checks](perm5/pure_proof_20261019/verification_results.json), [workstation acceptance](perm5/pure_proof_20261019/BUILD_ACCEPTANCE.json), and [handoff](perm5/pure_proof_20261019/HANDOFF.md) record the completed internal review and technical checks; they are not formal or external peer certification.

The frozen [20261016-r2 source](submissions/20261016-r2/perm5/) and its [reading PDF](dist/perm5_chow_rank_16_20261016-r2.pdf), as well as the older computation-assisted packages, remain unchanged as historical releases.

## Current `perm_4` proof

The canonical `perm_4` manuscript and PDF are now the computation-free revision dated October 19, 2026. The proof classifies the relevant cubic prolongations, proves the missing-derivative lemma, uses explicit row-column scaling and rank specialization, and closes the lower bound with `559 > 552`.

The earlier computation-assisted proof, source files, certificate scripts, and their original manifest are preserved under [`perm4/archive/computation-assisted/`](perm4/archive/computation-assisted/). They are historical material and are not the current reading version.

Run the optional regression checks from the repository root:

```sh
python -B perm4/paper/verify_supplementary.py
```

To rebuild the PDF, run twice from `perm4/paper/source/`:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The optional checks are not premises of the written proof.

## Reproduction and release records

- [Reproduction guide](REPRODUCING.md)
- [Current project handoff](HANDOFF.md)
- [20261016-r2 source and PDF checksums](dist/SHA256SUMS_20261016-r2)
- [20261016-r2 technical acceptance report](audit/20261016-r2/REPORT.md)
- [20261016-r2 mathematical review](audit/20261016-r2/MATHEMATICAL_REVIEW.md)
- [2026-10-18 package-integrity receipt](audit/20261018-submission/package_preflight.json)

## Scope and status

All stated results concern **ordinary Chow rank**, not border Chow rank. No general formula for arbitrary matrix size is claimed. The current `perm_4`, `perm_5`, and `perm_6` revisions have received internal mathematical review; they have not received external peer review or formal proof-assistant certification.

The historical `perm_5` and `perm_6` release packages remain frozen at **20261016-r2**. The current reading revisions are separately preserved in `perm5/pure_proof_20261019/` and `perm6/pure_proof_20261020/`. The arXiv workflow is paused; the PDFs linked here are reading copies, not arXiv-generated previews.

## Language and archive policy

Reader-facing documentation for the current release is maintained in English. Historical source files, manuscripts, and evidence packages are retained rather than silently rewritten. The original computation-assisted `perm_4` files remain available in the archive.
