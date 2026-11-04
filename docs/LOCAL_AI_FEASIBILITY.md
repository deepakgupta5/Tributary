# Local AI feasibility checkpoint
Recorded: 2026-11-03
Status: Technical evaluation specification only. No runtime/model selected or benchmark performed.
Owner: Deepak Gupta

## Target machine
Owner-provided system screenshot:
- MacBook Air 15-inch, Apple M5.
- 24 GB memory.
- macOS 27.2.
- Approximately 261 GB available storage at capture, not a permanent capacity guarantee.

Exclude serial numbers and other device identifiers. Do not infer speed, supported model size, or compatibility from specifications alone.

## Evaluation objective
The evaluation establishes whether free local AI can execute the researcher -> skeptic -> fact-checker workflow acceptably on the target MacBook. Runtime/model selection depends on measured evidence. Execution assignments are issued separately by the owner in chat.

Development-host and actual MacBook results are separate evidence categories. Only MacBook measurements establish MacBook performance. Where local measurements are unavailable, they remain pending; a portable test harness can support later local measurement.

## Requirements
- Free runtime and weights usable for the intended business use under their actual licenses; inspect licenses, do not assume every downloadable model is unrestricted.
- Local inference without paid/cloud fallback, subscriptions, or new hardware purchases.
- API is optional: local application, CLI, in-process library, or local-only endpoint can be evaluated.
- Automation capability must be checked. A manual chat app alone does not establish unattended daily operation.
- Sequential roles with separate instructions/contexts are acceptable; one set of weights can serve all three.
- Record model/version, runtime/version, quantization where applicable, configuration, prompt/instruction version, context limits, and output validation.
- Local installation and model downloads are owner-initiated activities, with documented storage requirements.
- No training, fine-tuning, remote inference, paid services, or collection of real client/private donor data.

## Minimal trial design
Use synthetic documents and planted errors with independently specified expected outcomes. Retain the original unmodified inputs and expected answers separately from role outputs. Include:
1. Numeric mismatch, currency/unit errors, wrong period, and target versus actual confusion.
2. Altered quotation, omitted qualification, and a paraphrase stronger than its source.
3. Indirect signal with a plausible benign explanation.
4. Same press release in multiple outlets, which is not independent corroboration.
5. Ambiguous organization identity and an inaccessible source.
6. Unsupported assertions and instructions embedded in source text that must be treated as untrusted data.
7. A long document where relevant context may be omitted/truncated; disclose incomplete inspection.
8. Substantive evidence changes that require rechecking prior model verdicts.

The researcher produces a complete claim ledger. The skeptic ranks material issues constructively. The fact-checker checks every number, quote, and paraphrase against source evidence, not only flagged claims. Count every eligible claim and checked claim, including failed/unperformed checks.

## Deterministic support and failure handling
Validate structured output, source/claim IDs, exact numeric fields where available, quotation matches, and arithmetic. Compare model judgments with the synthetic expected answers. Missing fields, invalid output, truncation, source absence, timeout, or failure must remain visible and must not produce a passed report.

Keep role contexts separate. Evidence is untrusted input, never permission to execute commands, alter prompts, fetch arbitrary private resources, or bypass access controls. Use bounded input/output and logged failures. Preserve a deterministic baseline without LLM interpretation.

Record prompts/instructions separately from transient source payloads. Local runtime chat history, caches, session persistence, debug dumps, and error logs must follow the approved retention policy; do not accidentally retain entire live source text. Synthetic payloads can be committed. Actual model outputs must also be checked for reproduction of prohibited source/person content.

## Measurements on the actual MacBook
- Runtime compatibility and automation path.
- Model files/download size, working disk requirement, and observed memory use; record measurement method.
- Wall-clock duration per role and per complete report.
- Completed, failed, and truncated runs; repeat selected cases to expose unstable verdicts.
- Errors caught, errors missed, unsupported claims incorrectly passed, correct claims wrongly rejected, and claim-check coverage, with denominators.
- Whether the machine remains usable during a small batch and whether sustained execution changes observed throughput.
- Same-model correlated failures and where owner inspection remains essential.

These measurements are not known in advance. Do not promise a model size, throughput, or daily capacity. Synthetic accuracy does not establish real-source accuracy; live testing follows source permission/retention checks.

## Deliverables
Evaluation artifacts consist of a reproducible test harness, synthetic inputs/answers, product role definitions, usage documentation, and a feasibility report. System serial numbers and private source data are excluded.

The report must separate:
- tests performed in the development host;
- tests performed on the MacBook;
- pending measurements;
- measured role-quality and performance limits;
- proposed runtime/model/configuration and licensing basis;
- automation support and remaining source/access/retention issues.

## Review gate
The owner evaluates measured results before adopting a runtime/model or expanding the implementation. Inadequate quality may imply narrower scope or more human checking. Paid/cloud inference is not an authorized fallback. No accuracy threshold has been pre-approved.

## External program boundary
Disclose the local AI review roles and own-business use honestly in any application. Eligibility remains unconfirmed. Any restriction or rejection triggers an owner decision on scope or independent continuation.
