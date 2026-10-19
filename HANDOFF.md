# Small-permanent results: publication and handoff

Updated: 2026-10-19, Asia/Shanghai. Active perm4 reading version: **computation-free revision 20261019**. Active perm5 / perm6 release: **20261016-r2**.

## Current direction — public GitHub publication

The author requested on 2026-10-18 that arXiv work stop for now and that the
n = 5 and n = 6 results be organized in this public mathematical project,
alongside its existing n = 3 and n = 4 results. The [repository homepage](README.md)
now links all four current manuscripts, sources and verification packages.
Both r2 ZIPs, PDFs, source trees and SHA-256 inventories are already public.

**arXiv is paused.** No source upload, server-generated PDF or public arXiv
submission was completed. Preserve the historical account-side observations
below; do not restart uploads or endorsement outreach unless the author asks.
The earlier license authorization remains a recorded choice for a possible
future arXiv workflow, not a new repository-wide reuse license.

This publication organization changes documentation only. All n = 3 / n = 4
files and the frozen n = 5 / n = 6 releases retain their existing Git blob IDs.
No mathematical re-audit, certificate rewrite, source rebuild or CI dispatch
is required for this documentation change.

## Read these first

[Submission guide](submissions/20261016-r2/SUBMISSION_GUIDE.md),
[acceptance report](audit/20261016-r2/REPORT.md),
[internal mathematical review](audit/20261016-r2/MATHEMATICAL_REVIEW.md),
[reference and policy check](audit/20261016-r2/REFERENCES_AND_ARXIV.md),
[artifact hashes](dist/SHA256SUMS_20261016-r2).

The two current source ZIPs and reading previews are:

| Paper | Source archive | Preview |
|---|---|---|
| perm5 | [21-member ZIP](dist/perm5_arxiv_20261016-r2.zip) | [7-page PDF](dist/perm5_chow_rank_16_20261016-r2.pdf) |
| perm6 | [16-member ZIP](dist/perm6_arxiv_20261016-r2.zip) | [11-page PDF](dist/perm6_chow_rank_32_20261016-r2.pdf) |

## What is fixed and what is frozen

The second audit began from public commit
`ff27dd3377e341ae89e4fd9017cf3d174f51d7c8` (2026-10-16), not from a
September-only snapshot. That commit already contained the first October
revision and internal audit. Its sources, reports and released files remain
historical evidence; the previous handoff is recoverable at that commit.

The original root `perm5/` and `perm6/` packages, their full original
`MANIFEST.sha256` files, and the `submissions/20261016/` release are unchanged.
R2's ancillary directory includes the complete required computational subset
copied byte for byte: 9 original computation files for perm5, 7 for perm6.
The unchanged full original manifests have 15 and 13 entries respectively.
The omitted entries are historical manuscripts or explanatory documents,
not missing computational inputs. They remain in the original repository
packages and r1 ZIPs. The r2 ancillary README and ORIGIN.json enumerate them.

Definite technical fixes: no historical TeX sources inside `anc/`; explicit
AI-assistance disclosure in both manuscripts; corrected standalone program
paths and perm6 case-domain wording; fixed creator-platform metadata and
uncompressed r2 ZIP storage; byte-preserving Git attributes for submission
and audit trees. The original release's DEFLATE bytes can differ between
zlib and zlib-ng even when every payload is identical. Do not rewrite a
legacy archive hash to conceal that difference.

Each r2 `SOURCE_MANIFEST.sha256` is a new, separately frozen inventory.
The builder checks inventories but never edits them. Any future manuscript
or ancillary-code change requires an explicit new release and acceptance.
Do not change original certificate expectations to obtain a PASS.

## Mathematical status

The active perm5 manuscript is the seven-page short proof with a rectangular
image-span inequality, the quintic half-defect bound and an explicit
contradiction excluding the endpoint N=15. It does not rely on the historical
58-state/terminal-orbit route. Review the current proof, not only the old PDF.

The active perm6 manuscript uses the symmetric middle-catalecticant inequality,
all five dependent-factor normal forms, the quotient-symbol estimate and the
global filtration cancellation. Actual derivative spaces are distinguished
from larger formal factor-product spans.

Both statements concern ordinary Chow rank over characteristic zero, not
border rank or a general-n equality. The second internal review found no
unfilled logical obligation in the dependencies it examined. It is an
AI-assisted internal review, not formal proof certification or external
peer review. Final author approval of the revised arguments is not recorded.
The earlier withdrawn joint arXiv record is not used as a proof premise;
the author's subsequent contribution statement is recorded below.

## Reproduction and acceptance

```sh
python -B submissions/20261016-r2/perm5/anc/verify_submission.py
python -B submissions/20261016-r2/perm6/anc/verify_submission.py
python -B scripts/build_arxiv_submissions.py
python -B audit/20261016-r2/test_release_contract.py
```

From either independently extracted ZIP:

```sh
python -B anc/verify_submission.py
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

Both original public entry points and both extracted r2 full wrappers pass
on native Windows Python 3.14.4. R2 was replayed with inherited optimization
levels 0, 1 and 2 and from a different working directory. All eight corrupted,
missing or unlisted input probes fail as expected. The 16 release-contract
tests pass normally and with optimization. Full native replay receipts are
in `release_acceptance.json`; the byte-conversion checkout test is recorded
separately in `checkout_eol_after.json`.

Native MiKTeX compilation succeeds without shell escape or automatic package
installation. A benign epstopdf/no-shell-escape warning remains; there are
no missing references or final layout warnings. All 18 pages were rendered
and visually checked; font embedding and page bounds pass. This is local
technical acceptance, not the actual arXiv processor preview.

## If arXiv is resumed later

Review the revised proofs, authorship, earlier-work relationship, AI-use
disclosure, license and final metadata. The 2026-10-16 acceptance did not inspect account endorsement or capacity,
and did not perform an arXiv upload, license acceptance, announcement or
external-review certification. The 2026-10-18 continuation below records the
later account-side inspection, author authorizations, and the endorsement gate before file upload.

All testing is local; do not add a duplicate CI/scheduler or use local Codex.
The unrelated private perm5-v15 LF/CRLF receipt issue is not a dependency of
these public proofs and has not been declared repaired. The newly repaired
public-checkout line-ending issue is separately demonstrated and documented.

Local audit workspace:
`D:\UserData\ResearchArchives\perm56\arxiv-audit-20261016-r2\repo`.
Raw transport-offset and intermediate failed-driver logs remain preserved
beside the workspace under `local-audit-evidence/`; compact readable receipts
are in the repository. No data-provider, quant database or perm7 task was used.

## Submission continuation — 2026-10-18

See [actual submission status and next gate](audit/20261018-submission/STATUS.md)
and [package integrity receipt](audit/20261018-submission/package_preflight.json).
The frozen **20261016-r2** release and mathematical evidence remain unchanged.

The author confirmed identity/current affiliation and authorized the saved
affiliation spelling correction. The author stated that the withdrawn joint
work is background only, with no earlier-coauthor contribution to the new
manuscripts. This supports the proposed two-new-work route subject to moderation;
no manuscript text or attribution was changed.

The author selected the **arXiv non-exclusive license for both papers** and
authorized accepting the Submission Agreement to continue upload/preview.
Those declarations were entered in the existing perm5 Start workflow. Continue
returned **"You are not endorsed for this archive"** for math.AG. The endorsement
request page reported that arXiv sent a code email to the account holder.
No message was forwarded to another person. Reopening the draft showed the Start
controls reset; the failed Start step did not persist these selections. The
author's permission remains recorded and can be reused when endorsement is ready.

| Paper | Actual arXiv state |
|---|---|
| perm5 | Existing incomplete draft; blocked at Start by missing math.AG endorsement |
| perm6 | No draft created yet; the same account/category eligibility gate applies |

Neither source ZIP has been uploaded; no arXiv-generated PDF or ancillary
preview has been inspected; neither paper has been publicly submitted by this
session. The local 7-page and 11-page PDFs are not server previews.
Private account details, endorsement codes and draft identifiers remain outside
this public repository.

The author subsequently paused this route in favor of GitHub publication.
If the author later requests resumption: obtain math.AG endorsement, check
whether the existing perm5 draft still exists, and then process both drafts. Reuse the already confirmed identity, license and
upload/preview authorization. Keep all frozen sources and certificates intact.
After inspecting both actual server previews, obtain explicit final confirmation
of manuscript content, AI disclosure, and public submission before Submit Article.
Do not treat the current endorsement blocker as a reason to rewrite the release
or choose an unrelated category.

## perm4 computation-free continuation — 2026-10-19

The complete computation-free proof source, seven-page PDF, English overview,
and review materials are published on `main` at `perm4/pure_proof_20261019/`.

Read first:
- [Complete LaTeX manuscript](perm4/pure_proof_20261019/main.tex)
- [English overview](perm4/pure_proof_20261019/README.md)
- [Internal audit](perm4/pure_proof_20261019/AUDIT.md)
- [Focused handoff](perm4/pure_proof_20261019/HANDOFF.md)
- [Optional supplementary checks](perm4/pure_proof_20261019/verify_supplementary.py)
- [Frozen supplementary result receipt](perm4/pure_proof_20261019/supplementary_results.json)

The missing-derivative lemma (P_{x_{00}}=D+Kx_{00}^3) proves the quotient
kernel at a coordinate vector. Explicit row-column scaling with weights 0, 1
and 2, followed by rank specialization, proves the uniform rank-99 lemma.
Together with direct prolongation proofs of 560 and 92, this removes the
computational dependencies from the ordinary rank-eight proof while retaining
the 559 > 552 subtraction argument.

The optional regression checks are not premises of the written proof. The
standalone seven-page PDF is retained as a conversation/library artifact and
has not yet been added to GitHub; therefore the repository's old PDF remains
the historical computation-assisted reading version. The new LaTeX source is
the current computation-free manuscript. No old source, PDF, certificate,
frozen release or unrelated n package was overwritten.

The internal audit found no unresolved step in the written argument. This is
not external peer review or formal proof-assistant certification. The theorem
concerns ordinary Chow rank only; no border-rank or general-n equality is
claimed. arXiv remains paused. No hosted CI was run for this documentation and
source synchronization.


## perm5 computation-free proof attempt — 2026-10-19

A separate research branch research/perm5-computation-free-20261019 is testing a
proof revision without altering the released 20261016-r2 source. The first
revision replaces the 352-case coordinate scan by a closed formula for the
rank of each coordinate symbol, replaces the four rational normal-form rank
checks by displayed derivative identities and coefficient pivots, and proves
the low-dimensional catalecticant floors from positive exponent partitions.
The manuscript and audit notes are under
perm5/pure_proof_20261019/.

This is a research draft until the source compiles and its mathematical
arguments are reviewed. The released source, original certificates, frozen
manifests, and main branch remain unchanged. No CI is run for this work.
