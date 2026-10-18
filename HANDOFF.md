# perm5 / perm6 arXiv preparation handoff

Updated: 2026-10-18, Asia/Shanghai. Active release: **20261016-r2**.

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

## Remaining author/account actions

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
Those declarations were saved in the existing perm5 Start workflow. Continue
returned **"You are not endorsed for this archive"** for math.AG. The endorsement
request page reported that arXiv sent a code email to the account holder.
No message was forwarded to another person.

| Paper | Actual arXiv state |
|---|---|
| perm5 | Existing incomplete draft; blocked at Start by missing math.AG endorsement |
| perm6 | No draft created yet; the same account/category eligibility gate applies |

Neither source ZIP has been uploaded; no arXiv-generated PDF or ancillary
preview has been inspected; neither paper has been publicly submitted by this
session. The local 7-page and 11-page PDFs are not server previews.
Private account details, endorsement codes and draft identifiers remain outside
this public repository.

Next: obtain math.AG endorsement, resume the existing perm5 draft, then process
the separate perm6 draft. Reuse the already confirmed identity, license and
upload/preview authorization. Keep all frozen sources and certificates intact.
After inspecting both actual server previews, obtain explicit final confirmation
of manuscript content, AI disclosure, and public submission before Submit Article.
Do not treat the current endorsement blocker as a reason to rewrite the release
or choose an unrelated category.
