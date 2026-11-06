# Tributary: seven-day plan to a daily prospect worklist
Owner: Deepak Gupta
Status: Planning target, approved by the owner as a seven-project-day schedule on 2026-11-05. Start date unset.
Baseline: `codex/bounded-live-prototype-v1` at `a81f047`.

This plan replaces the earlier seven-day design and synthetic-foundation schedule in this file. Those milestones have been completed through a bounded live run. The current task is to turn that run into a repeatable daily research operation. Seven days are project days, not a guarantee of seven calendar days or nationwide source completeness. Day 7 succeeds on observed output, not elapsed time.

## Delivery status on November 5, 2026

Day 1 shipped at merge `30e5e03`. Day 2 is under review in [PR #4](https://github.com/deepakgupta5/Tributary/pull/4). The [first-run evidence](../evidence/day-2/first-run.md) measures discovery, and the [repeat-run evidence](../evidence/day-2/second-run.md) measures duplicate suppression. Day 3 resolution and reviewed identity relationships are in [PR #5](https://github.com/deepakgupta5/Tributary/pull/5). The Day 4 implementation on this branch provides [candidate signals and fresh collection results](../evidence/day-4/signal-report.md), with [reproduction and limitations](../evidence/day-4/README.md). It advances the next permitted backfill batch and separates older newly observed events from recent developments. Day 5 separate-role review and owner usefulness review remain pending.

## Objective and Day X

Tributary supports nonprofit business development for Autonomy Bridge. It finds potential clients and credible organizational routes in across Canada and Washington State. It surfaces dated evidence of operational, fundraising, campaign, or data-related pressure and opportunity, as well as funder-sponsored support. Deepak makes relevance and pursuit decisions privately. Tributary does not send outreach.

**Day X is the first operational daily cycle.** A local run produces:
1. New signal-bearing accounts, including candidates with visible unresolved checks.
2. New or materially changed signals at accounts already known.
3. A concise organization-level worklist: what happened, when, source links and locators, why to investigate (labelled interpretation), alternative explanations, unknowns, and a documented route in or "none identified."
4. A searchable account history and a private owner decision field: investigate, monitor, or dismiss.
5. A short run/coverage record distinguishing no findings from no successful collection.

A credible day can contain zero new accounts or zero new signals. No quota forces weak items into the worklist. The worklist is a research input for outbound, not a claim of need, budget, authority, or willingness to engage. Only supported, checked claims may be labelled verified. Open questions and uncertain but potentially relevant accounts remain visible.

## Corrections from the bounded live run

- Greater Vancouver Food Bank Society must appear in the account queue. The 2024 CRA record supports its identity at that date; lack of a current-status check is shown as an open field, not grounds to hide the account. Resolve current status when promoting a current-status claim. Preserve the original run and its decision history.
- Separate discovery, identity resolution, signal review, and private commercial qualification. An admitted organization is not automatically a prospect; a pending admission does not erase a discovered organization from the queue.
- The saved `OutBound/evidence/live_runs/session-001/run.py` replays saved records and assessments. It does not fetch new material or perform new reasoning. Day X must process fresh inputs from another run and must label supervised versus automated work honestly.
- The long audit report remains available behind the worklist. It is not the owner's default reading surface.

## Research-informed build constraints

The [signal-generator evidence review](../research/SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md) records the external research behind the implementation direction. It establishes design evidence and failure modes, not proof that a public event predicts a consulting purchase.

- Build an account-centered event monitor, not a buyer-intent predictor.
- Keep account, source document, event, signal assessment, action priority, and owner feedback as distinct concepts.
- Use current official registries for identity and eligibility where available; use annual filings as historical context rather than a freshness gate.
- Resolve duplicate documents and repeated coverage into events before producing owner-facing signals.
- Preserve source, publication date, retrieval time, locator, content hash, rule/version, and correction history.
- Collect broadly but alert narrowly through `act`, `investigate`, `monitor`, and `suppress` tiers.
- Use incremental per-source checkpoints and distinguish no change from collection failure.
- Measure worklist precision, duplicate leakage, resolution errors, freshness, source health, and owner review burden. Do not use generic accuracy as the principal measure.
- Defer predictive scoring, machine-learned ranking, unattended model verification, automatic outreach, and nationwide completeness claims.

## Delivery sequence

| Day | Build and research work | Evidence to inspect at day's end |
| --- | --- | --- |
| 1. Account and output correction | Implement the four distinct states above, show Greater Vancouver Food Bank in the account queue with its status gap, and produce a compact card and daily-worklist format from existing live records. Keep detailed packets accessible. | Existing three cases render without hiding pending accounts or treating a hypothesis as a fact. Diff and relevant regression checks. |
| 2. Broad source setup | Configure repeatable incremental collection from available official registers, funder/sector announcements, organization publications, procurement sources, and local reporting. Set up a source inventory spanning Canada and Washington, with geography/type, actual endpoint, access outcome, validator/checkpoint, and last successful check. Start a staged 12-month backfill without claiming unmonitored places are covered. | A fresh source attempt log and newly collected items beyond the saved three-case session. Unchanged, failed, blocked, and successful source outcomes remain distinct. Missing geographic/source-type coverage is visible. |
| 3. Account and event resolution | Extract organizations from collected items, connect exact official IDs where available, group aliases and suspected duplicates conservatively, and connect stories to existing accounts. Add basic document deduplication and event grouping so repeated coverage does not multiply signals. Discover new sources from organization research as well as organizations from sources. | Batch import and discovery counts reconcile. Unresolved identities remain in a possible-link queue. Rerun does not multiply accounts, source records, documents, or events. |
| 4. Signal generation | Convert fresh events into dated factual observations and candidate signals for all agreed categories. Track event, publication, first-seen, and retrieval dates separately. Record possible service relevance, alternative explanations, evidence of capacity to engage, and route in as separate fields. | New-account and existing-account signals from fresh material; unsupported consulting-budget, authority, willingness, or donor-retention inferences are not promoted as facts. |
| 5. Review and owner worklist | Apply collection/data QC and the existing researcher, skeptic, and fact-checker process to promoted findings and admissions. Render concise account cards with evidence quality and uncertainty. Assign `act`, `investigate`, `monitor`, or `suppress`, and preserve the owner's decision and reason across runs. | Source-faithful sample checked against original pages; every displayed number, quote, and paraphrase has a completed check or a visible pending label. Full audit remains retrievable. |
| 6. Daily execution and recovery | Add a local daily runner, per-source successful checkpoints, continuation after an interrupted batch, catch-up when the host resumes, and worklist export. Keep free-only operation and source access limits. Do not infer that the machine ran while off or asleep. | Successive run and identical-rerun tests, plus simulated missed day, partial source failure, and restart. Failed sources do not advance their successful checkpoints. |
| 7. Operational trial and correction | Run the daily cycle on new material, inspect the output with Deepak, repair material defects, and document actual source/geographic coverage and time spent on the supervised review step. Deliver the first usable worklist and a prioritized expansion backlog. | One fresh daily worklist, linked account histories, run/coverage report, test log, known defects, and Deepak's actual usefulness feedback if available. Replay of session 001 alone does not pass. |

Days 2–5 can overlap where independent source setup, output design, and tests permit it. A blocked endpoint does not stop other accessible sources. Scope is broad by geography and source type, but coverage is reported from successful checks rather than inferred from the intended universe.

## Minimum daily worklist contract

Each row/card carries: stable organization ID and name; official ID if known; headquarters and area served as distinct fields; new account or changed existing account; event and publication dates; signal category; factual observation; source URL and locator; possible relevance as a hypothesis; alternative explanation; evidence quality and review status; missing facts; documented funder/intermediary route, if any; prior-account history; and next investigation action. The organization appears once even if several stories support it. An export usable for manual outbound preparation accompanies the review view, but private pursuit data and messages stay out of the public repository.

Lists must distinguish **newly discovered**, **newly signal-bearing**, and **already known with a new signal**. A charity-register row alone may establish an identity or create a candidate, but it is not by itself a commercial signal.

## Acceptance checks and reconciliation

- Fresh live inputs flow from collection to account matching, signal candidates, checked findings, and the daily worklist. The saved assessment replay remains a regression fixture only.
- Every collected item has a disposition: unique, duplicate, or quarantined, with pending work explicit. Candidate organizations and sources reconcile to their current states; a pending review does not make a candidate disappear.
- A sampled worklist is checked against original source pages for identity, dates, numbers, paraphrases, and alternative explanations. Incorrect matches and unsupported claims are corrected or visibly held. Same-assistant checks are labelled as such, never independent verification.
- A rerun is idempotent. Changed evidence reopens affected checks. A missed day and partial source failure are visible and recoverable where source history permits.
- Report configured, attempted, and successful sources by geography and type; do not claim completeness across Canada or Washington from a narrow sample. Measure useful items, missed relevant items in a sampled source set, duplicates, false matches, and owner review time without inventing pass percentages or quotas.
- Day X is reached only when the daily cycle produces a usable fresh worklist and the operational checks above pass. If owner usefulness review is unavailable, record that separately; do not fabricate it.

## Execution boundary and operating model

Zero additional monetary operating cost remains the constraint. Use English-language freely accessible sources; do not bypass access controls. Store source links, metadata, factual notes and necessary permitted short checking passages, not whole live articles, recordings or transcripts. Record specific restrictions found rather than presume all public research is blocked.

Current coding-session reasoning is supervised. A scheduled local collector may gather and organize candidates, but the repository does not yet provide an unattended model reviewer. The Day X worklist therefore distinguishes automatically collected candidates from supervised, checked findings. If a daily supervised pass is necessary, measure its actual time and report when it was skipped. Do not represent unreviewed candidates as independently verified or outbound-ready.

After Day X, continue daily collection and worklist generation, weekly owner feedback and source/geographic expansion, and weekly reconciliation of coverage, missed signals, duplicates, and review backlog. Prioritize demonstrated prospect usefulness over register size or checkpoint volume.
