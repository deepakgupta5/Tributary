# Synthetic Tributary report

**Basis: Hand-authored fixture replay; no actual coding-session role review performed. No model accuracy, live-source feasibility, or owner usefulness is established by this report.**

All names and evidence are fictional. Source locators use synthetic references.

## Register and approval queue

## Organization group: o-ambiguous

### o-ambiguous: Fictional Cedar (ambiguous name)

Kind: organization; version: 1; state: **pending**.

- Blocker: Missing admission claim ledger
- Blocker: Required detail unresolved: identity
- Blocker: Required geography unresolved
- Blocker: Required detail not verified: eligibility
- Blocker: Required detail not verified: identity
- Unresolved possible duplicate: o-cedar

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:o-ambiguous:qc | True / passed |
| researcher | initial:o-ambiguous:researcher | True / passed |
| skeptic | initial:o-ambiguous:skeptic | True / passed |
| fact_checker | initial:o-ambiguous:fact_checker | True / passed |

Claim-check coverage: 0/0 completed; 0 submitted; 0 pending (0 unsubmitted) (fixture_replay).


Context record: Hand-authored replay; no model execution or context isolation.

## Organization group: o-cedar

### o-cedar: Fictional Cedar Support

Kind: organization; version: 2; state: **admitted**.

- Optional information: {"revenue": null}

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | recheck:o-cedar:qc | True / passed |
| researcher | recheck:o-cedar:researcher | True / passed |
| skeptic | recheck:o-cedar:skeptic | True / passed |
| fact_checker | recheck:o-cedar:fact_checker | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **identity — verified [fixture_replay]:** Fictional Cedar Support is a BC service-delivery nonprofit.
  Evidence: e-news / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Hand-authored replay; no model execution or context isolation.

### f-campaign: Cedar campaign observation

Kind: finding; version: 2; state: **pending**.

- Blocker: Checkpoint missing/stale/not passed: fact_checker
- Blocker: Material claim not verified: receipts
- Blocker: Claim not checked: receipts
- Limitation: Donor retention is unknown.
- Limitation: The organization report still states CAD 120000; source disagreement remains visible.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | recheck:f-campaign:qc | True / passed |
| researcher | recheck:f-campaign:researcher | True / passed |
| skeptic | recheck:f-campaign:skeptic | True / passed |
| fact_checker | partial:fact_checker | True / incomplete |

Claim-check coverage: 3/4 completed; 4 submitted; 1 pending (0 unsubmitted) (fixture_replay).

- **receipts — pending [fixture_replay]:** 2025 receipts were CAD 110000 according to the corrected bulletin.
  Evidence: e-news / p2; Fixture check deliberately left unperformed.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **quote — verified [fixture_replay]:** Demand increased, but donor retention has not been measured.
  Evidence: e-news / p3; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **cause — verified [fixture_replay]:** Venue flooding explains the extension; donor loss is not established.
  Evidence: e-news / p2; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **h-context — hypothesis — reviewed_hypothesis (not a verified fact) [fixture_replay]:** Campaign follow-through may warrant investigation; no consulting budget is established.
  Evidence: e-news / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Skeptic issues and dispositions:

- question: Optional retention context is not available. Material: False. Disposition: limitation_retained; Optional context remains visibly unknown..

Context record: Hand-authored replay; no model execution or context isolation.

Organization: o-cedar

Route investigation: not_investigated
- Alternative: Venue disruption explains the extension.

## Organization group: o-willow

### o-willow: Fictional Willow Network

Kind: organization; version: 2; state: **admitted**.


| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:o-willow:qc | True / passed |
| researcher | initial:o-willow:researcher | True / passed |
| skeptic | initial:o-willow:skeptic | True / passed |
| fact_checker | initial:o-willow:fact_checker | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **identity — verified [fixture_replay]:** Fictional Willow Network is a Washington umbrella nonprofit.
  Evidence: e-wa / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Hand-authored replay; no model execution or context isolation.

### f-grant: Willow restricted award

Kind: finding; version: 1; state: **pending**.

- Blocker: Checkpoint missing/stale/not passed: fact_checker
- Blocker: Material claim not verified: grant
- Limitation: A grant is not an introduction.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:f-grant:qc | True / passed |
| researcher | initial:f-grant:researcher | True / passed |
| skeptic | initial:f-grant:skeptic | True / passed |
| fact_checker | initial:f-grant:fact_checker | True / failed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **grant — contradicted [fixture_replay]:** USD 9000 is available for consulting.
  Evidence: e-wa / p2; Restricted to food; consulting is not established.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: USD 9000 restricted to food purchases.

Context record: Hand-authored replay; no model execution or context isolation.

Organization: o-willow

Route investigation: evidence_available

## Sources

### s-blocked: Synthetic access-uncertain source

Kind: source; version: 1; state: **pending**.

- Blocker: Missing admission claim ledger
- Blocker: Required detail unresolved: access
- Blocker: Required detail not verified: access
- Blocker: Required detail not verified: handling
- Blocker: Required detail not verified: identity
- Blocker: Required detail not verified: utility

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:s-blocked:qc | True / passed |
| researcher | initial:s-blocked:researcher | True / passed |
| skeptic | initial:s-blocked:skeptic | True / passed |
| fact_checker | initial:s-blocked:fact_checker | True / passed |

Claim-check coverage: 0/0 completed; 0 submitted; 0 pending (0 unsubmitted) (fixture_replay).


Context record: Hand-authored replay; no model execution or context isolation.

### s-news: Synthetic BC Community Bulletin

Kind: source; version: 2; state: **approved_for_collection**.


| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | recheck:s-news:qc | True / passed |
| researcher | recheck:s-news:researcher | True / passed |
| skeptic | recheck:s-news:skeptic | True / passed |
| fact_checker | recheck:s-news:fact_checker | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **identity — verified [fixture_replay]:** Synthetic BC Community Bulletin publishes freely reusable English community material.
  Evidence: e-news / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Hand-authored replay; no model execution or context isolation.

### s-org: Fictional Cedar publications

Kind: source; version: 2; state: **approved_for_collection**.


| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:s-org:qc | True / passed |
| researcher | initial:s-org:researcher | True / passed |
| skeptic | initial:s-org:skeptic | True / passed |
| fact_checker | initial:s-org:fact_checker | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **identity — verified [fixture_replay]:** Fictional Cedar publications contains freely reusable synthetic campaign reports.
  Evidence: e-org / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Hand-authored replay; no model execution or context isolation.

### s-wa: Synthetic Washington funder register

Kind: source; version: 2; state: **approved_for_collection**.


| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | initial:s-wa:qc | True / passed |
| researcher | initial:s-wa:researcher | True / passed |
| skeptic | initial:s-wa:skeptic | True / passed |
| fact_checker | initial:s-wa:fact_checker | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (fixture_replay).

- **identity — verified [fixture_replay]:** Synthetic Washington funder register publishes freely reusable grant awards.
  Evidence: e-wa / p1; Synthetic fixture citation.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Hand-authored replay; no model execution or context isolation.

## Discovery and coverage

Demonstrated categories: fictional BC community reporting, organization publication, and Washington funder record.
No real endpoint was attempted. No geographic completeness percentage is claimed.

- source_to_organization: s-news → o-cedar; mentioned in p1.
- organization_to_source: o-cedar → s-org; organization publication reference.
- source_to_organization: s-wa → o-willow; award recipient.
- organization_to_source: o-willow → s-wa; funder record.

## Reconciliation

```json
{
  "basis": "fixture_replay",
  "initial": {
    "opening_pending": 0,
    "new_candidates": 9,
    "reopened": 0,
    "admitted": 6,
    "closing_pending": 3,
    "population_ids": [
      "f-campaign",
      "f-grant",
      "o-ambiguous",
      "o-cedar",
      "o-willow",
      "s-blocked",
      "s-news",
      "s-org",
      "s-wa"
    ],
    "candidate_balance": true,
    "opening_active": 0,
    "activations": 6,
    "inactivations": 0,
    "closing_active": 6,
    "stock_balance": true,
    "discrepancies": [],
    "passed": true,
    "incomplete_runs": [
      "initial-ingestion"
    ],
    "limits": "Distinct candidate work per period; repeated revisions of one subject are coalesced in counts and retained individually in history. No merge/exclusion execution or scheduler. Retries are attempts, not new sources."
  },
  "after_change_before_recheck": {
    "f-campaign": "awaiting_recheck",
    "f-grant": "pending",
    "o-ambiguous": "pending",
    "o-cedar": "awaiting_recheck",
    "o-willow": "admitted",
    "s-blocked": "pending",
    "s-news": "awaiting_recheck",
    "s-org": "approved_for_collection",
    "s-wa": "approved_for_collection"
  },
  "changed_period": {
    "opening_pending": 3,
    "new_candidates": 0,
    "reopened": 3,
    "admitted": 3,
    "closing_pending": 3,
    "population_ids": [
      "f-campaign",
      "f-grant",
      "o-ambiguous",
      "o-cedar",
      "s-blocked",
      "s-news"
    ],
    "candidate_balance": true,
    "opening_active": 6,
    "activations": 0,
    "inactivations": 0,
    "closing_active": 6,
    "stock_balance": true,
    "discrepancies": [],
    "passed": true,
    "incomplete_runs": [
      "initial-ingestion"
    ],
    "limits": "Distinct candidate work per period; repeated revisions of one subject are coalesced in counts and retained individually in history. No merge/exclusion execution or scheduler. Retries are attempts, not new sources."
  },
  "rerun": {
    "opening_pending": 3,
    "new_candidates": 0,
    "reopened": 0,
    "admitted": 0,
    "closing_pending": 3,
    "population_ids": [
      "f-grant",
      "o-ambiguous",
      "s-blocked"
    ],
    "candidate_balance": true,
    "opening_active": 6,
    "activations": 0,
    "inactivations": 0,
    "closing_active": 6,
    "stock_balance": true,
    "discrepancies": [],
    "passed": true,
    "incomplete_runs": [
      "initial-ingestion"
    ],
    "limits": "Distinct candidate work per period; repeated revisions of one subject are coalesced in counts and retained individually in history. No merge/exclusion execution or scheduler. Retries are attempts, not new sources."
  },
  "rerun_ingestion": {
    "id": "repeat-ingestion",
    "input_hash": "55b70701a0be276efc361002ed230e1f3aaeb911379dab56c27f0a79fb862ef3",
    "items": [
      {
        "index": 0,
        "id": "e-news",
        "version": 2,
        "disposition": "duplicate"
      }
    ],
    "status": "complete",
    "input_count": 1,
    "counts": {
      "unique": 0,
      "duplicate": 1,
      "quarantined": 0
    },
    "pending_count": 0,
    "reconciled": true
  },
  "deterministic_checks": {
    "basis": "explicit synthetic structured amounts; not semantic extraction",
    "original_shortfall_CAD": "30000",
    "target_equals_actual": false
  },
  "actual_coding_session_review": "not_performed",
  "live_source_feasibility": "not_performed",
  "owner_usefulness": "not_performed",
  "partial_report_decision": {
    "id": "f-campaign",
    "state": "pending",
    "blockers": [
      "Checkpoint missing/stale/not passed: fact_checker",
      "Material claim not verified: receipts",
      "Claim not checked: receipts"
    ]
  }
}
```

## Limits

Review IDs and packets provide traceability, not reviewer independence. Semantic verdicts here are scripted. No authentication boundary prevents a trusted local operator editing SQLite directly. No live retrieval, scheduler, merge engine, paid dependency, or provider API is included.
