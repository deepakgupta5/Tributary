# Batch account resolution

Base: `0946f7a50471e066bb1607653d203878e97e1239` (Day 2 PR #4). [Worklist](worklist.md) · [Identity exceptions](exceptions.md) · [Account, document, event and item ledger](worklist.json).

Run `python3 -m tributary.resolution out/day3` from the repository root. The offline batch reads the [Day 2 ledger](../day-2/state.json), [inventory](../../data/day2-sources.json), [Day 1 discovery records](../live_runs/session-001/records.json), and [selected IRS lookup](irs-lookup.json). The lookup repeats the preliminary exact normalized-name search against the Washington CSV, preserves matching public fields and lists every search label. Three housing pilot names and their previously observed awards are outside this batch.

35 items comprise 12 register rows and 23 recipient rows in one Seattle announcement. The 31 new candidate labels and four previously known-account items map to 34 account rows: Nurturing Roots has two inputs. There are 11 registry-only accounts and 23 accounts with dated announcements. Of the latter, 11 require manual identity resolution. They retain provisional IDs until a payee or sponsor is identified. Unique exact normalized register-name matches are supported by Washington geography; city is the filing city. No official-domain lookup was performed. EIN linkage does not establish current operating status.

The event key uses the recipient and funder round for this announcement, which lists one award per recipient. Additional reporting can be attached with the same supported award reference. Separate awards need distinct references; the batch does not infer an award date or automatically link new articles.

Validation on the Day 3 branch: 65 unit tests passed. Two offline runs produced byte-identical worklist JSON, Markdown and exception queues, including IDs and counts. The Day 1 replay reproduced both committed worklists, and the two Day 2 report commands reproduced both saved reports byte-for-byte.
