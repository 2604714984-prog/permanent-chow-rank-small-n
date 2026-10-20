# Current publication handoff

Updated: October 20, 2026.

## Current state

The computation-free perm4, perm5 and perm6 manuscripts are the canonical current proofs. All three passed the October 20 internal mathematical audit. Sources are unchanged from the audited drafts; PDFs were rebuilt from source alone. This does not claim external peer review, journal acceptance, or formal proof-assistant certification.

| Package | Current PDF | Source | Internal audit |
|---|---|---|---|
| perm4 | [7 pages](perm4/paper/perm4_chow_rank_8.pdf) | [main.tex](perm4/paper/source/main.tex) | [Audit](perm4/paper/AUDIT.md) |
| perm5 | [8 pages](perm5/paper/perm5_chow_rank_16.pdf) | [main.tex](perm5/paper/source/main.tex) | [Audit](perm5/paper/AUDIT.md) |
| perm6 | [7 pages](perm6/paper/perm6_chow_rank_32.pdf) | [main.tex](perm6/paper/source/main.tex) | [Audit](perm6/paper/AUDIT.md) |

The [combined report](audit/20261020-computation-free/REPORT.md), [preservation receipt](audit/20261020-computation-free/PRESERVATION.json), and [acceptance receipt](audit/20261020-computation-free/ACCEPTANCE.json) give the checked boundaries. Each current package has a new manifest distinct from its original archived manifest. The mathematical source hashes are recorded in the combined report and each `paper/BUILD.json`.

## Preservation and repairs

The baseline was `0a6d651f0f1de8ebe711c183b41d71576a036248`. The original perm5 and perm6 packages were moved intact into their respective `archive/computation-assisted/` directories. The quartic archive's original manifest-bound README was recovered from Git rather than changing its expected checksum. Original archive guides are separate from the preserved READMEs.

All perm3 files, historical audit evidence, frozen r1/r2 submissions, and existing `dist/` artifacts remain byte-identical to the baseline. Pre-canonical computation-free snapshots remain at that immutable commit; English forwarding READMEs replace duplicated working copies on current main. The newly introduced Chinese quintic README is no longer in the current tree.

Only the quintic optional verifier needed a relocation adjustment to locate `paper/source/main.tex`. No mathematical source was edited. Source-only builds, optional checks, archive integrity, navigation and language checks are recorded in acceptance. Program outputs are not theorem premises.

## Maintenance rules

Keep one canonical reading version per result. Do not change an old expected hash to make a replay pass. Any future mathematical change requires a new review and a rebuilt PDF/source binding; retain the preceding release through Git and its archive.

All tests for this publication were local. The existing workflow remains manual-only; no hosted CI was dispatched. No local Codex, WSL restart, new scheduler, or unrelated research process was used. The arXiv workflow is still paused; no upload or submission is authorized by this reorganization.

Historical submission preparations and earlier handoffs are retained in Git at the baseline commit and in the [dated submission record](audit/20261018-submission/STATUS.md). They are not descriptions of the current manuscript layout.
