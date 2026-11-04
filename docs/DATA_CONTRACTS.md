# Foundation data contracts
Schema version: 1. Storage: SQLite, Python standard library. This describes the implemented synthetic boundary, not the full future product schema.

## Collection
The JSON input is a list of objects. Required strings are `source_id`, `native_id`, `organization_id`, `organization`, `region`, `language`, and `url`. Region is `CA` or `US-WA`, language is `en`, `synthetic` is true, and URL begins `fixture://`. `event_date` and `publication_date` are ISO dates or null. `passages` maps stable nonempty locators to nonempty text. Unknown identities are rejected with a reason; no name matching is inferred.

This adapter does not retrieve network sources or persist real articles. Marking something synthetic is a caller assertion, not an automated personal-data detector. Only synthetic test material belongs in this adapter.

## Persistent tables
| Table | Meaning |
| --- | --- |
| `evidence` | Immutable evidence versions keyed by organization, geography, event date, and exact passage content. |
| `occurrence` | Immutable source/native-ID/URL/publication-date provenance for each evidence version. |
| `source_head` | Current version for a source/native-ID pair; earlier versions remain in history. |
| `run` | Timestamp, mutually exclusive item dispositions, reconciled counters, and run status. |
| `stage` | Immutable submitted role artifact, evidence snapshot, upstream artifact ID, and receipt time. |

Exact evidence copies retain multiple origins without becoming independent corroboration. Whitespace changes, changed locator keys, fuzzy duplicates, and related events are not inferred to be duplicates. Stable organization IDs are supplied by fixtures, not resolved by this foundation.

The current evidence snapshot is a digest of active evidence and origins. An input digest also covers the schema, role contract version, role definition text, and predecessor outputs. A source change, provenance change, role-definition change, or revised predecessor invalidates affected reviews. Old records remain stored but cannot silently serve as current approval.

## Role envelopes
Every output contains `role`, `role_version`, `input_digest`, `actor`, `execution_id`, timezone-aware `created_at`, and `basis`. Basis is `synthetic_fixture`, `model_checked`, or `human_checked`. Model-based artifacts require `model_version`, with an explicit unavailable marker accepted where the environment does not expose it. Provenance is self-reported; the foundation cannot authenticate that a human/model actually performed a check.

Role contracts are `research-v1`, `skeptic-v1`, and `factcheck-v1`. JSON examples are in `fixtures/` and bound executable artifacts in `examples/`. `role-input` produces a packet containing source passages as untrusted data. It does not execute a model.

### Researcher
`claims` is a nonempty list with unique `claim_id`, `organization_id`, `evidence_id`, `locator`, `kind`, `classification`, and `text`. Kind is `number`, `quote`, `paraphrase`, or `hypothesis`; classification is `observation`, `attributed_statement`, or `hypothesis`. Numbers additionally require a finite decimal string `value` and `unit`. Quotes require exact `quote` text. Hypotheses require `alternative`. `unknowns` is a list of nonempty strings.

### Skeptic
`issues` has unique `issue_id`, valid `claim_ids`, severity (`high`, `medium`, `low`), `problem`, `evidence_needed`, and `remedy`. An empty issue list is permitted. It does not waive fact-checking.

### Fact-checker
`checks` covers every researcher claim exactly once. Each check identifies `claim_id`, `evidence_id`, `locator`, `status`, and `explanation`. Status is `verified`, `partly verified`, `contradicted`, `unverifiable`, or `pending`. Checked/contradicted factual results require an exact `support` excerpt from the cited passage. Corrections are optional and displayed beside the retained original claim.

`resolutions` covers every skeptic issue exactly once, with `issue_id`, `status`, and `reason`. Status is `corrected`, `supported as written`, `limitation retained`, or `unresolved`.

## Validation limits
Numeric token checks and quotation matching block obvious false passes. Numeric matching does not establish the correct period, currency, denominator, target/actual distinction, or causation. Paraphrase meaning, missing qualifications, and alternative explanations require coding-session review. Model-checked labels are not independent human verification. Hypotheses cannot be verified as facts. Missing source references or omitted claim checks fail validation; pending checks remain pending.

Role artifacts are submitted through the same documented CLI in Codex or Claude Code. No provider SDK or API key is needed. Separate artifacts preserve stage boundaries; same-session execution does not create independent contexts. The current version does not launch autonomous roles, schedule collection, validate live retention permissions, or implement private commercial review records.
