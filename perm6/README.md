# The Chow Rank of the Six-by-Six Permanent

**Current proof: computation-free. Ordinary Chow rank: 32.**

[Read the paper](paper/perm6_chow_rank_32.pdf) | [LaTeX source](paper/source/main.tex) | [Audit](paper/AUDIT.md) | [Historical versions](archive/README.md)

The current manuscript proves the ordinary Chow rank of the generic 6-by-6 permanent over every characteristic-zero field. The factors are arbitrary linear forms in all 36 variables; no tensor-rank or border-rank conclusion is substituted for this statement.

The entire argument is in `paper/source/main.tex`. No rank-program output, enumerated certificate or ancillary input is a premise. Internal mathematical review identified no unresolved proof obligation. This is not external peer review or proof-assistant certification.

## Build and optional checks

From `perm6/paper/source/`, run twice:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The repository PDF has 7 pages. [BUILD.json](paper/BUILD.json) binds the source and PDF hashes. Different TeX distributions or build timestamps may change PDF bytes.

From the repository root, the optional exact regression checks are:

```sh
python -B perm6/paper/verify_supplementary.py --output perm6-checks.local.json
```

These checks are error-detection tests, not an alternative proof. Use [MANIFEST.sha256](MANIFEST.sha256) and `python -B scripts/check_current_releases.py` for release integrity. The archived certificate computations belong to the previous proofs.

## Version boundary

The mathematical source is unchanged from the latest computation-free draft audited on October 20, 2026. The predecessor is retained byte for byte under `archive/computation-assisted/`; frozen October 16 submissions and archives are retained separately. Current documentation is in English. See the [combined review](../audit/20261020-computation-free/REPORT.md) for exact source identities, mathematical checks, and publication checks.
