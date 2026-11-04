# Workflow evaluation
Recorded: 2026-11-03
Status: Product specification. Actual checks and artifacts are recorded separately.

## Objective
Evaluate the collection, stored-evidence, researcher, skeptic, fact-checker, and report sequence in the coding environment. Codex is the initial environment; Claude Code can later continue from the same repository. Local model installation, MacBook benchmarking, and provider API integration are not prerequisites.

## Evidence categories
| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| Synthetic fixture replay | Record flow, stage ordering, validation, reproducibility, and known failure handling. | Model reasoning quality or live-source access. |
| Actual coding-session role outputs | What the assistant concluded from the supplied packet, with actor and limitations. | Independent reviewers, blind accuracy, or unattended operation. |
| Bounded live-source trial | Access, extraction fidelity, and usefulness for inspected sources. | Nationwide coverage or open-web completeness. |
| Daily operational run | Scheduling and recovery for the observed environment. | Continuous availability or automatic reasoning without an execution mechanism. |

## Synthetic cases
Known-answer fixtures include changed numbers, altered quotations, stronger paraphrases than their sources, hypotheses with benign alternatives, syndicated copies, ambiguous organizations, unknown dates, source revisions, stale reviews, inaccessible/absent evidence, and embedded hostile instructions treated as data.

The expected answers remain separate from role outputs. Every claim needs a source locator. Fact-checking covers all claims, including ones the skeptic did not flag. Missing checks and unresolved issues remain explicit. Comparison with hand-authored expected outputs tests the evaluator, not an AI model.

## Role contracts and provenance
Each stage records role, contract version, actor, execution ID, timestamp, execution basis, and a digest of its actual input. Model identity is recorded when available, otherwise explicitly unavailable. Separate output artifacts do not by themselves prove separate contexts or independent models. Same-session reviews must be labelled accordingly.

Research output contains a complete claim ledger, classified observations/attributed statements/hypotheses, source locators, and unknowns. Skeptic output contains ranked issues with affected claim IDs and remedies. Fact-checking covers every claim and every skeptic issue, with verification results, supporting passages, corrections, and unresolved limitations. New source or upstream versions reopen affected reviews.

## Measured outcomes
Record exact input/output counts, rejected records and reasons, duplicates, incomplete reviews, false passes, missed errors, and source failures with denominators where measured. A missing benchmark stays missing. Expected fixture verdicts are never reported as measured model accuracy. No numeric model-quality threshold has been approved.

## Retention and operation
Only permitted metadata and sanitized excerpts may persist from live sources. Whole synthetic documents are permitted test material. No paid service, credentials, hidden remote inference, or automatic charges are introduced. External program eligibility remains unconfirmed. Execution instructions and assistant code-review judgments stay in owner chat.

## Register expansion and reconciliation evaluation
Findings, organization additions, and source additions all pass the four checkpoints defined in RESEARCH_WORKFLOW.md. Tests distinguish candidate discovery from admission; a source inspection or organization name alone cannot confer approval. Cases include both discovery directions, identity ambiguity, source access/handling uncertainty, mergers preserving provenance, a required-check bypass attempt, unchanged records, and material revisions reopening affected checks.

Period accounting covers opening pending work, new discoveries, reopened versions, admissions, merges, blocked/excluded records, and closing pending work. Source attempts/retries are distinct from unique sources. PROJECT_PLAN.md defines delivery and data reconciliation and the seven-day/ongoing cycle. Actual observed counts are not quotas; no numerical quality threshold is treated as approved. PRD.md contains the single open-product-decision register.
