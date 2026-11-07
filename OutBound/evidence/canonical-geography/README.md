# Canonical BC geography and form stage

Applies D060 and owner boundary decision D066 to the retained Issue #9 population.

Input: **896 retained records**, comprising 551 historical size-fit and 345 staffing-enrichment records. The other population dispositions are not reconsidered by this stage.

| Disjoint route | Size-fit | Enrichment | Total |
| --- | ---: | ---: | ---: |
| corridor-funder-intermediary | 10 | 158 | 168 |
| pool-a | 231 | 92 | 323 |
| remote-funder-intermediary-monitor | 3 | 38 | 41 |
| remote-operating-monitor | 307 | 57 | 364 |
| **Total** | **551** | **345** | **896** |

## Interpretation

- Pool A is the in-corridor operating-organization research pool, with size-fit and incomplete-staffing records labelled separately. It is not an outreach-ready list.
- Foundations (CRA A/B) retain a separate funder/intermediary route regardless of geography. Their combined file includes corridor and remote rows; the route column distinguishes them.
- D066 explicitly includes Delta, Mission and White Rock. The remaining corridor is the D060 named localities, including Coquitlam. Aldergrove maps to the Langley routing area using the [Township community page](https://www.tol.ca/en/the-township/aldergrove.aspx).
- Canonical locality is a routing area. The source supplies historical mailing locality, not current operating address, service area or travel time. Langley and North Vancouver addresses do not distinguish City from Township/District. No one-hour driving-time verification is claimed.
- Case, punctuation and whitespace are normalized. Only explicit aliases are applied; no fuzzy matching. Unrecognized or blank localities and unknown CRA designations enter held-review. Prior category/admission holds are preserved.
- D065 remains applied: PLAN excluded before this stage; PACE retained only as a category disposition, with operating status still unchecked. The 28 moot out-of-band records do not enter the 896-record geography input.
- Current registry/operating status, donor-base materiality and live triggers are unassessed. Collection and outreach remain disabled. This stage performs no fresh collection or prospect enrichment.

## Outputs

- [All retained records and routes](../../data/geography/bc-geography-2024.tsv)
- [Pool A](../../data/geography/bc-pool-a-2024.tsv)
- [Funder/intermediary list, corridor and remote](../../data/geography/bc-funder-intermediaries-2024.tsv)
- [Remote/monitor, operating organizations and foundations](../../data/geography/bc-remote-monitor-2024.tsv)
- [Held geography/form review](../../data/geography/bc-geography-review-2024.tsv)
- [Per-locality reconciliation](../../data/geography/locality-reconciliation.tsv)
- [Machine reconciliation and input/rule hashes](reconciliation.json)

The funder list overlaps the remote list for remote foundations. Use the disjoint route table above when summing; do not add downloadable subset row counts.

```sh
python3 -m tributary.geography
python3 -m unittest discover -s tests -v
```
