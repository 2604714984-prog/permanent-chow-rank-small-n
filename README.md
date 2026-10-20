# Chow Ranks of Small Permanents

Manuscripts on the ordinary Chow rank of generic permanent polynomials over characteristic-zero fields.

## Read the papers

| Permanent | Ordinary Chow rank | Current manuscript | Source and guide |
|---|---:|---|---|
| `perm_3` | 4 | [PDF](perm3/paper/perm3_chow_rank_4.pdf) | [Source](perm3/paper/source/) · [Original package](perm3/README.md) |
| `perm_4` | 8 | [Computation-free proof · 7 pages](perm4/paper/perm4_chow_rank_8.pdf) | [LaTeX](perm4/paper/source/main.tex) · [Guide](perm4/README.md) |
| `perm_5` | 16 | [Computation-free proof · 8 pages](perm5/paper/perm5_chow_rank_16.pdf) | [LaTeX](perm5/paper/source/main.tex) · [Guide](perm5/README.md) |
| `perm_6` | 32 | [Computation-free proof · 7 pages](perm6/paper/perm6_chow_rank_32.pdf) | [LaTeX](perm6/paper/source/main.tex) · [Guide](perm6/README.md) |

The three computation-free manuscripts are the canonical current proofs. Each is self-contained: no program output, finite search table, or ancillary certificate is a premise. The PDF and its source live together under `permN/paper/`. Start with the PDF; optional checks and historical evidence are separate.

## What the proofs do

**Four-by-four.** Classify cubic prolongations, recover the omitted derivative condition, and use row-column scaling to obtain a uniform quotient-kernel statement. A subtraction argument excludes seven terms.

**Five-by-five.** A local polarization estimate for every actual factor span combines with a rectangular image-span inequality. The endpoint inequality excludes fifteen terms without the former state table or exact normal-form rank computations.

**Six-by-six.** Squarefree triple counting and an actual squarefree subspace replace the local computational endpoints. A middle-rank defect pays for missing cubic directions; two global inequalities cancel that defect and force thirty-two terms.

All three upper bounds are established directly by sign cancellation in Glynn's identity. The statements concern **ordinary Chow rank**, not border Chow rank or row-separated tensor rank.

## Audit and reproduction

The [October 20 combined audit](audit/20261020-computation-free/REPORT.md) reviews all three complete arguments and records source identities. Internal review found no unresolved proof obligation. It is not external peer review or formal proof-assistant certification.

[Reproduction instructions](REPRODUCING.md) distinguish source compilation, file-integrity checks, optional regression tests, and historical certificate replay. To check the current and archived inventories:

```sh
python -B scripts/check_current_releases.py
```

The optional tests are error-detection tools, not prerequisites for reading or proving the theorems.

## Historical versions

The earlier computation-assisted packages are preserved with their original contents and expected hashes:

- [perm4 archive](perm4/archive/README.md)
- [perm5 archive](perm5/archive/README.md)
- [perm6 archive](perm6/archive/README.md)

The separately frozen [October 16 r2 submissions](submissions/20261016-r2/) and [distributed artifacts](dist/) remain available as historical releases. They are not the current reading versions. Earlier research-directory snapshots remain in Git history; their old directory entrances now point to the canonical papers.

Current reader-facing material is in English. The arXiv workflow remains paused. For maintenance state and accepted source hashes, see [HANDOFF.md](HANDOFF.md).
