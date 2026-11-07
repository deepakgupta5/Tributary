# Source-review retention correction

6 November 2026, Vancouver. Implements option C under the unchanged PRD retention policy.

- Daily collection and any synchronous review share a per-command temporary directory. Normal exit or Python exception unwinding removes the full parsed originals, including failed and unfinished reviews.
- Standalone preparation also cleans up before returning. A desktop review performed later must re-fetch its original, check its version and locators, and reprepare if it changed. A 304 response cannot resurrect an expired original path.
- Persistent document state retains hashes, metadata and bounded checking excerpts, without the temporary cache path.
- The next invocation removes only recognized full-original files from the application's former state-dir `source-cache`. Feedback, unrelated files, source checkpoints and bounded excerpts are preserved. No legacy cache files were found in the existing Day 4 and Day 6 operating checkouts during this correction.
- No new live collection was needed to verify cleanup. Controlled tests exercise actual temporary files and real command control flow. Whole-original markers are absent from all surviving runtime files after the command.
- An uncatchable kill or power loss can interrupt standard OS-temp cleanup; immediate deletion under those conditions is not claimed. No permanent state-dir cache is introduced as a fallback.

Validation: 129 tests pass, including success/failure/unfinished-review cleanup, command exception cleanup, later re-fetch, legacy cleanup, unchanged review reuse and private feedback preservation. Original feasibility checkout and its uncommitted files are unchanged. This branch has not been activated in the existing scheduled operating checkout.
