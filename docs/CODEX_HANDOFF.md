# Codex development handoff
Prepared: 2026-11-03
Status: First task ready for execution in the repository-connected Codex coding environment. No implementation has been performed by this handoff.

## Start here
Read PRD.md, SOURCES.md, ROADMAP.md, DECISIONS.md, and DEVELOPMENT_FEEDBACK.md in this directory. Requirements are evolving drafts; confirmed decisions govern the first task. Do not treat open proposals as approvals.

These documents are initially on branch codex/product-docs-v0.1 in PR #1. Before implementation, check whether that PR has merged. If not, branch from its current head so the requirements are available; do not work from main without them. Never merge the documentation or implementation PR automatically.

## Working arrangement
The planning conversation defines requirements and prepares repository handoffs. The repository-connected Codex coding environment performs source feasibility, coding, tests, and technical QC as one development workflow. The owner reviews actual outputs and provides instructions and feedback. Record material iterations in DEVELOPMENT_FEEDBACK.md and link relevant code changes.

The earlier chat performed exploratory searches but did not commit a source register, establish automated collection access, or verify a deterministic extraction pipeline. No source should inherit verified status from that exploration.

## Task 001: first collection-to-review flow
Build a small, runnable local flow that collects permitted English-language source material, preserves evidence, surfaces transparent rule-based candidates, groups them by organization, and produces an inspectable local review output. Integrate source inspection into this task; do not substitute an unconnected research report for implementation.

The full product scope is Canada and Washington State. This first slice is intentionally small and must report its limited coverage. Working target, not a claim of representative coverage: inspect at least one Canadian local/community reporting source and one Washington local/community or funder source. Include a dated interview or podcast show-notes page if freely available and feasible. If access prevents this mix, document the gap and use synthetic cases to exercise the missing format. Never claim a show-notes page is a full transcript or evidence that audio was reviewed.

### Implementation sequence
1. Inspect the current repository and any applicable repository instructions. Choose a minimal local stack and document the rationale, prerequisites, and tradeoffs.
2. Create DEVLOG.md and a bounded task/checklist. Record actual work and dates, not manufactured history.
3. Inspect candidate source pages/formats and access conditions. Populate the source register in SOURCES.md or a linked data file. Distinguish manually readable, permitted automated access, and implemented/tested collection.
4. Define minimal organization, source, evidence item, candidate finding, rule trigger, and run-audit records. Namespace identifiers by source/jurisdiction. Unknown identity must remain unresolved rather than forced.
5. Implement collection with explicit network invocation, timeouts, failure reporting, incremental checkpoints, stable identifiers, and rerun deduplication. Offline examples and tests must not call the network.
6. Implement deterministic rules that surface candidate evidence passages with enough permitted context. Separate source facts, rule triggers, and reviewer interpretation. Do not invent fundraising diagnoses, consulting budgets, or introductions.
7. Produce a local review artifact or minimal interface grouped by organization, with source links, dates, triggered rules, unknowns, and coverage/failure details. A simple output is sufficient for this slice; the final dashboard remains a subsequent increment.
8. Allow local recording of the separate evidence-quality and relevance judgments defined in the PRD, using synthetic records for public demonstrations. Real feedback/output stays in ignored local paths.
9. Add meaningful synthetic fixtures and replay checks. Run them, inspect the output, and report exact results and limitations.
10. Open a reviewable implementation PR and give the owner exact run commands and concrete output to inspect. Pause for owner feedback before expanding source breadth or proceeding to later milestones.

### Acceptance checks
- A fresh checkout can run a documented synthetic collection-to-review example without network access or paid services.
- A live collection command is separate, explicit, and works on the bounded permitted sources, or reports specific access failures honestly.
- Each candidate includes stable ID, organization identity status, geography, source reference, publication/event dates or explicit unknowns, rule ID, and supporting evidence.
- Article age and event age are distinct. The 12-month discovery window uses an explicit run/as-of date; unknown dates are retained for review with visible status.
- Two stories about the same event do not silently count as independent corroboration. Matching ambiguity is visible.
- Every input item has a mutually exclusive final disposition. Counters reconcile, and a reconciliation error fails the run.
- Rerunning identical input does not multiply stored records. Failed sources do not advance successful checkpoints.
- Fixtures cover malformed input, absent dates, ambiguous organization identity, duplicates, irrelevant keyword matches, and an indirect clue with a plausible alternative explanation.
- Review output preserves contradictory/uncertain evidence and access to findings beyond any shortlist. No arbitrary quota discards findings.
- Private outputs, credentials, raw personal data, and restricted content are absent from tracked files.
- DEVLOG.md records changes and checks. DEVELOPMENT_FEEDBACK.md distinguishes actual owner feedback from assistant summaries and pending owner review.
- No runtime model calls, paid service dependencies, unsolicited outreach, account creation, or automatic merge.

## Product constraints
- Geography: Canada and Washington State; English only.
- Zero additional monetary operating cost. No paid subscriptions, hosting, APIs, or transcription; no automatic paid overages.
- Deterministic core, explicit human interpretation.
- Public organizational evidence only. Incidental person data and rights must be handled before storing raw content. Do not commit whole articles/transcripts merely because a page is readable.
- Initial discovery window: 12 months, with older records for comparisons. Recent six months gets priority only when evidence and relevance are comparable.
- Event/publication date, current status, relevance, and timing are separate.
- Daily local collection is the product requirement. First slice supports explicit runs and checkpoint/rerun behavior; OS scheduling is a later task because host OS and preferred time are not agreed.
- Weekly shortlist is an entry point. Human investigation may take multiple hours.
- Private pursuit choices and real commercial feedback stay outside public code and recorded sessions.
- No client donor analysis, campaign execution, or outreach.

## Not part of Task 001
Nationwide crawling, all-source adapters, a full funding graph, sophisticated ranking, full dashboard polish, OS scheduler installation, audio transcription, hosted deployment, productization, or external-program onboarding. Do not add an open-source license without owner selection.

No category exclusion or revenue cutoff is approved. Preserve these fields for later filtering without silently excluding organizations.

## Owner review checkpoint
Show the owner the actual review output and ask for feedback on:
- Whether candidate evidence warrants investigation.
- Missing context, alternative explanations, and incorrect identities.
- Important items omitted by the rules.
- Whether source context and organization grouping aid investigation.

Do not fill in owner judgments. Record pending review until feedback arrives. After feedback, revise prompts/instructions and implementation, rerun relevant checks, and link the before/after evidence in the development feedback log.

## Copy into Codex
> Read docs/CODEX_HANDOFF.md and the linked product documents on the documentation branch (or main if merged). Execute Task 001 on a new implementation branch. Integrate bounded source feasibility with a working deterministic collection-to-review flow, synthetic offline replay tests, reconciled audits, and development feedback traceability. Respect free-only operation and data boundaries. Open a PR with run commands, actual checks, limitations, and reviewable output. Do not merge or expand scope before owner review.
