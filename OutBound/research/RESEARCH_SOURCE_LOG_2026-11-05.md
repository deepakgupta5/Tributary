# Research source log: signal-generator design

**Research date:** 2026-11-05
**Related synthesis:** [Evidence review](SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md)

This log records the primary, research, and vendor materials inspected during the design review. `Used` means the source directly supports a conclusion in the synthesis. `Context` means it informed the analysis but was not necessary to the final recommendation. `Deferred` means it describes a later-stage technique that is deliberately outside the seven-day build.

## Government, standards, and official technical guidance

| Source | Disposition | Research use |
| --- | --- | --- |
| [CRA: How to get information about a charity](https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/information-about-a-charity.html) | Used | Separates current registration status from historical T3010 filing information. |
| [Government of Canada: 2023 List of charities](https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6) | Used | Confirms bulk identity and filing data availability. |
| [CRA: Information available from a T3010 return](https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/operating-a-registered-charity/information-available-public-a-registered-charitys-t3010-return.html) | Context | Defines the public filing boundary. |
| [IRS: Tax Exempt Organization Search](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search) | Used | US exempt-organization identity source. |
| [IRS: Public disclosure datasets and downloads](https://www.irs.gov/charities-non-profits/public-disclosure-datasets-and-downloads) | Context | Confirms official bulk data routes. |
| [IRS: Exempt Organizations Business Master File Extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) | Used | Official exempt-organization master data and monthly extraction context. |
| [IRS: Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads) | Context | Future financial and filing-history input. Not a daily signal source by itself. |
| [U.S. Census: Fellegi-Sunter record linkage](https://www.census.gov/library/working-papers/2000/adrm/rr2000-05.html) | Used | Supports links, possible links, and nonlinks instead of forced binary matching. |
| [NIST: Topic Detection and Tracking Evaluation Overview](https://www.nist.gov/publications/topic-detection-and-tracking-evaluation-overview) | Used | Separates first-story detection, topic detection, link detection, and tracking. |
| [NIST TREC: English Relevance Judgements](https://trec.nist.gov/data/reljudge_eng.html) | Used | Supports collection-specific relevance judgments and evaluated retrieval runs. |
| [W3C: PROV-O](https://www.w3.org/TR/prov-o/) | Used | Supports separation of source entities, processing activities, agents, derivation, and revision. |
| [NIST AI RMF Playbook: Measure](https://airc.nist.gov/airmf-resources/playbook/measure/) | Used | Supports production measurement, error tracking, input monitoring, and pre/post-deployment comparison. |
| [NIST: Challenges to monitoring deployed AI systems](https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation) | Used | Supports post-deployment monitoring for changing inputs and nondeterministic outputs. |
| [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) | Used | Supports conditional retrieval with ETag and Last-Modified validators. |
| [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) | Used | Caching and validation behavior for incremental collection. |
| [RFC 9309: Robots Exclusion Protocol](https://datatracker.ietf.org/doc/html/rfc9309) | Used | Standard crawler access convention and error/caching behavior. |
| [Google Search Central: Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) | Used | Supports feeds/sitemaps, accurate `lastmod`, canonical URLs, and ignoring `priority`/`changefreq`. |
| [Google Search Central: Troubleshoot crawling errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors) | Context | Supports failure visibility, server-aware crawl rates, and not resubmitting unchanged sitemaps repeatedly. |
| [Google SRE Workbook: On-Call](https://sre.google/workbook/on-call/) | Used | Supports actionable alert tiers and high signal-to-noise. |
| [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | Context | Additional operational alert-design guidance. |

## Peer-reviewed and research-conference material

| Source | Disposition | Research use |
| --- | --- | --- |
| [Elmagarmid, Ipeirotis and Verykios: Duplicate Record Detection, A Survey](https://archive.nyu.edu/jspui/handle/2451/27823) | Context | Documents missing common keys, transcription errors, incomplete information, and format variation in entity resolution. |
| [Murray: Probabilistic Record Linkage and Deduplication after Indexing, Blocking, and Filtering](https://www2.stat.duke.edu/~rcs46/linkage_readings/2015-Murray-Blocking-FellegiSunter.pdf) | Context | Supports blocking/indexing before pairwise comparison at larger scale. Not needed for the initial small universe. |
| [Bugert and Gurevych: Event Coreference Data from Online News](https://aclanthology.org/2021.emnlp-main.38/) | Used | Supports cross-document event identity and use of news hyperlinks as event-coreference evidence. |
| [Choubey and Huang: Automatic Data Acquisition for Event Coreference Resolution](https://aclanthology.org/2021.eacl-main.101/) | Context | High-precision rule acquisition for event pairs. Later-stage option. |
| [Örs, Yeniterzi and Yeniterzi: Event Clustering within News Articles](https://aclanthology.org/2020.aespen-1.11/) | Context | Pairwise event relationships followed by clustering. Later-stage option. |
| [Panagiotou et al.: First Story Detection using Entities and Relations](https://aclanthology.org/C16-1305/) | Used | Supports scalable detection of fresh events using entities and relations. |
| [Rodier and Carter: Online Near-Duplicate Detection of News Articles](https://aclanthology.org/2020.lrec-1.156/) | Used | Documents duplicate-induced analyst burden and high-precision online filtering. |
| [Tumre, Patil and Kumar: Near-Duplicate Detection for Aggregated and Paywalled News Feeds](https://aclanthology.org/2025.naacl-industry.73/) | Used | Supports metadata plus text similarity where only headlines/snippets are available. Deferred beyond simple week-one rules. |
| [Saito and Rehmsmeier: Precision-Recall for Imbalanced Datasets](https://doi.org/10.1371/journal.pone.0118432) | Used | Supports precision-recall and early-retrieval evaluation for rare positives. |
| [Language Models in the Loop: Incorporating Prompting into Weak Supervision](https://snorkel.ai/research-paper/language-models-in-the-loop-incorporating-prompting-into-weak-supervision/) | Deferred | Possible future method for combining noisy rules/prompts and abstentions. Requires labels and evaluation that do not exist in week one. |

## Commercial system documentation

These sources document product design and terminology. They do not independently validate vendor performance claims.

| Source | Disposition | Research use |
| --- | --- | --- |
| [LinkedIn: Activities that indicate Buyer Intent](https://www.linkedin.com/help/sales-navigator/answer/a1325209) | Used | Direct first-party engagement signals and identity visibility. |
| [LinkedIn: Sales Navigator Buyer Intent FAQ](https://www.linkedin.com/help/sales-navigator/answer/a507435) | Used | Aggregation of many recent activities at account level. Claims about response likelihood remain vendor claims. |
| [Bombora: Company Surge User Guide](https://customers.bombora.com/hubfs/%21MASTER_Bombora-Company%20Surge%20User%20Guide-January%202023.pptx%20%282%29.pdf) | Used | Account-specific historical baseline, event count, unique users, relevance, and engagement depth. |
| [Common Room: Go-to-market signals](https://www.commonroom.io/resources/signals/) | Used | Explicit distinction between high-intent direct behavior and lower-intent public company events. |
| [Crunchbase: Growth signal filters](https://support.crunchbase.com/hc/en-us/articles/38966398684691-Filter-your-searches-with-growth-signals) | Context | Separates evidence, categorized news, leadership events, and predictions. |

## Research gaps retained

- No controlled evaluation was found for a public-data nonprofit consulting-intent generator matching Tributary's scope.
- No source establishes that an operational nonprofit event implies budget, authority, or willingness to engage a consultant.
- Vendor effectiveness claims were not independently validated in this review.
- The review did not compare paid data providers because the product has a zero-additional-cost constraint.
- Operational usefulness must be evaluated from fresh runs, sampled source review, and owner decisions.
