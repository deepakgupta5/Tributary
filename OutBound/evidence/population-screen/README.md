# BC historical population reconciliation

Issue #9. Offline screen of archived CRA 2024 data. No collection or outreach enabled.

| Disjoint result | Records |
| --- | ---: |
| Input | 12,040 |
| Excluded: religious-organizations | 4,131 |
| Excluded: hospitals | 22 |
| Excluded: universities | 13 |
| Excluded: advocacy-groups | 2 |
| Retained size-fit | 551 |
| Retained enrichment | 345 |
| Remaining out-of-band / missing revenue | 6,976 |
| Reconciled total | 12,040 |

Historical pre-exclusion gates: **754 size-fit and 414 enrichment**, exactly reproducing 754/414. Category-first gates differ because D062 and the D065 activities decision remove 203 historical size-fit and 69 enrichment records. The historical numbers are not overwritten.

## Rules and limits

- Revenue band: CAD 1,000,000 through 5,000,000 inclusive. Staff proxy: permanent full-time positions plus part-time/part-year employees, 10 through 50 inclusive. A blank component remains unknown, never zero. This reproduces every saved band label.
- Category exclusions precede size disposition. Religion: CRA categories 0030–0090. Hospitals: 0100/0006, except a separately named hospital foundation. Universities: teaching institutions 0010 with subcategory 0015 or literal UNIVERSITY in the legal name, excluding school/daycare/foundation names. Colleges are not automatically excluded. Advocacy: literal ADVOCACY GROUP in the legal name plus the exact-ID D065 exclusion for PLAN.
- **D065 applies all 32 owner activities-review dispositions**: 1 excluded (PLAN, 131516320RR0001), 3 retained as service delivery (PACE, CYAC Kelowna, PeaceGeeks), 28 out-of-band records batch-resolved as moot for the pilot and held from buyer admission. Pending/reopened category reviews: **0**. Moot classifications reopen if a future screen moves the record in-band; changed identity/category evidence also reopens review. The category-review subset retains all reviewed rows as an audit, not just pending rows. [Owner authority D065](../../../decisions/DECISIONS.md) and [exact-ID decisions](../../data/bc-category-decisions-d065.json). This does not establish current eligibility. PACE operating status remains a downstream gate.
- Hospital auxiliaries and hospital foundations are not treated as hospital operators merely because HOSPITAL appears in their name. Religious-category foundations remain excluded as religious organizations.
- The recovered financial/staff file is a saved derivative, not newly fetched filings. It joins one-to-one on all 12,040 CRA IDs and matches the archived identification fields. Raw CRA financial/compensation rows are not in this archive, so the original derivative values cannot be independently audited from this input alone.
- These are historical size candidates. Current registry status, latest size, donor-base materiality, geography/form split and live triggers remain separate downstream gates. No account is qualified for outreach by this screen.

## Reproduce

```sh
python3 -m tributary.population_screen
python3 -m unittest discover -s tests -v
```

Category definitions: [CRA 2024 code list](https://open.canada.ca/data/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8/resource/e9f81074-9fc7-456f-8ce1-6fd101b77963/download/codes_en.pdf), section 2.3 (category/subcategory). Input hashes and machine counts: [reconciliation.json](reconciliation.json). All rows: [bc-population-2024.tsv](../../data/screened/bc-population-2024.tsv).
