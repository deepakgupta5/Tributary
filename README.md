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

Day 1 of the current seven-day plan is implemented. Fresh broad collection, event resolution, daily scheduling, and an operational daily worklist remain to be built and tested. Saved live-session replay is a regression fixture, not a fresh collection run.

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
