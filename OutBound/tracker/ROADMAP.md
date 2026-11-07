# Development roadmap
Status: Days 1–5 merged; main contains de4c852 at merge eb295bb. Day 6 local live runner and recovery proofs are on this review branch. Native Mac scheduler registration is blocked; scheduled execution and owner usefulness remain unproven.
Updated: 2026-11-05 (Vancouver), source-review completion

[PROJECT_PLAN.md](../frameworks/PROJECT_PLAN.md) defines the current seven-project-day path to a daily prospect worklist, starting from the bounded live prototype. The older design and synthetic-first sequence below records the completed foundation and deferred capabilities; it is not the current delivery schedule. [PRD.md](../frameworks/PRD.md) holds the open-product-decision register. Day numbers are planning targets, not dated commitments. There are no approved numerical quality targets or source/organization quotas.

## Progress against the seven-day plan

| Milestone | Evidence and remaining work |
| --- | --- |
| 1. Account visibility | Merged in PR #3. Known accounts remain visible with separate eligibility and commercial status. |
| 2. Incremental collection | Merged in PR #4. Live registry and announcement collection found 31 new candidates. Checkpoints and duplicate control demonstrated. Geographic and source breadth remain limited. |
| 3. Account and event resolution | Merged in PR #5. The [worklist](../evidence/day-3/worklist.md) reconciles 35 items to 34 accounts. Two identity questions remain. |
| 4. Candidate signals | Merged in PR #6. The automated backfill added two accounts and two historical awards. A [supervised non-award pass](../evidence/day-4/pressure-report.md) searched 39 existing accounts, producing six observations across four accounts and one investigation candidate. Recurring collection of these sources and broad category coverage remain open. |
| 5. Reviewed worklist | Merged in PR #7. [Reviewed worklist](../evidence/day-5/worklist.md): six original non-award observations checked, two qualified Surrey follow-ups, four unique account cards. Act 0, Investigate 1, Monitor 3, Suppress 0. [Review packets, tests and private feedback persistence](../evidence/day-5/README.md). Same-assistant review and unresolved current-status/identity checks remain explicit. |
| 6. Daily execution | [Live runner and proofs](../evidence/day-6/README.md): Initial collection: 57 endpoints, 0 new accounts, 5 new candidates. [Source-reviewed daily gate](../evidence/day-6/source-review/README.md): nine flags reviewed across seven documents, owner attention 6 → 0; live repeat reuses nine verdicts, with 0 new/changed candidates and no duplicates. Two claim questions plus four blocked/held source checks remain internal. Controlled failure and live 304 recovery preserve checkpoints. Private feedback is reused only for unchanged evidence. **Partial delivery:** native scheduler registration is blocked; app fallback registered with future Mac binding unverified. |
| 7. Operating trial | Run on separate days, measure actual yield and review effort, and record owner usefulness feedback. |

Next acceptance checks: resolve native Mac scheduler registration and observe an actual later scheduled execution. Clear pending candidate/source checks through the supervised review handoff. Separate-day yield and owner usefulness remain Day 7 evidence; a saved replay or manual run does not establish them.

## Day 2 results and Day 3 handoff

| Source | New candidate accounts | Items for previously known accounts |
| --- | ---: | ---: |
| CRA charity identification file (2024) | 4 | 1 |
| IRS exempt-organization data | 5 | 2 |
| Seattle Food Equity Fund announcement | 22 | 1 |
| Total | 31 | 4 |

The [first run](../evidence/day-2/first-run.md) produced 35 evidence items. Registry rows identify organizations as of the source period. The Seattle announcement identifies individual award recipients. The [immediate repeat](../evidence/day-2/second-run.md) added zero accounts, items or revisions. Daily discovery yield across separate dates remains unmeasured.

Day 3 takes these 35 items through batch identity matching and event grouping. Preserve the discovery source per account, registry-only accounts, and each recipient's relationship to its award. Produce one account worklist, a separate queue for ambiguous matches, and reconciliation back to every input. Greater Vancouver Food Bank Society stays visible with current registration marked unchecked.

## Foundation history

Development occurs in bounded increments in Codex. The repository preserves code, logic, product role definitions, data contracts, tests, and factual outcomes so Claude Code can later continue the work. No model installation, provider adapter, or hardware test is a prerequisite. See [WORKFLOW_EVALUATION.md](../frameworks/WORKFLOW_EVALUATION.md).

| Stage | Outcome | Evidence |
| --- | --- | --- |
| 1. Synthetic foundation | Collection to stored evidence, expanding organization/source registers, all four checkpoints, and report. | Fresh-checkout run, structured records, failure handling, known-answer tests, and actual outputs. |
| 2. Bounded live increment | Permitted sources in Canada and Washington feed the same flow. | Source register, original evidence, coverage gaps, source checks, and owner feedback. |
| 3. Refinement | Correct missed context, identity, duplicates, and role failures. | Changed rules/contracts, regression tests, and observed improvements or unresolved failures. |
| 4. Daily operation | Scheduling, checkpoints, catch-up, and visible failures. | Interrupted/missed-run tests and an actual operational run; unattended reasoning assessed separately. |
| 5. Expansion and submission | Broader demonstrated coverage and inspectable working history. | Measured coverage/quality, documented limits, honest external program disclosure. |

Stages do not imply dates, ticket counts, paid hours, or program approval. Owner feedback accompanies every increment. A broad manual source study is not required before implementing the bounded foundation.

## Accepted design and immediate scope
D046-D052 record accepted Day 1 design choices: Python + SQLite, JSON/JSONL interchange, Markdown report first, a minimal complete synthetic flow, explicit approval blockers, actual context-separation evidence, and dependency-based rechecks. Reversible merges, detailed funding relationships, HTML, and dashboard work are deferred. Suspected duplicates remain linked and unresolved without destructive merging.

Design acceptance does not authorize implementation or tests. Bounded synthetic implementation requires separate owner instruction. Live collection remains a separate gate, preceded by named candidate publications/datasets/endpoints with selection reasons and explicit verification/access states. Day 1 establishes no live feasibility, role accuracy, or usefulness result.

## Incremental implementation
Source feasibility, a bounded working implementation, technical QC, and owner review form repeated activities within small increments. A nationwide research exercise is not a prerequisite to all coding.

[FOUNDATION_SPEC.md](../frameworks/FOUNDATION_SPEC.md) describes the limited initial scope. The repository contains requirements, code, research logic, and analysis; it does not issue assignments to coding assistants. Execution instructions are supplied by the owner in chat.


## Current scope decisions and pending proposals
- Confirmed: zero additional monetary operating cost, with no paid subscriptions, source access, hosting, APIs, or transcription. Choose free/local methods; record inaccessible sources as coverage gaps. No automatic paid overages.
- Confirmed: deterministic data handling and separate coding-session research roles. Codex runs the initial workflow; Claude Code can later continue from the repository. No new paid runtime service is introduced.
- Confirmed: initial source trial and release use English only across Canada and Washington State. Record other-language coverage gaps.
- Confirmed: service-delivery nonprofits; foundations and umbrella bodies as potential buyers/routes; no revenue cutoff. Hospitals, universities, religious organizations, and advocacy groups remain undecided.
- Confirmed: BC/Washington first live sample, prioritizing local reporting, organization publications, and official/funder records. The overall geography remains Canada and Washington.
- Confirmed: first delivery is Day 1 design only, returning proposed technical design, record formats, source sample, and test matrix for owner review before separately authorized implementation.
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

## First technical slice, conditional on Day 1 design review and implementation approval
The first implementation is a bounded synthetic end-to-end example demonstrating evidence becoming a dated organization finding in a review queue, with both expanding registers and all four checkpoints. Source inspection and bounded live collection belong to a separately authorized later gate. Identity resolution and funding joins can be limited or unresolved in this first slice; the complete funding map and official-data adapters are later increments. Explicitly report routes not yet investigated versus none found after investigation.

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
Maintain [DEVELOPMENT_FEEDBACK.md](DEVELOPMENT_FEEDBACK.md) alongside implementation: owner-provided product feedback, changed requirement or implementation, related commits, actual verification evidence, and unresolved factual limits. Execution prompts and assistant review judgments remain in owner chat. Link code changes and checks. Preserve unresolved and unsuccessful outcomes where material. Update the record during work rather than reconstructing an invented history. Private or restricted material stays outside the public log.

## Researcher, skeptic, and fact-checker workflow
The initial implementation follows [RESEARCH_WORKFLOW.md](../frameworks/RESEARCH_WORKFLOW.md): researcher report and full claim ledger, constructive skeptic's ranked issues, comprehensive source fact-checking, then a report with individual verification flags and unresolved problems. Collection and QC remain separate. Findings, organization additions, and source additions all pass collection/separate data QC, researcher, skeptic, and fact-checker checkpoints. Both discovery directions and changed-record rechecks are acceptance cases. Every number, quote, and paraphrase must be checked; a skeptic's silence is not approval.

Implement distinct versioned outputs and actors for each review stage. Coding-session role execution is authorized; deterministic checks and owner judgment remain separate. Model labels must not impersonate independent human verification. Test faulty numbers, altered quotes, misleading paraphrases, source access failures, and invalidated approvals. Technical code QC remains separate from evidence review and owner relevance judgments.


## Deferred decisions
Detailed schema/runtime contracts, later interface implementation details, hosting, collection scheduling, free/local source access and transcription feasibility, source refresh frequency and historical comparison periods, numeric quality targets, and milestone effort are decided from the PRD and trial. No client donor-analysis or outreach capability is planned.

## Source-review completion, 5 November 2026 Vancouver

The desktop workflow now reads originals before owner publication and returns version-bound structured factual and commercial verdicts. Python validates all required claims, locators, periods and commercial gates atomically. Relevant/cited passage changes reopen affected claims; unchanged evidence preserves decisions and review dates. Collection-only or inaccessible-review fallback publishes dated collection status and the last reviewed worklist. The original checkout and private owner journal remain preserved. See [first batch, real repeat and test evidence](../evidence/day-6/source-review/README.md). Scheduled app instructions were updated; later scheduled Mac execution remains unproven.

## Issue #9: historical BC population screen

Deterministic screen and one-to-one filing join implemented. Historical 754 size-fit / 414 enrichment reproduce. After D062 rules and D065 owner review: 551 size-fit / 345 enrichment; 4,168 category exclusions; 6,976 remainder. [Reconciliation, rules and input hashes](../evidence/population-screen/README.md). All 12,040 rows have a reason. D065 resolves all 32 category clues: PLAN excluded using CRA ID 131516320RR0001; PACE, CYAC Kelowna and PeaceGeeks retained as service delivery; 28 out-of-band records batch-resolved as moot and held from admission. Moot records reopen if a later screen brings them in-band. Pending category reviews: zero. No current buyer-eligibility or donor-base qualification is claimed. Geography/form cut remains the next downstream population step; current eligibility, donor-base and live-trigger gates still apply. PACE operating status remains a downstream current-status check.

## Canonical geography and form routing

D060/D066 applied to all 896 retained historical records. [Reconciliation](../evidence/canonical-geography/README.md): Pool A 323 (231 size-fit, 92 staffing-enrichment); corridor foundations 168; remote operating organizations 364; remote foundations 41. Zero unresolved geography/form checks. Delta, Mission and White Rock explicitly included by owner decision D066. Original locality is preserved beside canonical routing area; no current operating-location verification or travel-time claim. Foundation designations A/B remain separate from operating organizations C. Prior D065 dispositions and holds are preserved. The next operating-plan step is a bounded trigger-screen batch from Pool A, with current status and donor-base evidence still required before qualification.
