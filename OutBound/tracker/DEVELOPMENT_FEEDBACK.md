# Development feedback record
Status: Product development record
Recorded: 2026-11-03

## Scope
This record contains owner-provided product feedback, resulting product changes, and actual validation evidence. Assistant opinions, assistant-to-assistant messages, review verdicts, task assignments, and execution prompts are excluded. All such communication passes through the owner in chat.

This documentation branch contains no approved implementation checks or development log. Future implementation records must identify checks actually performed. No hardware benchmark is required by current scope.

## Record fields
- Date and product area.
- Owner feedback, directly quoted or owner-approved.
- Affected requirement and decision reference.
- Resulting implementation or documentation change.
- Related commit.
- Validation actually performed and supporting artifact.
- Unresolved factual limitation.

Owner reasoning is recorded only when supplied by the owner. Synthetic fixture outcomes, actual source checks, and model/hardware measurements remain distinguishable.

## Owner decisions recorded
| Product area | Owner-provided feedback | Requirement record |
| --- | --- | --- |
| Geography | "Canada and Washington state" | PRD geography and D002. |
| Language | "English only" | PRD language and D012. |
| Cost | "everything ghas to be free...no paid subscruptions" | Cost constraint and D016. |
| Collection | "daily run" | Collection schedule and D023. |
| Human review | "I can spend multiple hours on this" | Review capacity and D024. |
| Collection/data QC | "data collection and data QC has to be seperate roles" | Research workflow and D028-D029. |
| Execution continuity | "Build everything as if you are running in Codex (the way I would run in Claude Code)" | D036 supersedes the earlier local-inference interpretation. |
| Repository communication | "no assistant-to-Codex instructions" | D034-D035. |
| Expanding registers | "even the list of non profits AND the daily source addition have to go through these 4 checks" | D039-D040; four checkpoints apply to all three record types. |
| Baseline deliverable | "one consistent baseline in the product documents, with open decisions explicitly identified. No unapproved numerical quality targets or source quotas." | D041-D042; PROJECT_PLAN.md and the PRD open-decision register. |
| Starting decisions | "agree on all three...lock them" | D043-D045: starting categories/no revenue cutoff, BC/Washington pilot, and design-only first delivery for review before implementation. |
| Instruction channel | "all instructions via me only", "in the chat" | D034-D035. |

These entries record product decisions, not paid-session ratings or a claim of software validation. Private commercial judgments, credentials, client data, and restricted source content are excluded.

## 2026-11-05: account visibility and review scale

- Owner feedback: "Greater Vancouver Food Bank is valid..it should have been included" and "I cant do this one by one...need to go wode".
- Requirement affected: discovered accounts remain visible independently of admission, signal review, and private commercial qualification; the default output must support organization-level review rather than requiring the owner to inspect audit records one by one.
- Change: added a compact Markdown and JSON account worklist. It separates discovery, identity, eligibility, signal review, and private business relevance. Greater Vancouver Food Bank Society appears in the worklist with verified historical identity and its current-status question visible. The detailed report and packets remain the audit trail.
- Branch: `codex/day-1-account-worklist`.
- Validation: 60 unit tests passed; the bounded live replay generated a 69-line worklist containing all three organizations, compared with the 573-line detailed audit report. JSON parsing and `git diff --check` passed.
- Limitation: this Day 1 output uses the existing saved live session. Fresh broad collection and signal generation begin in later days of the seven-day plan.

## 2026-11-05: evidence review and repository organization

- Owner feedback: "all research needs to be stored" and the repository should be structured using the useful operating separation from the Fractional repository, adapted to Tributary rather than copied literally.
- Requirement affected: external research must remain in the repository with sources, conclusions, evidence limits, and implementation implications. Operating material, run evidence, code, test data, decisions, examples, and owner-facing artifacts need clear homes.
- Change: added `OutBound/research/SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md`; incorporated its week-one implications into `OutBound/frameworks/PROJECT_PLAN.md`; organized current material into `OutBound/frameworks`, `research`, `evidence`, `tracker`, `data`, and `archive`; retained standard code/test roots; reserved `Library` for actual reviewable artifacts; removed empty Fractional-specific placeholder directories that had no Tributary function.
- Branch: `codex/day-1-account-worklist`.
- Validation: 60 unit tests passed. The moved bounded-live replay reproduced a 69-line worklist and 573-line audit report. All local Markdown links resolved, all committed JSON parsed, `git diff --check` passed, and the retained-file scan found no PDF, CSV, spreadsheet, or SQLite/database artifact.
- Limitation: the evidence review identifies transferable system practices and failure modes. It does not prove that any public event predicts nonprofit consulting purchases. Fresh operational runs and owner judgments remain necessary.
