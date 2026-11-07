# BC historical population reconciliation

Issue #9. Offline screen of archived CRA 2024 data. No collection or outreach enabled.

| Disjoint result | Records |
| --- | ---: |
| Input | 12,040 |
| Excluded: religious-organizations | 4,131 |
| Excluded: hospitals | 22 |
| Excluded: universities | 13 |
| Excluded: advocacy-groups | 1 |
| Retained size-fit | 552 |
| Retained enrichment | 345 |
| Remaining out-of-band / missing revenue | 6,976 |
| Reconciled total | 12,040 |

Historical pre-exclusion gates: **754 size-fit and 414 enrichment**, exactly reproducing 754/414. Category-first gates differ because D062 now removes 202 historical size-fit and 69 enrichment records. The historical numbers are not overwritten.

## Rules and limits

- Revenue band: CAD 1,000,000 through 5,000,000 inclusive. Staff proxy: permanent full-time positions plus part-time/part-year employees, 10 through 50 inclusive. A blank component remains unknown, never zero. This reproduces every saved band label.
- Category exclusions precede size disposition. Religion: CRA categories 0030–0090. Hospitals: 0100/0006, except a separately named hospital foundation. Universities: teaching institutions 0010 with subcategory 0015 or literal UNIVERSITY in the legal name, excluding school/daycare/foundation names. Colleges are not automatically excluded. Advocacy: literal ADVOCACY GROUP in the legal name.
- **32 unresolved category clues** remain explicitly marked in the dataset and category-review subset. CRA has no general advocacy-group category. Advocacy in a service-provider name and a human-rights purpose alone do not establish an advocacy-group buyer. Those rows are held from buyer admission pending activities review. Organizations without such clues can still be misclassified; this is a deterministic historical screen, not a completed current-eligibility review.
- Hospital auxiliaries and hospital foundations are not treated as hospital operators merely because HOSPITAL appears in their name. Religious-category foundations remain excluded as religious organizations.
- The recovered financial/staff file is a saved derivative, not newly fetched filings. It joins one-to-one on all 12,040 CRA IDs and matches the archived identification fields. Raw CRA financial/compensation rows are not in this archive, so the original derivative values cannot be independently audited from this input alone.
- These are historical size candidates. Current registry status, latest size, donor-base materiality, geography/form split and live triggers remain separate downstream gates. No account is qualified for outreach by this screen.

## Reproduce

```sh
python3 -m tributary.population_screen
python3 -m unittest discover -s tests -v
```

Category definitions: [CRA 2024 code list](https://open.canada.ca/data/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8/resource/e9f81074-9fc7-456f-8ce1-6fd101b77963/download/codes_en.pdf), section 2.3 (category/subcategory). Input hashes and machine counts: [reconciliation.json](reconciliation.json). All rows: [bc-population-2024.tsv](../../data/screened/bc-population-2024.tsv).
