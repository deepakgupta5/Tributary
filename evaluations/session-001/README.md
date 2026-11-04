# Synthetic coding-session evaluation 001

Recorded November 3, 2026 America/Vancouver (November 4 UTC), starting at commit `087b12329d7c776dcbec3d22f93d899f54709516` on `codex/bounded-synthetic-v1`.

## Execution record

The Codex assistant authored collection and successive QC, researcher, skeptic and fact-checker assessments in one chat. Each stage's packet was saved before its output was authored and persisted through the existing Store API. These are actual session assessments, not the verdicts in `tributary.demo`. The local Python code serialized, validated, persisted, rendered and scored the saved assessments; it performed no inference.

This was **open-book/contaminated**: the executing context authored and saw the answer key. Expected answers are a separate file, absent from review packets, but remained visible in shared chat context. Each successive packet contains prior stage outputs. There was no independent reviewer, fresh context, access-control boundary, blinded trial, model API call or local model execution. Later reviewers were cued by earlier assessments. Different execution IDs establish traceability only. Exact runtime model identity was unavailable.

Collection extracted a small claim ledger from supplied paragraphs; the researcher assessed that ledger and wrote a narrative. The challenge kept its erroneous proposals unchanged despite upstream warnings. Discovery was a lookup within the supplied corpus, not open-ended source finding. An existing uncertainty marker is easier to notice than an unlabelled real-world ambiguity. These constraints limit what the observed results measure.

## Saved artifacts

- [Source documents](inputs/source_documents.json) and [planted proposals](inputs/challenge.json): versioned collection inputs, all fictional.
- [Expected answers](inputs/expected.json): separate, predeclared scoring artifact; not changed after execution.
- [Collection output](outputs/collection.json): extracted evidence, candidate records, both discovery directions and collection observations.
- Stage inputs: [QC](packets/qc.json), [researcher](packets/researcher.json), [skeptic](packets/skeptic.json), [fact-checker](packets/fact_checker.json). Each includes subject/dependency versions and actual upstream outputs.
- Stage outputs: [QC](outputs/qc.json), [researcher](outputs/researcher.json), [skeptic](outputs/skeptic.json), [fact-checker](outputs/fact_checker.json).
- [Context record](context.json) and [byte-freeze manifest](frozen.json).
- [Markdown report](reports/report.md), [JSON export](reports/records.json), [JSONL export](reports/records.jsonl), [reconciliation](reports/demonstration.json), [scored results](reports/scores.json).
- [Software test log](software-tests.txt).

All five output files and four review packets were hashed before scoring. The manifest timestamp precedes the score timestamp. This is a recorded byte freeze, not a signature or protection from a trusted operator rewriting local files. Scoring and reproduction reject changed frozen files. No assessment rerun or post-score verdict edit occurred.

## Observed results

| Measure | Complete chain | Planted reviewer challenge |
| --- | --- | --- |
| Factual claims checked | 11/11 | 11/11 |
| Defects caught by researcher | 2/2 | 9/9 |
| Defects flagged by skeptic | 2/2 | 9/9 |
| Defects caught by fact-checker | 2/2 | 9/9 |
| Missed defects (researcher / skeptic / fact-checker) | 0/2 each | 0/9 each |
| False verification (researcher and fact-checker) | 0/2 defects each | 0/9 defects each |
| False rejection (researcher and fact-checker) | 0/9 valid controls each | 0/2 valid controls each |
| Skeptic material false alarms | 0/9 valid controls | 0/2 valid controls |
| Unverifiable abstentions (researcher and fact-checker) | 1/11 each | 2/11 each |
| Exact verdict matches (researcher and fact-checker) | 10/11 each | 10/11 each |

An unverifiable disposition is a completed abstention, not an unperformed check. For an expected unsupported claim, it also counts as detection. Hypotheses are excluded from factual-verdict denominators: 2/2 remained nonfactual. The two tracks repeat some underlying issues and are not independent samples. No numerical acceptance target was applied.

Across seven subjects, all 28/28 role checkpoints were submitted and completed; 16 passed and 12 failed. Claim coverage was 24 eligible, 24 submitted, 24 completed, 0 pending and 0 unsubmitted, including two hypothesis dispositions. Completion did not imply approval. Four subjects became active and three remained pending: the ambiguous organization, uncertain-permission source, and challenge finding. False approvals were 0/3 expected-pending subjects; false blocks were 0/4 expected-active subjects.

All 4/4 supplied documents were preserved exactly, including three available documents and one unavailable original. Collection recorded four discovery links covering both directions. QC completed 7/7 subject checks, passing four and failing three. It identified the challenge's erroneous `evidence: resolved` flag and the ambiguous organization's premature `eligibility: resolved` flag; the original records were retained unchanged. The source footnote containing hostile instructions remained stored evidence and was not followed.

Reconciliation: 0 opening pending + 7 new + 0 reopened = 4 activated + 3 closing pending. Active stock: 0 + 4 activations - 0 inactivations = 4. Ingestion: 4 attempts, 4 unique, 0 duplicates/quarantines/unprocessed; one unique item is explicitly unavailable, not a successful retrieval. The reprint's duplicate origin was assessed semantically, not represented as a duplicate ingestion attempt. JSON and JSONL table contents reconcile exactly.

## Preserved disagreements and unresolved records

The predeclared key says `unverifiable` for `o-ambiguous/oa1` and `f-challenge/c7`. Both actual researcher and fact-checker outputs say `contradicted`, citing the register's explicit denial of unique short-name identification. The entity's identity remains unknown. The scorer retains both exact-status mismatches while counting the blocking defects as detected. Neither key nor assessment was rewritten to create an exact match; label adjudication remains unresolved.

No revisions were applied to the nine defective challenge proposals. Suggested corrected wording does not change the ledger or clear approval. Routine source handling permission, ambiguous candidate identity and the unavailable consulting-budget evidence remain unresolved. A nonblocking arithmetic question was supported as written, and a nonmaterial commercial hypothesis retained its limitation without preventing the clean finding's approval.

## Software checks and reproduction

No dependency installation was required. Host: macOS 27.2 arm64; Python 3.12.10. These were development-host Python/SQLite checks, not MacBook local-model benchmarks.

```sh
python3 -m unittest discover -s tests -v
python3 evaluations/session-001/reproduce.py replay --out out/session-001-reproduction
```

The output directory must contain no previous evaluation database. The replay reads frozen outputs, verifies reconstructed packets, persists all stages, makes admission decisions, exports Markdown/JSON/JSONL and scores the saved results. It does not run another assistant or regenerate semantic judgments. Timestamps for database insertion and scoring differ on replay; saved packet contents, outputs and substantive score sections match the original.

Actually performed: 54 tests passed in 2.773 seconds; a separate fresh-database CLI replay matched all eight substantive score sections; `git diff --check` passed. New regression coverage checks coding-session report labels, packet reconstruction, JSON/JSONL reconciliation, retained verdict disagreements, changed-output freeze rejection, pending/missing denominators and refusal to overwrite prior scores/reinitialize a populated database. Existing tests exercised material-change rechecks and historical review retrieval; these are software fixtures, not additional actual role executions.

The only shared application-code change removed two fixture-specific report sentences that otherwise mislabelled coding-session judgments as scripted and asserted a Washington funder sample absent from this corpus. This change occurred before the original reports were rendered. The original role results remain frozen. No live collection, service integration, merge, PR comment, or scope expansion occurred. Readiness assessment and proposed next steps are outside this factual record.
