# Evidence review: nonprofit account and signal generation

**Research date:** 2026-11-05
**Decision context:** Build a useful daily account and signal worklist within seven project days, while preserving an architecture that can improve from observed results.
**Product boundary:** Tributary supports private nonprofit business-development research for Autonomy Bridge. It does not establish buyer intent, purchasing authority, consulting budget, or willingness to engage unless direct evidence supports those claims.

## Executive conclusion

The week-one product should be an account-centered event monitor with a narrow action queue. It should produce:

1. newly discovered nonprofit accounts;
2. new or materially changed events associated with known accounts;
3. evidence-backed commercial hypotheses with explicit unknowns; and
4. a short `act`, `investigate`, `monitor`, or `suppress` queue.

Public news, filings, organization publications, funder announcements, procurement notices, and local reporting can establish organizational change and context. They usually do not establish buyer intent. Commercial intent systems reserve their strongest signals for direct behavior such as company-page or website visits, ad engagement, pricing activity, product usage, or outreach response. Public company events are commonly treated as contextual or lower-intent signals.

The design should separate collection, account resolution, event resolution, signal assessment, action priority, and owner feedback. The Greater Vancouver Food Bank error demonstrated why: current identity, historical financial context, a current event, possible service relevance, and ability to buy are different questions.

## Evidence standard used in this review

| Evidence class | How it is used |
| --- | --- |
| Government and standards documents | Authoritative support for registries, provenance, retrieval, monitoring, and evaluation practices. |
| Peer-reviewed or major research-conference papers | Evidence for retrieval evaluation, event resolution, near-duplicate handling, and record-linkage methods. |
| Vendor product documentation | Evidence of how an existing commercial system is designed and labels signals. It is not independent proof of sales effectiveness. |
| Tributary live-run evidence | Evidence of product-specific errors and operating constraints. It is not evidence that the system generalizes. |

Vendor statements about likelihood to respond, active demand, or predictive performance are treated as product claims unless independently evaluated.

## Reference architecture

```text
source collection
  -> source document
  -> account resolution
  -> event resolution
  -> signal assessment
  -> action queue
  -> owner feedback
```

Each stage must retain its own state. A failure or uncertainty at one stage must not silently erase a valid record from another stage.

### Required persistent entities

| Entity | Purpose | Minimum fields for week one |
| --- | --- | --- |
| Account | Stable nonprofit identity | Account ID, legal and operating names, aliases, official ID, domain, headquarters, service area, category, identity status. |
| Source | Collection endpoint | Source ID, publisher, source type, geography, URL, access state, handling decision, last attempt, last success. |
| Source document | One retrieved page or filing | Document ID, canonical URL, publisher, title, published date, retrieval time, content hash, permitted evidence passage. |
| Event | One real-world occurrence | Event ID, event type, event date, involved accounts, document links, first seen, last updated, duplicate/coreference state. |
| Signal assessment | Commercial interpretation of an event | Factual observation, evidence strength, possible relevance, alternative explanation, unknowns, review state. |
| Action | Owner-facing priority | `act`, `investigate`, `monitor`, or `suppress`; next step; reason; owner decision. |
| Source checkpoint | Incremental collection state | Validator or last-modified value, last successful item/date, failure state, retry metadata. |

The implementation can retain the existing record store, but these concepts must not be collapsed into a single finding or approval field.

## Findings from documented systems

### 1. Resolve accounts before evaluating signals

The Fellegi-Sunter record-linkage model divides candidate pairs into links, possible links, and nonlinks. The possible-link category deliberately delays uncertain decisions. Tributary should use exact official identifiers first, normalized name/domain/location second, and an unresolved queue for ambiguous cases.

Week-one rules:

- CRA business number or US EIN is the strongest identity link.
- An official domain plus name and location can support a match when an official identifier is unavailable.
- Name similarity alone cannot auto-merge accounts.
- Suspected duplicates remain linked and reversible.
- Uncertain matches remain visible in the resolution queue.

**Primary source:** U.S. Census Bureau, *Using the EM Algorithm for Weight Computation in the Fellegi-Sunter Model of Record Linkage* (2000), https://www.census.gov/library/working-papers/2000/adrm/rr2000-05.html

### 2. Account identity and signal freshness are separate

The CRA List of Charities is designed to report whether a charity is registered, revoked, annulled, suspended, or penalized. T3010 returns supply contact, activity, and financial information from previous fiscal periods. The IRS Tax Exempt Organization Search and Business Master File play a comparable identity role for US organizations, and the BMF extract is produced monthly.

Consequences:

- A currently valid account enters the account universe without needing a current commercial signal.
- A stale filing does not invalidate a currently registered account.
- A register row is identity evidence, not a commercial signal.
- Historical filings provide baselines and context, not proof of current pressure or buying capacity.

**Primary sources:**

- Canada Revenue Agency, *How to get information about a charity*, https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/information-about-a-charity.html
- Government of Canada Open Data, *2023 List of charities*, https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6
- Internal Revenue Service, *Tax Exempt Organization Search*, https://www.irs.gov/charities-non-profits/tax-exempt-organization-search
- Internal Revenue Service, *Exempt Organizations Business Master File Extract*, https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf

### 3. Documents and events are different objects

NIST Topic Detection and Tracking separates first-story detection, topic detection, tracking, link detection, and segmentation. Cross-document event-coreference research likewise treats multiple mentions as references to an underlying event. News aggregators face repeated and lightly rewritten stories in real time.

Consequences:

- One article is a source document, not automatically one signal.
- Multiple documents can support one event.
- A later document can update an existing event rather than create another signal.
- Event novelty and document duplication are different decisions.

Week one does not need an advanced clustering model. Start with canonical URL, exact-content hash, normalized headline similarity, account, event type, event date proximity, and a manual merge/split correction.

**Research sources:**

- NIST, *Topic Detection and Tracking Evaluation Overview*, https://www.nist.gov/publications/topic-detection-and-tracking-evaluation-overview
- Bugert and Gurevych, *Event Coreference Data (Almost) for Free: Mining Hyperlinks from Online News*, EMNLP 2021, https://aclanthology.org/2021.emnlp-main.38/
- Panagiotou et al., *First Story Detection using Entities and Relations*, COLING 2016, https://aclanthology.org/C16-1305/
- Rodier and Carter, *Online Near-Duplicate Detection of News Articles*, LREC 2020, https://aclanthology.org/2020.lrec-1.156/
- Tumre, Patil and Kumar, *Improved Near-Duplicate Detection for Aggregated and Paywalled News-Feeds*, NAACL Industry 2025, https://aclanthology.org/2025.naacl-industry.73/

### 4. Strong signals use behavior, change, recurrence, or baselines

LinkedIn Sales Navigator documents more than 180 activity inputs, including connections, profile and company-page activity, advertising interaction, InMail response, and tagged website visits. Bombora documents elevated content consumption relative to an organization's historical baseline using event count, unique users, topic relevance, and engagement depth. Common Room labels pricing-page activity and product-usage changes as high intent, while job openings and mergers are lower-intent context.

These descriptions establish a design distinction, not independent proof that the vendors' scores cause better sales outcomes.

Tributary cannot recreate first-party behavioral intent from public nonprofit sources. It should apply the defensible parts of the pattern:

- treat one public mention as an observation;
- build an episode from repeated related events;
- compare future activity against the account's own history;
- raise evidence strength when independent sources corroborate an event;
- keep direct engagement evidence separate and stronger if it becomes available later.

**Vendor documentation:**

- LinkedIn, *Activities that indicate Buyer Intent in Sales Navigator*, https://www.linkedin.com/help/sales-navigator/answer/a1325209
- LinkedIn, *Sales Navigator Buyer Intent FAQ*, https://www.linkedin.com/help/sales-navigator/answer/a507435
- Bombora, *Company Surge User Guide*, https://customers.bombora.com/hubfs/%21MASTER_Bombora-Company%20Surge%20User%20Guide-January%202023.pptx%20%282%29.pdf
- Common Room, *Go-to-market signals*, https://www.commonroom.io/resources/signals/
- Crunchbase, *Filter your searches with growth signals*, https://support.crunchbase.com/hc/en-us/articles/38966398684691-Filter-your-searches-with-growth-signals

### 5. Provenance is part of the data model

W3C PROV distinguishes entities, activities, agents, derivation, revision, primary sources, and timestamps. Tributary does not need to implement the full ontology, but it needs the same conceptual separation.

Minimum provenance:

- source URL and publisher;
- publication and retrieval dates;
- content hash or source version;
- short evidence passage and locator;
- extraction rule or model version;
- review actor and review state;
- links from assessment to event and evidence;
- preserved correction history.

**Standard:** W3C, *PROV-O: The PROV Ontology*, https://www.w3.org/TR/prov-o/

### 6. Store broadly, alert narrowly

Google's Site Reliability Engineering guidance classifies operational events by urgency and states that immediate alerts should be actionable. Low signal-to-noise creates alert fatigue. This is an alerting source, not a sales-research study, but the human-attention constraint directly applies.

Tributary action tiers:

| Tier | Definition | Default treatment |
| --- | --- | --- |
| Act | Evidence supports a concrete outbound-preparation step now. | Daily primary worklist. |
| Investigate | Potentially relevant, with one material question to resolve. | Daily research queue. |
| Monitor | Valid account or event without sufficient urgency or relevance. | Retain and re-evaluate on change. |
| Suppress | Duplicate, irrelevant, out of scope, or demonstrably incorrect. | Hide from default view, retain reason. |

**Primary operational source:** Google SRE Workbook, *On-Call*, https://sre.google/workbook/on-call/

### 7. Evaluate rare useful results with precision and recall

Useful outbound signals will be rare relative to collected pages. Research on imbalanced classification shows that ROC-style summaries can conceal large false-positive burdens, while precision-recall directly represents the share of correct positive predictions. NIST TREC evaluation also ties relevance judgments to the exact collection being tested.

Week-one metrics:

- worklist precision: useful `act` and `investigate` items divided by surfaced items;
- discovery yield: valid new accounts per source run;
- duplicate leakage: repeated documents or events reaching the worklist;
- account-resolution error rate;
- freshness from publication to appearance;
- review burden per useful item;
- source attempt, success, unchanged, failure, and blocked counts.

Recall can only be estimated against a reviewed sample or a defined test collection. It must not be claimed from the surfaced worklist alone.

**Research sources:**

- Saito and Rehmsmeier, *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*, PLOS ONE 2015, https://doi.org/10.1371/journal.pone.0118432
- NIST TREC, *English Relevance Judgements*, https://trec.nist.gov/data/reljudge_eng.html

### 8. Collection should be incremental and failure-aware

HTTP conditional requests use entity tags and modification dates to avoid transferring unchanged data. `If-Modified-Since` can also limit traversal to resources changed during a recent window. Accurate sitemap modification dates and feed endpoints should be preferred when available. A failed fetch must not be interpreted as no new information.

Week-one rules:

- use RSS/Atom, APIs, sitemaps, or index pages before broad crawling;
- store the last successful checkpoint per source;
- use ETag or Last-Modified validators where available;
- use canonical URL and content hash when validators are absent;
- distinguish `no change`, `no qualifying item`, `fetch failed`, `parse failed`, and `blocked`;
- use bounded retries and backoff;
- respect robots and access controls;
- do not refetch all historical content every day.

**Standards and official guidance:**

- IETF, *RFC 9110: HTTP Semantics*, https://www.rfc-editor.org/rfc/rfc9110.html
- IETF, *RFC 9111: HTTP Caching*, https://www.rfc-editor.org/rfc/rfc9111.html
- IETF, *RFC 9309: Robots Exclusion Protocol*, https://www.rfc-editor.org/rfc/rfc9309.html
- Google Search Central, *Build and submit a sitemap*, https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap

### 9. Model output requires post-deployment monitoring

NIST recommends measuring known errors, comparing pre- and post-deployment performance, monitoring inputs, retaining audit histories, and examining unexpected operational cases. Its 2026 deployed-AI paper states that controlled pre-deployment evaluation cannot expose all issues caused by nondeterminism and changing inputs.

If language-model extraction is introduced later:

- the model proposes structured observations and can abstain;
- source evidence remains attached;
- deterministic checks validate schema and invariants;
- human corrections are stored as feedback events;
- rule/model versions are retained;
- output distributions and error reasons are monitored over time.

**Primary sources:**

- NIST AI RMF Playbook, *Measure*, https://airc.nist.gov/airmf-resources/playbook/measure/
- NIST, *Challenges to the monitoring of deployed AI systems*, 2026, https://www.nist.gov/publications/challenges-monitoring-deployed-ai-systems-center-ai-standards-and-innovation

## Documented and observed failure modes

| Failure mode | Consequence | Week-one control |
| --- | --- | --- |
| Keyword match treated as a signal | Mentions are promoted without materiality or context. | Require account, event, dated fact, source evidence, and relevance hypothesis. |
| Public event called buyer intent | Context is presented as willingness to buy. | Use `signal` or `event`, never `buyer intent`, without direct behavior. |
| One article treated as one event | Syndication inflates activity and owner workload. | Document hashes, URL normalization, event grouping. |
| One opaque score | Unsupported inference is hidden inside ranking. | Preserve fit, evidence, freshness, recurrence, access, and unknowns separately. |
| Binary approval gate | Valid but uncertain accounts disappear. | Separate account universe, review state, and action tier. |
| Filing recency used for identity admission | Currently valid accounts can be excluded. | Current registry for identity; filings for history. |
| Fuzzy-name auto-merge | Evidence attaches to the wrong legal entity. | Exact IDs first; possible-link queue. |
| Full historical crawl every day | Cost, duplicate records, site load, and slow runs. | Per-source incremental checkpoints. |
| Every detected item shown to the owner | Alert fatigue and loss of confidence. | Broad monitor store, narrow action queue. |
| Same assistant reviews its own output | Traceability is mistaken for independence. | Label same-assistant review; use source corroboration and owner checks. |
| Predictive model trained immediately | No stable label, outcome definition, or representative history. | Deterministic rules and feedback capture first. |
| Accuracy used as the principal metric | Rare positive failures are hidden by abundant negatives. | Precision, recall on a reviewed sample, and review burden. |

## Seven-project-day implementation boundary

| Day | Deliverable informed by this review |
| --- | --- |
| 1 | Separate account discovery, identity, eligibility, signal review, and private business relevance. Keep Greater Vancouver Food Bank visible. |
| 2 | Build source registry and incremental adapters for official registries, organization publications, funder/sector announcements, procurement sources, and selected local reporting. |
| 3 | Batch account resolution, exact-ID matching, possible-link queue, document deduplication, and basic event grouping. |
| 4 | Deterministic event-to-signal rules with factual observation, event date, evidence, relevance hypothesis, alternative explanation, and explicit unknowns. |
| 5 | Owner worklist with `act`, `investigate`, `monitor`, and `suppress` tiers; persist decision and reason. |
| 6 | Fresh batch run, idempotence and restart checks, source-failure visibility, and correction of false positives and duplicate leakage. |
| 7 | Repeatable fresh daily package with new accounts, new events, updated episodes, action queue, coverage report, and actual operating limitations. |

### Week-one event classes

- new program, service, geography, or facility;
- material demand or usage change;
- funding award, funding loss, or fundraising campaign;
- leadership change;
- partnership or major commitment;
- opening, closure, relocation, or service reduction;
- hiring surge or critical vacancy;
- financial pressure;
- technology, data, or operational modernization initiative;
- public request for vendors, proposals, or specialized support.

Each surfaced item must answer:

```text
Which account?
What happened?
When did it happen?
What source directly supports it?
Why might it matter to Autonomy Bridge?
What alternative explanation exists?
What remains unknown?
What is the next concrete action?
```

## Explicitly deferred

- predictive buyer-intent scoring;
- automatic outreach or message generation;
- machine-learned account ranking;
- unattended model verification;
- a national-scale unrestricted crawler;
- universal numeric thresholds before observed results;
- dashboards that do not improve the daily decision;
- claims of Canada/Washington completeness;
- inference of budget or authority from operational context alone.

## Research implications for the existing product

1. Preserve the existing auditable record store and compact owner worklist.
2. Add a first-class event concept before Day 4 signal generation.
3. Treat account admission and owner priority as independent dimensions.
4. Replace a single approved/pending presentation with action tiers while retaining detailed review states.
5. Capture source checkpoints and content hashes during Day 2, not as later optimization.
6. Measure precision and owner review burden from the first fresh run.
7. Store every correction reason so later rules or models can be evaluated against actual owner decisions.

## Research limits

- No independent field study was found that validates a public-data nonprofit consulting-intent generator with Tributary's exact use case.
- Vendor documentation describes product design and vendor claims, not controlled proof of sales outcomes.
- Research on record linkage, event resolution, alerting, provenance, retrieval evaluation, and deployed-AI monitoring transfers as system design evidence, not as proof that a specific signal predicts purchase.
- Week-one usefulness must therefore be established through fresh operational runs and Deepak's judgments on the surfaced worklist.
