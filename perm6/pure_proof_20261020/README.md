# Computation-free proof of the Chow rank of perm6

Revision: **2026-10-20 — complete internal mathematical revision**.

The manuscript proves the **ordinary Chow rank** of the generic six-by-six permanent to be 32 over every characteristic-zero field. It makes no border-rank or general-size equality claim.

## Read first

- [Complete source](main.tex) and [reading PDF](perm6_chow_rank_32_computation_free.pdf).
- [Reader guide](READER_GUIDE.md), [internal mathematical audit](AUDIT.md), and [handoff](HANDOFF.md).
- [Optional exact checks](verify_optional.py) and [actual results](verification_results.json).

**The proof remains complete when the program and all its outputs are removed.** Its only build input is `main.tex`. This is internally reviewed, AI-assisted mathematics, not external peer review or formal proof-assistant certification.

## What replaces the computations

| Earlier computational endpoint | Written replacement |
|---|---|
| Labelled bipartite graphs with at most six edges | Two different four-cycles use at least six edges; equality gives a complete two-by-three graph |
| 45,696 coordinate squarefree-symbol cases | Count killed triples by outside-vertex count, then use a union bound and two short small-edge arguments |
| Five exact dependent-factor rank profiles | A squarefree-completion argument: the middle-rank defect pays for the missing squarefree cubic directions |
| Positive-partition rank floors | A uniform formula for degree-three divisors, with a direct inequality for each possible factor-span size |
| Finite local interval minimizations | An absolute-value identity and the small-complement kernel lemma |

The decisive new step is the five-dimensional factor span. In the normal forms `T_s`, take a squarefree cubic subspace `U0` of the actual derivative space and write `m = 10 - dim(U0)`. Explicit derivatives and product bidegrees prove

\[
 m\le(20-u)/2.
\]

The two nontrivial cases need only **upper bounds** `u <= 14` and `u <= 18`, not exact matrix ranks. Restricting the completed map back to `U0` loses at most `m` in rank, and the defect term covers that loss. The map is compared inside a common ambient quadratic quotient; the actual derivative space is never replaced by a formal product span.

The resulting local estimate is

\[
 \operatorname{rank}\beta+(20-u)/2\ge10d/3.
\]

The global argument combines

\[
 h\le10N-200-\Delta/2,
 \qquad h\ge120-\Delta/2.
\]

The full defect cancels, giving `N >= 32`. Glynn's 32-term upper bound is proved in the text by sign cancellation.

## Rebuild

In an empty directory containing only `main.tex`, run twice:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

An ordinary LaTeX installation with the listed standard packages is sufficient. No project module, data file, network fetch, shell command, included source file, or verification program is needed by the manuscript.

Optional tests require Python 3.11 or newer and its standard library:

```sh
python -B verify_optional.py --output fresh_results.json
```

They independently check the full 45,696-case coordinate domain, 352 five-variable symbols, all 8,436 cubic coefficient columns for the permanent prolongation, the actual five normal forms, 528 rational local examples, and 2,464 structured coordinate-boundary examples. The local and structured tests include 1,454 small-complement kernel checks and 50 checks using a second quotient-rank algorithm. They expand all 1,492,992 Glynn terms and verify the actual global image sums and 4,320 quotient derivatives. These are finite regression checks, not a proof for all parameters.

Two deliberate negative controls are retained: arbitrary killed edges can give rank 19 rather than 20 at the full six-variable symbol, and a rank-two quadratic line invalidates the small-complement kernel conclusion. The written proof uses the necessary hypotheses in both places.

## Preservation and status

The frozen `submissions/20261016-r2/perm6/` package, old `perm6/paper/` and computation materials, original manifests, and all other n packages remain unchanged. The new source and reading PDF live in a separate directory. The source manifest identifies the mathematics; build receipts distinguish platform-dependent PDF hashes.

No hosted CI, local Codex session, WSL restart, new scheduler, or arXiv submission is part of this delivery. Internal review has not identified an unresolved mathematical step in this revision. External peer review and formal certification have not been performed.
