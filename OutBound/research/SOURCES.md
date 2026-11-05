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
Confirmed initial scope: English-language sources only, including the integrated trial. Track French and other languages as coverage gaps across Canada and Washington State. Do not imply that all-language coverage exists in any jurisdiction. English sources concerning any in-scope location remain eligible.

## Free-only access and operation
Confirmed: no paid subscriptions, source access, hosting, APIs, transcription, or other paid operating services. Investigate permitted free sources, published transcripts, and local processing. Do not subscribe, purchase access, or introduce automatic paid overages.

Record paywalls and unavailable free transcripts as coverage gaps. A free alternative must be checked for sufficient evidence and permitted use. Free-tier quotas, expiry, and failure behavior must be documented; limits must stop or flag work rather than trigger charges. Audio transcription is deferred from the initial implementation. Use existing English transcripts or show notes, with their limits recorded; any later transcription method needs a separate scope/access decision and must comply with the approved coding-session scope and free-only constraint; transcription remains a separate deferred feature.

## Expanding registers and admission
Sources reveal new organizations; organization research reveals new sources. Discovery records retain first seen, method, parent record/evidence reference, candidate version, and next action. Neither register is complete on day zero. Daily research queues new candidates and changed versions; a daily additions quota is not required.

Canonical source admission states are candidate, inspected, approved for collection, blocked, merged, or inactive. Organization admission states are candidate, identity unresolved, admitted, merged, or excluded with reason. Fetch/parse status and the four checkpoint results are separate fields. Both registers and findings follow all four checks in RESEARCH_WORKFLOW.md before admission/approval; pending and blocked records remain visible.

Permitted bounded source inspection provides evidence for admission, without authorizing routine collection. Access and transient-retention conditions apply to inspection too. Newly approved sources can supply available 12-month history and then incremental checks, with archive gaps recorded. Both discovery directions are evaluated in the bounded foundation. BC and Washington State are the confirmed first live-sample geography; local reporting, organization publications, and official/funder records are the priority source types. Specific endpoints/localities, batch sizes, and subsequent expansion rules remain open in PRD.md.

Coverage reports distinguish discovered, admitted, configured, attempted, and successfully checked sources, and known/admitted organizations. Gaps by geography and source type guide expansion. No percentage of the entire nonprofit universe is inferred from an incomplete register.
## Source register fields
For every discovered source record:
- Source ID, publisher, URL/endpoint, category, geography, language, and organization/cause coverage.
- Discovery method, formats, identifier availability, available history, publication frequency, and expected lag.
- Access method: feed, API, download, permitted page retrieval, free authorized access, or manual import. Paid subscription methods are excluded.
- Access/retention/redistribution conditions, permitted evidence excerpt handling, costs, and authentication requirements without credentials.
- Audio/transcript availability, transcription permission and cost where applicable.
- Verification status, date checked, sample reference, owner, and next action.
- Operational status: last attempt, last success, failure reason, next check, and known coverage gaps.

Checkpoint outcomes are recorded for each reviewed source version. Inspection/access findings do not replace the canonical admission state or imply all four checks passed. Keep admission, review, and fetch status separate.

## Feasibility procedure
1. Inspect the actual publication or dataset and applicable access conditions.
2. Inspect small permitted samples. Record fields, dates, missingness, formats, organization identity clues, and personal information.
3. Assess whether it supplies evidence for a PRD question, rather than only keyword matches.
4. Check language support, geographic relevance, lag, availability of primary evidence, and duplication/syndication.
5. Define extraction, retention, attribution, refresh, and failure handling.
6. Record a decision and limits before implementation.

Search snippets can help discover a source but cannot alone verify a finding. A blocked or paywalled item remains an access gap unless authorized full evidence is available. Do not bypass access controls.

## Concrete candidate proposal before live collection
The live-source proposal identifies actual candidate publications, datasets, and exact endpoints, with locality/coverage, source category, selection reason, expected contribution, and verification/access status. Category lists alone do not satisfy this deliverable. Proposed endpoints remain explicitly unverified until permitted inspection supplies evidence; a candidate name or URL is not access clearance or source admission. No source quota is introduced.

This documentation records the requirement, not a verified endpoint list. Synthetic implementation does not depend on live collection. Live collection requires separate authorization and the source-specific access/handling and admission gates.

## Source inspection and human review within development
The first proposed live sample uses English-language BC and Washington material, prioritizing local reporting, organization publications, and official/funder records. Specific endpoints/localities and sample size remain open; no quota is approved. Expansion later covers other Canadian regions and broader source types, including interviews. A bounded sample does not establish full geographic feasibility.

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

## Integrated discovery evaluation
Source inspection, code, actual collection attempts, role outputs, and owner feedback are evaluated in bounded development increments. There is no nationwide manual trial prerequisite to coding.

Record rule triggers, supporting passages, false positives, missed relevant material, and context still needed. Test identity, syndication, date handling, and audit reconciliation separately from commercial relevance. Coding-session role outputs must be compared with original evidence and known-answer fixtures. A fixture replay does not demonstrate reasoning quality, and model agreement is not independent source corroboration.

## Daily collection and source checkpoints
Confirmed: daily local collection when the computer is available. Record per-source attempt and success times, last successful checkpoint, rate/access limits, missed intervals, and whether backfill is possible. On resume, attempt catch-up from the last successful checkpoint without duplicate records. Report unrecoverable feed/archive gaps.

The daily run checks sources that are due under their permitted access conditions. Any source-specific refresh exception must be documented; the default collection cadence remains daily. Static or slowly changing datasets need not be repeatedly downloaded unchanged. Initial historical discovery is distinct from daily incremental checks.

## Researcher, skeptic, and fact-checker review
Follow [RESEARCH_WORKFLOW.md](../frameworks/RESEARCH_WORKFLOW.md). The researcher uses the prescribed source mix, separates facts and attributed statements from speculation, and cross-checks consequential claims. The skeptic produces a short ranked issue list. The fact-checker checks the complete report's numbers, quotes, and paraphrases against the original documents, not merely the skeptic's flagged subset.

Each evidence claim needs a locator, checked version, verification state, reviewer identity, and check time. Record source-faithfulness and independent corroboration separately. Inaccessible originals, missing context, and unperformed checks remain explicit. A successful fetch is not factual verification.

Approved retention remains metadata/checksums and permitted sanitized excerpts, without permanent whole live articles/audio/transcripts. Source-specific access and transient-processing decisions still apply.


## Initial source evidence and live-source gate
Source inspection and implementation are integrated in the initial scope described in FOUNDATION_SPEC.md. Synthetic implementation may precede live access. For each proposed live source, record the access basis and a handling decision before collection: transient retrieval, permitted evidence/excerpts, raw retention or no retention, incidental-person-data removal, log fields, deletion rules, and redistribution limits. If uncertain, leave the source blocked and continue with fixtures. Unresolved policy choices remain with the owner.

A live-source attempt is not equivalent to a successful integration. Report separately: sources discovered, inspected, cleared for access/handling, attempted, fetched, parsed, and evidence produced. No verified source register or live integration is currently complete.
