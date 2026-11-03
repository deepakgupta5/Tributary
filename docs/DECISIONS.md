# Product decision log
Status: Draft v0.1
Recorded: 2026-11-03

Dates below are recording dates, not claims about when a discussion originally occurred. This log records agreed direction. Proposals and unanswered questions remain in [PRD.md](PRD.md).

| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D001 | 2026-11-03 | The sole product goal is discovering potential nonprofit clients and credible routes in. | Client delivery and donor analysis belong to separate work. |
| D002 | 2026-11-03 | Initial geography is all Canada and Washington State. | Earlier BC-only or BC/Washington suggestions were not accepted; Oregon and California are deferred. |
| D003 | 2026-11-03 | Discovery includes struggling organizations and campaign improvement opportunities alongside funding and expansion. | Announcements of positive growth alone do not capture the intended needs. |
| D004 | 2026-11-03 | Existing-supporter engagement, repeat giving, and campaign use of data are relevant discovery themes. | Look for public evidence of potential needs; do not infer private donor performance or build client donor analysis. |
| D005 | 2026-11-03 | Source coverage must include local/regional media, podcasts, newsletters, and sector/community sources as well as official records. | Generic web searches and funding datasets alone are insufficient. |
| D006 | 2026-11-03 | Keep evidence of need, engagement capacity, and access distinct. | A financial problem does not prove willingness or ability to hire; a shared funder does not guarantee an introduction. |
| D007 | 2026-11-03 | Preserve evidence, dates, uncertainty, and visible coverage gaps. | Findings must support human investigation and withstand source checking. |
| D008 | 2026-11-03 | Document requirements and stages before coding; begin development with Codex and prepare a working foundation before external submission. | Validate product usefulness and source feasibility before scaling engineering. |
| D009 | 2026-11-03 | Maintain PRD, source register, roadmap, and decisions as evolving repository documents. | Start with substantive drafts; distinguish agreed requirements from open decisions. |
| D010 | 2026-11-03 | Public development describes the real business-development purpose; private target choices, relationship notes, and commercial actions stay outside it. | Product requirements can be reviewed without exposing private decisions. |
| D011 | 2026-11-03 | Human review and feedback are part of product development. | Feedback refines source selection and rules; it does not authorize automated outreach or client delivery. |

## Additional confirmed decisions
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D012 | 2026-11-03 | English only for the initial release and manual source trial across Canada and Washington State. | French and other languages remain explicit coverage gaps; geographic scope is unchanged. |

| D013 | 2026-11-03 | Adopt an organization-based searchable dashboard with new/changed, organization profile, and coverage/collection views. | Aggregate related stories without losing evidence; expose collection gaps. |
| D014 | 2026-11-03 | Include a weekly shortlist of new or materially changed organizations, with reasons and no forced quota. | Keep wider findings searchable. Collection frequency, shortlist size, and ranking await trial evidence. |
| D015 | 2026-11-03 | Separate evidence-quality feedback from business relevance. | Evidence: supported, insufficient, incorrect, duplicate, stale. Relevance: worth investigating, monitor, irrelevant. Retain reasons and reviewed versions. Real commercial feedback remains private. |

| D016 | 2026-11-03 | All product operation must be free, with no paid subscriptions or operating services. | Zero additional monetary operating cost. Use free/local access and processing; paid-only sources become visible gaps. Free-tier limits must not trigger charges. This resolves the budget question. |

## Pending proposals, not agreed decisions
| Item | Proposal | Status |
| --- | --- | --- |
| Organization eligibility | Broad coverage across service-delivery nonprofits; foundations and umbrella bodies as buyers or routes in; hospitals, universities, religious organizations, and advocacy groups eligible when relevant; no initial revenue cutoff. | Unanswered. No category exclusions or size thresholds approved. |
| Review workload | Weekly human review capacity, shortlist size, and ranking rules. | Open. Review structure and weekly shortlist are confirmed by D013-D014. |
| Collection schedule | Source refresh frequency and freshness windows. | Open; weekly review does not determine collection frequency. |

## Earlier assumptions requiring revision or confirmation
- The original Canada-only funding-map emphasis has expanded to Canadian and Washington nonprofit discovery with broad signal coverage.
- Fresh media signals are core requirements, not merely an optional later feed.
- The original no-runtime-AI restriction requires explicit confirmation. This documentation does not authorize runtime AI.
- No nonprofit category exclusions, size cutoffs, numeric quality thresholds, or collection frequency have been agreed. Weekly shortlist cadence and the free-only cost constraint are confirmed.
- External program acceptance, hours, payment, and ownership conditions are not product guarantees and are not asserted here.

## Change procedure
Add a dated entry when the owner agrees a material product decision. If a decision changes, preserve its history and identify the superseding entry. Update affected requirements, sources, roadmap, and checks in the same change when practical.
