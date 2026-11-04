# Source coverage and feasibility
Status: Draft v0.1
Updated: 2026-11-03

## Current evidence status
This document defines required coverage and a verification process. No individual source or endpoint has been verified for ingestion in this repository. The categories below are candidates, not working integrations.

## Coverage requirements
Initial geography: all Canadian provinces and territories, plus Washington State. Track city/community and regional coverage as well as jurisdiction-level sources. A national outlet does not substitute for local coverage.

| Source category | Candidate material | Intended contribution |
| --- | --- | --- |
| Canadian official records | Charity listings, returns, government grants/disclosures, provincial and municipal grants | Identity, financial history, funding relationships. |
| US official records | Nonprofit filings/listings and federal, Washington State, and local disclosures | Identity, financial history, funding relationships. |
| Local/regional journalism | City/community newspapers, regional outlets, radio/TV reporting | Local strain, campaigns, service changes, commitments. |
| Sector media | Nonprofit/fundraising publications and cause-specific association material | Sector context and organization-specific evidence. |
| Podcasts/interviews | Community affairs, philanthropy, nonprofit leadership interviews | Explicit accounts of needs and constraints. |
| Organization publications | Annual reports, campaign pages, newsletters, public meeting material | First-party statements, campaign outcomes, commitments. |
| Funder/community networks | Foundation grant lists, sponsored support programs, umbrella bodies, event material | Organizational connections and funded support routes. |

## Language boundary
Confirmed initial scope: English-language sources only, including the manual trial. Track French and other languages as coverage gaps across Canada and Washington State. Do not imply that all-language coverage exists in any jurisdiction. English sources concerning any in-scope location remain eligible.

## Free-only access and operation
Confirmed: no paid subscriptions, source access, hosting, APIs, transcription, or other paid operating services. Investigate permitted free sources, published transcripts, and local processing. Do not subscribe, purchase access, or introduce automatic paid overages.

Record paywalls and unavailable free transcripts as coverage gaps. A free alternative must be checked for sufficient evidence and permitted use. Free-tier quotas, expiry, and failure behavior must be documented; limits must stop or flag work rather than trigger charges. Audio transcription is deferred from Task 001. Use existing English transcripts or show notes, with their limits recorded; any later transcription method needs a separate scope/access decision and must preserve the deterministic-core and free-only constraints.

## Source register fields
For every discovered source record:
- Source ID, publisher, URL/endpoint, category, geography, language, and organization/cause coverage.
- Discovery method, formats, identifier availability, available history, publication frequency, and expected lag.
- Access method: feed, API, download, permitted page retrieval, free authorized access, or manual import. Paid subscription methods are excluded.
- Access/retention/redistribution conditions, permitted evidence excerpt handling, costs, and authentication requirements without credentials.
- Audio/transcript availability, transcription permission and cost where applicable.
- Verification status, date checked, sample reference, owner, and next action.
- Operational status: last attempt, last success, failure reason, next check, and known coverage gaps.

Suggested verification states: candidate, sample inspected, access confirmed, approved for pilot, blocked, or retired. Keep verification status separate from fetch status.

## Feasibility procedure
1. Inspect the actual publication or dataset and applicable access conditions.
2. Inspect small permitted samples. Record fields, dates, missingness, formats, organization identity clues, and personal information.
3. Assess whether it supplies evidence for a PRD question, rather than only keyword matches.
4. Check language support, geographic relevance, lag, availability of primary evidence, and duplication/syndication.
5. Define extraction, retention, attribution, refresh, and failure handling.
6. Record a decision and limits before implementation.

Search snippets can help discover a source but cannot alone verify a finding. A blocked or paywalled item remains an access gap unless authorized full evidence is available. Do not bypass access controls.

## Source inspection and human review within development
Select a documented sample of English-language material across Canadian regions and Washington State, localities of different sizes, source types, and pressure/opportunity categories. Sample size and locations remain open; do not treat a small sample as proof of full geographic feasibility.

For each search/source checked, retain the query or retrieval method, date, outcome, and zero-result/access-failure cases. Prepare evidence-backed example findings for human review. Record useful findings, misleading indicators, missing evidence, duplicate stories, and unavailable material.

Use a separately reviewed sample to examine omissions where feasible. The observed review workload and error patterns inform first-build acceptance thresholds.

## Cross-source rules
- Retain source-native identifiers. Canadian charity identifiers and US identifiers are different namespaces and are never joined merely because their digits coincide.
- Confirm whether a published identifier denotes an organization, registration/account, branch, or filing before defining joins.
- Resolve organization names conservatively using location and documented aliases. Uncertain matches require review.
- Distinguish original reporting from syndicated copies and separate repeated campaigns from duplicate reports of one campaign.
- Preserve original currencies, dates, periods, language, and geographic distinctions.
- Store only permitted content. Organization-level extraction does not justify saving unfiltered personal data in raw archives.

## Contextual discovery and historical comparisons
Confirmed: use a 12-month discovery window, with recent-six-month priority only when evidence and relevance are comparable. Retain earlier campaign periods and permitted historical records for comparisons. Record event/publication dates and current-status checks separately.

Search beyond explicit terms such as fundraising shortfall. Inspect local interviews, podcasts, and community reporting for factual descriptions of demand, campaign participation, deadlines, funding concentration, and staff workload. Record alternative explanations and missing context. Repeated stories about one event do not supply independent corroboration.

The integrated source trial must examine whether indirect discovery produces useful, defensible investigation prompts. Include weak or misleading clues and checks for subsequent resolution; do not measure success solely by finding explicit admissions. Log access gaps and unsuccessful searches.

## Deterministic trial boundary
Use manual research and transparent rules to test discovery. AI assistance used to prepare code or conduct exploratory research must not be presented as proof that the deterministic product can perform the same interpretation.

For candidate rules, record trigger, supporting passage, false positives, missed relevant material, and the context the reviewer still needs. Test organization identity, syndication, date handling, and audit reconciliation separately from commercial relevance. Preserve enough permitted context for human judgment. No runtime model or local AI integration is part of the initial core.

## Daily collection and source checkpoints
Confirmed: daily local collection when the computer is available. Record per-source attempt and success times, last successful checkpoint, rate/access limits, missed intervals, and whether backfill is possible. On resume, attempt catch-up from the last successful checkpoint without duplicate records. Report unrecoverable feed/archive gaps.

The daily run checks sources that are due under their permitted access conditions. Any source-specific refresh exception must be documented; the default collection cadence remains daily. Static or slowly changing datasets need not be repeatedly downloaded unchanged. Initial historical discovery is distinct from daily incremental checks.

## Researcher, skeptic, and fact-checker review
Follow [RESEARCH_WORKFLOW.md](RESEARCH_WORKFLOW.md). The researcher uses the prescribed source mix, separates facts and attributed statements from speculation, and cross-checks consequential claims. The skeptic produces a short ranked issue list. The fact-checker checks the complete report's numbers, quotes, and paraphrases against the original documents, not merely the skeptic's flagged subset.

Each evidence claim needs a locator, checked version, verification state, reviewer identity, and check time. Record source-faithfulness and independent corroboration separately. Inaccessible originals, missing context, and unperformed checks remain explicit. A successful fetch is not factual verification.

Approved retention remains metadata/checksums and permitted sanitized excerpts, without permanent whole live articles/audio/transcripts. Source-specific access and transient-processing decisions still apply.


## Task 001 source deliverables and live-source gate
Source inspection and coding are integrated under CODEX_HANDOFF.md. Synthetic implementation may precede live access. For each proposed live source, record the access basis and a handling decision before collection: transient retrieval, permitted evidence/excerpts, raw retention or no retention, incidental-person-data removal, log fields, deletion rules, and redistribution limits. If uncertain, leave the source blocked and continue with fixtures. The owner must resolve policy choices rather than having the coding assistant imply approval.

A live-source attempt is not equivalent to a successful integration. Report separately: sources discovered, inspected, cleared for access/handling, attempted, fetched, parsed, and evidence produced. No verified source register or live integration is currently complete.
