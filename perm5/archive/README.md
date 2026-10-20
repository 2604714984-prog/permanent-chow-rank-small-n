# Historical versions of the perm5 proof

The [current computation-free manuscript](../paper/perm5_chow_rank_16.pdf) is the main reading version. This directory preserves the earlier computation-assisted package, including its original README, relative file layout, expected hashes, source and evidence. Its historical README is intentionally not rewritten.

- [Original manuscript](computation-assisted/paper/perm5_chow_rank_16.pdf)
- [Original source](computation-assisted/paper/source/)
- [Original inventory](computation-assisted/MANIFEST.sha256)

Run integrity checks from the repository root with `python -B scripts/check_current_releases.py`. Replay commands with the relocated paths are in [REPRODUCING.md](../../REPRODUCING.md).

For n = 5 and n = 6, the direct October 16 short-proof predecessors are the separately frozen [r2 submission packages](../../submissions/20261016-r2/). Their sources, manifests and release ZIPs are unchanged. The older root packages archived here are not relabelled as the r2 manuscripts.

Earlier computation-free working copies remain in Git history at `0a6d651f0f1de8ebe711c183b41d71576a036248`. Their former directories now contain navigation pointers to the single canonical release.
