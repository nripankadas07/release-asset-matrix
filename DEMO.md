# Runnable example

Run `python demo.py`; it exercises the exact source API and fails if the intended positive/negative result changes. The installed CLI is separately exercised by `python verify.py` from outside the source directory.

Commands in `smoke.json` document the expected exit status for good, findings/replay and malformed-input cases. Snapshot files are synthetic and intentionally contain no credentials or private production data.

Expand a collision-free filename matrix and check exactly one uploaded asset per cell, size floors, optional SHA256 digest metadata, URL provenance, tag/draft/prerelease gates and extra-asset inventory.

Captured metadata only; never downloads or executes assets. Digest metadata syntax does not verify file bytes, authenticity or provenance. Does not build binaries, mutate releases, sign files or replace release automation. Extra assets are reported and allowed. Template permits only tag/os/arch/ext, no conversions/specifiers. Safe ASCII tags/names, 1,000 cells, 10,000 assets and 2 MiB snapshot CLI limit; snapshots may be stale. A covered cell can coexist with a global release failure or duplicate-ID finding; overall findings determine exit status.
