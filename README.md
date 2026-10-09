# release-asset-matrix

Captured GitHub release coverage checks for declared OS, architecture and archive-format matrices.

## Who and why

Release engineers reviewing binary release metadata after upload or during a release rehearsal. A release can have uploaded assets yet omit one supported platform, contain duplicate names or link to the wrong tag/repository.

Expand a collision-free filename matrix and check exactly one uploaded asset per cell, size floors, optional SHA256 digest metadata, URL provenance, tag/draft/prerelease gates and extra-asset inventory.

## Quickstart

Python 3.10+ and pip. Git source installation, no external-registry publication:

```sh
git clone https://github.com/nripankadas07/release-asset-matrix.git
cd release-asset-matrix
python -m venv .venv
# Unix: source .venv/bin/activate; Windows: .venv\Scripts\activate
python -m pip install .
release-asset-matrix release.json contract.json
python demo.py
python verify.py
```

CLI JSON on stdout. Exit **0** passes/claims, **1** policy findings or authentication/replay rejection, **2** malformed/unsupported input or IO errors. For automation, inspect the JSON and exit status together. Help: `release-asset-matrix --help`.

The fixture data is entirely synthetic. `demo.py` runs the example without installation and asserts a useful success and failure. `verify.py` additionally checks source tests, compilation and a fresh wheel installation in a temporary environment outside the source directory.

## Input and output

Read the checked-in fixture and policy JSON alongside `release_asset_matrix.py`. Policies reject unknown keys and invalid types rather than silently defaulting. See [DEMO.md](DEMO.md) for exact commands, expected outcome and schema notes; [VALIDATION.md](VALIDATION.md) for measured checks; [RESEARCH.md](RESEARCH.md) for dated comparable evidence and limits.

## Scope and limits

Captured metadata only; never downloads or executes assets. Digest metadata syntax does not verify file bytes, authenticity or provenance. Does not build binaries, mutate releases, sign files or replace release automation. Extra assets are reported and allowed. Template permits only tag/os/arch/ext, no conversions/specifiers. Safe ASCII tags/names, 1,000 cells, 10,000 assets and 2 MiB snapshot CLI limit; snapshots may be stale. A covered cell can coexist with a global release failure or duplicate-ID finding; overall findings determine exit status.

## Support

[Support, contribution and security](SUPPORT.md). MIT license. No performance or superiority claim; existing established tools are preferable when you need their broader workflows.
