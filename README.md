# Chow Ranks of Small Permanents

The repository contains four independent proof packages:

- [`perm3/`](perm3/):
  \(\operatorname{ChowRank}(\operatorname{perm}_3)=4\).
- [`perm4/`](perm4/):
  \(\operatorname{ChowRank}(\operatorname{perm}_4)=8\).
- [`perm5/`](perm5/):
  \(\operatorname{ChowRank}(\operatorname{perm}_5)=16\).
- [`perm6/`](perm6/):
  \(\operatorname{ChowRank}(\operatorname{perm}_6)=32\).

Each directory contains its own manuscript PDF, complete AMS LaTeX source,
exact certificates, verification entry point, and reproduction instructions.
No proof package depends on files from another directory.

## Current perm5 and perm6 submission revisions

Use the **[20261016-r2 submission release](submissions/20261016-r2/)**,
not the historical September manuscript PDFs or the superseded r1 source ZIPs.
The active perm5 manuscript is a seven-page short lower-bound proof; perm6
is an eleven-page derivative-space and half-defect proof.

| Paper | Complete source ZIP | Compiled preview |
|---|---|---|
| perm5 | [arXiv source](dist/perm5_arxiv_20261016-r2.zip) | [7-page PDF](dist/perm5_chow_rank_16_20261016-r2.pdf) |
| perm6 | [arXiv source](dist/perm6_arxiv_20261016-r2.zip) | [11-page PDF](dist/perm6_chow_rank_32_20261016-r2.pdf) |

See the [submission guide](submissions/20261016-r2/SUBMISSION_GUIDE.md),
[acceptance report](audit/20261016-r2/REPORT.md),
[internal mathematical review](audit/20261016-r2/MATHEMATICAL_REVIEW.md),
[release checksums](dist/SHA256SUMS_20261016-r2) and [handoff](HANDOFF.md).

The original `perm5/`, `perm6/`, their manifests, and the [r1 release](submissions/20261016/)
remain unchanged. R2 carries the byte-exact computational inputs from each
original package; historical TeX manuscripts are not placed inside ancillary
files. It adds AI-use disclosure, a separate exact prolongation check and
portable source-archive construction.

Local computational and technical acceptance is not external peer review,
formal proof certification, author sign-off or arXiv processor approval.
No arXiv submission has been made by this workflow.
