# Consolidated documentation review
Date: 2026-11-03
Reviewed baseline: 3e996d8cdd7bf35cf0c788bb8dd863d4acd38b75
Reviewer: planning assistant; this is not independent human QC or external program approval.
Status: Documentation corrections prepared; owner approval remains pending.

## Verdict
The six documents capture the agreed product direction, but were not ready to hand over unchanged. Corrected contradictions in sequencing, readiness, live-test success, and decision status. No product code, source integration, deployed scheduler, verified source register, or paid-program eligibility has been established.

## Findings and corrections
| Finding | Consequence | Correction |
| --- | --- | --- |
| PRD required a completed manual trial before coding; SOURCES required deliverables before coding; roadmap/handoff integrated those activities. | Circular gate and conflicting instructions to Codex. | Source inspection, bounded implementation, QC, and owner review occur within Task 001. Synthetic work and each source's live-access gate are separate. |
| Handoff said ready while PRD and task approval were pending. | Agent could mistake draft preparation for owner authorization. | Handoff marked pending owner approval after review. |
| Live acceptance allowed either success or reported failure. | All sources could fail while the task was reported passed. | Synthetic checks, live feasibility, and owner review are separate. Required Canadian/Washington live checks remain incomplete if blocked. |
| Some pending items still treated multiple-hour review capacity and daily collection as unresolved. | Repeated clarification or wrong implementation assumptions. | Retained exact allocation/time/ranking as open, confirmed broad capacity and daily cadence. |
| Decision log had table rows separated from headers. | Confirmed decisions could render as plain text. | Repaired affected tables. |
| Public repository exclusion did not specify local raw-content handling. | A collector could persist unapproved personal or restricted content locally. | Per-source access/retention/handling gate clarified. The policy choice below remains open. |
| Broad event deduplication looked like a solved prerequisite. | A first slice might overclaim semantic duplicate detection. | Exact/known syndication cases are checked; ambiguous event identity is flagged. |
| Route field did not distinguish missing research from no route found. | Incomplete work could look like negative evidence. | Explicit not-investigated / none-found / evidence-available distinction in handoff. |
| Feedback log's no-trial wording omitted exploratory browsing. | History could imply no research occurred. | Clarified browsing versus implemented trial; added actual owner feedback on execution environment. |
| Podcast discussion could imply transcription is an initial feature. | Scope creep or conflict with runtime-model constraints. | Task 001 uses existing text; transcription remains deferred. |
| PR description still referred to only four documents and resolved questions as open. | Reviewer would see an outdated summary. | Refresh PR metadata with current scope and review findings. |

## Scope update after this review
The owner subsequently authorized local AI researcher, skeptic, and fact-checker roles, superseding the earlier no-runtime-model restriction. Deterministic data handling remains. Target hardware is MacBook Air 15-inch, Apple M5, 24 GB, macOS 27.2. The next Codex checkpoint is LOCAL_AI_FEASIBILITY.md. This report's historical findings remain a record of the earlier review; current instructions are in the updated PRD and handoff.

## Confirmed baseline
Canada and Washington; English only; no paid operating services; local runtime review roles now permitted; 12-month discovery with contextual recency; daily local collection as a future product capability; organization-based review; substantial human investigation; development feedback recorded in Git. Client delivery, donor analysis, campaign execution, and outreach are excluded.

## Blockers versus deferred decisions
| Item | When needed | Current status |
| --- | --- | --- |
| Owner accepts the reviewed Task 001 scope/checks | Before issuing the implementation task | Pending; documents are not self-approving. |
| Source handling policy and source-specific permitted access | Before each live source is collected/persisted | Retention approach approved; each source's permissions and implementation checks remain to be established in Codex. |
| Stack and bounded source selection | Within Task 001 | Assigned to Codex; justify choices and report gaps. |
| Category exclusions/revenue cutoffs | Before applying such exclusions | None approved; do not silently filter. Does not block source-format fixtures. |
| Numeric commercial relevance/omission thresholds | Before broader rollout | Derive from owner review; do not invent acceptance rates. Functional Task 001 checks are already specified. |
| Exact weekly allocation, ranking, shortlist size | After trial outputs | Multiple-hour capacity confirmed; no forced quota. |
| Host OS, run time, scheduler installation | Before scheduled operation | Deferred. Explicit collection commands first. |
| License | Before representing the code as open source | Not selected; public visibility alone is insufficient. |
| External program rules | Before program-dependent work | Separate confirmation; not a technical bootstrap gate. |

## Source-handling choice, subsequently approved
For the first live slice, retain source metadata, checksums, and only necessary permitted sanitized evidence excerpts; do not keep persistent raw articles, audio, or transcripts. Retrieval still needs a source-specific transient-processing decision. Drop person fields from structured records; ensure excerpts and logs do not retain incidental personal information. If an excerpt cannot preserve useful organizational context within the handling rules, retain only a reference and visible gap. Do not claim full offline reproduction of live pages when raw content is not retained; offline repeatability comes from synthetic fixtures.

Owner approved this retention approach on 2026-11-03 and required separate collection/data-QC roles with explicit verification. See PRD.md, DECISIONS.md D027-D028, and CODEX_HANDOFF.md. Access conditions and permitted use still need source-specific inspection.

## Remaining product risk
Deterministic rules and local models may produce noisy or incomplete indirect signals. Model reviews can repeat errors across roles; prompt changes and source-grounded accuracy checks must be measured. More review hours do not remove that risk. Task 001 must show rule triggers, permit inspection of non-matching/uncertain items, and compare results with a small human-reviewed sample. Quality improvement is not established until observed.

Free English-only access will leave geographic/language and audio gaps. A daily run does not guarantee a 12-month archive. Public-page readability does not establish a stable free automated discovery service.

## README follow-up
README.md was updated during the review and now reflects Canada/Washington scope and the subsequently approved local AI roles. Implementation run instructions must wait for working code.

## Validation
All six baseline documents were read. Corrections were checked against confirmed discussion decisions; relative Markdown file links and decision-table structure were checked in the prepared document set. No software tests or source trials were run as part of this documentation review.
