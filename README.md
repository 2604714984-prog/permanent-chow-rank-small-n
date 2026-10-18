# Chow Ranks of Small Permanents

Public manuscripts and independent exact-verification packages for the ordinary
Chow ranks of small generic permanents over fields of characteristic zero.

## Papers and verification packages

| Permanent | Ordinary Chow rank | Current manuscript | Complete LaTeX source | Exact verification |
|---|---:|---|---|---|
| n = 3 | 4 | [PDF](perm3/paper/perm3_chow_rank_4.pdf) | [Source](perm3/paper/source/) | [Certificates and programs](perm3/certificates/) |
| n = 4 | 8 | [PDF](perm4/paper/perm4_chow_rank_8.pdf) | [Source](perm4/paper/source/) | [Certificates and programs](perm4/certificates/) |
| n = 5 | 16 | [7-page PDF — 20261016-r2](dist/perm5_chow_rank_16_20261016-r2.pdf) | [Source tree](submissions/20261016-r2/perm5/) · [Standalone ZIP](dist/perm5_arxiv_20261016-r2.zip) | [Programs and exact data](submissions/20261016-r2/perm5/anc/) |
| n = 6 | 32 | [11-page PDF — 20261016-r2](dist/perm6_chow_rank_32_20261016-r2.pdf) | [Source tree](submissions/20261016-r2/perm6/) · [Standalone ZIP](dist/perm6_arxiv_20261016-r2.zip) | [Programs and exact data](submissions/20261016-r2/perm6/anc/) |

Each paper's package is independent. The current n = 5 and n = 6 releases are
**20261016-r2**; use the links above for their current manuscripts. The original
[`perm5/`](perm5/) and [`perm6/`](perm6/) directories and the
[r1 submission release](submissions/20261016/) remain historical archives.
The n = 3 and n = 4 packages are unchanged.

The n = 5 and n = 6 results concern **ordinary Chow rank**, with no claim of
border-rank equality or a general-n formula. The papers and evidence have
undergone local mathematical review, exact computational replay and technical
packaging checks. These internal checks do not constitute external peer review
or formal proof certification.

## Download and reproduce n = 5 and n = 6

Each standalone ZIP contains `main.tex`, an `anc/` directory with independent
verification programs and exact inputs, and SHA-256 inventories. The n = 5
archive has 21 files, and the n = 6 archive has 16 files. The PDFs linked above
were compiled locally; they are not arXiv-generated previews.

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

The verification programs use Python 3.11 or newer and the standard library.
See the reproduction instructions for the versions actually used in acceptance.

## Latest publication status — 2026-10-18

The author chose to publish and organize both results in this public GitHub
project and **pause the arXiv submission workflow**. Both complete r2 source
packages, compiled PDFs, verification programs and checksums are publicly
available here alongside the n = 3 and n = 4 results.

- **2026-10-16:** the r2 manuscripts and technical acceptance artifacts were published.
- **2026-10-18:** the frozen source ZIPs, inventories and metadata were checked;
  account-side submission preparation reached a math.AG endorsement requirement
  before file upload. The author then requested GitHub publication only for now.
- **arXiv:** neither manuscript was uploaded or publicly submitted by this
  workflow, and no arXiv processor PDF was generated.

The frozen manuscripts, certificates, expected hashes and historical evidence
are unchanged. This documentation update does not introduce a new mathematical
release, run a new internal audit, or claim journal acceptance.

See the [current handoff](HANDOFF.md), the
[dated submission record](audit/20261018-submission/STATUS.md) and the retained
[submission guide](submissions/20261016-r2/SUBMISSION_GUIDE.md).
