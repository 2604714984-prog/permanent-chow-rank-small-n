# Acceptance driver correction

The first r2 acceptance attempt successfully replayed perm5 in four modes
and compiled it twice, then its log recorder called os.path.relpath across
Windows drives (project D:, system temporary files C:). This raised ValueError.
The correction concerns recording temporary test paths, not a certificate or
a mathematical calculation. The incomplete receipt is retained here; raw
partial logs are also preserved outside the repository in local-audit-evidence.
The final receipt comes from a fresh extraction and complete rerun.
