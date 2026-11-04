# Tributary project plan
Recorded: 2026-11-03
Owner: Deepak Gupta
Status: Day 1 design decisions and refinements accepted and recorded. Implementation has not been authorized through this planning conversation.
Start date: Unset. Days 1-7 are project days, not dated commitments.

## Document roles
This plan defines the beginning, first seven project days, ongoing cycle, expected deliverables, and reconciliation. [PRD.md](PRD.md) defines product scope and is the single register of open product decisions. [RESEARCH_WORKFLOW.md](RESEARCH_WORKFLOW.md) defines the four checkpoints for findings and both registers. [SOURCES.md](SOURCES.md) defines source admission and coverage. [FOUNDATION_SPEC.md](FOUNDATION_SPEC.md) defines foundation acceptance evidence; [WORKFLOW_EVALUATION.md](WORKFLOW_EVALUATION.md) distinguishes software checks from actual role quality, live feasibility, and owner usefulness. [ROADMAP.md](ROADMAP.md) provides the longer-term engineering stages.

There are no approved numerical accuracy targets, source quotas, organization quotas, weekly shortlist quotas, throughput promises, or effort estimates. Counts are observations unless the owner approves a target separately. Requirements such as checking every number, quote, and paraphrase remain applicable. No target date can turn an incomplete check into a pass.

## Confirmed starting decisions
- Initial eligibility: service-delivery nonprofits, with foundations and umbrella bodies as potential buyers or organizational routes in. No revenue cutoff.
- Hospitals, universities, religious organizations, and advocacy groups remain undecided. They are not silently included or permanently excluded; candidates in these categories remain pending an owner decision.
- First live sample: British Columbia and Washington State, prioritizing local reporting, organization publications, and official/funder records. Full product geography remains Canada and Washington; the bounded sample does not narrow that ambition.
- Initial delivery boundary: Day 1 design proposal only, comprising documentation inspection, proposed technical design, record formats, initial source sample, and test matrix. Owner review precedes any implementation. Approval of these starting decisions does not itself launch work or authorize implementation.

## Accepted Day 1 design and execution boundary
Day 1 design is complete. D046-D052 record the accepted choices and refinements: Python + SQLite, JSON/JSONL interchange, Markdown-first output, a minimum schema organized into six logical groups, explicit required-versus-optional approval criteria, actual context-separation evidence, and dependency-based rechecks. Reversible merges, detailed funding relationships, HTML, and dashboard work are deferred from the first synthetic build.

Implementation and tests still require separate owner authorization. Any next implementation authorization is for the bounded synthetic flow unless live work is separately authorized. Before live collection, the source proposal must name candidate publications, datasets, and exact endpoints with selection reasons and explicit verification states. No source quota is introduced. No live-source feasibility, role accuracy, or product usefulness result is established by design acceptance.

## Part 1: Beginning and baseline

### Purpose, scope, and expectations
The product supports nonprofit prospect discovery and documented organizational routes in across Canada and Washington State, using English-language, freely accessible material. It investigates pressure and opportunity, including indirect signals, with observations, attributed statements, hypotheses, alternative explanations, and unknowns kept distinct.

The organization and source universes are incomplete at launch and expand in both directions: sources reveal organizations; organization research reveals sources. Being registered is not evidence of being a commercially qualified prospect. The owner can spend multiple hours reviewing output. Coverage gaps and investigation backlogs remain visible.

Discovery uses a 12-month window, recent-six-month priority only when evidence and relevance are comparable, and older records for comparison. Daily collection/candidate discovery is the intended cadence; a weekly shortlist is a separate review view. No unattended operation is claimed before implementation and operational testing.

Cost is zero additional monetary operating cost. Permanent live content is limited to metadata/checksums and permitted sanitized excerpts, not whole articles, recordings, or transcripts. Private pursuit and relevance judgments remain outside the public repository. Outreach, client donor analysis, campaign delivery, model training, and fine-tuning are outside scope.

### Expected deliverables
| Deliverable | Required content | Acceptance evidence |
| --- | --- | --- |
| Consistent baseline | Product scope, decisions, deliverables, QC, testing, dependencies, exclusions, and open choices. | Cross-document consistency and an explicit owner approval state. |
| Organization register | Stable IDs, identity evidence, geography, aliases/official IDs where available, discovery provenance, admission status, review versions, and next action. | New/duplicate/ambiguous identity cases and versioned admission checks. |
| Source register | Publisher/endpoint, coverage, access and retention handling, discovery provenance, admission status, operating state, and next action. | Candidate inspection and four-check admission records; blocked sources stay visible. |
| Evidence and claim records | Dates, permitted passages, locators, organization/source links, duplicate grouping, uncertainties, and versions. | Traceability, exact known-answer cases, reruns, and visible incomplete evidence. |
| Role outputs and report | Research report, skeptic issues, complete claim checks, corrections, residual problems, and verification basis. | Full chain linked to actual reviewed inputs; unperformed checks cannot inherit approval. |
| Audits and coverage | Collection dispositions, review queues, register additions, source attempts/successes, geographic/source-type gaps, and reconciliations. | Accounted populations and explicit discrepancy records. |
| Development evidence | Actual changes, relevant checks/results, owner-provided product feedback, unresolved defects, and factual release records. | Links to actual artifacts and commits; no invented owner reasoning or assistant review commentary. |

These are delivered incrementally. Nationwide coverage, a polished dashboard, complete funding graph, scheduling, all adapters, and audio transcription are not first-week completion promises.

### QC and verification
The same four checkpoints apply to news/evidence findings, organization additions, and source additions:
1. Collection and data QC. Collection proposes records; a separate QC responsibility checks extraction, identity, dates, completeness, and duplicates. The collector cannot approve its own output.
2. Researcher. Evidence-backed details, relevance to scope, cross-checks, hypotheses, and unknowns.
3. Skeptic. Constructive ranked objections, alternative explanations, and evidence needed.
4. Fact-checker. Original-document checks for every number, quote, paraphrase, and required admission detail, including unflagged claims; disposition of every skeptic issue.

Each checkpoint has its own versioned result and actor/run identity; execution completion is separate from passing review. A skeptic question alone does not fail a record. Material unresolved required details block approval, while optional missing information and documented nonmaterial limitations may remain visible without blocking approval. Actual context separation is recorded; separate IDs/files do not prove isolation. Same-model reviews do not establish independent corroboration. Owner commercial usefulness is separate from all four checks. An unchanged approved record is not fully re-reviewed daily; a material change reopens affected checks before a revised version can replace an approval.

### Testing and acceptance
| Evidence category | Required cases or observations | What a pass establishes |
| --- | --- | --- |
| Synthetic software checks | Source and organization duplicates, ambiguous identity, unknown/malformed dates, missing evidence, admission bypass, changed versions, omitted claim checks, repeated runs, partial failure, and reconciled counts. | Specified software behavior for fixtures, not live access or model reasoning. |
| Actual role evaluation | Planted numeric errors, altered quotations, misleading paraphrases, missing qualifications, benign explanations, and non-independent corroboration. Expected answers are separate from reviewed inputs. | Observed errors caught/missed and false verification, with denominators; no unapproved accuracy target. |
| Bounded live trial | Permitted Canadian and Washington source material through the same pipeline; both organization-to-source and source-to-organization discovery. | Feasibility and extraction/review results for inspected material only. |
| Owner usefulness review | Actual reports examined for relevant context, missing evidence, misleading implications, and practical investigation value. | Owner-provided feedback, not an assistant-invented relevance rating. |
| Operational testing, later | Missed/interrupted runs, checkpoints, catch-up, idempotence, partial source failures, and host unavailability. | Demonstrated scheduling/recovery behavior, not continuous availability. |

Gate A is the synthetic foundation. Gate B is the bounded live flow. Owner usefulness and daily operation are additional distinct outcomes. Every outcome is passed, incomplete, failed, or explicitly deferred with evidence. A calendar milestone or fixture replay cannot substitute for missing live or owner evidence.

### Responsibilities and beginning checkpoint
The planning conversation reviews and updates product documentation and reports its judgments to the owner in chat. The owner separately instructs repository-connected Codex to implement and run tests, assesses usefulness, and approves scope changes. Codex implementation artifacts are evaluated from actual results. Claude Code may later continue from the same repository; private data access is separate.

The starting eligibility, BC/Washington pilot, and design-only first delivery are owner-confirmed. The beginning checkpoint is a consistent documentation baseline with remaining open decisions identified and no fabricated targets or source counts. Day 1 returns a design proposal for owner review before implementation. Approval of this plan does not itself launch work or authorize implementation. Source-specific access/handling is required before live material is collected.

## Part 2: First seven project days
This is a dependency-based planning target. Day 1 starts with the owner's design-assignment instruction; start date and availability remain unset. Days 2-7 remain conditional planning targets and cannot begin implementation until the owner reviews the Day 1 proposal and separately authorizes it. If a dependency fails, the affected outcome remains incomplete and is carried forward with a reason. It is not replaced by an invented pass or a weaker unrecorded requirement.

| Day | Planned outcome | Expected deliverables and completion evidence | Dependency |
| --- | --- | --- | --- |
| 1 | Design proposal only, returned for owner review before implementation. | Documentation inspection, proposed technical design, record formats, proposed BC/Washington source sample and coverage rationale, test matrix, and remaining design decisions. No preset source/organization count. | Owner instruction to begin the design assignment. No implementation or test execution is part of this stage. |
| 2 | Synthetic collection and persistent evidence foundation. | Source/organization references, storage/provenance, identity uncertainty, duplicate handling, reconciled dispositions, and reruns without multiplying records. | Owner review of Day 1 proposal, separate implementation authorization, agreed contracts, and synthetic fixtures. |
| 3 | Expanding registers and admission flow. | Both discovery directions demonstrated; candidate queues, four-check admission records, duplicate links/unresolved matches and exclusions, changed-version rechecks, and coverage reporting. | Day 2 storage and identifiers. |
| 4 | Complete research-to-report flow. | Separate researcher, skeptic, and fact-checker inputs/outputs; source locators, claim checks, residual problems, and a reviewable report. Actual role outputs are distinct from fixture replay. | Evidence storage and versioned review/admission logic. |
| 5 | Bounded live collection through the same flow. | Permitted Canadian and Washington source material, actual findings/candidate additions, access/QC results, and explicit gaps. If blocked, Gate B remains incomplete. | Separate live-collection authorization, concrete candidate endpoints, source access/retention decisions, and a working synthetic flow. |
| 6 | Owner review and corrections. | Actual owner feedback; resulting product/code changes; relevant regression evidence; unresolved defects. No invented review if owner input is unavailable. | Inspectable outputs and owner availability. |
| 7 | Reconciled week-one close and next increment. | Planned-versus-delivered register, data/queue reconciliation, acceptance outcomes, actual checks, limitations, carryovers, and a proposed next-week backlog. | Actual evidence from completed work; blocked outcomes remain visible. |

### Week-one target
A working, inspectable bounded flow supports collection, stored evidence, both expanding registers, all four checkpoints, and a reviewable report. Synthetic, live, role-quality, and owner-usefulness outcomes are reported separately. The first live sample tests the workflow without implying complete geographic coverage.

### Daily and weekly reconciliation
Delivery records contain commitment ID, planned deliverable, acceptance evidence reference, actual outcome, blocked/deferred reason, dependency, and next action. Daily states are completed with evidence, in progress, blocked, or carried forward with reason. Week-end closure identifies the actual evidence for each completed commitment; changed scope has an owner decision reference.

Data accounting uses defined populations and stages:
- At ingestion, input items equal unique evidence items plus duplicate items plus rejected/quarantined items. These dispositions are mutually exclusive for that ingestion stage.
- For each organization/source candidate population, opening pending plus new candidates plus reopened versions equals admitted plus merged plus excluded/blocked plus closing pending. Each candidate/version has one closing disposition; prior admitted records are not repeatedly counted as new admissions. A blocked record reopened later enters that later period's opening/reopened population.
- Register stock changes are separate from candidate admission flows: opening admitted/active records plus new admissions/reactivations minus merges, exclusions, or inactivations equal closing admitted/active records. Every transition references its record/version; an unchanged record does not count as new growth.
- Attempt counts are separate from distinct-source counts. Retries do not inflate the source universe or count as extra successful source coverage.
- For every checkpoint, reviewed versions have passed, limited/incomplete, failed, or pending outcomes with reasons; the admission decision cannot bypass a required pass.
- Claim ledgers account for every number, quote, and paraphrase. Checked claims reconcile by verification status; pending checks remain in the denominator. Skeptic issues reconcile to corrected, supported as written, limitation retained, or unresolved.
- Discrepancies are visible failed reconciliation checks, with affected records identified. A clean total cannot hide a source access failure, stale review, unsupported claim, or missing usefulness review.

Reconciliation counts describe the actual run/period. They are not growth quotas, quality targets, or claims of completeness across all nonprofits.

## Part 3: Week two onward
Week two begins at project day 8 and continues through evidence-based increments. Incomplete week-one work remains visible and takes priority where it blocks the core flow.

| Frequency | Activity | Evidence retained |
| --- | --- | --- |
| Daily research cycle | Collection from approved sources; source and organization candidate discovery; four-check queue processing; changed-record review; per-source failure reporting. Initially owner-initiated where unattended execution is unproven. | Run audit, candidate/admission dispositions, source attempts/successes, pending reviews, and last successful checkpoints. |
| Weekly owner review | Organization reports, missed context, weak reasoning, irrelevant findings, and investigation usefulness. | Actual feedback, changes, verification evidence, and unresolved concerns; commercial judgments remain private. |
| Weekly expansion | Prioritized geography/source-type gaps, discovered connections, candidate inspection, and admission through all checks. | Demonstrated coverage added, blocked sources, rejected/merged candidates, and next expansion priorities. |
| Weekly delivery reconciliation | Commitments, data/queue balances, acceptance outcomes, defects, review backlog, and carried work. | Factual weekly completion report and the next seven-day plan, based on actual capacity and dependencies. |
| Engineering increments | Scheduling/recovery, dashboard, funding relationships, better matching/deduplication, adapters, and feedback-driven refinement. | Feature-specific checks, observed operating behavior, regression evidence, and owner decisions. |

Expansion batches have continuation points so research does not become an unbounded recursive crawl. Batch sizes, priority weights, backlog limits, and refresh intervals remain open. Geographic and source-type gaps stay visible; existing concentrations must not be mistaken for full coverage. Register growth alone is not success.

Daily scheduling is adopted only after its checkpoints, catch-up, failure handling, and actual operational run have been demonstrated. Source access limits and free-only operation still apply. Weekly reporting continues even when no useful findings are produced.

## Open decisions and change control
The authoritative open-decision register is the Open decisions section in PRD.md. Starting organization eligibility, no revenue cutoff, BC/Washington pilot geography, priority source types, and the Day 1 design-only review boundary are confirmed. Specific source endpoints, undecided organization categories, detailed schema/runtime contracts and actual role-context separation, numerical quality thresholds, ranking/expansion rules, scheduling mechanism/time, source-specific permissions, and start date remain unresolved.

Decisions affecting Gate A, Gate B, weekly prioritization, or later operation are identified by their dependency rather than all being treated as day-zero blockers. Approved changes update the affected product documents and factual decision history together. Execution prompts, assistant-to-assistant handoffs, assistant review judgments, private prospect decisions, and unaided program ratings are not part of this plan.
