# Development roadmap
Status: Draft v0.1
Updated: 2026-11-03

Local hardware and role-quality feasibility precede runtime/model selection and collection expansion. Measurements on development hosts and on the target MacBook are separate evidence categories. See [LOCAL_AI_FEASIBILITY.md](LOCAL_AI_FEASIBILITY.md).

Stages are outcome-based. Dates, effort, source counts, and quality thresholds remain uncommitted. Implementation tool selection and assignments remain with the owner. A working foundation precedes any external program submission; program approval is not assumed.

| Stage | Work | Exit condition |
| --- | --- | --- |
| 1. Requirements | Refine the PRD, resolve first-release questions, agree evidence/output rules. | Owner approves the first-release scope, acceptance criteria, and unresolved items that can safely wait. |
| 2. Source feasibility | Populate source register; inspect permitted samples across Canada and Washington and required media types. | Access, formats, gaps, and evidence utility documented; bounded pilot sources proposed. |
| 3. Manual discovery and human review | Prepare example findings; inspect supporting evidence; owner records relevance and reasons. | Signal definitions refined, review workflow agreed, and measurable first-build quality thresholds set. |
| 4. Technical design and coding | Validate local role feasibility; select stack; define organization/source/finding/relationship records; build synthetic fixtures, ingestion, matching, deduplication, audit, and review flow. | Fresh checkout runs a complete example; bounded source ingestion works; records reconcile and meaningful checks pass. |
| 5. QC and real-data review | Check source fidelity, identity errors, unsupported claims, omissions in a reviewed sample, duplicate events, coverage, reruns, and review workload. | Agreed quality thresholds pass or deviations are documented and explicitly accepted; owner can run and explain the foundation. |
| 6. Submission readiness | Disclose local AI roles and business use honestly; prepare public description, setup/demo, actual development history, and remaining engineering backlog. | Working foundation can be inspected; applicable program eligibility/terms confirmed separately before program-dependent work. |
| 7. Expansion and refinement | Add sources and localities, improve coverage and matching, implement feedback-driven refinements. | Each increment meets its acceptance criteria and updates coverage/quality evidence. |

## Incremental implementation
Source feasibility, a bounded working implementation, technical QC, and owner review form repeated activities within small increments. A nationwide research exercise is not a prerequisite to all coding.

[FOUNDATION_SPEC.md](FOUNDATION_SPEC.md) describes the limited initial scope. The repository contains requirements, code, research logic, and analysis; it does not issue assignments to coding assistants. Execution instructions are supplied by the owner in chat.


## Current scope decisions and pending proposals
- Confirmed: zero additional monetary operating cost, with no paid subscriptions, source access, hosting, APIs, or transcription. Choose free/local methods; record inaccessible sources as coverage gaps. No automatic paid overages.
- Confirmed: deterministic data handling with local AI researcher, skeptic, and fact-checker roles. The owner reviews results; no paid/cloud model service is authorized. Local hardware and role-quality feasibility precede model selection.
- Confirmed: initial source trial and release use English only across Canada and Washington State. Record other-language coverage gaps.
- Pending: organization-category exclusions and size thresholds; broad eligibility and no revenue cutoff are proposals only.
- Confirmed: organization-based searchable dashboard with new/changed, organization profile, and coverage views; a weekly shortlist without a forced quota; separate evidence-quality and relevance judgments.
- Confirmed: daily local collection. Exact run time and source-specific access exceptions remain open.
- Confirmed: human review can take multiple hours. Exact weekly allocation, shortlist size, and ranking rules remain open.
- Resolve these open items in the PRD before treating them as approved implementation requirements.

## Repeatable development cycle
For every increment:
1. Define a concrete requirement and acceptance checks.
2. Verify data availability and access conditions.
3. Implement a bounded change on a branch.
4. Run relevant software and data-quality checks.
5. Inspect evidence-backed output and account for processing failures.
6. Obtain human relevance feedback and record reasons.
7. Revise rules or requirements where warranted; update documentation and commit actual work.

Human product feedback concerns usefulness and evidence quality. Any external program's assistant-response comparisons and required unaided reasoning are separate activities governed by that program.

## QC responsibilities
- Automated checks: validation, record reconciliation, known-answer identity cases, deduplication, idempotent reruns, evidence links, and failure reporting.
- Evidence review: factual accuracy, dates, source interpretation, contradictions, and whether suggested relevance exceeds the evidence.
- Owner review: commercial relevance, missing context, desired review workload, and scope decisions.
- Release record: what changed, what was checked, observed limits, and open defects.

## Foundation engineering requirements
Use synthetic fixtures with planted identity, duplicate, date, and malformed-input cases. Provide a replay harness that exercises the full fixture pipeline with zero live calls. Use stable identifiers and auditable rule triggers. Import counters and mutually exclusive dispositions must reconcile; reconciliation failure must be visible and fail the run.

Maintain a dated development log and commit actual changes as work happens. The owner must be able to run the foundation, inspect its output, and explain its limits. No inherited ticket count or effort estimate is treated as a requirement.

## First technical slice, pending documentation approval
The initial implementation integrates source inspection with a synthetic end-to-end example and bounded live collection where permitted. It demonstrates evidence becoming a dated organization finding in a review queue. Identity resolution and funding joins can be limited or unresolved in this first slice; the complete funding map and official-data adapters are later increments. Explicitly report routes not yet investigated versus none found after investigation.

Clear each live source's access and content-handling gate before collecting it. If all live sources are blocked, the synthetic foundation can pass its own checks, but live feasibility remains unproven. Broader source coverage and relevance thresholds follow owner review.

Do not implement nationwide collection simply to satisfy the geographic ambition. Expand coverage visibly without claiming unimplemented locations are monitored.

## Trial requirements for recency and indirect evidence
Use the agreed 12-month discovery window and older records for comparisons. Test direct statements and indirect observations from local reporting/interviews and other source categories. Human review must check alternative explanations, comparability, source independence, current-status updates, and whether a recent weak clue incorrectly outranks an older relevant pattern. Derive detailed ranking and refresh rules from these results.

## Daily local operation
Confirmed: daily local collection and visible missed-run reporting. Implement catch-up on resume, per-source successful checkpoints, idempotent reruns, partial-failure reporting, and explicit unrecoverable gaps. Test interrupted/failed runs and a period when the host is unavailable using fixtures. The weekly review view is separate from the collection schedule.

Scheduling is a later implementation deliverable, not an automation already running. Exact local time and mechanism remain open; source access limits and zero-cost operation still apply.

## Human investigation in the trial
Confirmed: the owner can spend multiple hours reviewing prospects. Exact weekly allocation remains open. Test detailed organization profiles, source context, conflicting evidence, candidate explanations, and access to uncertain findings beyond the shortlist. Record review time as an observation, not a restrictive target. Do not discard useful candidates to meet an arbitrary count or time limit.

## Development feedback traceability
Maintain [DEVELOPMENT_FEEDBACK.md](DEVELOPMENT_FEEDBACK.md) alongside implementation: initial instruction, observed response, actual owner feedback, revised instructions, resulting change, and verification evidence. Link code changes and checks. Preserve unresolved and unsuccessful outcomes where material. Update the record during work rather than reconstructing an invented history. Private or restricted material stays outside the public log.

## Researcher, skeptic, and fact-checker workflow
The initial implementation follows [RESEARCH_WORKFLOW.md](RESEARCH_WORKFLOW.md): researcher report and full claim ledger, constructive skeptic's ranked issues, comprehensive source fact-checking, then a report with individual verification flags and unresolved problems. Collection and QC remain separate. Every number, quote, and paraphrase must be checked; a skeptic's silence is not approval.

Implement distinct versioned outputs and actors for each review stage. Local LLM roles are authorized; deterministic checks and owner judgment remain separate. Model labels must not impersonate independent human verification. Test faulty numbers, altered quotes, misleading paraphrases, source access failures, and invalidated approvals. Technical code QC remains separate from evidence review and owner relevance judgments.


## Deferred decisions
Stack, interface implementation details, hosting, collection scheduling, free/local source access and transcription feasibility, source refresh frequency and historical comparison periods, numeric quality targets, and milestone effort are decided from the PRD and trial. No client donor-analysis or outreach capability is planned.
