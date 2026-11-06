# Source review, first live batch

Manual execution on 5 November 2026 Vancouver (6 November UTC). Same included desktop assistant performed researcher, skeptic and fact-checker passes in shared context. These are attributed source checks, not independent corroboration. No paid inference API or outreach was used.

[Current owner worklist](repeat/worklist.md) · [Each of the nine dispositions](dispositions.md) · [Structured verdicts](desktop-verdicts.json) · [First grouped request](source-review-request.json) · [Real repeat request](repeat/source-review-request.json)

## Actual result

| Measure | Before review | Reviewed first batch | Live repeat |
|---|---:|---:|---:|
| Owner attention accounts | 6 raw candidate cards | 0 | 0 |
| Flags with source dispositions | 0 | 9 | 9 reused |
| Unfinished claim research | 9 pending flags | 2 | 2 |
| Blocked/failed/held collection sources | 5 | 5 | 4 |
| Outstanding internal research | Previously conflated with attention | 7 | 6 |

Seven documents were retrieved once per account/document group for the first nine-flag review. Claims sharing Clark's year review and Food Lifeline's campaign article were checked separately. The live repeat rechecked seven originals, requested zero desktop reviews, reused all nine decisions and retained nine history records. It found 0 new accounts, 0 new candidates and 0 changed candidates. It created no duplicate owner cards. The initial six accounts were machine candidate/recheck cards, not six established commercial opportunities.

## Nine dispositions

| Account / flag | Disposition | Reason |
|---|---|---|
| Surrey, December operating pressure | Historical context | Just-sufficient fundraising coexists with better food supply and doubled distribution; no present capacity deficit established. |
| Surrey, June fundraising pressure | Contradicted interpretation | Donations were keeping up with demand. Summer concern was prospective. |
| Clark, operating strain in year review | Historical context | Lost staffing and increased demand are supported; distribution and volunteer response improved. |
| Clark, financial pressure in year review | Historical context | Nearly USD900,000 government funding lost; donor support rose 132%. No comparable dollar baseline or present net gap supplied. |
| Clark, VP appointment as strain | Unsupported interpretation | Appointment and capability improvements do not establish operational inadequacy. |
| FamilyWorks, campaign performance | Research required | Matching activity exists; campaign close, final outcome and growth comparison year remain unestablished. |
| Food Lifeline, campaign performance | Positive context | More than USD400,000 raised at the gala, without evidence of a missed target. |
| Food Lifeline, fundraising pressure | Unsupported interpretation | “Down” is part of Dress Down Hunger, not a donation decline. |
| Good Business Network, financial pressure | Research required | Substantive self-report of public funding cuts, but no date, amount or current remaining gap. A donation button was not the evidence. |

Latest dated comparative Surrey demand/donation evidence found ends on **11 June 2026**. Current distribution calendars show operating arrangements, not a demonstrated post-June change in demand, donations or distribution capacity. Searches checked later 2026 reporting and first-party operating pages; third-party social mirrors were not accepted as originals. No claim that all possible later evidence has been exhausted is made.

## Publication and recovery

Collection now emits `collection-worklist.json` as diagnostics and a separate `source-review-request.json`. Its default `worklist.md` is gated owner output, never a raw pending-flag queue. Structured desktop verdicts are validated against packet ID, candidate version, original version and passage hashes before any batch changes are applied. Factual judgments, flag interpretations and commercial judgments remain separate. Missing metadata cannot be hidden by calling an item actionable.

Unsupported interpretations are closed with reasons, not erased. Two unfinished claim questions remain in `research-queue.json`: FamilyWorks campaign period/outcome and Good Business Network's cut period/current impact. Current source issues are Hip Hop Is Green 403, Vancouver contracts robots restriction, North Delta Rotary robots access, and Greater Vancouver Food Bank report held under previously inspected handling terms. The CRA register transient failure in the prior snapshot recovered in the repeat. An unchanged/304 source is distinct from blocked/held access and from an old observation first discovered today.

Relevant or cited passage changes invalidate only affected claim approvals. Comparison and contradictory context can affect several claims. Unchanged reruns retain original review timestamps and semantic fingerprints. The existing append-only private feedback journal is preserved, applied only to identical fingerprints, and never exported publicly.

Full parsed originals for future desktop reading are cached only in ignored local runtime storage. Public evidence contains bounded checking excerpts, hashed locators and paraphrases. If desktop review cannot run, collection status remains current while the saved last-reviewed worklist keeps its original date and explicit fallback label.

## Validation and scheduling

All **122 tests pass**. [Test transcript](tests.txt) covers unchanged 200/304 reuse, one changed claim, changed cited evidence, new contradictory evidence, inaccessible-source fallback/recovery, incomplete/stale/malformed batches, donation-page interpretation, campaign success, local original cache and private decision preservation. Changed/contradictory/inaccessible cases are controlled tests, not purported live external changes. The repeat above is a real network run.

The existing morning app workflow was updated to follow [the desktop source-review protocol](../../../frameworks/DESKTOP_SOURCE_REVIEW.md). [Schedule update](schedule-update.json) records enabled status and the unchanged flexible daily recurrence. The returned schedule has DTSTART 08:05 Vancouver and RRULE 07:30, with no next-run timestamp supplied. No exact future firing time is asserted. Mac environment selection is inherited, with no binding details returned. Native registration remains blocked from the prior attempt. A later scheduled Mac run is still unverified. No new schedule was created.
