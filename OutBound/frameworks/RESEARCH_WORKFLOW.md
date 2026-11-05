# Research, skepticism, and fact-checking workflow
Recorded: 2026-11-03
Status: Agreed role sequence; implementation remains pending.
Scope: Tributary findings, organization additions, and source additions; separate from software code review and private pursuit decisions.

## Sequence and independence
Collection and separate data QC -> Researcher -> Skeptic -> Fact-checker -> admission decision or labelled finding -> owner investigation.

Each stage reads a versioned input and writes its own output with role identity, actor/run identity, time, and references. The researcher cannot approve its own output as independent QC. The skeptic and fact-checker have distinct instructions and review records; they must not simply inherit the researcher's confidence.

Current execution: Codex performs the initial workflow in coding sessions; Claude Code can later continue from the repository. Role definitions, source/evidence references, structured outputs, and evaluations are persistent product artifacts. Role contexts and outputs remain separate. Same-assistant passes can repeat errors and do not establish independent corroboration. Deterministic validators assist the flow; the owner reviews commercial conclusions. No provider API or MacBook model benchmark is a prerequisite. See WORKFLOW_EVALUATION.md. Session execution is not a claim of unattended automation.

## Four checkpoints across three record types
| Checkpoint | Finding | Organization addition | Source addition |
| --- | --- | --- | --- |
| 1. Collection and separate data QC | Extraction, dates, completeness, identity references, and duplicates. | Identity, geography, aliases, official identifiers where available, and duplicate matches. | Publisher/endpoint identity, coverage metadata, accessibility, and duplicates. |
| 2. Researcher | Evidence-backed observations, cross-checks, hypotheses, and unknowns. | Activities, area served, in-scope eligibility evidence, identity references, and unknowns. | Provenance, actual sample utility, independence, formats/history, access and handling basis, and limits. |
| 3. Skeptic | Unsupported conclusions, alternative explanations, and weak corroboration. | Mistaken identity, unsupported eligibility, stale organizational status, and weak admission grounds. | Reliability, redundant/syndicated material, coverage bias, and unsupported access/usefulness assumptions. |
| 4. Fact-checker | Every number, quotation, and paraphrase against original evidence, including unflagged claims. | Required organizational details and every number, quotation, and paraphrase against original records. | Required source/access/coverage details and every number, quotation, and paraphrase against the publication, conditions, and inspected samples. |

Collection and data QC are separate responsibilities and review records even though grouped in the first checkpoint. The collector cannot approve its own proposals. Each checkpoint identifies the candidate/finding version, actor/run, result, evidence, reason, unresolved issues, and next action. Researcher and later roles retain both the complete detail/claim ledger and relevant originals; the skeptic list is not the fact-checker's entire workload.

Required admission evidence includes resolved identity and scope for organizations, plus resolved access/handling suitability for sources. All required checkpoint results must pass for the reviewed version before admission or routine collection. Optional missing fields can remain explicit; material unresolved required evidence leaves the record pending or blocked. A successful fetch or model confidence does not confer admission.

Admission output records admitted/approved, merged into an existing record, pending/unresolved, or excluded/blocked with reason. The underlying register uses the canonical states in PRD.md. Merges preserve aliases and provenance rather than erasing prior discoveries when implemented. Reversible merge execution is deferred from the first synthetic build; suspected duplicates remain linked and unresolved without destructive merging. Unchanged approved records are not fully rechecked daily; affected checks reopen after material changes. Commercial relevance is never inherited from register admission.

Source inspection for admission is bounded and subject to source access/retention conditions. A candidate can be inspected without entering routine collection. Unknowns remain recorded without circularly requiring prior approval to inspect the permitted evidence needed for approval.
## Review completion and approval
Execution completion and checkpoint outcome are separate fields. A completed review may find a material contradiction and therefore prevent approval. All four required checkpoint results must be current for the exact reviewed version.

The required-detail checklist distinguishes:
- Required identity and eligibility evidence for organization admission.
- Required publisher/endpoint identity, access/handling suitability, and material coverage/usefulness evidence for source admission.
- Required identity references, supporting evidence, and complete checks of the finding's numbers, quotes, paraphrases, and material conclusions.
- Optional information and documented nonmaterial limitations, retained explicitly without automatically blocking approval.

Missing, stale, failed, or incomplete required checks block approval. Material unresolved identity, eligibility, access/handling, or factual issues also block approval. An unsupported or contradicted material assertion cannot pass unchanged. A skeptic question alone does not fail a record: each issue receives a disposition and reason, and any blocking classification identifies the affected required detail and material consequence. A limitation is nonblocking only when it does not undermine required admission evidence or the asserted conclusion; relabelling a material defect as a limitation does not resolve it.

Optional missing fields and nonmaterial limitations can remain visible on an approved record. Uncertain findings remain reviewable in the investigation queue without acquiring approval. Register admission still does not confer commercial qualification.

## Execution separation evidence
Collection and QC use separate executions and review records; the collector cannot approve its own proposal. Each role receives its specified versioned packet. Records describe actual context separation: packet contents/references, prior outputs available, shared-session context where applicable, and known limitations. Separate execution IDs and files establish traceability only. They do not prove independent review, isolated contexts, or enforcement.

Same-assistant limitations remain explicit. Any claimed isolation or enforcement must be supported by execution evidence; an unperformed required check stays incomplete. No model identity or independence is inferred from a role label.

## Researcher instructions
1. Work within Canada and Washington State, English-only, free permitted access, and the agreed 12-month discovery window. Use earlier records for comparisons, not as evidence of a current issue without a status check.
2. Cast a broad net: city/community and regional newspapers, local radio/TV reporting, podcasts/interviews with available text, sector media, organization publications, funder/community networks, and official records. Explain sampled coverage and gaps. General search alone is not coverage.
3. Record source identity, URL/reference, publication/event dates, location/area served, source type, claim locator, and permitted supporting evidence. Match organizations conservatively.
4. Separate source-supported observations from attributed statements, inference, speculative business hypotheses, and unknowns. A leader's statement is evidence of what was said, not independent proof of its truth.
5. Cross-check consequential claims using original records or genuinely independent sources where available. Record corroboration, contradiction, and absence of corroboration. Syndication, repeated press releases, and an outlet quoting the same original do not become independent confirmation.
6. Explain candidate relevance with plausible alternative explanations. Do not assert fundraising failure, poor donor retention, an available consulting budget, or a guaranteed introduction from indirect clues.
7. Emit a structured report and a complete claim ledger. Every number, direct quote, and paraphrase must have a claim ID and source locator. Calculations retain source inputs, units, periods, currencies, and formula.
8. Record collection failures, excluded records and reasons, and reconciliation. Do not hide uncertainty to produce a shortlist.

## Researcher output
Organization identity status; evidence items; factual observations; attributed statements; separate hypotheses; missing context; cross-checks and contradictions; current-status check; organizational routes and investigation status; claim ledger; collection/coverage audit.

A source locator may be a page, section, table/cell, paragraph anchor, or audio timestamp when that material was actually reviewed. Do not invent unavailable page numbers, transcripts, or timestamps. Existing show notes verify only their own content.

## Skeptic instructions
Review the research report and its evidence references. Be contrarian in service of accuracy, not opposition for its own sake.

- Ask what evidence supports the claim and whether it supports its strength.
- Challenge causal leaps, circular reasoning, selective evidence, mismatched periods, missing denominators, false equivalence, and assumptions that absence proves a problem.
- Check if an apparently current problem is historical, resolved, or merely recurring.
- Look for alternatives such as changed campaign design, seasonality, a larger target, restricted funds, or incomplete reporting.
- Check source independence and whether funding relationships are being presented as access or spending authority.
- Separate material defects from minor presentation issues. Do not reject a useful report simply because evidence is incomplete; specify the limitation or correction.

Produce a short ranked problem list. Each issue references affected claim IDs, evidence needed, severity, likely effect on the conclusion, and a proportionate remedy. Rank conclusion-changing errors first, then material uncertainty, then lesser issues. Acknowledge adequately supported claims; do not manufacture objections or impose an arbitrary issue quota.

## Fact-checker instructions
Receive the full report, complete claim ledger, source references, and skeptic's ranked issues. Do not receive only the problem list.

Check every number, direct quote, and paraphrase against the actual document it came from, including claims the skeptic did not challenge. Separately address every skeptic issue.

For numbers, check value, units, currency, period, geography, denominator, target versus actual, cumulative versus annual, estimates, rounding, and calculations. For quotes, check exact wording, attribution, omissions, and qualifications against permitted source text. For paraphrases, check meaning, scope, certainty, and context; correct stronger wording than the source supports.

Verify that sources concern the correct organization and that source/date changes are recorded. A snippet, prior assistant summary, working URL, or checksum alone is insufficient. If the original is inaccessible and the retained permitted evidence cannot support the check, mark it unverifiable. Do not bypass access controls.

Each claim gets: checked version, verification result, evidence locator, check time, reviewer identity, correction if needed, and explanation. Use verified, partly verified, contradicted, or unverifiable, with pending for unperformed checks. Record source-faithfulness separately from independent corroboration. A correct quotation can still contain an uncorroborated claim.

Resolve skeptic issues as corrected, supported as written, limitation retained, or unresolved, with reasons. Do not mark an inferential disagreement resolved merely because a number matches.

## Final report
- Organization and geography, identity certainty, and report version.
- Observations and attributed statements with individual verification labels and source locators.
- Separate hypotheses, alternative explanations, and outstanding questions.
- Corrections made and a short ranked residual-problem list.
- Claim-check coverage: counts by type/status, remaining unchecked claims, and source-access gaps.
- Documented funding/organizational routes with separate investigation status.
- Coverage limits and current-status dates.
- Links between research version, skeptic issues, verification results, and revisions.

Do not use one green report badge to imply every statement is verified. Use an explicit actor/basis label such as model-checked, deterministically checked, or human-checked beside each verification result. A model's verified verdict is not a guarantee or human approval. Checked claims can enter the evidence view with those labels; unresolved or partial claims remain visible in the investigation view. A partially checked report is not fully verified. Owner commercial relevance is a separate private judgment.

## Corrections and replay
A substantive edit creates a new version. Record changed fields and dependencies, reopen affected QC/researcher/skeptic/fact-checker checks, and retain prior decisions against their original versions. Material changes include identity, eligibility, evidence values or meaning, and source access/handling changes. The affected current version awaits recheck; unchanged records do not require full daily review. A nonmaterial change requires a recorded basis rather than silently inheriting approval. Deterministic tests should exercise numeric mismatch, altered quote, overstated paraphrase, missing qualifier, duplicate corroboration, unresolved identity, inaccessible original, and stale approval after edits. Synthetic fixture answers are not substitutes for live human review.

## Retention
Preserve metadata, checksums where available, and necessary permitted sanitized excerpts. No permanent whole live articles, audio, or transcripts. Transient retrieval must comply with source conditions and leave no unapproved raw content in caches/logs. If sanitization removes needed evidence, expose the limitation rather than manufacturing verification. Public fixtures and demonstrations use synthetic organizations/claims and reviews.
