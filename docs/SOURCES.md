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

Record paywalls and unavailable free transcripts as coverage gaps. A free alternative must be checked for sufficient evidence and permitted use. Free-tier quotas, expiry, and failure behavior must be documented; limits must stop or flag work rather than trigger charges. Audio processing without a published transcript requires a feasible free/local method and the access/handling checks below.

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

## Manual discovery trial
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

## Deliverable before coding
A populated source register, inspected samples, example findings, visible coverage gaps, access and data-handling decisions, and a proposed bounded source set for the first complete flow.
