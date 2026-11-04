# Product decision log
Status: Draft v0.1
Recorded: 2026-11-03

Dates below are recording dates, not claims about when a discussion originally occurred. Current direction is D036-D038 where it supersedes earlier entries. Earlier wording is retained as history, not a current implementation requirement. This log records agreed direction. Proposals and unanswered questions remain in [PRD.md](PRD.md).

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
- The original no-runtime-AI restriction recorded in D020 is superseded by D030. Historical entries remain; D036 supersedes the local-model interpretation.
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
| D026 | 2026-11-03 | Source feasibility, implementation, technical QC, and output iteration form an integrated development increment. | Initial planning referenced a coding handoff; D034 supersedes repository-based execution instructions. |

## Retention and separate data-review decisions
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D027 | 2026-11-03 | Approve metadata/checksums and necessary permitted sanitized excerpts, without permanent storage of whole live articles, recordings, or transcripts. | Source-specific permissions still apply. Transient processing needs cleanup; synthetic fixtures support offline replay. |
| D028 | 2026-11-03 | Collection and data QC must be separate roles, with explicit evidence verification. | Collector cannot approve its own output. Record versioned QC and verification outcomes; preserve labelled uncertain material for investigation. Owner relevance judgment remains separate. |

## Research review workflow refinement
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D029 | 2026-11-03 | Refine D028 into researcher, skeptic, and fact-checker roles with explicit instructions. | Researcher uses prescribed sources and separates facts/speculation; skeptic produces a constructive ranked problem list; fact-checker checks every number, quote, and paraphrase against the original, including unflagged claims. Final report retains claim-level verification flags and unresolved issues. Runtime-AI restriction is unchanged. |

## Historical local-AI interpretation, superseded by D036
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D030 | 2026-11-03 | Permit local AI researcher, skeptic, and fact-checker roles; supersede D020 and the no-runtime-model portions of D021/D029. | Deterministic data handling remains. Separate role contexts/outputs, model-check labels, and owner review are required. No paid/cloud model service or automatic training is authorized. |
| D031 | 2026-11-03 | No API interface is required. Local application, CLI, in-process library, or local-only endpoint may be considered. | Free-only operation remains; unattended automation support must be demonstrated. |
| D032 | 2026-11-03 | Target MacBook Air 15-inch with Apple M5, 24 GB memory, macOS 27.2. | User-provided screenshot; approximately 261 GB available at capture. Do not record serial number. Test actual hardware before selecting runtime/model. |
| D033 | 2026-11-03 | Proceed with this scope and disclose it honestly for external program assessment. | Eligibility remains unconfirmed; if refused, owner decides whether to revise or continue independently. |

## Execution instruction boundary
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D034 | 2026-11-03 | All execution instructions to coding assistants are issued by the owner through chat. | Repository content is product documentation, code, logic, analysis, and factual development records. Assistant-to-Codex task prompts and handoffs are excluded from the current branch. |

## Communication boundary
| ID | Recorded | Decision | Rationale / consequence |
| --- | --- | --- | --- |
| D035 | 2026-11-03 | Repository access for review and owner-directed product updates is permitted. Assistant judgments, review commentary, and instructions to other coding assistants are not repository content. | All review feedback and execution instructions pass through the owner in chat. Product requirements and factual development records remain in the repository. |

## Current execution and implementation decisions
| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D036 | 2026-11-03 | Build and execute the complete flow in Codex; preserve tested logic, rules, code, data contracts, role definitions, and factual results for continuation in Claude Code through repository access. | Supersedes the execution restrictions in D020, D024, D029-D032 and the local-inference interpretation. No MacBook benchmark, model installation, provider adapter, or API migration prerequisite. No new paid services or automatic charges. Daily unattended execution remains separately unproven. |
| D037 | 2026-11-03 | The intended first implementation scope is a bounded collection, stored-evidence, researcher, skeptic, fact-checker, and reviewable-report flow. | This is product scope, not authorization for the planning conversation to execute it. D038 specifies the execution boundary. Source trials and implementation form one bounded increment. |

## Planning and implementation boundary
| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D038 | 2026-11-03 | The planning conversation reviews and updates product documentation. The owner separately instructs repository-connected Codex through chat to build and run code. | D036-D037 do not authorize implementation or test execution in the planning conversation. PR #2 was closed at the owner's direction; its implementation branch remains untouched for traceability and is not an approved baseline. PR #1 remains documentation only. D034-D035 continue to exclude assistant handoffs and review judgments from repository content. |

## Change procedure
Add a dated entry when the owner agrees a material product decision. If a decision changes, preserve its history and identify the superseding entry. Update affected requirements, sources, roadmap, and checks in the same change when practical.
