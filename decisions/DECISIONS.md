# Product decision log
Status: Draft v0.1
Recorded: 2026-11-03

Dates below are recording dates, not claims about when a discussion originally occurred. Current direction includes D036-D054 where it supersedes earlier entries. Earlier wording is retained as history, not a current implementation requirement. This log records agreed direction. Proposals and unanswered questions remain in [PRD.md](../OutBound/frameworks/PRD.md).

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
The authoritative open-product-decision register is PRD.md, Open decisions. Earlier proposals remain unapproved unless a subsequent owner decision resolves them:
- Remaining undecided organization categories: PRD Q1; starting categories and no revenue cutoff are confirmed by D043.
- Owner availability, shortlist/ranking and expansion rules: PRD Q3.
- Collection scheduling and source-specific refresh details: PRD Q6.
- Other unresolved design/source/quality/start choices: PRD Q2 and Q7-Q10.

## Earlier assumptions requiring revision or confirmation
- The original Canada-only funding-map emphasis has expanded to Canadian and Washington nonprofit discovery with broad signal coverage.
- Fresh media signals are core requirements, not merely an optional later feed.
- The original no-runtime-AI restriction recorded in D020 is superseded by D030. Historical entries remain; D036 supersedes the local-model interpretation.
- D043 confirms starting categories and no revenue cutoff; other named categories remain undecided. Numerical quality thresholds remain unapproved. Daily collection, weekly shortlist cadence, and free-only operation are confirmed.
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

## Expanding universes and project baseline
| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D039 | 2026-11-03 | Organization and source universes expand continuously in both directions rather than assuming complete day-zero lists. | Candidate discovery, provenance, separate admission checks, bounded expansion, current statuses, and visible coverage gaps are required. No register-growth quota is approved. |
| D040 | 2026-11-03 | The same four checkpoints apply to findings, nonprofit additions, and daily source additions. | Collection/separate data QC, researcher, skeptic, and fact-checker are required; collector cannot approve its own proposals. Material changes reopen affected checks. Unchanged approved records do not require full daily re-review. |
| D041 | 2026-11-03 | The project plan has a beginning baseline, the first seven project days with expected achievements and reconciliation, and an ongoing cycle from week two. | PROJECT_PLAN.md records scope, deliverables, QC/testing, dependencies, evidence-based acceptance, and reconciliation. The owner separately instructs Codex to implement; no execution authorization is created for the planning conversation. |
| D042 | 2026-11-03 | The deliverable is one consistent product-documentation baseline with open decisions explicitly identified and no unapproved numerical quality targets or source quotas. | PRD.md is the single open-product-decision register. First-week day numbers are planning targets, not promises, measured results, or a start date. |

## Confirmed starting scope and first delivery
| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D043 | 2026-11-03 | Begin with service-delivery nonprofits; include foundations and umbrella bodies as potential buyers or routes in; no revenue cutoff. | Hospitals, universities, religious organizations, and advocacy groups remain undecided and pending admission decisions, not silently included or permanently excluded. |
| D044 | 2026-11-03 | The first live sample focuses on BC and Washington, using local reporting, organization publications, and official/funder records. | Overall geography remains Canada and Washington. Specific endpoints/localities and subsequent expansion remain design choices; no source quota is approved. |
| D045 | 2026-11-03 | The initial delivery is Day 1 only: documentation inspection and proposed technical design, record formats, initial source sample, and test matrix. | The proposal returns to the owner for review before implementation. Days 2-7 remain conditional; implementation requires separate owner authorization. All execution assignments still pass through owner chat. |

## Accepted Day 1 design decisions
| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D046 | 2026-11-03 | Use Python and SQLite for the bounded foundation, JSON/JSONL interchange, and a Markdown report before a dashboard. | No additional service or provider integration is required. Exact schema and runtime details remain implementation contracts. |
| D047 | 2026-11-03 | Minimize the first implementation while demonstrating the complete synthetic flow. | Six logical record groups organize the design, not six mandatory tables or separate subsystems. Reversible merges, detailed funding relationships, HTML output, and dashboard work are deferred; suspected duplicates remain linked and unresolved without destructive merging. |
| D048 | 2026-11-03 | Separate review execution completion from passing review and distinguish required details from optional fields and documented limitations. | Missing/stale required checks and material unresolved identity, eligibility, access/handling, or factual issues block approval. A skeptic question alone does not fail a record. Nonmaterial limitations and optional missing fields remain visible without automatically blocking approval. |
| D049 | 2026-11-03 | Separate collection/QC executions and role packets; record actual context separation and shared-assistant limitations. | Execution IDs and separate files establish traceability, not independent review or demonstrated isolation. Collection cannot approve its own output. No enforcement or independence claim exceeds observed execution evidence. |
| D050 | 2026-11-03 | Reopen affected checks through recorded dependencies after material changes. | Changed evidence cannot inherit old approval. Historical decisions remain; the affected current version awaits recheck. Unchanged records do not require full daily review. |
| D051 | 2026-11-03 | Identify actual candidate publications, datasets, and endpoints with selection reasons before live collection. | Candidates may remain explicitly unverified pending permitted inspection. Categories alone are insufficient for the live-source proposal; no source quota is introduced. |
| D052 | 2026-11-03 | Day 1 design is complete and its accepted choices are recorded as product requirements. | Design acceptance and documentation updates do not authorize implementation or tests. Bounded synthetic implementation requires separate owner instruction; live collection remains a separate gate. Live-source feasibility, role accuracy, and product usefulness are not established. |

## Research retention and repository organization

| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D053 | 2026-11-05 | Store substantive external product research in the repository. | Each research record retains scope, sources, conclusions, evidence limits, and implementation implications. Chat-only conclusions are insufficient for decisions that affect the build. |
| D054 | 2026-11-05 | Adapt the useful operating and Library separation from the Fractional repository to Tributary without copying unused folders. | Current operating material is organized under `OutBound/`; code and tests retain standard roots; accepted decisions and examples retain distinct roots; `Library/` is reserved for actual owner-facing artifacts. Empty project-specific placeholders are not created before use. |

## Account-centered event monitor

| ID | Recorded | Decision | Consequence |
| --- | --- | --- | --- |
| D055 | 2026-11-05 | Admit accounts using resolved identity, geography, and in-scope eligibility, independently of signal recency or commercial strength. Current official registry status and historical filings serve different purposes. | Greater Vancouver Food Bank Society is included as a valid account. A stale filing, unknown consulting budget, or weak current signal cannot remove an otherwise valid account. This supersedes D040 and D048 only where their generic checkpoint wording could be read to block account admission for missing signal or commercial evidence. |
| D056 | 2026-11-05 | Build the week-one product as an account-centered event monitor with separate documents, accounts, events, assessments, actions, and feedback. | The daily outputs are new accounts, new account events, evidence-backed commercial hypotheses, and a short action queue. Duplicate documents cannot inflate event counts. |
| D057 | 2026-11-05 | Use `Act`, `Investigate`, `Monitor`, and `Suppress` as operational tiers, supported by explicit sorting rules rather than a universal numeric score. | Valid accounts can remain monitored. Action items require a concrete next step and explicit unknowns. Week one does not claim predictive buyer intent, trained ranking, or automatic outreach. |
| D058 | 2026-11-06 | Adopt the BC conversation plan ([now in Non-Profits](https://github.com/deepakgupta5/Non-Profits/blob/main/OutBound/frameworks/BC_CONVERSATION_PLAN.md)): objective is actual conversations with BC nonprofit people by Fri Nov 13, 2026, success = 5 held or firmly booked; the plan, objective, steps, and decisions are recorded in the repository, not only in chat. | The repo is the shared workspace and record for the owner, Codex, Bertie (Muse), and ChatGPT. Chat-only plans do not govern execution. |
| D059 | 2026-11-06 | The working pitch for BC nonprofit conversations is the tight pitch: help nonprofits raise more money from their existing donors, and fine-tune how they do that using analytics and systems. This supersedes the website's operational-leadership framing for outbound use. | Buyer order: development/fundraising lead first, ED second. The PRD target/trigger definitions are corrected to the tight pitch (donor-base gate, donor-side triggers). The website mismatch is known; revising the website is a separate owner decision, not yet made. |
| D060 | 2026-11-06 | BC outbound parameters: warmth inventory is zero (warmth is manufactured via events, intermediaries, social engagement); channels LinkedIn, Facebook, Twitter/X, Threads, Instagram are all in for this work; in-person geography is West Vancouver to Abbotsford (~1 hour from Coquitlam), outside = remote/monitor only for the pilot. | Direct outreach is the starting route. These parameters are specific to BC nonprofit outbound and do not change boundaries set for other work. |
| D061 | 2026-11-06 | Event rule: pay for in-person networking; paid virtual events are not proposed; free virtual is acceptable. Attend: AFP National Philanthropy Day (Nov 13, $130 non-member, buy decision by Nov 11), CAGP Greater Vancouver Nov 25–26 (fee enquiry open), AFP AGM Nov 25 (free, virtual), Coquitlam Foundation breakfast Dec 3 ($30). Skip and do not re-propose: Housing Central (Nov 16–18), Crisis Comms Lab (Dec 1), AFP Global sponsored webinar (Dec 9). | Event spend for the pilot is in-person rooms where the donor-revenue buyer is present. Skips are recorded so they are not re-researched or re-proposed. |
| D062 | 2026-11-06 | PRD open decision Q1 is decided: hospitals, universities, religious organizations, and advocacy groups are EXCLUDED as buyers for the BC pilot. Rationale: religious organizations — congregation giving is member/tithe-based and ~26% of the archived list is religious-category, which would swamp the screens; hospitals — government-funded institutions with procurement gates (hospital FOUNDATIONS are separate entities with real donor bases and remain eligible); universities — advancement offices are large, sophisticated, in-house analytics, mostly far above the size band; advocacy groups — membership/grant-skewed revenue, weakest donor-analytics fit, monitor only. | The Step 4 screen applies these exclusions with per-category counts in the reconciliation table. Each exclusion is reversible by a new dated decision entry; none is permanent. Q1 in the PRD is closed by this entry. |
| D064 | 2026-11-06 | After completing the available local and cloud backup searches without finding a recoverable journal, initialize a new empty private owner-feedback database at the configured location. The checked evidence does not establish that the former store was ever populated: Day 5/Day 6 dispositions are assistant assessments, and feedback-persistence validation used synthetic temporary databases. | This is a new zero-entry baseline, not a restoration or a claim of confirmed history loss. Any prior owner-feedback history, if it ever accumulated, was not recoverable from the checked sources. Do not import assistant dispositions as owner decisions. Preserve existing source-review history; future owner feedback remains private and version-bound. See [initialization audit](../OutBound/evidence/private-feedback-initialization/README.md). |
| D065 | 2026-11-06 | Activities review of the 32 ambiguous category records held by the Issue #9 population screen (owner-reviewed and decided): Planned Lifetime Advocacy Network is EXCLUDED as an advocacy group under D062 — it delivers support networks for people with disabilities, but policy advocacy and a membership model are core to it (it led the campaign that created the RDSP). Three records are RETAINED as service-delivery organizations where advocacy names a service component, not an advocacy purpose: Providing Advocacy Counselling & Education Society (PACE Society — front-line harm-reduction services for sex workers), Child and Youth Advocacy Centre of Kelowna Society (child advocacy centre service model), and PeaceGeeks International Society (technology project delivery for peace and humanitarian partners). The remaining 28 flagged records are out-of-band on size regardless of classification and are resolved as a batch: advocacy clue noted, classification moot for the pilot, held from buyer admission, revisit only if a future screen brings a record in-band. | Pool effect: retained size-fit 552 -> 551 (Planned Lifetime Advocacy Network removed); retained enrichment unchanged at 345 (both in-pool enrichment records retained). The screen owner applies these dispositions to the Issue #9 dataset artifacts; Issue #9 is closable once applied. PACE Society's operating status (closed around 2025, rebuilding toward a fall 2026 relaunch) is a downstream current-status gate item, not a category question. |

| D066 | 2026-11-06 | Canonical geography stage: owner explicitly includes Delta, Mission and White Rock in the in-person BC pilot corridor, in addition to the D060 localities. | Apply to the retained 551 size-fit and 345 enrichment records. Preserve raw mailing locality and canonical routing area; split foundations (A/B) to the funder/intermediary list. Other localities remain remote/monitor. This boundary decision does not establish current operating geography, donor-base fit, live triggers or outreach permission. |

| D067 | 2026-11-09 | Correction to D062 (owner, 2026-11-09): the 'college' and 'religious' categories were intended as review FILTERS — flags for an owner decision — not hard exclusions. St. Mark's College is IN on that basis: a registered charity since 1967 and UBC's affiliated Catholic theological college, and, on the owner's counterweight, Catholic colleges in BC receive no provincial government funding, so it is wholly donor-dependent and the D062 rationale (public funding, large advancement machinery) does not apply. | Advocacy dispositions under D065 are NOT reopened: Planned Lifetime Advocacy Network remains excluded. Any other college or religious record the screen surfaces is decided by the owner case by case and recorded the same way. Immediate effect: St. Mark's College (rank 9, CALL_PRIORITY_2026-11-08) is dial-ready in Wave 1. |

## Change procedure
Add a dated entry when the owner agrees a material product decision. If a decision changes, preserve its history and identify the superseding entry. Update affected requirements, sources, roadmap, and checks in the same change when practical.
