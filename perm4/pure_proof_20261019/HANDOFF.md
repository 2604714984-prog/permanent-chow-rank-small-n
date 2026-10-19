# Handoff — perm4 pure proof

Updated: 2026-10-19.

## Result

A complete computation-free rewrite of the ordinary rank-eight proof has been produced. The new ingredient is the missing-derivative lemma

    P_x00 = D + K*x00^3,

proved by excluding forbidden cubic monomials and recovering a missing matching-coefficient equality along a three-swap path. It gives the quotient kernel at x00. The row-column scaling with corner/boundary/interior weights 0/1/2 then gives the uniform rank-99 statement by rank specialization. The proof retains the original low-rank classification and the 559 > 552 subtraction contradiction, re-proved in full.

## Read first

- `main.tex`: complete mathematical proof; sections 3 and 4 are the new central arguments.
- `README.zh.md`: Chinese explanation and six-stage outcome.
- `AUDIT.md`: internal dependency/edge-case review.
- `verify_supplementary.py` and `supplementary_results.json`: optional independent regression tests, not proof premises.

The locally compiled seven-page PDF and a complete package are delivered in the conversation. The repository stores the source and review materials; it does not require the PDF as a verification input.

## Boundaries

- Ordinary Chow rank only; no border-rank claim.
- No general-n Chow-rank equality, and no perm5/perm6/perm7 claim.
- Original manuscript, original certificate expectations, frozen releases, and main branch remain unchanged.
- The earlier research note is retained as a historical record, with a new pointer to this completed revision.
- This is internally reviewed AI-assisted mathematics, not an external referee report or a formal proof-assistant certificate.
- No CI run or local Codex was used. arXiv remains paused.

## Reproduction

Run the optional script with Python 3 and the standard library. Compile `main.tex` twice with pdflatex and shell escape disabled. These commands are given in the Chinese README.

## Next acceptance gate

Author review of the new missing-derivative proof and its scaling argument before promoting this revision to replace the archived public reading version. This is a publication/acceptance gate, not an unresolved lemma in the present draft.
