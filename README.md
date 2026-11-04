# Tributary

Tributary is a research tool for discovering potential nonprofit clients and organizational routes in across Canada and Washington State. It supports Autonomy Bridge's business development through public organizational funding records and evidence from free English-language local media, interviews, and other sources.

Software gathers and organizes evidence; the owner interprets context and makes commercial decisions. Initial requirements include zero additional operating cost, deterministic data handling, coding-session researcher/skeptic/fact-checker roles, and owner review. Codex executes the initial development and research workflow; Claude Code can later continue from the same repository. Client donor analysis, campaign delivery, and outreach are outside scope.

## Status
Planning documents only. No collector, dashboard, daily scheduler, or verified source integration is implemented. The documentation is under review in PR #1; no license has been selected.

## Project baseline
[PROJECT_PLAN.md](docs/PROJECT_PLAN.md) defines the starting baseline, the first seven project days, and week two onward. [PRD.md](docs/PRD.md) is the single open-product-decision register. The plan is documentation, not authorization to execute implementation in the planning conversation. The start date is unset. Numerical quality thresholds and source/organization quotas have not been approved.

Both the organization register and source register expand continuously. Findings, organization additions, and source additions all pass collection/data QC, researcher, skeptic, and fact-checker checkpoints. Collection and data QC are separate responsibilities. Candidate discovery does not itself admit a record.
## Confirmed starting decisions
- Initial eligibility: service-delivery nonprofits, with foundations and umbrella bodies as potential buyers or organizational routes in. No revenue cutoff.
- Hospitals, universities, religious organizations, and advocacy groups remain undecided. They are not silently included or permanently excluded; candidates in these categories remain pending an owner decision.
- First live sample: British Columbia and Washington State, prioritizing local reporting, organization publications, and official/funder records. Full product geography remains Canada and Washington; the bounded sample does not narrow that ambition.
- Initial delivery boundary: Day 1 design proposal only, comprising documentation inspection, proposed technical design, record formats, initial source sample, and test matrix. Owner review precedes any implementation. Approval of these starting decisions does not itself launch work or authorize implementation.

## Accepted Day 1 design
Python + SQLite, JSON/JSONL interchange, and Markdown-first reporting are accepted for a minimal synthetic foundation. Review completion and approval are separate; actual context separation is recorded; material changes reopen dependent checks. See D046-D052 and FOUNDATION_SPEC.md. Reversible merges, detailed funding relationships, HTML, and dashboard work are deferred. Implementation/tests require separate owner authorization, and live collection remains a separate gate. No live feasibility, role accuracy, or product usefulness has been established.

## Documents
- [Project plan and baseline](docs/PROJECT_PLAN.md)
- [Product requirements](docs/PRD.md)
- [Sources and feasibility](docs/SOURCES.md)
- [Roadmap](docs/ROADMAP.md)
- [Decisions](docs/DECISIONS.md)
- [Development feedback](docs/DEVELOPMENT_FEEDBACK.md)
- [Foundation specification](docs/FOUNDATION_SPEC.md)
- [Research workflow](docs/RESEARCH_WORKFLOW.md)
- [Workflow evaluation](docs/WORKFLOW_EVALUATION.md)

The specifications describe expected behavior and evaluation evidence. All execution instructions to coding assistants are supplied by the owner through chat. Private commercial judgments and restricted material stay outside this public repository.

The planning conversation is limited to documentation and review. Implementation and test execution are separately directed by the owner to Codex in chat. Closed PR #2 and its preserved branch are not an approved implementation baseline. PR #1 remains the documentation proposal.
