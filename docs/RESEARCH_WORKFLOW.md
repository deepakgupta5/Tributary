# Research, skepticism, and fact-checking workflow
Recorded: 2026-11-03
Status: Agreed role sequence; implementation remains pending.
Scope: Tributary evidence reports, separate from software code review and private pursuit decisions.

## Sequence and independence
Researcher -> Skeptic -> Fact-checker -> labelled evidence report -> owner investigation.

Each stage reads a versioned input and writes its own output with role identity, actor/run identity, time, and references. The researcher cannot approve its own output as independent QC. The skeptic and fact-checker have distinct instructions and review records; they must not simply inherit the researcher's confidence.

Current authorization: local AI may execute these three roles, with separate instructions, contexts, outputs, and reviewer/run identities. One model may run them sequentially; three models are not required. Same-model passes are not independent corroboration and may repeat errors. Deterministic validators assist the pipeline; the owner reviews conclusions and revises prompts/instructions. Do not simulate human approval with model role names. Follow LOCAL_AI_FEASIBILITY.md before selecting a model/runtime. No paid/cloud model service is authorized, and no API interface is required.

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
A substantive edit creates a new version. Reopen affected verification and skeptic issues; retain prior decisions. Deterministic tests should exercise numeric mismatch, altered quote, overstated paraphrase, missing qualifier, duplicate corroboration, unresolved identity, inaccessible original, and stale approval after edits. Synthetic fixture answers are not substitutes for live human review.

## Retention
Preserve metadata, checksums where available, and necessary permitted sanitized excerpts. No permanent whole live articles, audio, or transcripts. Transient retrieval must comply with source conditions and leave no unapproved raw content in caches/logs. If sanitization removes needed evidence, expose the limitation rather than manufacturing verification. Public fixtures and demonstrations use synthetic organizations/claims and reviews.
