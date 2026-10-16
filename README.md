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

The [October 16, 2026 submission directory](submissions/20261016/) contains
the current perm5 and perm6 manuscripts and standalone ancillary material.
The perm5 revision gives a new short lower-bound proof; the perm6 revision
retains its proof architecture with expanded arguments and corrected
reproduction instructions. The September directories above are preserved
unchanged as historical evidence.

The [source ZIPs and preview PDFs](dist/) have passed local extraction,
compilation, and complete computational replay. See the
[audit report](audit/20261016/REPORT.md) and [handoff](HANDOFF.md) for the
mathematical review boundary. This is an internal audit, not external human
peer review, and no arXiv submission has been made by this workflow.
