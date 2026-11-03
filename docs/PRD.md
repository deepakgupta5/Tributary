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

## Review experience
Required capabilities: inspect findings and organization evidence, filter by geography/signal/date, inspect relationships, see coverage gaps, and record feedback. Exact interface and delivery cadence remain open.

Proposed feedback labels: useful, irrelevant, insufficient evidence, stale, duplicate, and incorrect organization match. Record a reason and the reviewed finding version. Private prospect choices, relationship notes, and actions stay outside the public repository and recorded development sessions.

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
7. Reviewer feedback is retained and traceable.
8. Coverage reporting distinguishes intended, configured, and successfully checked coverage.

These are draft acceptance criteria. Numeric quality thresholds and the live-source set are not yet approved.

## Success measures to establish in the trial
Measure source/geographic coverage, findings judged useful, unsupported claims, incorrect identity matches, duplicate events, source-to-review delay, missed relevant items in an independently reviewed sample, and review time per useful finding. Do not claim completeness across the open web. Revenue or introductions are downstream outcomes, not guaranteed software results.

## Open decisions
| ID | Question |
| --- | --- |
| Q1 | Which nonprofit categories and size ranges, if any, should be excluded? |
| Q2 | Which locations and languages form the manual trial sample? How will French-language and other coverage be handled? |
| Q3 | Which interface, delivery cadence, and weekly human review capacity are preferred? |
| Q4 | What monthly infrastructure, subscription, transcription, and source-access budget is acceptable? |
| Q5 | Does the original no-runtime-AI constraint remain firm? No runtime AI is authorized by this draft. |
| Q6 | What signal freshness windows, historical periods, and refresh frequencies are appropriate? |
| Q7 | What source-retention, incidental-person-data, licensing, and audio-transcription policies are workable? |
| Q8 | What measured quality thresholds and verified sources define the first build? |

See [ROADMAP.md](ROADMAP.md) for stages and [DECISIONS.md](DECISIONS.md) for agreed decisions.
