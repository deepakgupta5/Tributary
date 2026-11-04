# Foundation specification
Status: Product scope; bounded synthetic subset implemented
Recorded: 2026-11-03

## Purpose
The foundation demonstrates a bounded collection-to-report flow executed in the coding environment. Source feasibility, implementation, data QC, and owner review are evaluated together. Full product geography remains Canada and Washington State.

This document specifies software behavior and evidence requirements. Coding assignments and execution instructions are supplied by the owner in chat.

## Scope
- Local execution with zero additional monetary operating cost.
- Deterministic collection controls, identifiers, arithmetic checks, deduplication, counters, and checkpoints.
- Researcher, skeptic, and fact-checker roles executed within coding sessions with distinct contexts and outputs.
- Separate evidence quality and private business relevance judgments.
- Local inspectable output grouped by organization; complete dashboard styling is outside the initial scope.
- A bounded English-language source sample includes Canadian local/community reporting and Washington local/community or funder material. Dated interviews or existing podcast text are additional candidates.
- Limited source coverage and unavailable source types remain explicit.

Workflow evaluation is described in WORKFLOW_EVALUATION.md. A synthetic executable foundation does not establish live-source coverage, autonomous reasoning, or daily scheduling.

## Data records
The minimum record types are organization, source, evidence item, claim, candidate finding, role output, review judgment, and run audit. Records retain stable identifiers, versions, source locators, dates or explicit unknowns, geography, identity certainty, and evidence references.

Route investigation status distinguishes not investigated, none found after investigation, and evidence available. An unresolved organization identity is not a forced match.

## Collection behavior
Live retrieval is explicit and separate from offline replay. Collection has bounded timeouts and visible source failures. Source-specific permitted access and transient/retention handling precede live collection. Failed sources do not advance their successful checkpoint.

Identical-input reruns do not multiply records. Every input has a mutually exclusive disposition, and counters reconcile; reconciliation errors fail the run. Known duplicates are grouped, while ambiguous event matches remain labelled.

Initial historical discovery and daily incremental collection are distinct. Event and publication dates remain separate. Unknown dates are retained with visible uncertainty rather than fabricated. No feed's rolling window is assumed to provide a complete 12-month archive.

## Research and review behavior
RESEARCH_WORKFLOW.md defines the researcher, skeptic, and fact-checker logic. Fact-checking covers every number, quote, and paraphrase, including claims not flagged by the skeptic. A model-checked status is distinct from deterministic checking, human review, and independent source corroboration.

Substantive evidence changes invalidate affected approvals. Uncertain, partial, contradicted, and inaccessible evidence remains inspectable with reasons. The weekly shortlist does not cap access to wider findings.

## Retention
Persisted live content is limited to metadata, checksums where available, and permitted sanitized evidence excerpts. Whole live articles, recordings, and transcripts are not permanently retained. Transient processing, caches, logs, histories, and error output follow the source-specific handling decision. Public demonstrations use synthetic records.

## Acceptance evidence
| Area | Required evidence |
| --- | --- |
| Offline functionality | Fresh-checkout synthetic example, documented prerequisites, and zero live calls. |
| Live feasibility | Permitted retrieval and parseable evidence from a Canadian source and a Washington source. Blocked portions remain incomplete. |
| Claim provenance | IDs, source locators, dates/unknowns, organization certainty, role/model/prompt versions, and supporting evidence. |
| Data QC | Reconciled dispositions, duplicate handling, identity uncertainty, and no success inherited from collection alone. |
| Role quality | Expected synthetic outcomes compared with recorded role outputs; errors and false verification reported. |
| Versioning | Changed evidence reopens affected reviews. |
| Privacy/retention | No unapproved raw content, credentials, device serial numbers, or private judgments in tracked files. |
| Human review | Actual owner feedback distinguished from assistant summaries and unperformed review. |

Synthetic functionality, live-source feasibility, and owner usefulness review have separate outcomes. One does not establish the others.

## Test cases
Malformed input; missing dates; ambiguous identity; exact/syndicated duplicates; irrelevant keywords; indirect clues with alternative explanations; numeric mismatch; altered quotes; overstated paraphrases; omitted qualifications; inaccessible originals; partial runs; rerun idempotence; stale approval; and source text containing untrusted instructions.

## Deferred scope
Nationwide crawling, full funding graph, all source adapters, advanced ranking, polished dashboard, scheduler installation, audio transcription, hosting, and productization are later increments. Source coverage, benchmark quality, and operating constraints govern their feasibility. Category exclusions, revenue cutoffs, and a license have not been selected.

## Implemented subset and remaining evidence
The executable subset supports synthetic JSON collection, SQLite storage, exact-content deduplication, audit reconciliation, versioned role submission, stale-review detection, and report rendering. DATA_CONTRACTS.md documents the actual schema and validator limits. Examples retain fixture replay and same-session role outputs separately.

Live Canadian/Washington retrieval, source-specific retention checks, identity resolution, arithmetic beyond count reconciliation/numeric tokens, independent role contexts, private commercial judgments, dashboard, and daily scheduling are not implemented. The live-feasibility and owner-usefulness acceptance outcomes remain pending.
