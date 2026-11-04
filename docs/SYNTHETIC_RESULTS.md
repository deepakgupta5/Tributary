# Synthetic development record

Recorded: 2026-11-03 (America/Vancouver).
Implementation branch: `codex/bounded-synthetic-v1`.
Starting commit: `f91734d98392bcfc3066c45972fad26695c86472`.

The branch was created from the approved documentation commit in a fresh checkout. This increment implements D046–D052's bounded synthetic flow. It includes no live collection, paid dependency, provider integration, local-model installation, or PR merge.

## Actual checks

- `python3 -m unittest discover -s tests -v`: 38 tests passed on Python 3.12.10. The complete command output, including measured duration, is in [examples/tests.txt](../examples/tests.txt).
- `python3 -m tributary.demo --out out/release-demo`: synthetic end-to-end demonstration completed; captured outputs are in [examples](../examples/).
- `git diff --check`: no whitespace errors.

The suite covers stage order and bypass attempts on all three admission subject types, collection/QC execution separation checks, explicit context metadata, optional versus material issues, required claim/detail/issue accounting, unavailable locators, stale inputs, upstream review changes, transitive material-change rechecks, dependency-cycle rollback, persistence, duplicate/repeated runs, malformed/unknown dates, interrupted ingestion recovery, answer-key separation, numeric context/arithmetic, evaluator counters, network refusal during the demo, and export reconciliation. The network refusal check patches socket creation; the application itself contains no network integration.

An earlier test run exposed reuse of a test execution ID after a changed packet. The test was corrected to use a new execution ID; the implementation's rejection remains covered. This was a test-fixture error, not a successful changed-packet approval.

A subsequent regression run caught a misplaced name-validation statement in historical-version lookup. The statement was moved to subject validation; the historical-version preservation test covers that path in the final run.

## Demonstrated data outcomes

| Observation | Actual fixture outcome |
| --- | --- |
| Initial ingestion | 5 attempted items = 3 unique evidence items + 1 duplicate + 1 quarantined malformed-date item. The run remains partial even though counts reconcile. |
| Candidate population | 9 subjects = 6 approved/admitted + 3 pending. |
| Approved population | 3 fictional sources, 2 fictional organizations, 1 finding. |
| Pending population | Ambiguous organization identity; unresolved source access; contradicted consulting-budget claim. |
| Discovery | Both source-to-organization and organization-to-source events persisted; repeated discovery does not create an additional candidate. |
| Material correction | A bulletin receipt correction reopens the bulletin source, Cedar organization, and dependent campaign finding. Unrelated records remain current. |
| Recheck period | 3 opening pending + 3 reopened = 3 re-admitted + 3 closing pending; active stock remains 6. |
| Identical rerun | 1 duplicate evidence input; no new candidate or admission, and no new evidence version. |
| Arithmetic | Explicit fixture amounts produce CAD 30000 original shortfall; target and actual amounts are not equal. This does not measure prose extraction. |

The finding after correction attributes CAD 110000 to the corrected bulletin and retains the organization report's conflicting CAD 120000 as a visible limitation. Fixture replay does not establish that a reasoning model would identify or handle this distinction correctly.

## Delivery reconciliation

| Authorized deliverable | Artifact and observed state |
| --- | --- |
| Versioned six-group foundation | `tributary/core.py`; SQLite records, reviews, decisions, history, runs; logical groups documented in SYNTHETIC_IMPLEMENTATION.md. Implemented and exercised. |
| Both discovery directions | `tributary/demo.py`, discovery history in `examples/records.json`; exercised. |
| Four checkpoints and blockers | Packet/review/decision functions and `tests/test_flow.py`; exercised with scripted outputs. |
| Rechecks and reconciliation | Dependency fingerprints, history and audit functions; demonstrated before/after correction and rerun. |
| Reproducible demonstration | Commands in README and SYNTHETIC_IMPLEMENTATION.md; executed. |
| Markdown/JSON/JSONL | `examples/report.md`, `records.json`, `records.jsonl`, `demonstration.json`; generated and export-row accounting checked. |
| Known-answer evaluation support | Separate `fixtures/role_inputs.json` and `fixtures/expected.json`; evaluator tested with deliberately flawed saved verdicts. |
| Actual coding-session role evaluation | Not performed. No accuracy or independent-review result claimed. |
| Live feasibility and owner usefulness | Not performed; separate review gates. |

## Remaining limits

All role verdicts in the demonstration are hand-authored fixture replay. Structural validation cannot establish semantic truth. Collector-ID separation is traceability rather than identity authentication or context isolation. Review dependencies must be explicitly represented. Candidate counts coalesce repeated revisions within a period while preserving revision history. No destructive/reversible entity merges, fuzzy matching, live-content handling, scheduler, JSON importer, production security boundary, or geographic completeness claim is included. See [SYNTHETIC_IMPLEMENTATION.md](SYNTHETIC_IMPLEMENTATION.md) for details.

The implementation awaits owner review before live work or further expansion.
