# The Chow Rank of the Five-by-Five Permanent

**Current proof: computation-free. Ordinary Chow rank: 16.**

[Read the paper](paper/perm5_chow_rank_16.pdf) | [LaTeX source](paper/source/main.tex) | [Audit](paper/AUDIT.md) | [Historical versions](archive/README.md)

The current manuscript proves the ordinary Chow rank of the generic 5-by-5 permanent over every characteristic-zero field. The factors are arbitrary linear forms in all 25 variables; no tensor-rank or border-rank conclusion is substituted for this statement.

The entire argument is in `paper/source/main.tex`. No rank-program output, enumerated certificate or ancillary input is a premise. Internal mathematical review identified no unresolved proof obligation. This is not external peer review or proof-assistant certification.

## Build and optional checks

From `perm5/paper/source/`, run twice:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The repository PDF has 8 pages. [BUILD.json](paper/BUILD.json) binds the source and PDF hashes. Different TeX distributions or build timestamps may change PDF bytes.

From the repository root, the optional exact regression checks are:

```sh
python -B perm5/paper/verify_supplementary.py --output perm5-checks.local.json
```

These checks are error-detection tests, not an alternative proof. Use [MANIFEST.sha256](MANIFEST.sha256) and `python -B scripts/check_current_releases.py` for release integrity. The archived certificate computations belong to the previous proofs.

## Version boundary

The mathematical source is unchanged from the latest computation-free draft audited on October 20, 2026. The predecessor is retained byte for byte under `archive/computation-assisted/`; frozen October 16 submissions and archives are retained separately. Current documentation is in English. See the [combined review](../audit/20261020-computation-free/REPORT.md) for exact source identities, mathematical checks, and publication checks.
