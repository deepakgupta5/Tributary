# Day 2 batch collection

[First run](first-run.md) · [Repeat run](second-run.md) · [Source inventory](../../data/day2-sources.json) · [Checkpoints, attempts and evidence versions](state.json)

## Day 3 input and delivery

Use [state.json](state.json) for ordered attempts, original account keys, locators and evidence versions, and [day2-sources.json](../../data/day2-sources.json) for endpoint identity and handling. For pre-existing accounts use [Day 1 discovery records](../live_runs/session-001/records.json) and the [three-account housing pilot](https://github.com/deepakgupta5/Tributary/blob/4a8d611/OutBound/evidence/day-2/collection.json). Its [standalone parser](https://github.com/deepakgupta5/Tributary/blob/4a8d611/OutBound/evidence/day-2/seattle_awards.py) and run history remain on the pilot branch. The three housing names were seeded into Day 2. Their earlier awards belong to the pilot, outside the incremental batch totals.

Reproduce the saved baseline offline from the repository root:

```sh
mkdir -p out/day2-baseline
python3 -m tributary.collection_report OutBound/evidence/day-2/state.json 1 out/day2-baseline/first-run.md
python3 -m tributary.collection_report OutBound/evidence/day-2/state.json 2 out/day2-baseline/second-run.md
cmp out/day2-baseline/first-run.md OutBound/evidence/day-2/first-run.md
cmp out/day2-baseline/second-run.md OutBound/evidence/day-2/second-run.md
```

Day 3 deliverables are one account worklist with structured output, an ambiguous-match queue with specific missing evidence, and item-level reconciliation to all 35 inputs. Preserve the first discovery source. Separate identity rows from events, announcement dates from award dates, and recipient relationships from the shared announcement. Keep registry-only accounts visible, including Greater Vancouver Food Bank Society with current registration unchecked. A local Day 3 branch was prepared at `0d15b32`; the initial batch inspection and IRS name lookup produced no committed implementation or published PR as of this reconciliation.

## Continue live collection

From the repo root, copy the saved state to a working directory to continue. An empty directory starts a separate baseline.

```sh
mkdir -p out/daily
cp -n OutBound/evidence/day-2/state.json out/daily/state.json
python3 -m tributary.collect out/daily
python3 -m tributary.collection_report out/daily/state.json 3 out/daily/run-3.md
```

Use the one-based run number in the report command. Add `--advance` to the collection command to enable the next inventoried archive page. Normal runs revisit active sources. The saved batch is 1 of 2. The rolling 12-month window applies to dated events. The 2024 CRA dataset is separate historical identity evidence. Its public fields are attributed to the Canada Revenue Agency under the [Open Government Licence](https://open.canada.ca/en/open-government-licence-canada). Washington rows come from the [IRS](https://www.irs.gov/about-irs/use-of-content-from-irsgov).

The baseline includes the three Day 1 accounts and the three previously collected Seattle housing names at pilot commit `4a8d611`. New items count additions to this collection ledger. The food fund batch collects the announcement's named award recipients. A published recipient can be a program or a project with a fiscal sponsor. Official IDs anchor register rows; award-only entries are provisional. Exact known names link automatically, while aliases and legal-entity review remain open. The registry filter includes monitored IDs plus names containing “food bank” in selected cities. The procurement endpoint checks the latest 100 matching records, and the housing feed scans current publisher summaries for monitored housing names.

Every successful source stores its response hash and any HTTP validators. Each item uses a source-qualified row locator and keeps factual revisions. Failed and blocked attempts retain the last good checkpoint. The state file is atomically replaced under a single-writer lock. Raw bodies stay in process memory. Only public fields and attributed factual notes are saved. Python 3 and system curl suffice. The trial uses supervised source selection; no schedule is installed.
