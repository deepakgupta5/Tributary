# Synthetic Tributary report

**Basis: Recorded execution bases: coding_session; context separation must be assessed from the records. No model accuracy, live-source feasibility, or owner usefulness is established by this report.**

All names and evidence are fictional. Source locators use synthetic references.

## Register and approval queue

## Organization group: o-ambiguous

### o-ambiguous: Harbor Meals (unresolved)

Kind: organization; version: 1; state: **pending**.

- Blocker: Required detail unresolved: identity
- Blocker: Required geography unresolved
- Blocker: Checkpoint missing/stale/not passed: qc
- Blocker: Checkpoint missing/stale/not passed: researcher
- Blocker: Checkpoint missing/stale/not passed: skeptic
- Blocker: Checkpoint missing/stale/not passed: fact_checker
- Blocker: Required detail not verified: eligibility
- Blocker: Required detail not verified: identity
- Blocker: Material claim not verified: oa1
- Blocker: Material issue requires resolution/revision: oa-identity
- Limitation: Unverified candidate identity assertion. Two distinct registry entities share the short form; do not merge or infer identity.
- Unresolved possible duplicate: o-harbor

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:o-ambiguous | True / failed |
| researcher | session-001:researcher:o-ambiguous | True / failed |
| skeptic | session-001:skeptic:o-ambiguous | True / failed |
| fact_checker | session-001:fact_checker:o-ambiguous | True / failed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (coding_session).

- **oa1 — contradicted [coding_session]:** The shortened name Harbor Meals uniquely identifies the Washington organization.
  Evidence: d-register / p1; p1 says the shortened name does not distinguish Society and Trust. This contradicts unique Washington identification; it does not identify which entity was intended.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Retain unresolved identity until a distinguishing identifier is supplied.

Skeptic issues and dispositions:

- oa-identity: oa1 claims uniqueness despite the explicit two-entity warning. Material: True. Disposition: unresolved; Unique identifier absent; no merge or admission..

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

## Organization group: o-harbor

### o-harbor: Harbor Meals Society

Kind: organization; version: 1; state: **admitted**.

- Optional information: {"consulting_budget": "unknown; optional"}

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:o-harbor | True / passed |
| researcher | session-001:researcher:o-harbor | True / passed |
| skeptic | session-001:skeptic:o-harbor | True / passed |
| fact_checker | session-001:fact_checker:o-harbor | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (coding_session).

- **oh1 — verified [coding_session]:** Harbor Meals Society, SYN-BC-041, is a service-delivery nonprofit in British Columbia.
  Evidence: d-register / p1; p1 states all four identifying/eligibility facts together.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

### f-chain: Harbor Meals campaign evidence

Kind: finding; version: 1; state: **approved**.

- Limitation: No demonstrated commercial need or available consulting budget.
- Limitation: Grant is restricted to food purchases.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:f-chain | True / passed |
| researcher | session-001:researcher:f-chain | True / passed |
| skeptic | session-001:skeptic:f-chain | True / passed |
| fact_checker | session-001:fact_checker:f-chain | True / passed |

Claim-check coverage: 6/6 completed; 6 submitted; 0 pending (0 unsubmitted) (coding_session).

- **f1 — verified [coding_session]:** The 2025 campaign received CAD 84500 against a CAD 100000 target.
  Evidence: d-annual / p1; p1 gives 2025 CAD 84500 actual against CAD 100000 target.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **f2 — verified [coding_session]:** The 2025 campaign shortfall was CAD 15500, calculated as 100000 minus 84500.
  Evidence: d-annual / p1; Same currency and 2025 period: 100000 - 84500 = 15500. This is a derived shortfall, not a new source quotation.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **f3 — verified [coding_session]:** We may reduce weekend deliveries if the restricted grant is not renewed.
  Evidence: d-annual / p2; Quoted sentence matches p2 exactly, retaining may, if and restricted.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **f4 — verified [coding_session]:** The deadline extension followed venue flooding; donor retention has not been measured.
  Evidence: d-annual / p3; p3 states extension followed flooding and retention has not been measured. No improved retention is inferred.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **f5 — verified [coding_session]:** The 2024 receipts included a CAD 20000 one-time gift and eligibility changed; totals alone do not establish comparable donor behavior.
  Evidence: d-annual / p1; p1 states one-time CAD 20000 gift, changed eligibility and noncomparability limitation.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **f6 — hypothesis — reviewed_hypothesis (not a verified fact) [coding_session]:** Campaign administration assistance might be relevant; demand and budget remain unknown.
  Evidence: d-annual / p3; Possible assistance relevance is not verified demand. Unknown budget and demand remain explicit.
  Corroboration: unknown; this is separate from source-faithfulness.

Skeptic issues and dispositions:

- f-arithmetic: Confirm the CAD 15500 calculation uses the 2025 target and actual, not a cross-year difference. Material: False. Disposition: supported_as_written; Both inputs are 2025 CAD amounts; subtraction yields CAD 15500..
- f-hypothesis: The report does not establish a consulting need, budget or purchasing intent. Material: False. Disposition: limitation_retained; Nonmaterial hypothesis stays nonfactual; no budget or demand inferred..

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

Organization: o-harbor

Route investigation: not_investigated
- Alternative: Flooding explains the extension without evidence of fundraising process failure.

### f-challenge: Unapproved reviewer challenge ledger

Kind: finding; version: 1; state: **pending**.

- Blocker: Source not currently approved: s-reprint
- Blocker: Source not currently approved: s-reprint
- Blocker: Checkpoint missing/stale/not passed: qc
- Blocker: Checkpoint missing/stale/not passed: researcher
- Blocker: Checkpoint missing/stale/not passed: skeptic
- Blocker: Checkpoint missing/stale/not passed: fact_checker
- Blocker: Required detail not verified: evidence
- Blocker: Required detail not verified: identity
- Blocker: Material claim not verified: c1
- Blocker: Material claim not verified: c2
- Blocker: Material claim not verified: c3
- Blocker: Material claim not verified: c4
- Blocker: Material claim not verified: c5
- Blocker: Material claim not verified: c6
- Blocker: Material claim not verified: c7
- Blocker: Material claim not verified: c8
- Blocker: Material claim not verified: c9
- Blocker: Material issue requires resolution/revision: ch-number
- Blocker: Material issue requires resolution/revision: ch-currency
- Blocker: Material issue requires resolution/revision: ch-quote
- Blocker: Material issue requires resolution/revision: ch-condition
- Blocker: Material issue requires resolution/revision: ch-retention
- Blocker: Material issue requires resolution/revision: ch-origin
- Blocker: Material issue requires resolution/revision: ch-identity
- Blocker: Material issue requires resolution/revision: ch-permission
- Blocker: Material issue requires resolution/revision: ch-budget
- Limitation: Imported planted proposals, not collector-endorsed facts.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:f-challenge | True / failed |
| researcher | session-001:researcher:f-challenge | True / failed |
| skeptic | session-001:skeptic:f-challenge | True / failed |
| fact_checker | session-001:fact_checker:f-challenge | True / failed |

Claim-check coverage: 12/12 completed; 12 submitted; 0 pending (0 unsubmitted) (coding_session).

- **c1 — contradicted [coding_session]:** The 2025 campaign received CAD 845000.
  Evidence: d-annual / p1; Source amount has one fewer zero: CAD 84500.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: CAD 84500 in 2025.
- **c2 — contradicted [coding_session]:** The 2025 campaign received USD 84500.
  Evidence: d-annual / p1; p1 uses CAD; no USD conversion supports this assertion.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Restore CAD.
- **c3 — contradicted [coding_session]:** The director said: We have reduced weekend deliveries because the grant was not renewed.
  Evidence: d-annual / p2; p2 is a future possibility conditional on nonrenewal; no completed reduction is stated.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: We may reduce weekend deliveries if the restricted grant is not renewed.
- **c4 — contradicted [coding_session]:** The organization will reduce weekend deliveries, regardless of grant renewal.
  Evidence: d-annual / p2; Regardless of renewal reverses the explicit if-condition and will overstates may.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Retain may and if the restricted grant is not renewed.
- **c5 — partly_verified [coding_session]:** The campaign received CAD 84500 and improved donor retention.
  Evidence: d-annual / p3; CAD 84500 is in p1, but p3 says retention was not measured. The conjunctive claim is only partly supported.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Report the receipt amount separately; retention improvement is not established.
- **c6 — contradicted [coding_session]:** The annual report and Dispatch reprint are two independent confirmations of receipts.
  Evidence: d-reprint / p1; Dispatch p1 explicitly names a reprint of the society statement and no independent reporting. Two documents are one origin.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Single-origin evidence, not two independent confirmations.
- **c7 — contradicted [coding_session]:** A record labelled only Harbor Meals uniquely identifies the Washington organization.
  Evidence: d-register / p1; Registry explicitly says the short name does not distinguish the two entities. Uniqueness is contradicted; entity identity is still unknown.
  Corroboration: single_origin; this is separate from source-faithfulness.
  Correction: Unresolved identity; do not assign Washington from the short name.
- **c8 — unverifiable [coding_session]:** Reading the Dispatch without a login establishes permission for routine collection and retention.
  Evidence: d-reprint / p0; The readable sample supplies no routine collection/retention permission. No conclusion about actual permission can be verified.
  Corroboration: unknown; this is separate from source-faithfulness.
- **c9 — unverifiable [coding_session]:** The unavailable original confirms a CAD 60000 consulting budget.
  Evidence: d-missing / None; d-missing has no available original or paragraph. No CAD 60000 budget evidence exists in the supplied corpus.
  Corroboration: unknown; this is separate from source-faithfulness.
- **c10 — verified [coding_session]:** The 2025 campaign received CAD 84500 against a CAD 100000 target.
  Evidence: d-annual / p1; p1 gives both 2025 CAD amounts and actual/target roles exactly.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **c11 — verified [coding_session]:** We may reduce weekend deliveries if the restricted grant is not renewed.
  Evidence: d-annual / p2; Matches original p2 sentence exactly including modal and condition.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **c12 — hypothesis — reviewed_hypothesis (not a verified fact) [coding_session]:** Campaign administration assistance might be relevant, but budget and demand for assistance remain unknown.
  Evidence: d-annual / p3; Exploratory relevance is not an established fact or buying signal. Budget and demand remain unknown.
  Corroboration: unknown; this is separate from source-faithfulness.

Skeptic issues and dispositions:

- ch-number: c1 adds a zero to the source amount. Material: True. Disposition: unresolved; Correction proposed only; original candidate text remains erroneous..
- ch-currency: c2 changes CAD to USD without conversion evidence. Material: True. Disposition: unresolved; Original USD assertion not revised..
- ch-quote: c3 changes a conditional future possibility into completed reductions and nonrenewal. Material: True. Disposition: unresolved; Altered quote retained in failed ledger; corrected wording supplied in check..
- ch-condition: c4 drops may/if and makes the reduction unconditional. Material: True. Disposition: unresolved; Missing qualification remains in original proposal..
- ch-retention: c5 joins a supported amount to an unsupported retention improvement. Material: True. Disposition: unresolved; No retention measurement supplied..
- ch-origin: c6 counts a declared reprint as independent corroboration. Material: True. Disposition: unresolved; Original independence assertion remains false..
- ch-identity: c7 assumes a unique Washington identity from an ambiguous short name. Material: True. Disposition: unresolved; No distinguishing identity supplied..
- ch-permission: c8 treats no-login readability as routine collection/retention permission. Material: True. Disposition: unresolved; No routine handling basis supplied..
- ch-budget: c9 purports to verify a budget from an unavailable original. Material: True. Disposition: unresolved; Original still unavailable; budget not established..

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

Organization: o-harbor

Route investigation: not_investigated

## Sources

### s-annual: Harbor Meals annual report

Kind: source; version: 2; state: **approved_for_collection**.

- Limitation: First-party assertions, not independent corroboration.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:s-annual | True / passed |
| researcher | session-001:researcher:s-annual | True / passed |
| skeptic | session-001:skeptic:s-annual | True / passed |
| fact_checker | session-001:fact_checker:s-annual | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (coding_session).

- **sa1 — verified [coding_session]:** The society publishes this first-party report and permits reading and retaining attributed excerpts for this exercise.
  Evidence: d-annual / p0; p0 identifies society publication and attributed excerpt permission; registry p2 corroborates endpoint relationship, not receipt accuracy.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

### s-register: Synthetic Coastal Register

Kind: source; version: 2; state: **approved_for_collection**.

- Limitation: Fictional permission statement only; no real endpoint inspected.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:s-register | True / passed |
| researcher | session-001:researcher:s-register | True / passed |
| skeptic | session-001:skeptic:s-register | True / passed |
| fact_checker | session-001:fact_checker:s-register | True / passed |

Claim-check coverage: 1/1 completed; 1 submitted; 0 pending (0 unsubmitted) (coding_session).

- **sr1 — verified [coding_session]:** The fictional public register permits reading and attributed reuse of its synthetic entries without authentication or payment.
  Evidence: d-register / p0; p0 explicitly states public register, attributed reuse, and no authentication/payment.
  Corroboration: single_origin; this is separate from source-faithfulness.

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

### s-reprint: North Inlet Dispatch

Kind: source; version: 2; state: **pending**.

- Blocker: Required detail unresolved: handling
- Blocker: Checkpoint missing/stale/not passed: qc
- Blocker: Checkpoint missing/stale/not passed: researcher
- Blocker: Checkpoint missing/stale/not passed: skeptic
- Blocker: Checkpoint missing/stale/not passed: fact_checker
- Blocker: Required detail not verified: handling
- Blocker: Material claim not verified: sp2
- Blocker: Material issue requires resolution/revision: sp-handling
- Limitation: sp2 is an unverified admission proposition, not an adopted extraction. Permission remains unknown.

| Checkpoint | Execution | Completion / outcome |
| --- | --- | --- |
| qc | session-001:qc:s-reprint | True / failed |
| researcher | session-001:researcher:s-reprint | True / failed |
| skeptic | session-001:skeptic:s-reprint | True / failed |
| fact_checker | session-001:fact_checker:s-reprint | True / failed |

Claim-check coverage: 2/2 completed; 2 submitted; 0 pending (0 unsubmitted) (coding_session).

- **sp1 — verified [coding_session]:** The supplied Dispatch sample is readable without login and reprints the society statement without independent reporting.
  Evidence: d-reprint / p1; p1 identifies the reprint and absence of independent reporting; p0 separately states no-login readability.
  Corroboration: single_origin; this is separate from source-faithfulness.
- **sp2 — unverifiable [coding_session]:** Routine collection and retention permission is established for this publication.
  Evidence: d-reprint / p0; No routine permission/retention basis supplied. Readability cannot supply it.
  Corroboration: unknown; this is separate from source-faithfulness.

Skeptic issues and dispositions:

- sp-handling: sp2 infers permission that p0 expressly leaves unspecified. Material: True. Disposition: unresolved; No permission evidence added; candidate remains pending..

Context record: Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.

## Discovery and coverage

Source coverage is limited to the fictional records listed above; it does not establish live publication or geographic coverage.
No real endpoint was attempted. No geographic completeness percentage is claimed.

- source_to_organization: s-register → o-harbor; Registry p1 identifies BC entity.
- source_to_organization: s-register → o-ambiguous; Registry p1 exposes shared short name, held unresolved.
- organization_to_source: o-harbor → s-annual; Registry p2 names organization publication endpoint.
- organization_to_source: o-harbor → s-reprint; Supplied corpus reverse lookup finds reprinted society statement.

## Reconciliation

```json
{
  "run": "session-001",
  "execution": "original recorded coding session",
  "tracks": {
    "complete_chain": [
      "s-register",
      "s-annual",
      "s-reprint",
      "o-harbor",
      "o-ambiguous",
      "f-chain"
    ],
    "reviewer_challenge": [
      "f-challenge"
    ]
  },
  "context": {
    "session": "session-001",
    "baseline": "087b12329d7c776dcbec3d22f93d899f54709516",
    "basis": "coding_session",
    "actor": "Codex assistant",
    "model_identifier": "Exact runtime model identifier unavailable",
    "context": "Same Codex chat and assistant; stage-specific saved packet but no isolated context. Source documents, challenge construction and expected answers were visible in this context. Open-book/contaminated; not independent or blind.",
    "context_isolation": false,
    "expected_answers_seen": true,
    "execution": "Actual assistant-authored stage assessments serialized during this coding session. Reproduction loads these saved assessments; it does not execute a new reviewer.",
    "stage_packets": "Separate versioned packets include prior stage outputs. Prior reasoning and answer key also remained in shared chat context.",
    "collection_qc_separation": "Different saved collection and QC executions by the same assistant; no personnel or context independence.",
    "transport": "Python standard library and existing Store/report. No model API calls or local model runtime.",
    "started_at": "2026-11-04T05:08:47.248871+00:00"
  },
  "decisions": [
    {
      "id": "s-register",
      "state": "approved_for_collection",
      "blockers": []
    },
    {
      "id": "s-annual",
      "state": "approved_for_collection",
      "blockers": []
    },
    {
      "id": "s-reprint",
      "state": "pending",
      "blockers": [
        "Required detail unresolved: handling",
        "Checkpoint missing/stale/not passed: qc",
        "Checkpoint missing/stale/not passed: researcher",
        "Checkpoint missing/stale/not passed: skeptic",
        "Checkpoint missing/stale/not passed: fact_checker",
        "Required detail not verified: handling",
        "Material claim not verified: sp2",
        "Material issue requires resolution/revision: sp-handling"
      ]
    },
    {
      "id": "o-harbor",
      "state": "admitted",
      "blockers": []
    },
    {
      "id": "o-ambiguous",
      "state": "pending",
      "blockers": [
        "Required detail unresolved: identity",
        "Required geography unresolved",
        "Checkpoint missing/stale/not passed: qc",
        "Checkpoint missing/stale/not passed: researcher",
        "Checkpoint missing/stale/not passed: skeptic",
        "Checkpoint missing/stale/not passed: fact_checker",
        "Required detail not verified: eligibility",
        "Required detail not verified: identity",
        "Material claim not verified: oa1",
        "Material issue requires resolution/revision: oa-identity"
      ]
    },
    {
      "id": "f-chain",
      "state": "approved",
      "blockers": []
    },
    {
      "id": "f-challenge",
      "state": "pending",
      "blockers": [
        "Source not currently approved: s-reprint",
        "Source not currently approved: s-reprint",
        "Checkpoint missing/stale/not passed: qc",
        "Checkpoint missing/stale/not passed: researcher",
        "Checkpoint missing/stale/not passed: skeptic",
        "Checkpoint missing/stale/not passed: fact_checker",
        "Required detail not verified: evidence",
        "Required detail not verified: identity",
        "Material claim not verified: c1",
        "Material claim not verified: c2",
        "Material claim not verified: c3",
        "Material claim not verified: c4",
        "Material claim not verified: c5",
        "Material claim not verified: c6",
        "Material claim not verified: c7",
        "Material claim not verified: c8",
        "Material claim not verified: c9",
        "Material issue requires resolution/revision: ch-number",
        "Material issue requires resolution/revision: ch-currency",
        "Material issue requires resolution/revision: ch-quote",
        "Material issue requires resolution/revision: ch-condition",
        "Material issue requires resolution/revision: ch-retention",
        "Material issue requires resolution/revision: ch-origin",
        "Material issue requires resolution/revision: ch-identity",
        "Material issue requires resolution/revision: ch-permission",
        "Material issue requires resolution/revision: ch-budget"
      ]
    }
  ],
  "reconciliation": {
    "opening_pending": 0,
    "new_candidates": 7,
    "reopened": 0,
    "admitted": 4,
    "closing_pending": 3,
    "population_ids": [
      "f-chain",
      "f-challenge",
      "o-ambiguous",
      "o-harbor",
      "s-annual",
      "s-register",
      "s-reprint"
    ],
    "candidate_balance": true,
    "opening_active": 0,
    "activations": 4,
    "inactivations": 0,
    "closing_active": 4,
    "stock_balance": true,
    "discrepancies": [],
    "passed": true,
    "incomplete_runs": [],
    "limits": "Distinct candidate work per period; repeated revisions of one subject are coalesced in counts and retained individually in history. No merge/exclusion execution or scheduler. Retries are attempts, not new sources."
  }
}
```

## Limits

Review IDs and packets provide traceability, not reviewer independence. Execution basis and actual context limitations are recorded per review. No authentication boundary prevents a trusted local operator editing SQLite directly. No live retrieval, scheduler, merge engine, paid dependency, or provider API is included.
