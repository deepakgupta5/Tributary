# Tributary

Tributary is a research tool for discovering potential nonprofit clients and organizational routes in across Canada and Washington State. It supports Autonomy Bridge's business development through public organizational funding records and evidence from free English-language local media, interviews, and other sources.

Software gathers and organizes evidence; the owner interprets context and makes commercial decisions. Initial requirements include zero additional operating cost, deterministic data handling, coding-session researcher/skeptic/fact-checker roles, and owner review. Codex executes the initial development and research workflow; Claude Code can later continue from the same repository. Client donor analysis, campaign delivery, and outreach are outside scope.

## Status
A bounded synthetic foundation is implemented: JSON source collection, SQLite evidence/provenance storage, exact-content deduplication, reconciled audits, versioned role packets and submissions, stale-review detection, and a Markdown report. No live-source adapter, autonomous role runner, dashboard, or daily scheduler is implemented. No license has been selected.

## Run
Requires Python 3.10 or later, with no third-party packages, model installation, API keys, or network calls.

```sh
python -m unittest discover -s tests -v
python scripts/demo.py --db tributary.sqlite --output output
```

The demo replays **synthetic role fixtures** and writes `output/report.md`, collection counts, and each role's actual input/output. It does not execute a model. Repeating it preserves evidence IDs and avoids multiplying evidence records.

The same coding-session interface is available in Codex or Claude Code:

```sh
python -m tributary --db tributary.sqlite collect fixtures/sources.json
python -m tributary --db tributary.sqlite role-input researcher
python -m tributary --db tributary.sqlite submit path/to/researcher-output.json
python -m tributary --db tributary.sqlite role-input skeptic
python -m tributary --db tributary.sqlite submit path/to/skeptic-output.json
python -m tributary --db tributary.sqlite role-input fact-checker
python -m tributary --db tributary.sqlite submit path/to/fact-checker-output.json
python -m tributary --db tributary.sqlite report
```

`submit` accepts an output authored from the exported packet; it does not generate reasoning. The paths above are placeholders for actual role artifacts, not installed files. [Recorded examples](examples/README.md) distinguish fixture replay from same-assistant coding-session outputs. [Data contracts](docs/DATA_CONTRACTS.md) define the required fields and validation limits. Missing or stale stages prevent a report. Collection with some rejected records reports a partial outcome; total rejection exits with an error.

SQLite databases and transient output are ignored by Git. Only synthetic demonstration artifacts are tracked. Private operational data must be transferred separately with authorization; repository access does not include it.

## Documents
- [Product requirements](docs/PRD.md)
- [Sources and feasibility](docs/SOURCES.md)
- [Roadmap](docs/ROADMAP.md)
- [Decisions](docs/DECISIONS.md)
- [Development feedback](docs/DEVELOPMENT_FEEDBACK.md)
- [Foundation specification](docs/FOUNDATION_SPEC.md)
- [Research workflow](docs/RESEARCH_WORKFLOW.md)
- [Workflow evaluation](docs/WORKFLOW_EVALUATION.md)
- [Data contracts](docs/DATA_CONTRACTS.md)
- [Factual development log](DEVLOG.md)

The specifications describe expected behavior and evaluation evidence. All execution instructions to coding assistants are supplied by the owner through chat. Private commercial judgments and restricted material stay outside this public repository.
