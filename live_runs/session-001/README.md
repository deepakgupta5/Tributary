# Bounded live prototype session 001

Run date: 2026-11-05

Scope: supervised, noncommercial research; three service-delivery nonprofit candidates in British Columbia or Washington

Execution: one Codex assistant and one chat context across collection, data QC, researcher, skeptic, and fact-checker stages

This session exercises the existing workflow with live, bounded records. Separate, versioned packets and outputs provide traceability but not reviewer independence. Later stages could see earlier outputs. No whole article, report, dataset, audio, or transcript is committed.

## Source handling used in this run

| Source | Inspect | Record factual notes and links | Retain source text | Retain dataset fields | Result |
| --- | --- | --- | --- | --- | --- |
| IRS Washington EO BMF CSV | Yes | Yes | No whole file | Selected public fields for two exact rows | Approved for collection |
| CRA 2024 charity identification CSV | Yes | Yes | No whole file | Selected public fields for one exact row | Approved for collection; current status not established |
| Food Lifeline FY2025 impact report | Yes | Yes | No report prose or whole PDF | Not applicable | Approved for factual-note-only collection |
| South Seattle Emerald article | Yes | Yes | One short attributed checking passage; no whole article | Not applicable | Pending because routine copied-text handling was not established |

The two CSV downloads were temporary. Their URLs, byte counts, and SHA-256 hashes are recorded in `records.json`; the downloaded files were deleted after the selected fields and hashes were checked. The CRA file was accessible, so no CRA access failure occurred.

## Outcomes

- Food Lifeline and Nurturing Roots were admitted as organization candidates. Greater Vancouver Food Bank Society remains pending because the 2024 CRA row does not establish current status.
- The Food Lifeline visit-growth finding was approved: its first-party report lists 10,755,509 FY24 visits and 16,001,264 FY25 visits. The calculated increase is 5,245,755, approximately 48.77%. This does not establish unique people served, operational strain, budget, or buying intent.
- The Nurturing Roots finding remains pending. The local article supports the reported program, participant ages, and $85,260 funder relationship, but does not support the planted proposition that the award may pay outside operational or data consultants. The source's routine copied-text handling also remains unresolved.
- Reconciliation passed: 9 evidence items were unique, 0 duplicate, 0 quarantined, and 0 pending. Six of nine reviewed admission subjects were active; three remained pending.

These findings help identify and begin understanding prospects: the registers establish exact identities, while the report/article add scale or program context. They do not establish a need for services, purchasing authority, available consulting budget, or willingness to engage.

## Reproduce

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 live_runs/session-001/run.py --out /tmp/tributary-live-session-001
```

The runner refuses to overwrite an existing output directory. It validates the three-organization limit, bounded evidence retention, and the Food Lifeline arithmetic; saves the exact packet and output for every checkpoint; exports Markdown, JSON, and JSONL; and deletes its temporary SQLite database.

## Software checks performed

`python3 -m unittest discover -s tests -v` completed on 2026-11-05 with 58 tests passing in 3.713 seconds. The run completed with balanced candidate and active-stock reconciliation and no incomplete ingestion runs.

No live collection scheduler, dashboard, broad crawler, authenticated access, paid service, outreach, branch merge, or source-by-source policy subsystem was added.
