# Development roadmap
Status: Draft v0.1
Updated: 2026-11-03

Stages are outcome-based. Dates, effort, source counts, and quality thresholds remain uncommitted. Initial implementation uses Codex. A working foundation precedes any external program submission; program approval is not assumed.

| Stage | Work | Exit condition |
| --- | --- | --- |
| 1. Requirements | Refine the PRD, resolve first-release questions, agree evidence/output rules. | Owner approves the first-release scope, acceptance criteria, and unresolved items that can safely wait. |
| 2. Source feasibility | Populate source register; inspect permitted samples across Canada and Washington and required media types. | Access, formats, gaps, and evidence utility documented; bounded pilot sources proposed. |
| 3. Manual discovery and human review | Prepare example findings; inspect supporting evidence; owner records relevance and reasons. | Signal definitions refined, review workflow agreed, and measurable first-build quality thresholds set. |
| 4. Technical design and coding | Select stack; define organization/source/finding/relationship records; build synthetic fixtures, ingestion, matching, deduplication, audit, and review flow. | Fresh checkout runs a complete example; bounded source ingestion works; records reconcile and meaningful checks pass. |
| 5. QC and real-data review | Check source fidelity, identity errors, unsupported claims, omissions in a reviewed sample, duplicate events, coverage, reruns, and review workload. | Agreed quality thresholds pass or deviations are documented and explicitly accepted; owner can run and explain the foundation. |
| 6. Submission readiness | Prepare honest public project description, setup/demo, actual development history, and remaining engineering backlog. | Working foundation can be inspected; applicable program eligibility/terms confirmed separately before program-dependent work. |
| 7. Expansion and refinement | Add sources and localities, improve coverage and matching, implement feedback-driven refinements. | Each increment meets its acceptance criteria and updates coverage/quality evidence. |

## Current scope decisions and pending proposals
- Confirmed: zero additional monetary operating cost, with no paid subscriptions, source access, hosting, APIs, or transcription. Choose free/local methods; record inaccessible sources as coverage gaps. No automatic paid overages.
- Confirmed: initial source trial and release use English only across Canada and Washington State. Record other-language coverage gaps.
- Pending: organization-category exclusions and size thresholds; broad eligibility and no revenue cutoff are proposals only.
- Confirmed: organization-based searchable dashboard with new/changed, organization profile, and coverage views; a weekly shortlist without a forced quota; separate evidence-quality and relevance judgments.
- Pending: collection frequency, shortlist size, ranking rules, and weekly human review capacity. Trial feedback will set these.
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

## First technical slice, provisional
A synthetic end-to-end example plus a small approved live-source set should demonstrate more than funding joins: source evidence becomes a dated organization finding in a review queue. The exact mix of official records and local/media material is selected after feasibility and human review.

Do not implement nationwide collection simply to satisfy the geographic ambition. Expand coverage visibly without claiming unimplemented locations are monitored.

## Deferred decisions
Stack, interface implementation details, hosting, collection scheduling, runtime AI, free/local source access and transcription feasibility, refresh windows, numeric quality targets, and milestone effort are decided from the PRD and trial. No client donor-analysis or outreach capability is planned.
