# Reproducing current manuscripts and archived proof packages

## Current computation-free perm5 manuscript

The current reading version is `perm5/pure_proof_20261019/main.tex`, with its PDF, internal audit, reader guides, and source manifest in the same directory. It develops the October short proof and has no computer-generated proof premise.

Copy `main.tex` alone into an empty directory, then compile twice:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The result is an eight-page PDF. No ancillary file, program output, network service, or external figure is needed to establish or compile the written proof.

Optional exact regression tests can be run from the repository root:

```sh
python -B perm5/pure_proof_20261019/verify_optional.py --output /path/to/temporary/verification_results.json
```

Use an existing temporary output directory to avoid overwriting an archived receipt. The program uses Python's standard library. `SOURCE_MANIFEST.sha256` identifies the source and companion text/programs; `LOCAL_BUILD.json` and `BUILD_ACCEPTANCE.json` distinguish the local TeX Live and workstation MiKTeX PDF bytes. Both engines compiled the same mathematical source, including in a source-only empty directory. Normal and optimized exact-test payloads matched across platforms. These checks are not proof premises, external peer review, or formal certification.

## Archived computational packages

Each historical package is independent. Its original entry point still runs from the repository root:

```text
python -B perm3/certificates/verify_all.py
python -B perm4/archive/computation-assisted/certificates/verify_all.py
python -B perm5/verify_all.py
python -B perm6/verify_all.py
```

`perm4`'s historical computation-assisted replay has the dependency declared in
`perm4/archive/computation-assisted/certificates/requirements-replay.txt`.
The current computation-free perm4 proof is in `perm4/paper/source/main.tex`;
its optional supplementary checks run with the standard library:

```sh
python -B perm4/paper/verify_supplementary.py
```

The current perm4 and perm5 proofs do not depend on their optional checks or the archived computational packages. The historical `perm5` and `perm6` verification programs use only the standard library.

Every historical package retains its own `MANIFEST.sha256`.

## Frozen standalone source submissions: 20261016-r2

The two frozen submission packages are independent. Their wrappers verify the
complete source inventory, the original expected hashes of the computational
subset, and all finite computations used in those respective manuscripts:

```sh
python -B submissions/20261016-r2/perm5/anc/verify_submission.py
python -B submissions/20261016-r2/perm6/anc/verify_submission.py
```

Python 3.11 or newer with its standard library is sufficient. This second
acceptance was actually run with native Windows Python 3.14.4, including
inherited `PYTHONOPTIMIZE=0,1,2`; no unexecuted minimum-version test is claimed.

For either frozen source ZIP, extract into an empty directory and run:

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

## Additional historical audit-only checks

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
