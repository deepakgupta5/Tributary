# November 7 daily collection: manual recovery and reviewed publication

[Reviewed worklist](worklist.md) · [Eleven dispositions](dispositions.md) · [Internal research queue](research-queue.json) · [Collection attempt log](run.json) · [Verification](verification.json)

The app scheduler recorded a failed attempt for Tributary daily collection. Its diagnostics expose no technical cause; delivery status is unknown. The operating checkout's latest result still dated to the November 5 manual proof before this recovery. This record does not establish a successful unattended run or a scheduler repair.

The included desktop assistant manually invoked `python3 scripts/run_daily.py --scheduled` on the Mac on November 7. The invocation started at 08:23:46 Vancouver time. The command labels its run `scheduled_local` because of that flag; **it was a manual recovery, not an observed scheduler execution**. It used the configured operating checkout at commit `81b6798`, preserved its runtime source checkpoints and private owner journal, and resumed after the missed November 6 collection day. No operating-checkout code, schedule or source inventory was changed.

| Actual result | Count |
| --- | ---: |
| Configured/attempted source endpoints | 57 |
| Unchanged checks | 51 |
| Successful updated source checks | 2 |
| Blocked checks | 3 |
| Handling holds | 1 |
| New accounts | 0 |
| New signal candidates | 0 |
| Changed signal candidates | 0 |
| Historical-source rechecks | 2 |
| Claims checked in desktop review | 11 |
| Owner attention accounts | 0 |
| Outstanding research | 6 |

Two changed source responses are not two new or changed signal candidates. Old observations rechecked today are not newly occurring events.

## Source review

Nine original documents were re-fetched using permitted source handling and reconciled to the packet's exact document versions and paragraph hashes. An incomplete tool display required one giving-profile retrieval to be repeated; this was recovery from truncated output, not per-flag fetching. Full originals were not saved to a persistent cache. The producing command's temporary originals were confirmed expired. Persisted document state contains hashes, metadata and bounded checking excerpts, not full text.

The operating state had nine earlier verdicts without linked checkpoint IDs, plus two pending claims. These were reopened for the required chain rather than falsely inherited as approved decisions. All eleven claims now have separate factual and commercial verdicts, explicit dates or unknown reporting periods, comparison bases, source locators/hashes and counterevidence. Four sequential checkpoint executions are saved under `checkpoints/`. They used the same included assistant and shared context; they are not independent reviewers.

Python validated the full linked chain and saved the verdicts at **08:29:28 Vancouver time, November 7** before publishing the owner view:

- Six supported context dispositions, including positive campaign results and Surrey's dated ED search. None establishes a concrete current donor-revenue decision for owner escalation.
- Three unsupported or contradicted pressure interpretations, including the `Down` keyword in the name Dress Down Hunger and Surrey's explicit June statement that donations were keeping up.
- Two continuing claim questions: an undated Good Business Network funding-cut statement, and FamilyWorks campaign timing/goal status.

The Food Lifeline article's October 20 metadata conflicts with a retrospective October 29 passage. That discrepancy is recorded rather than silently resolved. Surrey's November 8 hiring deadline is current, but an ED vacancy alone does not establish donor-revenue work at risk. Comparable reviewed evidence on demand, donations and distribution still ends on June 11; the later recruitment brief provides a different, incompletely dated basis.

Four source-access/handling items remain: philanthropy.org returned HTTP 403; Vancouver procurement is blocked by robots; North Delta Rotary's robots request returned 403; Greater Vancouver Food Bank first-party processing remains held under the inspected terms. They remain internal, separately from the two claim questions. They are not counted as unchanged checks or absent findings.

## Recovery verification and limits

A second invocation of the scheduled command was skipped by the same-day guard. It did not perform a second collection. The private feedback database hash remained unchanged across review completion. The source review CLI validated all eleven verdicts against the packet and recorded state. Recheck the saved public chain offline with:

```sh
python3 OutBound/evidence/daily-2026-11-07/verify.py
```

No paid model API, source purchase, login, outreach or schedule change was used. This evidence update is published separately at the owner's subsequent instruction; the recovery job itself did not commit or push. Runtime state, private feedback, full source originals and private worklist overlays are excluded.

Remaining operational limits: unattended execution is unverified, the scheduler failure has no exposed cause, and six research items remain. The existing 57-endpoint inventory is the bounded Day 6 scope, not monitoring of the new 323-record BC Pool A. Current registry status, donor-base qualification and Pool A trigger research remain separate work.
