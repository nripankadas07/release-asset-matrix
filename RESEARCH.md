# Brief and comparable review — 9 October 2026

Observation: 9 October 2026, 06:34 UTC. Live connected GitHub queries `release assets check sort:stars; release in:name topic:cli sort:stars; release automation sort:stars` sorted by stars, bounded result pages. Repository star counts fetched separately, with current default-branch code/docs/issues. Highest-star relevant comparable found: **semantic-release/semantic-release (24,097)**. This is not an exhaustive global ranking; HTML-only parsers, unrelated extractors, mobile-only release automation and report-only tools were distinguished by workflow relevance. Stars are discovery signals, not reliability/performance measurements.

Actual user: Release engineers reviewing binary release metadata after upload or during a release rehearsal.

Painful task: A release can have uploaded assets yet omit one supported platform, contain duplicate names or link to the wrong tag/repository.

Smallest useful capability: Expand a collision-free filename matrix and check exactly one uploaded asset per cell, size floors, optional SHA256 digest metadata, URL provenance, tag/draft/prerelease gates and extra-asset inventory.

Acceptance: good synthetic fixture passes; confirmed contract violation produces actionable JSON/exit 1; malformed input produces exit 2; installed quickstart works outside source; core boundary/concurrency/format regressions pass; remote Python matrix passes before LIVE.

Evidence and demand: Platform-matrix review is an inferred need, not a verified issue request. Current release tools already automate assets; this separate captured-metadata check makes explicit declared support reviewable without executing a release. Need for this exact MVP is inferred, not an upstream request to build it.

Portfolio/distinctness: wheel-sentinel verifies wheel internal records; this checks cross-platform asset inventory, publication state and release download URLs without reading archive internals. Compared all five briefs and 148 current owned repository descriptions and files where overlapping. No fork, rename or product subdivision counted as new.

Discovery: GitHub release missing platform and asset matrix searches; GoReleaser-adjacent review fixture.

| Comparable | Stars | Last push UTC | License metadata | Observed workflow/capability tradeoff |
| --- | ---: | --- | --- | --- |
| [goreleaser/goreleaser](https://github.com/goreleaser/goreleaser) | 16094 | 2026-10-09T03:39:45Z | MIT | Release automation building/uploading multiple languages and platforms; broader release orchestration. |
| [release-it/release-it](https://github.com/release-it/release-it) | 9067 | 2026-10-07T14:52:59Z | MIT | npm CLI for versioning/tagging/releases/assets/plugins; configurable orchestration workflow. |
| [semantic-release/semantic-release](https://github.com/semantic-release/semantic-release) | 24097 | 2026-10-09T00:23:35Z | MIT | Automated semantic versioning/release notes/publishing; broader commit-driven release process. |

- [goreleaser/goreleaser source](https://github.com/goreleaser/goreleaser/blob/ccaac66e8d36f5ce989ea129314af17bc26e650e/internal/client/github.go), head `ccaac66e8d36f5ce989ea129314af17bc26e650e`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: fix(git): redact credentials from http remote URLs too, fix(docker): select baseline CPU variants for Docker v2 platforms
- [release-it/release-it source](https://github.com/release-it/release-it/blob/45483990a7fef3959fbbb36ea00d719b1bc6102f/lib/plugin/github/GitHub.js), head `45483990a7fef3959fbbb36ea00d719b1bc6102f`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: Add type declarations for Plugin and related types, Feature request: Create Skills for release-it that will be available on skills.sh
- [semantic-release/semantic-release source](https://github.com/semantic-release/semantic-release/blob/04c1923646eb801cf6f0f90455cf00b78b94fdb7/lib/verify.js), head `04c1923646eb801cf6f0f90455cf00b78b94fdb7`. README `README.md`, source and up to five current issue/PR entries read. Maintenance signal is the dated push, not a guarantee of support. Issue examples: Confused about updates, build(deps-dev): bump @grpc/grpc-js from 1.14.4 to 1.14.5

Installability, time to first result, reliability and support comparison: README instructions, examples, current source and issues were reviewed. Competitor clean installations, workload timing, historical support response and demo reliability were **not measured**. Our own clean installation/demo proves only our behavior. NOASSERTION is incomplete license metadata, not a conclusion about permission. Licenses/attribution require actual upstream license review before reuse; no upstream code reused here.

No technical-performance benchmark or superiority claim. Workloads/hardware/versions were not measured equivalently, so stars and a successful example do not imply we outperform these tools. Broader tools already offer valuable workflows; this MVP chooses a small explicit contract with significant limits.
