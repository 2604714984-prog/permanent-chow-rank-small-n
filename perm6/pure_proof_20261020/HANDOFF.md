# Handoff — perm6 computation-free proof

Updated: 2026-10-20.

## Result and entry points

The complete written proof is `main.tex`; the named reading copy is
`perm6_chow_rank_32_computation_free.pdf`. Start with Section 5 for the new
squarefree-completion argument. `READER_GUIDE.md` explains it, and `AUDIT.md`
records the full dependency review. The conclusion is ordinary Chow rank 32
in characteristic zero, not border rank or a general-size formula.

## Decisive change

For five-dimensional factor span, find an actual squarefree cubic subspace
U0 of codimension m inside the ten-dimensional squarefree completion. Explicit
derivatives and disjoint-variable product bounds prove m <= (20-u)/2.
Restricting a map to U0 loses at most m, so the defect pays for the loss.
Only u<=14 and u<=18 are needed for the two exceptional forms. The five exact
normal-form rank profiles are no longer proof inputs.

Direct four-cycle reasoning replaces the bipartite-graph scan. Surviving-triple
counts replace the coordinate symbol table. A divisor formula and algebraic
inequalities replace partition and interval enumerations. The symmetric
image-span inequality and the actual factor-span filtration then give

    120 - Delta/2 <= h <= 10*N - 200 - Delta/2,

forcing N>=32. Glynn's formula supplies equality by a written sign argument.

## Regression and technical checks

`verify_optional.py` is independent of the previous proof scripts and its
outputs are not premises of the paper. The exact receipt includes coordinate
symbols, actual derivatives, generic rational and structured boundary
quotients, negative controls, and the actual Glynn global image sums.
`SOURCE_MANIFEST.sha256` identifies source and companion materials. Build
receipts distinguish local and workstation PDFs, which may have different
bytes despite identical mathematical source.

## Preservation

The base inspected was fb03220dda763c3dc859042853a1f9e12a8c3e3e. Keep the
frozen submissions/20261016-r2/perm6 package, old perm6 paper/computations and
original manifest unchanged. Other n packages, releases and historical
records must not be rewritten. Root reading links may point to this new
folder without modifying those frozen inputs.

No hosted CI, local Codex, WSL restart, new scheduler or arXiv upload is needed.
All testing is local. The result has internal review, not external peer review
or formal proof-assistant certification. No future research was left running
as a substitute for this delivery.
