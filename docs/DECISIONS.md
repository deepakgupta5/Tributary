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
| D014 | 2026-11-03 | Include a weekly shortlist of new or materially changed organizations, with reasons and no forced quota. | Keep wider findings searchable. Daily collection was subsequently confirmed by D023; shortlist size and ranking await trial evidence. |
| D015 | 2026-11-03 | Separate evidence-quality feedback from business relevance. | Evidence: supported, insufficient, incorrect, duplicate, stale. Relevance: worth investigating, monitor, irrelevant. Retain reasons and reviewed versions. Real commercial feedback remains private. |
| D016 | 2026-11-03 | All product operation must be free, with no paid subscriptions or operating services. | Zero additional monetary operating cost. Use free/local access and processing; paid-only sources become visible gaps. Free-tier limits must not trigger charges. This resolves the budget question. |

## Pending proposals, not agreed decisions
| Item | Proposal | Status |
| --- | --- | --- |
| Organization eligibility | Broad coverage across service-delivery nonprofits; foundations and umbrella bodies as buyers or routes in; hospitals, universities, religious organizations, and advocacy groups eligible when relevant; no initial revenue cutoff. | Unanswered. No category exclusions or size thresholds approved. |
| Review workload | Exact weekly allocation, shortlist size, and ranking rules. | Multiple-hour capacity is confirmed by D024; precise allocation and ranking remain open. |
| Collection implementation | Exact local run time, source-specific access exceptions, and scheduler mechanism. | Daily collection confirmed by D023; implementation details remain open. |

## Earlier assumptions requiring revision or confirmation
- The original Canada-only funding-map emphasis has expanded to Canadian and Washington nonprofit discovery with broad signal coverage.
- Fresh media signals are core requirements, not merely an optional later feed.
- The original no-runtime-AI restriction is confirmed for the initial core by D020. AI-assisted development is separate from runtime behavior.
- No nonprofit category exclusions, size cutoffs, or numeric quality thresholds have been agreed. Daily local collection, weekly shortlist cadence, and the free-only cost constraint are confirmed.
- External program acceptance, hours, payment, and ownership conditions are not product guarantees and are not asserted here.

## Further confirmed decisions
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D017 | 2026-11-03 | Use a 12-month discovery window, with recent-six-month priority where evidence and relevance are comparable. | No hard six-month exclusion. Older records support trends and campaign comparisons; current-status checks precede shortlisting older findings. |
| D018 | 2026-11-03 | Investigate indirect evidence without relying on explicit admissions of fundraising difficulty. | Local interviews and contextual reporting are important. Preserve observations, hypotheses, alternative explanations, missing evidence, and source independence. |
| D019 | 2026-11-03 | Distinguish recency, relevance, current status, and action timing. | Recent weak clues do not automatically outrank older supported patterns. Missing updates mean status unknown, not continuing need. |

## Deterministic implementation decisions
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D020 | 2026-11-03 | Initial core is deterministic, with no runtime AI or model calls, including local models. | Software surfaces evidence through transparent processing and rules; humans interpret context and commercial relevance. |
| D021 | 2026-11-03 | Foundation includes synthetic fixtures, replay without live calls, stable identifiers, rule provenance, reconciled audits, and actual development history. | These engineering practices support reproducibility, QC, and owner understanding. |
| D022 | 2026-11-03 | Earlier project plans do not establish external program eligibility or transfer their buyer profiles, productization plans, ticket counts, or paid-hour estimates. | Program terms require separate confirmation; this repository records Tributary product requirements. |

## Collection cadence decision
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D023 | 2026-11-03 | Run collection daily on the local computer when available. | Weekly shortlist remains separate. Show missed runs, catch up from successful source checkpoints where possible, and report unrecoverable gaps. No running scheduler is claimed by this decision. |

## Human investigation decision
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D024 | 2026-11-03 | Human investigation is core; the owner can spend multiple hours reviewing prospects, with exact weekly allocation open. | Support context, history, conflicting evidence, transparent triggers, and uncertain findings beyond the shortlist. No arbitrary cap should discard useful evidence. Trial measures usefulness and review workload; review is manual, not runtime LLM review. |

## Development feedback decision
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D025 | 2026-11-03 | Record material development feedback and the resulting instruction/code changes in the repository. | Trace initial instruction, observed issue, actual owner feedback, revisions, changes, and verification using DEVELOPMENT_FEEDBACK.md and linked Git history. Keep private judgments and external program ratings separate; do not fabricate owner reasoning. |

## Execution environment decision
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D026 | 2026-11-03 | Execute source feasibility, coding, technical QC, and output iteration in the repository-connected Codex coding environment. | This planning conversation prepares requirements and handoffs. Task 001 integrates a bounded source trial with a working collection-to-review flow; owner feedback drives the next increment. |

## Documentation review note
The consolidated review in DOCUMENT_REVIEW.md corrects stale sequencing and status wording without approving unresolved product choices. Synthetic development, live-source feasibility, and owner relevance review have separate pass conditions. Source handling must cover local persistence as well as public repository content.

## Retention and separate data-review decisions
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D027 | 2026-11-03 | Approve metadata/checksums and necessary permitted sanitized excerpts, without permanent storage of whole live articles, recordings, or transcripts. | Source-specific permissions still apply. Transient processing needs cleanup; synthetic fixtures support offline replay. |
| D028 | 2026-11-03 | Collection and data QC must be separate roles, with explicit evidence verification. | Collector cannot approve its own output. Record versioned QC and verification outcomes; preserve labelled uncertain material for investigation. Owner relevance judgment remains separate. |

## Research review workflow refinement
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D029 | 2026-11-03 | Refine D028 into researcher, skeptic, and fact-checker roles with explicit instructions. | Researcher uses prescribed sources and separates facts/speculation; skeptic produces a constructive ranked problem list; fact-checker checks every number, quote, and paraphrase against the original, including unflagged claims. Final report retains claim-level verification flags and unresolved issues. Runtime-AI restriction is unchanged. |

## Change procedure
Add a dated entry when the owner agrees a material product decision. If a decision changes, preserve its history and identify the superseding entry. Update affected requirements, sources, roadmap, and checks in the same change when practical.
