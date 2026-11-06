# Tributary product requirements
Status: Bounded live prototype and Day 1 account worklist complete; seven-day daily-worklist plan is the current delivery schedule
Owner: Deepak Gupta
Updated: 2026-11-06

## Purpose and user
Tributary supports nonprofit business development for Autonomy Bridge. Its sole product goal is to find potential clients and credible organizational routes to reach them. Deepak reviews evidence and makes commercial decisions privately. The week-one product is an account-centered event monitor, not a buyer-intent prediction system.

The product must produce four daily outputs:

1. Newly discovered nonprofit accounts.
2. New events associated with known accounts.
3. Evidence-backed commercial hypotheses.
4. A short action queue for investigation or outbound preparation.

The initial geographic scope is all of Canada and Washington State. Oregon and California are future possibilities, not initial requirements. Collection can be introduced in stages, but coverage gaps must remain visible.

## Current outbound target: mid-sized BC nonprofits

The active outbound market is BC nonprofits with roughly $1M–$5M in annual revenue and 10–50 paid staff, with at least one live trigger below. Working interpretation for the BC pilot: CAD, latest available annual revenue, and paid headcount. Record fiscal year, currency, staff measurement basis, date and source. Label FTE or full-time-only figures explicitly. Approximate bands guide fit; missing or borderline size evidence goes to research. The wider discovery register can retain organizations outside this target.

**Working pitch (D059, 2026-11-06).** The pitch used in BC conversations is the tight pitch: help nonprofits raise more money from their existing donors, and fine-tune how they do that using analytics and systems. This supersedes the website's operational-leadership framing for outbound use; revising the website is a separate owner decision, not yet made. Buyer order under this pitch: development/fundraising lead first, Executive Director second.

**Donor-base gate (2026-11-06).** Applied after size fit and before trigger assessment. From the T3010 revenue mix, tax-receipted gifts and fundraising revenue must be a material share of revenue — the account must have an existing-donor base to work with. An organization funded predominantly by government contracts or fees goes to Monitor regardless of size fit. Record the revenue mix on the account: tax-receipted gifts, total gifts, fundraising revenue, government revenue, total revenue, fiscal year, and source.

| Live trigger | Evidence needed for a qualified account |
| --- | --- |
| A funder or supporter wants to do more | A specific expression of interest in expanding support, a decision deadline, and a need for a feasible delivery outline, reliable costs and evidence of impact. Record what decision the material will support. |
| A funded commitment or partnership is stalling | Evidence of an existing funded obligation, a delayed or blocked milestone, and the dependency between programs, finance or development that is holding up delivery. Record what is due and who needs to act. |
| Leadership transition, leave or growth puts delivery at risk | Evidence of the transition, leave or expansion plus a specific delivery obligation at risk during that window. Record the responsibility, timing and evidence of the capacity gap. |

**Donor-side triggers (added 2026-11-06).** Same evidence standard as the triggers above and [BC_TRIGGER_SCREEN.md](BC_TRIGGER_SCREEN.md) — an anchor, a corroborating clue on the same initiative, and a still-open decision window:

- **Donor revenue trend:** tax-receipted gifts flat or declining across consecutive T3010 filings while programs or costs grow.
- **Open campaign window:** a dated donor decision point is approaching — GivingTuesday (December 1, 2026), a year-end appeal, or a seasonal campaign — with preparation work still open.
- **Donor-program systems signal:** an active monthly-donor or lapsed-donor program, a development hire posted, or a CRM/donor-database change, indicating donor-data work underway without evidence of segmentation or follow-through analysis.

The first trigger in the table (a funder or supporter wants to do more) is already a donor-side trigger and is unchanged. The second and third table triggers remain Investigate signals; under the tight pitch they qualify an account for outbound preparation only when the at-risk decision is a donor-revenue decision, recorded explicitly.

For outbound qualification, record size fit and trigger status separately. For each trigger retain the dated source, what remains open, deadline or next milestone where known, and last status check. A grant announcement, ED vacancy, generic appeal or growth figure alone is a research lead. Keep plausible leads with missing evidence in Investigate; keep size-fit accounts without a live trigger in Monitor. A qualified account is eligible for private outbound preparation; the owner decides whether to contact it.

## Decisions the product supports
- Which nonprofits show evidence of needs relevant to operational leadership, fundraising support, or better use of data in campaigns and existing-supporter engagement?
- Which funders or intermediaries sponsor outside operational or capacity-building support?
- What documented funding or organizational relationships offer a plausible route in?
- What changed, how reliable is the evidence, and what needs investigation before deciding to pursue an organization?
- Which items require action now, further investigation, continued monitoring, or suppression as duplicates/irrelevant records?

Client delivery, donor analysis, campaign execution, and outreach are outside this product's scope.

## Project baseline and delivery
[PROJECT_PLAN.md](PROJECT_PLAN.md) defines the current seven-project-day path from the bounded live prototype to a daily prospect worklist. [BC_CONVERSATION_PLAN.md](BC_CONVERSATION_PLAN.md) is the operating plan for BC outbound — objective, execution steps, and owner decisions — distinct from that build schedule. The earlier Day 1 design and synthetic/live foundation milestones are historical. The current schedule has no calendar start date; completion depends on fresh operational results, not elapsed days.

The documented design basis is [SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md](../research/SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md). The immediate build deliberately implements a usable subset of those practices. It does not claim predictive buyer intent, national-scale crawling, automated outreach, or trained ranking.

No numerical quality targets, source quotas, organization quotas, throughput targets, or forced shortlist count have been approved. Expected source/organization growth is measured, not promised. Product open choices are listed only in this document's Open decisions section; other documents refer here.
## Confirmed starting decisions
- Initial eligibility: service-delivery nonprofits, with foundations and umbrella bodies as potential buyers or organizational routes in. No revenue cutoff.
- Hospitals, universities, religious organizations, and advocacy groups: decided 2026-11-06 (D062) — excluded as buyers for the BC pilot; hospital foundations remain eligible as separate entities. Each exclusion is reversible by a new dated decision entry.
- First live sample: British Columbia and Washington State, prioritizing local reporting, organization publications, and official/funder records. Full product geography remains Canada and Washington; the bounded sample does not narrow that ambition.
- Day 1 delivery: a batch account worklist that separates discovery, identity, eligibility, signal review, and private business relevance. Greater Vancouver Food Bank Society is a valid in-scope account and must be included; an older CRA filing may provide historical context but does not negate current registry status.
- Account admission is independent of whether the account has a recent actionable signal. Weak or unknown commercial evidence leaves the account available for monitoring.

## Accepted foundation design
Accepted choices are recorded in D046-D052 and detailed in FOUNDATION_SPEC.md and RESEARCH_WORKFLOW.md:
- Python + SQLite; JSON/JSONL interchange; Markdown report before dashboard.
- Minimum schema supporting the complete synthetic flow; six logical record groups, not mandatory separate subsystems.
- Review completion separate from passing review; material unresolved required details block approval, while optional omissions and nonmaterial limitations remain visible.
- Separate collection/QC executions and role packets, with actual context separation and shared-assistant limits recorded.
- Dependency-based rechecks after material changes.
- Named candidate publications, datasets, and exact endpoints with selection reasons before live collection; no unperformed verification implied.

The bounded foundation and Day 1 worklist are implemented and tested. Live collection still has a source-specific access and handling gate. No unattended-operation or owner-usefulness result is established by software tests alone.

## Operating model and data boundaries
The processing stages remain separate:

| Stage | Required result |
| --- | --- |
| Source collection | A retrieved document or official record with provenance and retrieval status. |
| Account resolution | A definite, possible, or rejected association with a stable account. |
| Event resolution | The underlying occurrence, grouped across duplicate or corroborating documents. |
| Signal assessment | A supported explanation of why the event may matter, with uncertainty and unknowns. |
| Action queue | An operational tier and concrete next step. |
| Human feedback | A dated decision and reason that can improve explicit rules without implying model training. |

The core records are `account`, `source_document`, `event`, `account_event`, `signal_assessment`, and `action_item`. Stable identifiers, append-only observations, versioned rules, source checkpoints, content hashes, and separate event/publication/retrieval dates are required architectural allowances.

Public news, filings, and organization updates can establish change, pressure, expansion, funding, leadership movement, and operating context. They usually do not establish consulting budget, purchasing authority, or willingness to engage. Those fields support explicit `unknown` values. Direct first-party behaviour, if available later under an approved handling policy, ranks above inferred public context.

## Discovery requirements
Discovery must cover both pressure and opportunity. Successful fundraising or expansion is not a prerequisite. Candidate signals include:
| Category | Evidence to investigate |
| --- | --- |
| Fundraising pressure | Reported donation declines, missed targets, funding loss, or explicit concerns about repeat giving and retention. |
| Campaign improvement | Comparable published campaign results, declining participation, or explicit gaps in segmentation, supporter re-engagement, and follow-through. |
| Financial pressure | Recurring deficits, reserve reductions, funding expiry, or financially driven service reductions. |
| Operational strain | Publicly reported demand/capacity imbalance, delivery delays, staffing gaps, and difficulty fulfilling commitments. |
| New commitments | Grants, partnerships, expansion, and funded programs with stated delivery requirements. |
| Sponsored support | Capacity-building programs, consulting eligibility, provider rosters, and funder-paid support. |

An active campaign does not establish poor performance. A deficit does not establish a donor-retention problem. A grant does not establish an unrestricted consulting budget. Financial pressure may reduce ability to engage.

Keep evidence of need, evidence of capacity to engage, and evidence of access separate. Unknown capacity or access must be visible, not treated as proof of absence or used to silently discard a finding or account.

Week-one extraction starts with observable event classes: new programs/services/geographies; material demand or usage increases; funding awards, losses, or campaigns; leadership changes; partnerships or major commitments; facility openings, closures, or relocations; hiring surges or critical vacancies; financial pressure or service reductions; technology/data/operational modernization; and public requests for vendors, proposals, or specialized support.

## Continuously expanding organization and source universes
The product begins with bounded seeds, not an assumed complete list of nonprofits or sources. Two discovery directions are required: a source reveals organizations, and research on an organization reveals sources. Each discovery has a stable record ID, first-seen date, discovery method, parent organization/source/evidence reference, last check, reviewed version, status, reason, and next action.

New organizations and sources enter candidate queues. Organization admission checks identity, geography, aliases, available official identifiers, and in-scope eligibility. Current official registry evidence establishes current registration status; historical filings provide financial and activity context for their stated periods. A stale filing does not invalidate a currently registered account. Source admission checks publisher/endpoint identity, coverage, sample utility, independence/syndication, access, formats/history, and permitted handling. Admission is separate from commercial qualification and signal priority. Unknown organization identity remains unresolved; an accessible URL does not prove source suitability.

Findings, organization additions, and source additions pass the applicable checkpoints in RESEARCH_WORKFLOW.md. Collection and data QC are separate responsibilities within the first checkpoint. Collection cannot approve its own proposals. Researcher, skeptic, and fact-checker maintain distinct versioned records. Account admission requires resolved identity, geography, and in-scope eligibility, not a recent event, consulting-budget evidence, or a passing commercial assessment. Source admission and finding verification retain their own required checks.

Organization states are candidate, identity unresolved, admitted, merged, or excluded with reason. Source states are candidate, inspected, approved for collection, blocked, merged, or inactive. These admission states are distinct from fetch status, event status, signal assessment, action tier, review status, and private business relevance. Missing optional information is explicit; unresolved identity or required eligibility prevents account admission. Source access/handling gaps prevent the affected source admission. Material verification gaps affect the finding or action tier, not an otherwise valid account.

A candidate source can receive bounded permitted inspection to establish its admission evidence; inspection is not approval for routine collection. On source admission, inspect available history within the agreed discovery window and then use incremental checks. Incomplete archives remain gaps. Material changes reopen affected checks; unchanged approved records do not require the full process daily.

Daily research includes candidate discovery and queue processing when execution is available. Bounded batches and continuation points prevent unbounded recursive research. Pending checks can carry across runs. Expansion priorities use geographic/source-type gaps, useful findings, and owner feedback; detailed batch sizes remain open. Coverage distinguishes intended, discovered, admitted, configured, attempted, and successfully checked populations. No percentage of all nonprofits is claimed without a defensible denominator.

Account resolution uses official identifiers first, then official domain, normalized name, city, and jurisdiction. Ambiguous associations enter a resolution queue. Name similarity alone cannot auto-merge accounts. Document deduplication starts with canonical URL and exact-content hash, then normalized headline, organization, event type, and close event dates. Multiple documents about one occurrence become one event with multiple evidence records and a manual merge/split path.

One document is an observation. Repeated related events can form an episode, and a material change from the account's own history is stronger than a generic keyword mention. Week one accumulates this history without claiming a baseline that does not yet exist.

## Execution and repository continuity
Codex is the initial execution environment. Collection, storage, deduplication, audits, research logic, role definitions, input/output contracts, evidence records, tests, and actual results belong to the repository or its documented private data store. Claude Code can later inspect and continue the same project through repository access. No provider adapter, API migration, local model installation, or hardware benchmark is required for this continuity.

Collection controls, identifiers, arithmetic checks, deduplication, reconciliation, checkpoints, and audits are deterministic. Researcher, skeptic, and fact-checker roles use separate versioned inputs and outputs. Coding-assistant reasoning remains probabilistic; same-assistant passes are not independent corroboration. Owner commercial review is separate.

Role evaluation compares actual outputs with independently specified expected answers and planted errors. See [WORKFLOW_EVALUATION.md](WORKFLOW_EVALUATION.md). Synthetic replay, coding-session role execution, and unattended operation are different capabilities and must be reported separately. Repository access alone does not schedule a daily run or grant access to private data.

No automatic model training or fine-tuning is included. External program eligibility remains unconfirmed; the actual workflow and business purpose must be disclosed honestly.

## Cost constraint
Confirmed: zero additional monetary operating cost. No paid subscriptions, paid source access, paid hosting, paid APIs, paid transcription, or other paid operating services. Use local execution or genuinely free services without automatic paid overages. Development must not introduce a paid runtime dependency.

Paywalled sources and recordings without a usable free transcript remain visible coverage gaps unless a permitted free alternative is available. Do not bypass access controls. A free tier's limits must be recorded; reaching them must pause or report the affected work rather than incur charges. Any future change to this constraint requires an explicit owner decision.

## Language scope
Confirmed: English only for the initial release and integrated source trial across Canada and Washington State. French and other languages are recorded as coverage gaps. Nationwide geography does not imply multilingual coverage. English reporting about organizations in any Canadian jurisdiction remains eligible.

## Discovery window and indirect signals
Confirmed on 2026-11-03: discover signals from the past 12 months. Give the most recent six months review priority when relevance and evidence are otherwise comparable; six months is not an exclusion cutoff. Keep older financial/funding records and earlier campaign periods for context and comparisons.

Assess event date, publication date, last status check, relevance, current status, and timing separately. A recent weak clue must not automatically outrank an older supported pattern. Before promoting older findings to the shortlist, check for updates; record ongoing, resolved, recurring, or current status unknown, with supporting evidence. No update does not prove continuation.

Do not depend on explicit admissions of fundraising difficulty. Investigate contextual observations in local reporting, interviews, podcasts, organizational publications, and records. Candidate observations include repeated campaign deadline extensions, comparable declines in participation, service-demand growth alongside flat donations, concentrated funding, and publicly described renewal/follow-up workload.

These observations are investigation prompts. Record the underlying facts, possible relevance, alternative explanations, missing evidence, and period comparability. A deadline extension may be routine; a campaign change may explain participation differences. Never convert an indirect clue into a factual claim of fundraising failure, donor-retention problems, consulting budget, or willingness to engage. Independent observations may strengthen a case; syndicated copies are not independent corroboration.

## Source breadth and coverage
Use official records together with city/community newspapers, provincial/state and regional media, local radio/TV, sector publications, podcasts, newsletters, organizational publications, and funder/community networks. Generic search is one discovery channel, not the coverage strategy.

Track coverage by province/territory or state, city/region, source type, language, and last successful check. Record unserved areas and access failures. Headquarters location and area served are distinct fields. Source feasibility is defined in [SOURCES.md](../research/SOURCES.md).

## Required information
Each finding must carry:
- Organization identity, country, available official identifier, location and area served.
- Source URL or durable reference, publisher, title, source type, publication date, retrieval date, event date when known, and reporting period where applicable.
- A permitted supporting passage, record reference, or audio timestamp, with original language recorded.
- Signal category, factual observation, possible relevance, uncertainty, and contradictory evidence.
- Any documented organizational route in, with its own evidence. A shared funder is a relationship clue, not a promised introduction.
- Duplicate-event grouping and links to supporting sources.
- Processing status and an explanation for uncertain identity matches or rejected records.

Amounts retain original currency and period. Missing dates, identifiers, amounts, and full text must be explicit. Do not invent them.

## Collection schedule
Confirmed: one daily local collection run when the host computer is available. The weekly shortlist remains a separate review view. This is a product requirement. Delivery status (Day 6: live daily command and app morning fallback registered; native Mac scheduler registration blocked and unverified) is maintained in [PROJECT_PLAN.md](PROJECT_PLAN.md), which is the single status source; this document does not restate it.

On startup or resume, identify missed daily runs and perform a catch-up collection from the last successful source checkpoint, within source availability and access limits. Do not claim complete recovery where feeds or archives no longer expose missed items. Avoid repeated full-history downloads; initial 12-month discovery/backfill and ongoing incremental collection are separate operations.

Record scheduled date, actual start/end, run status, per-source attempts, last success, and failures. A partial run must not advance failed sources' successful checkpoints. Reruns must not multiply records. Show missed runs and unrecoverable gaps in the coverage view. Respect free access limits and publisher conditions; daily scheduling does not override source restrictions.

Exact local run time, scheduler mechanism, and source-specific refresh exceptions remain implementation details to resolve before scheduling. Local execution cannot guarantee collection while the computer is off or asleep.

## Review experience
Confirmed design: a searchable dashboard organized around organizations, with a weekly shortlist as one view. Multiple stories about an organization remain visible as evidence without creating multiple prospect entries.

| View | Purpose |
| --- | --- |
| New and changed | New organizations, fresh evidence, and material updates to existing findings. |
| Organization profile | Signals, campaign history, funding relationships, contradictory evidence, and possible routes in, linked to source records. |
| Coverage and collection | Sources checked, failures, geographic/language gaps, and last successful updates; distinguish no findings from no coverage. |

The daily queue uses four operational tiers:

| Tier | Meaning | Treatment |
| --- | --- | --- |
| Act | Evidence supports a concrete next step. | Put on the daily outbound-preparation worklist. |
| Investigate | Potential relevance with one or more material gaps. | Put on the daily research queue with the missing evidence named. |
| Monitor | Valid account or event without current urgency. | Retain, continue incremental monitoring, and keep searchable. |
| Suppress | Duplicate, irrelevant, or demonstrably incorrect item. | Hide from active queues and retain the reason. Suppressing an item does not remove a valid account. |

Week one uses explicit sorting rules, not a universal numeric score. The account must be in scope, the event must be timely enough for its type, the evidence must directly support the event, the event must map to an Autonomy Bridge problem area, and the item must have a concrete investigation or outbound step. Independent evidence, recurrence, or a material change from the account's own history raises priority. Fit, evidence, freshness, and access remain separate components even if no combined score exists.

Filter by geography, signal category, and date. Each review card must answer:
- What happened: factual observation, event date, and publication date, with missing dates explicit.
- Why examine it: a specific connection to the intended services, labelled as interpretation.
- What supports it: direct evidence and access to its source.
- What remains unknown: including budget, internal causes, and whether the issue persists.
- What route exists: documented organizational connections, or "none identified."

The weekly shortlist contains new or materially changed organizations worth reviewing, with a visible reason for inclusion. There is no fixed quota that forces weak findings into the list. Wider findings remain searchable. Daily local collection is confirmed. Shortlist size, ranking rules, and source-specific access exceptions will be determined from the source trial and review workload. A weekly shortlist does not imply weekly collection.

Record two separate judgments:
| Judgment | Options |
| --- | --- |
| Evidence quality | Supported, insufficient, incorrect, duplicate, stale |
| Business relevance | Worth investigating, monitor, irrelevant |

Evidence quality applies to a finding and its version; relevance is recorded against the organization and the findings supporting that judgment. Leave unreviewed judgments explicit. Record the reason and date. New evidence must not silently overwrite prior feedback or imply that an old review covers changed evidence. A supported finding may be irrelevant; a potentially relevant organization may lack sufficient evidence.

Action tier is a third, operational judgment. It belongs to the current signal assessment/action item, carries a reason and next step, and can change without rewriting account identity or prior evidence-quality decisions.

Private pursuit decisions, relationship notes, outreach status, and actual business-relevance feedback stay outside the public repository and recorded development sessions. Public examples and session demonstrations use synthetic review records. The product may support private feedback without publishing it.

Feedback informs documented prompts, role instructions, collection/filtering rules, and review presentation. It does not authorize automatic learning, training, or fine-tuning.

## Human investigation requirement
Confirmed: human review is a core product activity. The owner can spend multiple hours investigating potential prospects; exact weekly allocation remains open. Do not impose a small review-time budget or use an arbitrary shortlist cap to discard potentially useful evidence.

Support deep investigation with permitted source context, original links, dated history, contradictory evidence, and explanations of why each candidate surfaced. Keep uncertain but potentially relevant findings accessible and clearly labelled. The weekly shortlist is an entry point, not the boundary of review. Preserve the distinction between unreviewed, uncertain, and rejected findings.

Use human feedback to refine documented collection and filtering rules. In the source trial, measure investigation time and usefulness without treating speed alone as success. Test whether evidence organization improves the owner's ability to assess a prospect, including plausible alternative explanations. Coding-session roles prepare research and review outputs; the owner manually examines results and makes commercial decisions.

## Development feedback record
Confirmed: record material owner feedback on assistant outputs and resulting development changes in [DEVELOPMENT_FEEDBACK.md](../tracker/DEVELOPMENT_FEEDBACK.md), linked to relevant commits, issues, checks, and pull requests. Record owner-provided or owner-approved product feedback, changed requirements/implementation, related commits, and actual validation evidence. Assistant judgments, review commentary, execution prompts, and instructions to other assistants remain in owner chat and are excluded from repository records.

This records how the owner steers development and improves role instructions. Coding-session role execution follows the current scope. Private prospect judgments and external program ratings remain separate. Any unaided ratings/reasoning are authored by the owner under applicable program rules.

## Researcher, skeptic, and fact-checker roles
Confirmed sequence: researcher -> skeptic -> fact-checker -> labelled evidence report -> owner investigation. Detailed role instructions and outputs are defined in [RESEARCH_WORKFLOW.md](RESEARCH_WORKFLOW.md).

| Role | Responsibility | Output |
| --- | --- | --- |
| Researcher | Use the required source types, separate observations/attributed statements from speculation, and cross-check consequential claims. | Evidence report, full claim ledger, source locators, coverage gaps, and collection audit. |
| Skeptic | Challenge evidence and logic constructively; identify alternatives without becoming a roadblock. | Short ranked issue list, referencing claims and needed evidence. |
| Fact-checker | Recheck every number, quote, and paraphrase against its original document, including unflagged claims; resolve or retain skeptic issues. | Versioned claim checks, corrections, verification flags, and residual issues. |
| Owner | Assess relevance and decide what to investigate or pursue. | Private commercial judgment, separate from factual checking. |

These are separate responsibilities with separate review records. The researcher cannot approve its own QC. The fact-checker receives the full report and claim ledger as well as the skeptic's list, so unchallenged errors do not escape review.

Keep collection completion, skeptic review, and claim verification separate. Only checked claims appear as verified; partially checked reports and unresolved material stay labelled and accessible. Verified source-faithfulness does not prove an attributed statement is independently true or a business hypothesis is established. New substantive evidence/claim versions invalidate affected approvals.

The three roles execute within the coding environment under owner direction. Unattended role execution is not established by a session run. Deterministic validators and owner review remain separate. Label model-generated checks as model checks, not independent human verification; keep pending or unresolved cases visible.


## Approved retention policy
Retain source metadata, checksums where available, and necessary permitted sanitized evidence excerpts. Do not permanently store whole live articles, audio, or transcripts. Full content may be processed transiently only where the source-specific access/handling decision permits it; exclude it from persistent caches, logs, tracked files, and error dumps. Record transient cleanup behavior and verify it.

Verification can revisit the original source. If it is unavailable and retained evidence is insufficient, mark verification incomplete. Synthetic fixtures provide repeatable offline checks; do not claim full replay of live pages from metadata alone. Source-specific access and excerpt permissions still require inspection.

## Reliability and data boundaries
- Every relationship and signal must be traceable to evidence; distinguish facts from interpretation.
- Conservative identity matching with an unresolved queue; never force a name match.
- Reconcile records through import stages, using mutually exclusive dispositions and explicit duplicate/rejection/unmatched counts.
- Preserve permitted sanitized evidence excerpts, checksums where available, and retrieval metadata. These do not guarantee full replay of a live page. The approved no-permanent-whole-content retention policy governs all source handling.
- Public code and fixtures remain organization-level. No donor records, director lists, private watchlists, credentials, or client data.
- Incidental personal information in articles and transcripts requires a handling policy before ingestion. Public availability alone does not settle storage or redistribution. Repository exclusion alone is insufficient: persistent local raw storage, transient retrieval, evidence excerpts, and logs each require an explicit handling decision. If unresolved, use synthetic fixtures and source references without retaining live content.
- Respect source access conditions. Snippets alone do not qualify a substantive finding as verified.

## First-build acceptance criteria
The initial implementation is described in [FOUNDATION_SPEC.md](FOUNDATION_SPEC.md). Source inspection, implementation, technical QC, and owner review are parts of the same bounded increment. Repository specifications describe expected behavior; execution assignments are issued by the owner through chat. Synthetic work does not require prior live-source approval; each live source requires its own access and handling decision before collection. Broader rollout thresholds follow observed results. At minimum:
1. A fresh checkout runs the documented synthetic example and meaningful tests.
2. A bounded, verified source set feeds a complete collection-to-review flow.
3. Every emitted finding links to evidence and separates observation from interpretation.
4. Source documents, events, account-event relationships, signal assessments, and action items remain distinct; duplicate stories do not inflate the underlying event count.
5. Incorrect/uncertain matches and inaccessible sources appear in visible queues.
6. Import counts reconcile; rerunning identical inputs does not multiply records.
7. Separate evidence-quality and relevance judgments retain reasons, dates, and reviewed versions; changed evidence does not silently inherit approval.
8. Coverage reporting distinguishes intended, configured, and successfully checked coverage.
9. Valid accounts remain admitted when their latest event, commercial relevance, budget, authority, or willingness to engage is unknown.
10. Each surfaced action contains the account, event type/date, observed fact, source evidence, possible relevance, unknowns, tier, and concrete next step.

These are draft acceptance criteria for the bounded foundation as a whole. Gate A is the synthetic end-to-end implementation and its software checks. Gate B is permitted live-source collection through the same flow, with separate source/QC evidence. Owner usefulness review is a further distinct outcome. Passing Gate A does not establish Gate B or owner approval. Numeric quality thresholds and the live-source set are not yet approved.

## Success measures to establish in the trial
Measure worklist precision (the share of `Act` and `Investigate` items judged worth seeing), discovery yield, unsupported claims, incorrect account associations, duplicate documents/events reaching the worklist, source-to-review delay, review load per useful item, and source health. Estimate recall only against a defined, independently reviewed sample. Also report source/geographic coverage and missed relevant items in that sample. Do not claim completeness across the open web. Revenue or introductions are downstream outcomes, not guaranteed software results.

## Open decisions
This is the authoritative open-product-decision register. Resolved requirements remain in the product sections and DECISIONS.md; they are not additional open blockers. No unapproved proposal is an implementation requirement.

| ID | Open choice | Dependency / when required |
| --- | --- | --- |
| Q1 | **Decided 2026-11-06 (D062):** hospitals, universities, religious organizations, and advocacy groups are excluded as buyers for the BC pilot. Service-delivery nonprofits plus foundations/umbrella bodies as potential buyers/routes are confirmed, with no revenue cutoff. Hospital foundations are separate entities and remain eligible. | Closed. Each exclusion is reversible by a new dated decision entry in DECISIONS.md. |
| Q2 | Specific source endpoints/localities within the confirmed BC/Washington pilot and subsequent expansion priorities. Priority source types are local reporting, organization publications, and official/funder records. No quota is approved. | A concrete proposal naming candidate publications, datasets, and exact endpoints with selection reasons is required before live collection; verification/access states remain explicit. Source-specific admission precedes routine collection. Canada-wide geography remains the product scope. |
| Q3 | Exact weekly owner availability, shortlist presentation, expansion batch sizes, continuation limits, and backlog priorities. Multiple-hour review capacity, no forced shortlist quota, the four action tiers, and initial explicit sorting rules are confirmed. | Owner availability before scheduling review; detailed batching before relying on those behaviors. No arbitrary quality discard based on an unapproved limit. |
| Q6 | Local run time, scheduler mechanism, source-specific refresh exceptions, and comparison periods beyond the agreed discovery window. | Before unattended daily operation or source-specific scheduling; initial research can remain owner-initiated. |
| Q7 | Source-specific access, permitted transient processing/excerpts, cleanup, personal-data handling, and redistribution basis. | Before inspection/collection under the applicable source conditions. Whole live content is not permanently stored. Transcription is deferred. |
| Q8 | Measured numerical quality/omission thresholds and the source/role evaluation sample. Required functional checks and complete claim accounting are already specified. | Measurement method before the trial; numerical acceptance targets require owner approval before a numerical pass claim. Trial observations can be reported without declaring an unapproved threshold met. |
| Q9 | Exact schema/runtime contracts, demonstrated role-context separation, and repository license. Python + SQLite, JSON/JSONL interchange, and Markdown-first reporting are accepted by D046-D049. | Detailed contracts before the authorized synthetic build; actual isolation evidence before claiming enforcement or independence; license before claiming usage/distribution rights. No provider migration or local model benchmark is required. |
| Q10 | Seven-project-day start date and actual owner availability for usefulness review. | Schedule when work begins; a missing owner review is recorded separately and cannot be invented. |

See [ROADMAP.md](../tracker/ROADMAP.md) for stages and [DECISIONS.md](../../decisions/DECISIONS.md) for agreed decisions.
