# Tributary product requirements
Status: Draft v0.1, not approved for implementation
Owner: Deepak Gupta
Updated: 2026-11-03

## Purpose and user
Tributary supports nonprofit business development for Autonomy Bridge. Its sole product goal is to find potential clients and credible organizational routes to reach them. Deepak reviews evidence and makes commercial decisions privately.

The initial geographic scope is all of Canada and Washington State. Oregon and California are future possibilities, not initial requirements. Collection can be introduced in stages, but coverage gaps must remain visible.

## Decisions the product supports
- Which nonprofits show evidence of needs relevant to operational leadership, fundraising support, or better use of data in campaigns and existing-supporter engagement?
- Which funders or intermediaries sponsor outside operational or capacity-building support?
- What documented funding or organizational relationships offer a plausible route in?
- What changed, how reliable is the evidence, and what needs investigation before deciding to pursue an organization?

Client delivery, donor analysis, campaign execution, and outreach are outside this product's scope.

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

Keep evidence of need, evidence of capacity to engage, and evidence of access separate. Unknown capacity or access must be visible, not treated as proof of absence or used to silently discard a finding.

## Deterministic core and human interpretation
Confirmed: the initial core uses deterministic processing, with no runtime AI or model calls, including local models. AI-assisted development is distinct from product operation.

Software collects permitted sources, normalizes dates, resolves organization identities conservatively, removes duplicates, applies transparent rules to surface candidate passages, joins funding records, displays organizational connections, and preserves evidence and processing audits. Rules surface candidates; they do not diagnose fundraising or donor-retention problems.

The reviewer interprets context, examines alternative explanations, judges service relevance, and decides whom to pursue. Every rule-based candidate must identify its triggering rule and supporting passage or record. Human interpretation must remain distinguishable from recorded facts and rule output.

The source trial must measure whether deterministic collection and filtering reduce reading effort while preserving relevant context. If this approach proves insufficient, record the limitation and revisit scope explicitly. Runtime AI requires a future owner decision; it is not implicitly permitted by a free/local implementation.

## Cost constraint
Confirmed: zero additional monetary operating cost. No paid subscriptions, paid source access, paid hosting, paid APIs, paid transcription, or other paid operating services. Use local execution or genuinely free services without automatic paid overages. Development must not introduce a paid runtime dependency.

Paywalled sources and recordings without a usable free transcript remain visible coverage gaps unless a permitted free alternative is available. Do not bypass access controls. A free tier's limits must be recorded; reaching them must pause or report the affected work rather than incur charges. Any future change to this constraint requires an explicit owner decision.

## Language scope
Confirmed: English only for the initial release and manual source trial across Canada and Washington State. French and other languages are recorded as coverage gaps. Nationwide geography does not imply multilingual coverage. English reporting about organizations in any Canadian jurisdiction remains eligible.

## Discovery window and indirect signals
Confirmed on 2026-11-03: discover signals from the past 12 months. Give the most recent six months review priority when relevance and evidence are otherwise comparable; six months is not an exclusion cutoff. Keep older financial/funding records and earlier campaign periods for context and comparisons.

Assess event date, publication date, last status check, relevance, current status, and timing separately. A recent weak clue must not automatically outrank an older supported pattern. Before promoting older findings to the shortlist, check for updates; record ongoing, resolved, recurring, or current status unknown, with supporting evidence. No update does not prove continuation.

Do not depend on explicit admissions of fundraising difficulty. Investigate contextual observations in local reporting, interviews, podcasts, organizational publications, and records. Candidate observations include repeated campaign deadline extensions, comparable declines in participation, service-demand growth alongside flat donations, concentrated funding, and publicly described renewal/follow-up workload.

These observations are investigation prompts. Record the underlying facts, possible relevance, alternative explanations, missing evidence, and period comparability. A deadline extension may be routine; a campaign change may explain participation differences. Never convert an indirect clue into a factual claim of fundraising failure, donor-retention problems, consulting budget, or willingness to engage. Independent observations may strengthen a case; syndicated copies are not independent corroboration.

## Source breadth and coverage
Use official records together with city/community newspapers, provincial/state and regional media, local radio/TV, sector publications, podcasts, newsletters, organizational publications, and funder/community networks. Generic search is one discovery channel, not the coverage strategy.

Track coverage by province/territory or state, city/region, source type, language, and last successful check. Record unserved areas and access failures. Headquarters location and area served are distinct fields. Source feasibility is defined in [SOURCES.md](SOURCES.md).

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
Confirmed: one daily local collection run when the host computer is available. The weekly shortlist remains a separate review view. This is a product requirement; no collection scheduler is deployed yet.

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

Private pursuit decisions, relationship notes, outreach status, and actual business-relevance feedback stay outside the public repository and recorded development sessions. Public examples and session demonstrations use synthetic review records. The product may support private feedback without publishing it.

Feedback is used to refine documented collection and filtering rules. It does not imply automated learning or runtime AI.

## Reliability and data boundaries
- Every relationship and signal must be traceable to evidence; distinguish facts from interpretation.
- Conservative identity matching with an unresolved queue; never force a name match.
- Reconcile records through import stages, using mutually exclusive dispositions and explicit duplicate/rejection/unmatched counts.
- Preserve reproducibility using permitted source snapshots or checksums and retrieval metadata. Full source retention depends on rights and personal-data handling.
- Public code and fixtures remain organization-level. No donor records, director lists, private watchlists, credentials, or client data.
- Incidental personal information in articles and transcripts requires a handling policy before ingestion. Public availability alone does not settle storage or redistribution.
- Respect source access conditions. Snippets alone do not qualify a substantive finding as verified.

## First-build acceptance criteria
The first implementation scope must be approved after a manual source trial. At minimum:
1. A fresh checkout runs the documented synthetic example and meaningful tests.
2. A bounded, verified source set feeds a complete collection-to-review flow.
3. Every emitted finding links to evidence and separates observation from interpretation.
4. Duplicate stories do not inflate the underlying event count.
5. Incorrect/uncertain matches and inaccessible sources appear in visible queues.
6. Import counts reconcile; rerunning identical inputs does not multiply records.
7. Separate evidence-quality and relevance judgments retain reasons, dates, and reviewed versions; changed evidence does not silently inherit approval.
8. Coverage reporting distinguishes intended, configured, and successfully checked coverage.

These are draft acceptance criteria. Numeric quality thresholds and the live-source set are not yet approved.

## Success measures to establish in the trial
Measure source/geographic coverage, findings judged useful, unsupported claims, incorrect identity matches, duplicate events, source-to-review delay, missed relevant items in an independently reviewed sample, and review time per useful finding. Do not claim completeness across the open web. Revenue or introductions are downstream outcomes, not guaranteed software results.

## Open decisions
| ID | Question |
| --- | --- |
| Q1 | Which nonprofit categories and size ranges, if any, should be excluded? Pending proposal: broad service-delivery coverage, foundations and umbrella bodies as buyers or routes in, hospitals/universities/religious/advocacy organizations eligible when relevant, and no initial revenue cutoff. No approval or exclusions have been recorded. |
| Q2 | Which locations form the manual trial sample? Language is resolved: English only; French and other languages remain visible coverage gaps. |
| Q3 | What weekly human review capacity, shortlist size, and transparent ranking rules are appropriate? Dashboard views, weekly shortlist, and separate feedback judgments are confirmed. |
| Q4 | Resolved: zero additional monetary operating cost; no paid subscriptions or operating services. Which free/local access methods are feasible is determined in the source trial. |
| Q5 | Resolved for the initial core: deterministic processing, no runtime AI or model calls; human interpretation remains explicit. |
| Q6 | Discovery is set to 12 months and local collection to daily. What local run time, source-specific access exceptions, and category-specific historical comparison periods are appropriate? |
| Q7 | What source-retention, incidental-person-data, licensing, and audio-transcription policies are workable? |
| Q8 | What measured quality thresholds and verified sources define the first build? |

See [ROADMAP.md](ROADMAP.md) for stages and [DECISIONS.md](DECISIONS.md) for agreed decisions.
