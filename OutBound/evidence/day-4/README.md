# Day 4: candidate signal generation

[Readable signal report](signal-report.md) · [Structured output](signals.json) · [Fresh checkpoints](state.json) · [Repeat checkpoints](repeat-state.json) · [Tests](tests.txt)

Based on Day 3 PR #5, commit `c21b34f7de1f92668ecf05317b78df6b1036300b`. Its PRD, seven-day project plan, signal-generator evidence review and recipient identity findings govern this increment. No Day 4 branch or PR was present before execution. The original local feasibility checkout and its uncommitted files were preserved. Execution used an isolated checkout because this session could not write to the original checkout.

## Observed result

Collection ran on November 5, 2026 in Vancouver, November 6 UTC. It resumed the saved Day 2 checkpoints and advanced batch 1 to the next permitted batch, 2 of 2. Six sources were successfully checked, four unchanged and two parsed; GVFB publication remained held under the existing terms decision. Five housing recipient rows were added. Twenty-three food-recipient rows were duplicates, with no changed recipient facts despite a changed page response hash.

The earlier housing pilot already contained Bellwether Housing, Chief Seattle Club and Compass Housing Alliance and their three awards. The [frozen pilot metadata](pilot-baseline.json) is copied from `4a8d611`'s `OutBound/evidence/day-2/collection.json`, rather than inferred from seeded account names. This avoids counting those awards twice. Solid Ground and Plymouth Housing Group are two new candidate accounts with two newly observed awards. Both were announced February 6, 2026; neither is a recent development. Award dates and current operating status remain unknown. This bounded run establishes zero current candidate investigation reasons. It does not establish that no current needs exist.

The repeat run started from the newly saved checkpoints. All six accessible sources were unchanged, GVFB remained held, and no rows, accounts or events were added or revised. Reconciliation includes 40 collection items, 12 identity rows and 28 event evidence rows, mapped to 28 events. Three of those events also have pilot evidence.

## Implementation and limits

`tributary.signals.build` resolves current collection records against the Day 3 identity ledger and earlier pilot. Stable Day 3 IDs and relationship roles survive. A fundraising host's EIN stays on the relationship. Operating-entity and program-parent identifiers carry an explicit role and entity name. All award payees remain unknown. Registry-only accounts remain visible without generating signals.

`tributary.signals.assess` is a deterministic typed-event rule interface for all six agreed signal categories: fundraising pressure, campaign improvement, financial pressure, operational strain, new commitments and sponsored support. Named event classes and aliases cover the week-one event taxonomy. The optional `--event-inputs FILE` accepts `current` and `baseline` arrays of typed observations for these categories. Each row requires `account_id`, `event_type`, a stable `event_reference`, `fact`, `url`, `locator`, nullable `event_date` and `publication_date`, and timezone-aware `first_seen_at` and `retrieved_at`. Unknown accounts/types and repeated references are rejected. The baseline array prevents a carried-forward observation from becoming a new event each run. All imports remain candidates with pending checks; this delivery used no supplemental typed observations. Each assessment separates observations, relevance hypothesis, alternative explanation, capacity, access route, missing facts, contradiction-check state and candidate review state. Rule/evidence hashes identify assessment versions. No approval is inherited after changes.

The current live adapters extract award events, registry identity rows and contextual housing-feed mentions. Rules for other event classes are implemented and tested, but this run did not collect examples of every category. There is no general prose classifier or unattended reviewer. A feed mention without a typed substantive event remains unclassified context. Source titles not captured by the collector remain explicitly unknown. Repeated documents do not constitute independent corroboration.

Event date takes precedence over publication date for recency; missing event dates are retained rather than replaced with publication dates. First-seen and retrieval times stay separate. The PRD's recent-six-month review priority supplies the `recent_development` bucket. This is an explicit candidate-context rule, not an exclusion cutoff, proof of ongoing need or a validated commercial predictor. Older material stays in the monitoring ledger and needs a current-status check before promotion. No `act` output, purchasing intent or donor-retention claim is established.

Separate researcher, skeptic and fact-checker execution remains Day 5 work. These outputs are candidates, not independently verified findings. A same-assistant direct source inspection confirmed the five displayed housing award amounts and program context against the live award table. This source-faithfulness check does not verify current conditions, legal payees, eligibility or commercial relevance, and does not substitute for the separate review workflow. No owner usefulness judgment or prospect pursuit decision is recorded. Outreach stays manual.

No whole live pages are stored. Fresh response bodies were transient in collector memory; persisted evidence contains selected organization-level facts, links, locators, hashes and attempt metadata. Coverage remains selected BC/WA English-language sources. Other Canadian jurisdictions, local reporting, sector publications and complete procurement/archive coverage remain gaps. Batch 2 exhausts only this inventory's two pages, not every available historical source. No schedule or paid dependency was added.

## Validation

All 77 unit tests pass. They cover live-delta reconciliation, pilot-event deduplication, historical and missing dates, unsupported capacity inferences, identity relationships, repeated runs, changed facts, typed events at known accounts and failed-source checkpoint preservation. Offline regeneration reproduces both signal files byte-for-byte. The live repeat yields zero new or materially changed events. Tests do not establish source completeness or owner usefulness.

## Reproduce offline

From the repository root:

```sh
python3 -m tributary.signals OutBound/evidence/day-4/state.json out/day4-reproduce --baseline OutBound/evidence/day-2/state.json --as-of 2026-11-06
cmp out/day4-reproduce/signals.json OutBound/evidence/day-4/signals.json
cmp out/day4-reproduce/signal-report.md OutBound/evidence/day-4/signal-report.md
python3 -m tributary.signals OutBound/evidence/day-4/repeat-state.json out/day4-repeat --baseline OutBound/evidence/day-4/state.json --as-of 2026-11-06
python3 -m unittest discover -s tests -v
```

## Continue collection

Start from these checkpoints rather than an empty directory:

```sh
mkdir -p out/day4-next
cp -n OutBound/evidence/day-4/repeat-state.json out/day4-next/state.json
python3 -m tributary.collect out/day4-next
```

Then generate signals against the previous state, with the UTC as-of date of the new run. `--advance` was already applied in this delivery; there is no batch 3 in the saved inventory. Source failures retain their prior successful checkpoints. Live commands require working network access. The MacBook's connected local runtime supplied that access in this session; the restricted shell could not resolve external hostnames.
