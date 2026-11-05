# Day 2 batch collection

[First run](first-run.md) · [Repeat run](second-run.md) · [Source inventory](../../data/day2-sources.json) · [Checkpoints, attempts and evidence versions](state.json)

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
