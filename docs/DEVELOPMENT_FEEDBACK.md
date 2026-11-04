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
