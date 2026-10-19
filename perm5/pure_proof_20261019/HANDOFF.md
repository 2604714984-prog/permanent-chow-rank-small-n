# Handoff — perm5 computation-free final revision

Updated: 2026-10-19.

## Mathematical result

The complete written proof establishes ordinary Chow rank 16 over characteristic zero. There is no remaining finite-scan, matrix-rank, partition-table, or interval-table premise. The final lower-bound endpoint is

    h2 + Delta/2 <= 10*N - 150.

At N=15 this forces h2=Delta=0 and contradicts the one-dimensional intersection bound. All dependent and repeated-factor cases and arbitrary factor-span quotients are included.

## Read first

`main.tex` is the authoritative mathematical text. `README.md` is the entry point; `README.zh.md` explains the new short proof in Chinese. `AUDIT.md` records the internal dependency and edge-case review. `SOURCE_MANIFEST.sha256` fixes the source and companion documents/programs. The reading PDF is `perm5_chow_rank_16_computation_free.pdf`.

`verify_optional.py` and `verification_results.json` are optional independent regression checks. Removing them does not change the written proof. Build receipts record the tested source hash and platform-specific PDF hash.

## Changes beyond the initial draft

- Replace the 352-pair scan by a formula and a nonnegative factorization.
- Replace positive partitions by the uniform divisor formula.
- Avoid determining the four normal-form ranks: zero derivatives, one relation, and explicit cubic inclusions suffice.
- Replace interval minimizations by one symbolic inequality.
- State the direction of every specialization, the constant dimensions of the local quotients, the actual-image conventions, and the filtration argument explicitly.
- Remove stale external ancillary instructions and update the title/date.

## Acceptance and boundaries

The internal mathematical revision is complete, with no unresolved lemma identified in its audit. External peer review, author responsibility, and formal proof-assistant certification are separate matters and are not claimed as completed.

The canonical reading entry on repository main should point here after successful publication. The old research drafts remain in Git history. The frozen 20261016-r2 release, historical computational packages, and other n results are retained unchanged. This revision proves no border-rank equality, no general-n equality, and no new perm6 or perm7 result. arXiv remains paused. No hosted CI, local Codex, provider request, quant database write, or scheduler change is part of this work.

## Rebuild

Compile `main.tex` twice with pdflatex and shell escape disabled. To run optional exact checks, use `python -B verify_optional.py --output verification_results.json`. See `README.md` for the full commands. Do not edit a frozen historical certificate or expected hash to make a new check pass.
