# Data

[Day 2 source inventory](day2-sources.json) lists configuration and handling by endpoint. The saved [attempts and checkpoints](../evidence/day-2/state.json) record actual fetch outcomes. The five successful sources, one handling hold and one deferred archive page are accounted for in the [baseline and continuation notes](../evidence/day-2/README.md).

`fixtures/` contains committed synthetic inputs and expected results used by tests. Live or restricted source documents must not be placed here.

## BC historical screen

`archive/BC-charity-candidates-2024.txt` is the unchanged 12,040-row identification archive. `archive/BC-size-screen-2024.txt` was recovered byte-for-byte from the owner's `BC-nonprofit-screen-12040.zip` downloaded archive. The ZIP's identification member exactly matches the repository identification archive. Its financial/staffing member is a saved CRA-derived screen, not a fresh raw filing download. No private owner data is included. Input SHA-256 values are committed in the reconciliation.

`screened/` contains all 12,040 dispositions plus size-fit, enrichment and unresolved-category subsets. Read the [reconciliation](../evidence/population-screen/README.md) before use. Rebuild with `python3 -m tributary.population_screen`. The archive remains disabled for collection/outreach.
