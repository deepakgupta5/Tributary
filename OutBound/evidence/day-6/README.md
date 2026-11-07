> Latest: [November 7 manual recovery and reviewed worklist](../daily-2026-11-07/README.md). The counts below describe earlier Day 6 proofs, not the latest run.

> Superseded attention counts: the raw-candidate view below is historical collection evidence. The [source-reviewed worklist](source-review/repeat/worklist.md) is now the owner publication. Nine flag dispositions reduce owner attention from 6 to 0. See [source-review proof](source-review/README.md).

# Day 6: live daily command and recovery

[Live worklist](live/worklist.md) · [Immediate repeat](repeat/worklist.md) · [Run verification](verification.json) · [Recovery proof](recovery-proof.json) · [Schedule status](schedule-status.json) · [Tests](tests.txt)

## Baseline and Day 5 merge

PR #7 was reviewed against the Day 5 contract. Its source-faithfulness limits, pending Surrey attribution, four-tier cards, claim accounting, private feedback and repeated-output behaviour remain explicit. A clean clone at `de4c85227e5f37f36e306049fa8f2f695bec8240` passed all 90 tests. PR #7 was merged at `eb295bb9181cea6922608c94d023d17fa4d408ba`. Fetched `main` contains `de4c852`; this branch starts from that updated main. [Merge/review record](day5-review.json). The original local feasibility checkout's uncommitted files were untouched.

## One Mac command

From the operating checkout:

```sh
python3 scripts/run_daily.py
```

The command performs fresh free-source collection, account discovery, non-award candidate extraction, review handoff and dated public worklist export. It uses Python's standard library and system curl. It makes no model/provider API calls, sends no outreach, performs no login and does not commit or push results automatically.

Runtime state is in ignored `out/daily/state.json`. Dated exports are under `out/daily/runs/LOCAL-DATE/TIME/`; `out/daily/latest/worklist.md` points to the newest local result. A single-writer lock serializes overlapping triggers. Atomic state replacements after each source preserve completed work on interruption; an interrupted invocation resumes pending sources. Successful source checkpoints survive failures. Dates and identity aliases come from the prior ledgers, not a newly invented account list.

Existing Day 2/4 registry and announcement checkpoints are reused for account discovery. The new inventory supplies four organization publication feeds and a local-news feed, plus the selected Day 4 account pages and exact Day 5 evidence pages. Together this is 57 deduplicated endpoints for the 39-account universe. Giving-directory/identity pages are bounded checks, not comprehensive organization-news coverage. Other Canadian jurisdictions, source types and unexposed history remain gaps. New exact-ID registry rows can create candidates; registry rows do not create commercial signals. Existing aliases resolve against Day 3 IDs. No fuzzy auto-merge or new current-status admission is claimed.

## Actual live result

The manually executed release-candidate run on November 5, 2026 in Vancouver produced:

| Result | Count |
|---|---:|
| New accounts | 0 |
| New non-award signal candidates | 5 |
| Changed signal candidates | 0 |
| Newly observed older/undated candidates | 3 |
| Historical-source rechecks | 4 |
| Unique cards requiring attention | 6 |
| Current pending review tasks | 9 |

The five new candidates come from four documents: undated FamilyWorks and Good Business Network of Washington giving pages; a March Clark County publication; and an October 20 Food Lifeline publication matching two categories. The two October category matches are one document, not two independently corroborated events. The giving pages and March item are older/undated context, not fresh developments. Both giving-page organizations were already known accounts, so their first signal appearance does not count as a new organization.

These are deterministic review proposals. The notes identify potential fundraising pressure, campaign performance, financial pressure and operational strain; they do not assert an unmet need or consulting intent. Source text is processed transiently; only URLs, dates, selected organization-level notes and content fingerprints are retained. Relevant-text hashes avoid retaining incidental personal details. No whole pages or feed bodies are saved. Original event/publication dates remain distinct from first-seen/check times. Historical Day 5 observations are explicitly carried forward and are not described as newly occurring today.

Live source outcomes: 50 success, 2 unchanged, 3 blocked, 1 failed and 1 held. The CRA request timed out. The procurement endpoint is excluded by robots; one selected account page returned HTTP 403 and another source's robots file returned 403. GVFB first-party handling remains held. A blocked or failed source is never counted as no change or no findings. These are actual coverage gaps, not evidence of absent need.

## Immediate repeat and recovery

The immediate real repeat produced 0 new accounts, 0 new candidates and 0 changed candidates. Its six card IDs, signal IDs/versions and review-task IDs match the first run. Nine current pending reviews remain pending; a repeat cannot erase an unresolved review obligation. Feed and page coverage attach to one candidate ID with source-specific fingerprints, preventing duplicate coverage from oscillating versions. Superseded review tasks remain in history but do not multiply current pending work.

[Recovery](recovery-proof.json) uses a copy of real persisted state. An HTTP 503 and a missed-run bookmark are deliberately injected and labelled as simulation. The failed attempt preserves the prior successful checkpoint. A subsequent real request to the Compass feed returns HTTP 304, advances its successful check, and adds no accounts or candidate versions. Production state is not modified by this proof. The missing date is a simulated bookmark, not a claim that a real day was missed. Feeds/archives are bounded, so catch-up does not promise every missed publication is recoverable.

For a current local recovery demonstration after a live run:

```sh
python3 OutBound/evidence/day-6/recover.py
```

The saved proof references this development session's `out/operations-v2` state. On another checkout, supply/copy its actual live state rather than representing the saved snapshot as a new live run.

## Review and private decisions

`review-queue.json` contains stable claim/candidate IDs, evidence versions, sources and review status. New or changed evidence stays pending for researcher, skeptic and fact-checker review. No unattended factual approval is added. Exact unchanged previously reviewed documents can retain their old review; changed documents or failed/missing checks reopen the relevant current check. Raw response changes can conservatively trigger rechecking even if an editor or advertisement changed rather than the substantive claim. The worklist labels this as a source recheck, not an established material claim change.

Private owner feedback uses the Day 5 append-only SQLite journal. `TRIBUTARY_FEEDBACK_DB` or `--feedback-db` selects the existing file; the local wrapper also reads the ignored `out/schedule/config.json`. In this session it points to the prior Day 5 checkout's journal path. No existing decision was overwritten or fabricated. If no journal exists, public collection runs without creating fake owner feedback.

Private reasons appear only in ignored `out/daily/private-latest`; public exports never include them. Decisions apply only when the current card fingerprint matches the reviewed fingerprint. Changed evidence or uncertain current checks preserve the old decision in history and flag it for re-review instead of silently reusing it. A public candidate tier is not an owner pursuit decision.

## Scheduling status and blocker

The zero-additional-cost local runtime is built and manually tested. **Native Mac scheduler registration is not verified.** The managed shell denies `crontab` access. A valid local launchd plist was generated and passed `plutil`, but `launchctl bootstrap` exited 5, and a subsequent `launchctl print` confirmed no job with the Tributary label. The Codex app's local automation API also failed. None of these attempts is described as installed.

A daily morning app automation was successfully registered as a fallback, around 08:05 America/Vancouver. The scheduler returned inherited environment selection with no explicit Mac binding. A manual `run_now` invocation was executed inline on the Mac; the `--scheduled` guard correctly skipped collection because a manual collection had already completed that day. This proves the local guard, not a later clock-triggered execution or future Mac access. No later scheduled collection has been observed. [Exact status](schedule-status.json).

`python3 -m tributary.schedule` provides a native persistent user-crontab installer, preserving unrelated entries and verifying registration. It needs to run in an ordinary local Terminal session with scheduler access, outside this managed restriction. Its hourly minute-05 trigger invokes the daily guard: one collection per Vancouver date at/after 08:00, at the next available trigger if the Mac was asleep. It makes no automatic model calls. Until native registration succeeds, the requested Mac-resident schedule remains a blocker; the app fallback's future Mac access is unverified.

The alternate `python3 -m tributary.launchd_schedule` registers a current-login job when allowed. Its plist remains in the writable checkout. It does not install reboot/login auto-loading, and the code explicitly reports that limitation. No protected LaunchAgents or system spool files were edited directly, and no permission bypass was attempted.

## Validation and readiness

109 tests pass, including all four signal categories, HTML entities/empty feeds, registry discovery, same-page multi-source deduplication, changed-evidence invalidation, failure checkpoint preservation, missed-date catch-up, restart, Vancouver-time scheduling guards, private-feedback isolation and non-duplicating cards. The real live/repeat and controlled-failure/live-recovery records accompany the tests. Owner usefulness judgments and a separate-day operational trial remain Day 7 work.

Day 6 is **partially delivered**: the local command and live/repeat/recovery proofs are published; native scheduler registration is blocked. Remaining blockers to unattended daily use are native scheduling/Mac access, currently blocked/failed source coverage and the explicit supervised-review step. The public worklist can be used now to decide what to investigate. It is not an automatically cleared outreach list. Outreach remains manual.
