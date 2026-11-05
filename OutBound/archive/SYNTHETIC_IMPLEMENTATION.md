# Bounded synthetic implementation

Baseline: `f91734d98392bcfc3066c45972fad26695c86472` (D046–D052).

The implementation uses Python's standard library and SQLite. It performs no network calls, downloads, model inference, or paid-service access. No local model, provider adapter, scheduler, live collector, HTML renderer, or merge engine is included.

## Reproduce

From a checkout of `codex/bounded-synthetic-v1`, using Python 3.12 or later with its SQLite module:

```sh
python3 -m unittest discover -s tests -v
python3 -m tributary.demo --out out/demo
python3 -m tributary.demo --partial --out out/partial-demo
```

The demonstration refuses an existing output directory. Choose a new directory to repeat it. It creates `tributary.sqlite`, `report.md`, `records.json`, `records.jsonl`, and `demonstration.json`. No dependency installation is necessary. All data is fictional. Audits and records contain execution timestamps; business records, decisions, and reconciliation outcomes repeat, but timestamped export bytes need not be identical.

`examples/` contains a captured run, excluding the database. The executable source fixture is `tributary/demo.py`. `OutBound/data/fixtures/role_inputs.json` is an additional standalone role-evaluation packet; its answer key is in `OutBound/data/fixtures/expected.json`. The demonstration and packet construction do not load that key. Scoring tests load it separately to exercise the evaluator, not to simulate model accuracy.

## Storage and contracts

Six logical groups use five small SQLite tables:

| Logical group | Storage |
| --- | --- |
| Organizations | `records`, kind `organization` |
| Sources | `records`, kind `source` |
| Evidence | `records`, kind `evidence` |
| Findings and claims | `records`, kind `finding`, nested claim ledger |
| Reviews and decisions | `reviews` and `decisions` |
| Runs and history | `runs` and `history` |

Record IDs are stable, while substantive edits append immutable versions. Equal-content writes do not create versions. The first build conservatively treats all stored body changes as material; it does not implement cosmetic-edit classification. Collection proposals are versioned `records` with collector execution IDs; QC results are distinct `reviews`. Source references identify provenance; explicit dependency edges determine rechecks. Discovery links are not dependency edges and can expand in both directions without creating dependency cycles. Evidence can describe the source under inspection without requiring that source's prior admission. Findings additionally require current organization/source admission.

Source-to-organization and organization-to-source discoveries retain first-seen run, parent, method, and next action. Repeated discovery retains the existing event. Unknown identity stays pending with candidate duplicate links; no identity merge is performed. Evidence deduplication uses stable input IDs and equal content, not fuzzy matching or automatic cross-URL syndication detection. Source origin is retained; human/role analysis must establish independence.

`Store.packet(subject, stage)` exports the actual subject, transitive current dependency versions, required-detail names, and prior stage outputs. The packet excludes answer keys. `Store.review(packet, output)` validates provenance, order, full claim/detail coverage, evidence locators, and skeptic issue dispositions. The fact-checker receives all claims, including unflagged claims. Reviews may record a completed execution with a failed or incomplete outcome. `Store.decide` computes approval; callers do not submit an admission state directly.

Review contract version 2 persists the exact packet alongside each output and its hash. `Store.get_review(execution_id)` returns that historical packet without consulting current source or upstream-review versions, and verifies its hash. Packets include the subject and dependency versions/bodies and the actual prior review outputs. JSON and JSONL exports include these packets; export schema version 2 also includes claim coverage in the JSON envelope. Existing databases receive a nullable packet column. Legacy rows with no saved packet remain inspectable as `unavailable_legacy`, cannot count as current passing checks, and cannot be silently backfilled. New review executions are required. Packet retention here is suitable only for synthetic inputs; it does not authorize persisting whole live documents.

Coverage separates eligible claims, submitted entries, completed checks, pending checks, and unsubmitted entries. An explicit pending entry is submitted but not completed; missing entries are also pending. A completed check can be contradicted or unverifiable and is not synonymous with verification. Hypothesis review completion also does not count as factual verification.

Hypothesis claims retain their classification in the saved packet and exports. Their only dispositions are `reviewed_hypothesis` and `pending`; factual verdicts such as verified or partly verified are rejected. A reviewed nonmaterial hypothesis can remain visible as speculation, labelled not a verified fact. A material hypothesis cannot satisfy a required factual basis for admission and remains blocking. Factual claims cannot use the hypothesis disposition. The main example includes a hypothesis inside the claim ledger; the partial example leaves a factual check pending and shows less than full completed coverage.

The stage order is QC, researcher, skeptic, fact-checker; collection is recorded separately before QC. A distinct QC execution ID is required, including against dependency collectors. This is a traceability check, **not authentication or proof of separate contexts**. All outputs retain a basis and context description. Trusted callers can supply misleading IDs or edit the database directly; no independent-review enforcement is claimed.

Missing/stale required checkpoints, unresolved required details, undecided organization categories, unverified material claims, pending checks, and unresolved material issues block approval. Optional information and nonmaterial issues can remain visible. A material question can be supported as written with a recorded reason; calling a material defect a retained limitation does not unblock it. A correction requires a revised record and a fresh affected chain. Semantic truth is not inferred by structural validation.

Changed dependency fingerprints invalidate affected review packets transitively. Changed upstream review outputs invalidate downstream stage packets too. Historical versions/reviews/decisions remain stored. A previously approved current record becomes `awaiting_recheck`; unchanged unrelated records retain their reviews. These are operational queue states, separate from the PRD's canonical register admission vocabulary. `pending` represents unresolved work; `awaiting_recheck` does not overwrite historical admission.

## Reconciliation and recovery

Each ingestion attempt has exactly one disposition: unique, duplicate, or quarantined. Interrupted runs additionally expose pending items. An identical completed run ID returns its prior audit; changed inputs under that run ID are rejected. A running run resumes remaining items. An interruption between an item commit and its audit update can classify that item as a recovered duplicate; it cannot multiply the stored evidence. This limitation is not hidden as an exactly-once transport guarantee.

Candidate-period accounting uses distinct subjects: opening pending + newly discovered subjects + previously approved subjects reopened during the period = admitted work + closing pending. Repeated revisions of one subject during the same period are coalesced in counts but individually retained in history. This is not a count of every version transition. Stock accounting is separate and re-admission does not inflate register growth. Merge/exclusion transitions and scheduling are deferred. Ingestion totals are recomputed from item dispositions; mismatches fail reconciliation. Incomplete/partial run IDs remain visible even if counts balance.

JSON exports contain version history, reviews, decisions, audits and current status. JSONL contains the same table rows, tagged by group; the JSON envelope additionally contains the current-status projection and demonstration summary. No importer or multiwriter synchronization is included.

## Evidence boundaries

The demonstration's research, skeptic, and fact-checker outputs are **hand-authored fixture replay**. They test flow and approval handling, not actual reasoning, independent review, blind accuracy, or product usefulness. Actual coding-session role evaluation has not been performed in this increment. The separate expected-answer fixtures support later evaluation; an executing session that has seen the key cannot claim a blind evaluation.

The amount utilities compare explicit structured value/currency/unit/period/basis and calculate shortfalls with decimal arithmetic. They do not extract or semantically verify arbitrary prose. The evaluator counts missing checks, abstentions, false verification, false rejection, and exact verdict matches, with denominators; no numerical acceptance target is introduced.

Only synthetic input is accepted. This flag is an input contract, not automatic detection of real-world content. Live access permissions, transient cleanup, session-history retention, source-specific adapters, geographic completeness, sustained performance, actual role accuracy, and owner usefulness remain unestablished. The Markdown renderer is intended for trusted synthetic fixtures; adversarial markup sanitization and live-data publication controls are not implemented.
