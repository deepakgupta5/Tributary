# Tributary

Tributary is a local research system for discovering nonprofit accounts and generating evidence-backed organizational signals across Canada and Washington State. It supports Autonomy Bridge's private business-development decisions. It does not send outreach or infer need, budget, authority, or willingness to engage without direct evidence.

## Current status

The repository contains:

- a versioned Python and SQLite research workflow;
- synthetic fixtures and evaluation sessions;
- one bounded live-source session covering three nonprofit accounts;
- a compact account worklist that keeps Greater Vancouver Food Bank visible while separating identity, eligibility, signal review, and private commercial relevance;
- an approved seven-project-day path to fresh daily account and signal output; and
- a documented evidence review of signal-system practices and failure modes.

Days 1–6 are merged into `main`. The [latest reviewed worklist](OutBound/evidence/daily-2026-11-07/worklist.md) is the **November 7 manual recovery**, with **0 owner attention accounts** and **6 outstanding research items**. Collection across the existing 57 endpoints found 0 new accounts and 0 new/changed signal candidates. Eleven claims were checked against nine original documents through four linked, shared-context desktop checkpoint executions: six context findings, three unsupported/contradicted pressure interpretations and two continuing claim questions. See the [run, dispositions and verification](OutBound/evidence/daily-2026-11-07/README.md).

The app scheduler recorded a failed attempt and exposed no technical cause. The recovery manually invoked `--scheduled`; that flag does not establish unattended execution. A same-day retry correctly skipped collection. Private feedback remained unchanged. The four remaining blocked/held source checks stay internal alongside the two claim questions. No successful unattended scheduler execution or scheduler repair is claimed. The 57-endpoint daily inventory does not yet monitor the new 323-account BC Pool A. Outreach remains manual.

Earlier Day 6 [source-review evidence](OutBound/evidence/day-6/source-review/README.md) and the [November 5 repeat](OutBound/evidence/day-6/source-review/repeat/worklist.md) remain historical records. See [desktop review operation](OutBound/frameworks/DESKTOP_SOURCE_REVIEW.md).

Source-review originals use per-command temporary storage, removed at command exit, including Python exceptions and unfinished reviews. A later review re-fetches the permitted source. Persistent state retains hashes, metadata and bounded excerpts only; the PRD retention policy is unchanged.

[D064 private-feedback baseline](OutBound/evidence/private-feedback-initialization/README.md): available local/cloud backup searches found no recoverable journal or evidence of prior population. A new empty private journal is initialized; assistant review dispositions are not owner feedback.

## BC population screen, Issue #9

[Reconciliation and limits](OutBound/evidence/population-screen/README.md): 12,040 historical records reconcile to 4,168 category exclusions, 551 retained size-fit, 345 retained enrichment and 6,976 remainder. Historical pre-exclusion 754/414 reproduces exactly. D065 resolves all 32 category clues: PLAN excluded, three service-delivery accounts retained, 28 out-of-band records batch-resolved and held from buyer admission. Pending category reviews: zero. Current eligibility, donor-base and trigger gates are unassessed. No collection or outreach enabled.

## Canonical BC geography

[Geography reconciliation](OutBound/evidence/canonical-geography/README.md): 896 retained historical records yield Pool A of **323 operating organizations** (231 size-fit, 92 staffing-enrichment), **168 in-corridor foundations**, and **405 remote/monitor records** (364 operating, 41 foundations). D066 includes Delta, Mission and White Rock. No unresolved geography/form checks. The source is historical mailing locality; current operating geography, donor-base and live triggers remain unchecked. Outreach stays manual and disabled in the artifacts.

## Repository structure

| Path | Purpose |
| --- | --- |
| `tributary/` | Application code. |
| `tests/` | Unit and regression tests. |
| `OutBound/frameworks/` | Product requirements, seven-day plan, and system/workflow specifications. |
| `OutBound/research/` | External research, source strategy, feasibility, and limitations. |
| `OutBound/evidence/` | Preserved bounded live runs and evaluation sessions. |
| `OutBound/tracker/` | Roadmap and owner feedback tied to implementation. |
| `OutBound/data/` | Safe committed fixtures and operating data. |
| `OutBound/archive/` | Historical implementation records. |
| `decisions/` | Accepted product decisions. |
| `examples/` | Generated synthetic examples. |
| `Library/` | Future owner-facing documents, spreadsheets, and PDFs. |

This adapts the operating/library separation used in the Fractional repository without copying folders that Tributary does not currently need.

## Key documents

- [Seven-day project plan](OutBound/frameworks/PROJECT_PLAN.md)
- [Product requirements](OutBound/frameworks/PRD.md)
- [Signal-generator evidence review](OutBound/research/SIGNAL_GENERATOR_EVIDENCE_REVIEW_2026-11-05.md)
- [Source strategy and feasibility](OutBound/research/SOURCES.md)
- [Research workflow](OutBound/frameworks/RESEARCH_WORKFLOW.md)
- [Foundation specification](OutBound/frameworks/FOUNDATION_SPEC.md)
- [Roadmap](OutBound/tracker/ROADMAP.md)
- [Development feedback](OutBound/tracker/DEVELOPMENT_FEEDBACK.md)
- [Accepted decisions](decisions/DECISIONS.md)

## Validation

Run the complete test suite:

```sh
python3 -m unittest discover -s tests -v
```

Reproduce the bounded live-session outputs from saved inputs:

```sh
python3 OutBound/evidence/live_runs/session-001/run.py --out /tmp/tributary-live-session-001
```

The resulting `worklist.md` is the compact owner view. The detailed report, exact review packets, and structured records remain the audit trail.

Run the synthetic demonstration:

```sh
python3 -m tributary.demo --out out/demo
```

Captured synthetic outputs are in [`examples/`](examples/). Historical implementation notes are in [`OutBound/archive/`](OutBound/archive/).

## Operating boundary

Tributary uses freely accessible English-language sources and stores links, metadata, factual notes, and necessary permitted short checking passages. It does not bypass access controls or commit whole articles, PDFs, source CSVs, or private pursuit data. Same-assistant review provides traceability, not independent verification.

## Repository boundary, 2026-11-08

Tributary holds the signal system: application code, tests, collection and review workflows, source research, population/geography screens, trigger rules, and supporting product evidence and decisions. Commercial execution plans and client-delivery ideas belong in [Non-Profits](https://github.com/deepakgupta5/Non-Profits).

The BC conversation plan and lapsed-donor tracker idea have moved to Non-Profits at their original `OutBound/` paths. Links in the indexes and PRD point to the new locations. Earlier decision entries retain their historical wording; the current commercial execution record is maintained in Non-Profits.
