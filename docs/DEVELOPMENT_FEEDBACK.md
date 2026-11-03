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
- Owner rationale: explicit concern that organizations rarely announce fundraising problems; relevant context may emerge in local interviews.
- Revised instruction/constraint: discover indirect contextual observations, preserve alternative explanations, and avoid depending on explicit admissions.
- Change made: PRD, source coverage, roadmap, and decision log revised in PR #1.
- Verification and evidence: documentation changes are recorded in Git history; no source trial or runtime extraction has been performed.
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
