# Development feedback log
Status: Active process; initial entries are requirements discussions, not paid-session records
Updated: 2026-11-03

## Purpose
Record how owner feedback, analysis, and revised instructions change assistant responses and the resulting product. This is a user-required repository practice. It is not a claim that an external program mandates this exact format.

The product remains deterministic. The assistant is used during development. Development feedback differs from private prospect judgments and external program response ratings.

## Entry requirements
Record material feedback near the relevant work, with links to issues, pull requests, commits, and checks where available. Keep unsuccessful attempts when they explain a decision. Do not manufacture iterations, backdate entries, or claim unperformed tests.

Distinguish direct owner statements, assistant-prepared summaries, proposed changes, and observed results. Owner reasoning must not be inferred or invented. Where a program requires unaided reasoning or ratings, the owner authors those independently in the required system; this log is not a substitute.

Do not copy full session transcripts, restricted task instructions, credentials, private commercial decisions, donor/client data, or private source material into this public log. Summarize permitted technical feedback and implementation evidence. If feedback cannot be published, record only a safe technical consequence or leave the entry private.

## Template
### FB-XXX: concise issue
- Date:
- Stage/task:
- Initial requirement or instruction:
- Observed response/result:
- Owner feedback: direct quote or clearly labelled summary.
- Owner rationale: owner-authored, or not recorded.
- Revised instruction/constraint:
- Change made:
- Verification and evidence:
- Outcome: improved, unchanged, regressed, or not yet verified.
- Remaining issue/next step:
- Related issue/PR/commit:

## Initial documented feedback
### FB-001: broaden discovery beyond positive announcements
- Date: 2026-11-03, recording date; discussion occurred before this entry.
- Stage/task: product definition.
- Initial requirement or instruction: discover nonprofit prospects and routes in.
- Observed response/result: early assistant proposals emphasized funding announcements and expansion.
- Owner feedback, assistant-prepared summary: include struggling nonprofits, existing-supporter and campaign improvement opportunities, and city/regional newspapers, media, and podcasts.
- Owner rationale, assistant-prepared summary of stated concern: organizations rarely announce fundraising problems; relevant context may emerge in local interviews.
- Revised instruction/constraint: discover indirect contextual observations, preserve alternative explanations, and avoid depending on explicit admissions.
- Change made: PRD, source coverage, roadmap, and decision log revised in PR #1.
- Verification and evidence: documentation changes are recorded in Git history; no implemented source trial or runtime extraction has been performed. Later exploratory chat browsing did occur; it did not verify collector feasibility.
- Outcome: product definition changed; discovery effectiveness not yet verified.
- Remaining issue/next step: test these requirements against permitted free English-language sources.
- Related PR: https://github.com/deepakgupta5/Tributary/pull/1

### FB-002: make development feedback traceable
- Date: 2026-11-03.
- Stage/task: development process.
- Observed response/result: assistant conflated product relevance feedback, runtime model training, and guidance of the coding assistant.
- Owner feedback, direct quote: "the data is HOW do I work at giving feedback, changing prompts, changing instructions to get better reposnse"
- Owner feedback, assistant-prepared summary: record this development feedback in the GitHub repository.
- Owner rationale: not separately recorded.
- Revised instruction/constraint: retain the development sequence from requirement through feedback and revised instructions to checked results.
- Change made: this log and associated process requirements added.
- Verification and evidence: repository documentation only; no external program requirement or acceptance is verified.
- Outcome: process documented; use in engineering remains to be demonstrated.
- Related PR: https://github.com/deepakgupta5/Tributary/pull/1

### FB-003: execute source trial inside repository-connected Codex
- Date: 2026-11-03, recording date.
- Stage/task: execution handoff.
- Observed response/result: the planning assistant began standalone web research after proposing a source trial.
- Owner feedback, assistant-prepared summary: the work should be performed by the repository-connected coding environment.
- Owner rationale: not separately recorded.
- Revised instruction/constraint: keep this conversation to planning, documentation, and handoff; integrate source inspection with implementation and owner review in Codex.
- Change made: CODEX_HANDOFF.md and roadmap sequencing updated; inconsistent pre-coding gates corrected during documentation review.
- Verification and evidence: documentation consistency review only. No implementation has begun here.
- Outcome: execution responsibilities clarified; product effectiveness not verified.
- Related PR: https://github.com/deepakgupta5/Tributary/pull/1

### FB-004: specify constructive skepticism and complete source checking
- Date: 2026-11-03, recording date.
- Stage/task: data-review design.
- Observed response/result: generic collection, data-QC, and verification roles lacked the owner's detailed review instructions.
- Owner feedback, assistant-prepared summary: start with an instructed researcher, pass its report to a contrarian but constructive skeptic, then have a fact-checker verify every number, quote, and paraphrase against the original document. Final output must flag verified and unverified material.
- Owner rationale: stated intended result is fewer errors with explicit verification flags.
- Revised instruction/constraint: add RESEARCH_WORKFLOW.md; give the fact-checker the full report and claim ledger as well as ranked issues, to avoid checking only flagged claims.
- Change made: role specifications linked from PRD, SOURCES, ROADMAP, CODEX_HANDOFF, and DECISIONS.
- Verification and evidence: documentation changes only; no implementation or runtime role execution performed.
- Outcome: instructions clarified; error reduction remains unmeasured.
- Remaining issue/next step: implement separate review handoffs in Codex without introducing runtime AI; semantic checks require actual human review under the current constraint.
- Related PR: https://github.com/deepakgupta5/Tributary/pull/1
