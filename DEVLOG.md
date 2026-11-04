# Factual development log

## 2026-11-03, bounded synthetic foundation

Recorded owner direction: execution in Codex with repository continuity for Claude Code; collection, stored evidence, researcher, skeptic, fact-checker, and reviewable report. D036-D037 capture the product direction. No new owner usefulness review or unaided program rating is recorded.

Implemented Python standard-library CLI and SQLite persistence, synthetic source validation, exact-content deduplication with multiple origins, reconciled import dispositions, immutable source/role versions, current source heads, role input digests, full-claim fact-check coverage, skeptic issue dispositions, and Markdown reporting.

Validation performed on the development host, Python 3.12.14:
- `python -m unittest discover -s tests -v`: 18 tests passed.
- Repeated in an isolated fresh directory containing only source, fixtures, tests, and documents: 18 tests passed.
- Eleven CLI invocations checked first-run fixture replay, identical-input rerun, report rendering, replay of recorded coding-session submissions, missing-stage failure, and total-rejection failure. All returned their expected exit code.
- Collection fixture: 4 inputs, 2 inserted evidence records, 1 duplicate, 1 rejection. Identical-input rerun: 0 inserts, 3 duplicates, 1 rejection.
- Fixture report: 6/6 claims checked, 2 verified, 2 contradicted, 1 partly verified, 1 unverifiable. These are hand-authored fixture expectations replayed through the implementation, not model-accuracy results.
- Coding-session report: 6/6 claims checked, 5 model-checked as source-faithful, 1 unverifiable hypothesis; lack of independent corroboration/status update remains unresolved. One assistant authored all three outputs in a shared session with access to expected fixture answers. This is not a blind test or independent review.
- No network retrieval, model calls from code, new paid service, model installation, or hardware benchmark occurred.

Observed boundaries: synthetic JSON collector only; exact content deduplication only; no live-source feasibility, automated entity resolution, independent review contexts, unattended role execution, scheduler, dashboard, private relevance store, or approved real-source retention implementation. Numeric/quote validation is mechanical; contextual source checking remains a coding-session responsibility. Stored basis/actor fields are self-reported, not authenticated.

Artifacts: `examples/fixture-replay/`, `examples/session/`, `docs/DATA_CONTRACTS.md`, and `tests/test_flow.py`. Source examples, reports, and stored demonstration packets contain only synthetic organizations and text. SQLite files and transient output are excluded from Git.
