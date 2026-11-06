# Day 5: reviewed daily worklist

[Worklist](worklist.md) · [Structured cards](worklist.json) · [Full observation and follow-up ledger](observations.json) · [Fact checks](fact-checker.json) · [Test log](tests.txt)

## Result and baseline

`origin/main` was fetched and confirmed to equal `1002f1dea10e1b412595ce789236c8f0a3a5d862`, containing merged Days 2–4. Day 5 uses a clean branch from that commit in the isolated checkout. The original feasibility checkout and its uncommitted files were untouched.

The six Day 4 non-award observations were reviewed against all five original pages, with fresh direct retrieval metadata and response hashes. One mixed-source Surrey observation was corrected: the December source cannot support the June donation statement. That statement remains separately linked to June 11. The original Day 4 snapshot remains unchanged. Two bounded Surrey follow-up observations were added. Eight observations form four account cards: Act 0, Investigate 1, Monitor 3, Suppress 0. Unsupported interpretations are withheld separately; no valid account was removed because its service relevance is uncertain.

Surrey's comparable demand and donation evidence ends on June 11, 2026. Newer information includes an October recruitment posting and a local partner's report of food distribution at Delview. These do not establish later demand totals, donation adequacy or a distribution shortfall. The Delview item's year is inferred from the site's dated 2026 sequence; the Surrey operator link needs primary confirmation. Mirrors suggest a link but are not independent corroboration. The checked official locations page does not list Delview. The dated recruitment posting establishes an advertised search, not the state of the appointment today. An October article and recruitment financial figures refer to the annual report covering October 1, 2024 through September 30, 2025, rather than post-June 2026 outcomes. These distinctions remain visible in the worklist and audit.

## Review and provenance

The recorded process is collection/data QC, researcher, skeptic, then fact-checker. Exact versioned inputs are in [packets](packets/); outputs are [collection QC](collection-qc.json), [researcher](researcher.json), [skeptic](skeptic.json) and [fact-checker](fact-checker.json). Each output binds to the full input packet and prior outputs. Each observation has a stable ID, original fact where corrected, source URL/locator, source version, separate publication/event/first-seen/retrieval dates and a claim ledger. The fact-checker covers every claim, not only the skeptic's issues, and records dispositions for every issue. Three additional context checks establish the report period and limited observations about the checked official pages.

These are supervised same-assistant role passes with shared session context. They do not establish independent human corroboration or enforced role isolation. Source-faithfulness is distinct from independently confirming publisher statements, identity admission, current need and private commercial relevance. No new organization or routine-source admission is granted. Material Delview attribution gaps remain pending. Current consulting budget, authority and willingness remain unknown.

Only links, metadata, hashes, factual notes and short permitted checking context are retained. Whole HTML/PDF responses were processed transiently and not stored. The GVFB first-party hold remains in place; this increment did not use that held content. Source checks are bounded inspections, not a new recurring crawl. The [Day 4 coverage record](../day-4/pressure-report.md) remains the wider account search audit; this delivery rechecked its six findings and Surrey follow-up, not all 39 accounts.

## Reproduce the public worklist

From the repository root:

```sh
python3 -m tributary.daily_worklist build --out out/day5
cmp out/day5/worklist.md OutBound/evidence/day-5/worklist.md
cmp out/day5/worklist.json OutBound/evidence/day-5/worklist.json
python3 -m tributary.daily_worklist build --out out/day5
python3 -m unittest discover -s tests -v
```

This replays frozen supervised review records. It does not fetch sources, redo model reasoning or claim that an old review is fresh. Changed observations, sources or predecessor reviews invalidate the bound checks and require a new review. Unchanged reruns produce byte-identical public outputs and one card per account.

## Private owner feedback

Public builds never open the private feedback database and never export owner reasons. No actual owner decision was invented for this delivery. Feedback is separate from evidence quality and the recommended action tier.

A private append-only SQLite journal defaults to `out/private/owner-feedback.sqlite`, which is ignored by Git. Set `TRIBUTARY_FEEDBACK_DB` to an existing durable local database path when using multiple checkouts. Do not delete that database when cleaning a checkout. An existing database is opened without truncation. SQLite is a local single-user data store, not encrypted storage.

Record a real decision explicitly, using a card's account ID:

```sh
python3 -m tributary.daily_worklist feedback ACCOUNT_ID monitor --reason 'Your private reason' --worklist out/day5/worklist.json
python3 -m tributary.daily_worklist build --private --out out/day5-private
```

Supported owner decisions are `investigate`, `monitor` and `dismiss`. Identical repeated decisions do not append duplicate journal rows. Private views preserve decisions and reasons across process/database reopen; a changed evidence fingerprint retains the old decision but flags it for re-review and uses the current recommended tier until reviewed. Dismissal suppresses a card only in the private view. It does not delete the account or alter the public report. Private exports must be outside the repository or under an ignored directory, so they cannot overwrite the public evidence report. Newly created database and private output files receive owner-only file permissions.

## Validation and remaining daily-use gap

All 90 tests pass. Reproduction and a repeat build produce identical files and four unique cards. Tests reopen the database with synthetic decisions, verify preservation without duplicate history, flag changed evidence, reject stale or incomplete reviews, check full claim coverage, and confirm private reasons do not appear in public Markdown or JSON. Actual owner relevance/usefulness judgments remain unmeasured.

The worklist can be used now for manual investigation and outbound preparation. No Act item is established. Day 6 still needs a fresh non-award runner, per-source recovery and catch-up integration, and an explicit supervised-review step. Scheduling is not installed. Saved-review replay cannot substitute for fresh daily collection and reasoning. Broader geographic/source coverage and the Day 7 separate-day usefulness trial remain open. No outreach, login, paid dependency or automatic sending was added.
