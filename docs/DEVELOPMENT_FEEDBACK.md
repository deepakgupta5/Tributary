# Development feedback record
Status: Product development record
Recorded: 2026-11-03

## Scope
This record contains owner-provided product feedback, resulting product changes, and actual validation evidence. Assistant opinions, assistant-to-assistant messages, review verdicts, task assignments, and execution prompts are excluded. All such communication passes through the owner in chat.

Actual implementation checks are recorded in DEVLOG.md. No hardware benchmark is required by current scope.

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
| Instruction channel | "all instructions via me only", "in the chat" | D034-D035. |

These entries record product decisions, not paid-session ratings or a claim of software validation. Private commercial judgments, credentials, client data, and restricted source content are excluded.
