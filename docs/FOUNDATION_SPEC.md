# Foundation specification
Status: Accepted Day 1 design with refinements; implementation pending separate authorization
Recorded: 2026-11-03

## Purpose
The foundation demonstrates a bounded collection-to-report flow executed in the coding environment. Source feasibility, implementation, data QC, and owner review are evaluated together. Full product geography remains Canada and Washington State.

This document specifies software behavior and evidence requirements. Coding assignments and execution instructions are supplied by the owner in chat.

## Scope
- Execution in the owner-directed coding environment with zero additional monetary operating cost; cloud development is permitted.
- Deterministic collection controls, identifiers, arithmetic checks, deduplication, counters, and checkpoints.
- Researcher, skeptic, and fact-checker roles executed within coding sessions with distinct contexts and outputs.
- Separate evidence quality and private business relevance judgments.
- Local inspectable output grouped by organization; complete dashboard styling is outside the initial scope.
- The first bounded English-language live sample focuses on BC and Washington, prioritizing local reporting, organization publications, and official/funder records. Dated interviews or existing podcast text remain additional candidates for expansion.
- Limited source coverage and unavailable source types remain explicit.

Workflow evaluation is described in WORKFLOW_EVALUATION.md. A synthetic executable foundation does not establish live-source coverage, autonomous reasoning, or daily scheduling.

## Expanding-register scope
The bounded foundation demonstrates source-to-organization and organization-to-source discovery, versioned candidate queues, and all four checkpoints before admission. Collection and data QC have separate responsibilities. Unresolved or blocked additions remain visible, merges retain provenance, and changed records reopen affected checks. Daily source/organization growth is not a quota. PROJECT_PLAN.md defines the baseline, first seven project days, and ongoing reconciliation; PRD.md holds open decisions.

## Initial design boundary
Starting eligibility is service-delivery nonprofits, with foundations and umbrella bodies as potential buyers/routes and no revenue cutoff. Hospitals, universities, religious organizations, and advocacy groups remain undecided. Day 1 design is complete and the accepted refinements are recorded below. Implementation requires separate authorization; this specification is not an execution assignment. Concrete live-source candidates and source-specific permissions remain prerequisites to the separately authorized live gate.

## Accepted implementation scope
Python + SQLite provide the bounded deterministic foundation; JSON/JSONL provide interchange and the first reviewable report is Markdown. No additional paid service, provider API integration, or local-model benchmark is required. The first implementation demonstrates the complete synthetic collection-to-report flow and both discovery directions with the minimum schema. Live collection is a separate gate.

Reversible merges, detailed funding relationships, HTML output, and dashboard work are deferred. Exact duplicate inputs can be grouped without multiplying records; suspected entity duplicates remain linked and unresolved rather than destructively merged. The long-term merge requirements do not require a reversible-merge subsystem in the first synthetic build.

## Data records
The initial schema uses the minimum necessary structures for six logical record groups. These groups are not a prescribed table count or separate subsystems.

| Group | Required content |
| --- | --- |
| Organizations | Identity, eligibility, provenance, admission state. |
| Sources | Publisher/endpoint, coverage, access/handling basis, admission state. |
| Evidence | Permitted content, dates, locators, source/version references. |
| Findings and claims | Observations, assertions, hypotheses, supporting evidence. |
| Reviews and decisions | Separate collection/QC records, researcher, skeptic, fact-checker, issues, required-detail checklist, and admission decisions. |
| Runs and history | Discovery events, version changes, dependencies/invalidation, dispositions, and reconciliation. |

Records retain stable identifiers, versions, source locators, dates or explicit unknowns, geography, identity certainty, and evidence references. Logical detail such as discovery provenance or claim checks may share a storage structure without losing its separate meaning or reviewed version.

Route investigation status distinguishes not investigated, none found after investigation, and evidence available. An unresolved organization identity is not a forced match.

## Collection behavior
Live retrieval is explicit and separate from offline replay. Collection has bounded timeouts and visible source failures. Source-specific permitted access and transient/retention handling precede live collection. Failed sources do not advance their successful checkpoint.

Identical-input reruns do not multiply records. Every input has a mutually exclusive disposition, and counters reconcile; reconciliation errors fail the run. Known duplicates are grouped, while ambiguous event matches remain labelled.

Initial historical discovery and daily incremental collection are distinct. Event and publication dates remain separate. Unknown dates are retained with visible uncertainty rather than fabricated. No feed's rolling window is assumed to provide a complete 12-month archive.

## Research and review behavior
RESEARCH_WORKFLOW.md defines the researcher, skeptic, and fact-checker logic. Fact-checking covers every number, quote, and paraphrase, including claims not flagged by the skeptic. A model-checked status is distinct from deterministic checking, human review, and independent source corroboration.

Material changes reopen affected checks through recorded dependencies. Historical decisions remain attached to their original versions; an affected current version awaits recheck and cannot inherit old approval. Unchanged records do not require full daily review. Review completion is distinct from passing review, and the required-detail checklist follows RESEARCH_WORKFLOW.md. Actual context separation must be recorded; separate execution IDs and files alone do not demonstrate isolation or independence.

Substantive evidence changes invalidate affected approvals. Uncertain, partial, contradicted, and inaccessible evidence remains inspectable with reasons. The weekly shortlist does not cap access to wider findings.

## Retention
Persisted live content is limited to metadata, checksums where available, and permitted sanitized evidence excerpts. Whole live articles, recordings, and transcripts are not permanently retained. Transient processing, caches, logs, histories, and error output follow the source-specific handling decision. Public demonstrations use synthetic records.

## Acceptance evidence
| Area | Required evidence |
| --- | --- |
| Offline functionality | Fresh-checkout synthetic example, documented prerequisites, and zero live calls. |
| Live feasibility | Permitted retrieval and parseable evidence from a Canadian source and a Washington source. Blocked portions remain incomplete. |
| Claim provenance | IDs, source locators, dates/unknowns, organization certainty, role/model/prompt versions, and supporting evidence. |
| Data QC | Reconciled dispositions, duplicate handling, identity uncertainty, all four checks for each of the three record types, and no success inherited from collection alone. |
| Discovery/admission | Both discovery directions, candidate queues, admission blocked by missing required checks, provenance-preserving duplicate links/unresolved matches, and changed-version rechecks. Reversible merge execution is deferred. |
| Role quality | Expected synthetic outcomes compared with recorded role outputs; errors and false verification reported. |
| Versioning | Changed evidence reopens affected reviews. |
| Privacy/retention | No unapproved raw content, credentials, device serial numbers, or private judgments in tracked files. |
| Human review | Actual owner feedback distinguished from assistant summaries and unperformed review. |

Gate A covers synthetic functionality and software checks. Gate B covers permitted live-source feasibility through the same flow. Owner usefulness review is separate from both. Passing one gate does not establish the others. These are staged outcomes within the bounded foundation, not permission for the planning conversation to execute implementation.

## Test cases
Malformed input; missing dates; ambiguous identity; exact/syndicated duplicates; irrelevant keywords; indirect clues with alternative explanations; numeric mismatch; altered quotes; overstated paraphrases; omitted qualifications; inaccessible originals; partial runs; rerun idempotence; stale approval; and source text containing untrusted instructions.

## Deferred scope
Nationwide crawling, full funding graph, all source adapters, advanced ranking, polished dashboard, scheduler installation, audio transcription, hosting, and productization are later increments. Source coverage, benchmark quality, and operating constraints govern their feasibility. Starting categories and no revenue cutoff are confirmed. Additional categories, specific source endpoints, and a license remain open.
