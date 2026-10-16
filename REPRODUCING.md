# Reproducing the four proof packages

Each package is independent. Run its entry point from the repository root:

```text
python -B perm3/certificates/verify_all.py
python -B perm4/certificates/verify_all.py
python -B perm5/verify_all.py
python -B perm6/verify_all.py
```

`perm4` has the dependency declared in
`perm4/certificates/requirements-replay.txt`. The `perm5` and `perm6`
verification programs use only the standard library.

Every package has its own `MANIFEST.sha256`.

## Current standalone source submissions: 20261016-r2

The two current manuscript packages are independent. Their wrappers verify the
complete source inventory, the original expected hashes of the computational
subset, and all finite computations used in their respective manuscripts:

```sh
python -B submissions/20261016-r2/perm5/anc/verify_submission.py
python -B submissions/20261016-r2/perm6/anc/verify_submission.py
```

Python 3.11 or newer with its standard library is sufficient. This second
acceptance was actually run with native Windows Python 3.14.4, including
inherited `PYTHONOPTIMIZE=0,1,2`; no unexecuted minimum-version test is claimed.

For either downloaded source ZIP, extract into an empty directory and run:

```sh
python -B anc/verify_submission.py
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

No repository checkout, other paper's files, network service, nonstandard
Python dependency, external figure or shell-escape command is required.
Each original `verify_all.py` still executes its complete computational
sequence. Historical manuscript/document files omitted from the ancillary
computational subset remain unchanged in the original public directories and
in the r1 source ZIPs. The ancillary README and ORIGIN.json list them precisely.

## Build source ZIPs without changing an inventory

```sh
python -B scripts/build_arxiv_submissions.py
# Equivalent explicit selection:
python -B scripts/build_arxiv_submissions.py --release 20261016-r2
```

R2 uses stored ZIP members with fixed timestamps, permissions and creator
platform. This avoids differences between the zlib and zlib-ng compression
backends and preserves the new archive hashes on rebuild. The builder only
reads and checks `SOURCE_MANIFEST.sha256`; it never rewrites expected hashes.
The `.gitattributes` rules protect original and submission byte inventories
from Windows automatic line-ending conversion.

To reproduce a historical compressed archive's exact **member payloads**:

```sh
python -B scripts/build_arxiv_submissions.py --release 20261016 --output-dir /path/to/temporary-output
```

The r1 compressed archive bitstream can differ between zlib implementations.
Do not overwrite its published archive or expected hash to conceal that
transport difference. R1 originals are preserved, not reissued as r2.

## Additional audit-only checks

```sh
python -B audit/20261016-r2/test_release_contract.py
python -B audit/20261016-r2/verify_prolongation_independent.py
```

The second command checks all cubic coefficients independently of the old
state tables. The full native acceptance driver and PDF preflight script are
also archived; the latter additionally uses PyMuPDF, pypdf and Pillow solely
for the auditor's rendering checks, not for reader proof replay.

The active perm5 proof does not depend on its historical 58-state/terminal
classification route. PASS markers certify the stated finite calculations
and integrity checks, not the entire written proof or external peer review.
