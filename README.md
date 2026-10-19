# Chow Ranks of Small Permanents

Public manuscripts and verification packages for the ordinary Chow ranks of small generic permanents over fields of characteristic zero.

## Papers and verification packages

| Permanent | Ordinary Chow rank | Current manuscript | Complete LaTeX source | Exact verification |
|---|---:|---|---|---|
| n = 3 | 4 | [PDF](perm3/paper/perm3_chow_rank_4.pdf) | [Source](perm3/paper/source/) | [Certificates and programs](perm3/certificates/) |
| n = 4 | 8 | [Computation-free proof source (2026-10-19)](perm4/pure_proof_20261019/main.tex) · [Chinese explanation](perm4/pure_proof_20261019/README.zh.md) | [Standalone source package](perm4/pure_proof_20261019/) | [Internal audit](perm4/pure_proof_20261019/AUDIT.md) · [Optional regression checks](perm4/pure_proof_20261019/verify_supplementary.py) |
| n = 5 | 16 | [7-page PDF — 20261016-r2](dist/perm5_chow_rank_16_20261016-r2.pdf) | [Source tree](submissions/20261016-r2/perm5/) · [Standalone ZIP](dist/perm5_arxiv_20261016-r2.zip) | [Programs and exact data](submissions/20261016-r2/perm5/anc/) |
| n = 6 | 32 | [11-page PDF — 20261016-r2](dist/perm6_chow_rank_32_20261016-r2.pdf) | [Source tree](submissions/20261016-r2/perm6/) · [Standalone ZIP](dist/perm6_arxiv_20261016-r2.zip) | [Programs and exact data](submissions/20261016-r2/perm6/anc/) |

For n = 4, the new standalone manuscript is the current computation-free proof revision. The older [PDF](perm4/paper/perm4_chow_rank_8.pdf), [source tree](perm4/paper/source/) and [certificate package](perm4/certificates/) are preserved as the historical computation-assisted release; they have not been overwritten. The seven-page PDF compiled from the new source is currently retained as a conversation/library artifact and is not yet included in this repository. Do not mistake the historical PDF for the new manuscript.

Each paper's package is independent. The current n = 5 and n = 6 releases are **20261016-r2**; use the links above for their current manuscripts. The original `perm5/` and `perm6/` directories and the [r1 submission release](submissions/20261016/) remain historical archives.

The n = 5 and n = 6 results concern **ordinary Chow rank**, with no claim of border-rank equality or a general-n formula. The new n = 4 revision is internally reviewed AI-assisted mathematics; it has not received external peer review or formal proof-assistant certification.

## Reproduce n = 4 supplementary checks

From the repository root, run:

```sh
python -B perm4/pure_proof_20261019/verify_supplementary.py
```

These exact rational and finite-field regression checks are optional consistency checks, **not premises** of the written proof. To build the seven-page reading PDF, compile `perm4/pure_proof_20261019/main.tex` twice with `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error`. The compilation itself has not been independently replayed in this repository update.

## Download and reproduce n = 5 and n = 6

Each standalone ZIP contains `main.tex`, an `anc/` directory with independent verification programs and exact inputs, and SHA-256 inventories. The n = 5 archive has 21 files, and the n = 6 archive has 16 files. The PDFs linked above were compiled locally; they are not arXiv-generated previews.

- [SHA-256 checksums for both source ZIPs and PDFs](dist/SHA256SUMS_20261016-r2)
- [Reproduction instructions for all four results](REPRODUCING.md)
- [R2 technical acceptance report](audit/20261016-r2/REPORT.md)
- [R2 internal mathematical review](audit/20261016-r2/MATHEMATICAL_REVIEW.md)
- [2026-10-18 package-integrity receipt](audit/20261018-submission/package_preflight.json)

From the repository root:

```sh
python -B submissions/20261016-r2/perm5/anc/verify_submission.py
python -B submissions/20261016-r2/perm6/anc/verify_submission.py
```

From either independently extracted ZIP:

```sh
python -B anc/verify_submission.py
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The verification programs use Python 3.11 or newer and the standard library. See the reproduction instructions for the versions actually used in acceptance.

## Publication status — 2026-10-19

The n = 4 computation-free proof source and supporting audit materials have been merged into the public repository at `perm4/pure_proof_20261019/`. The original n = 4 proof source and computation certificates remain unchanged. The new source's optional regression results are retained separately and are not invoked as proof premises.

The n = 5 and n = 6 arXiv workflow remains paused. Neither manuscript was uploaded or publicly submitted by this workflow, and no arXiv-generated preview was produced. The frozen manuscripts, certificates and historical evidence for n = 5 and n = 6 remain unchanged.

See the [current handoff](HANDOFF.md), the [n = 4 proof handoff](perm4/pure_proof_20261019/HANDOFF.md), the [n = 4 internal audit](perm4/pure_proof_20261019/AUDIT.md), and the [dated submission record](audit/20261018-submission/STATUS.md).
