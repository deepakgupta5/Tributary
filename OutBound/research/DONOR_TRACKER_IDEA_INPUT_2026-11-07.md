# Idea input: lapsed-donor tracker (owner-shared, 2026-11-07)

Status: owner-provided idea, recorded at the owner's instruction on 2026-11-07. Not an approved build item; captured for the BC pilot's offer design and conversation prep.

## Source

Newsletter item shared by the owner (screenshot, 2026-11-07), "Community AI workflow of the day": reader Shimon built an AI fundraising campaign assistant with Make.com. The workflow reads emails sent from the crowdfunding platform used for a campaign, extracts the relevant information, and records it in a spreadsheet. Using spreadsheets from previous years' campaigns, it maintains a list of people who have not donated to this campaign yet but have donated in the past. The agent answers emailed questions, e.g. who has already donated, who has not donated but previously gave more than $1,000, or how much a specific person donated. Stack: Make.com AI tools connected to a Gmail account, a Google Drive account holding the spreadsheets, and a ChatGPT account as the processing agent.

## The idea, adapted to the BC pilot

The transferable core is the comparison, not the email scraping: current-campaign (or current-year) giving compared against prior years produces the lapsed-donor (hasn't-given-yet) list, queryable in plain language with amount thresholds.

Adaptation for the pilot's target organizations ($1M-$5M revenue, 10-50 staff, existing donor base):

- Input is a donor CRM export, not crowdfunding emails; Pool A organizations run donor programs out of a CRM.
- Output is the hasn't-given-yet list with prior-giving amounts, plus plain-language questions over it ("who hasn't given this year but gave $1,000+ last year?").
- Donor data stays inside the organization's own systems and access controls. The source workflow routes donor data through Gmail, Drive, and ChatGPT; donor privacy is the expected first objection from a development lead, and keeping data in-house is the differentiator.

## Fit

- Matches the tight pitch (D059): raise more money from existing donors, fine-tuned with analytics and systems.
- Gives the conversation close a concrete fixed-scope first deliverable: stand up the tracker on the organization's existing donor file ahead of a live campaign window (e.g. year-end / GivingTuesday), instead of an abstract analytics engagement.
- Slots into the BC conversation plan's script step: follows the discovery question about who follows up with lapsed donors today.

## Limitations and open questions

- Shimon's implementation is campaign/crowdfunding-shaped; CRM data quality varies by organization (the same untrusted-CRM problem the trigger screen treats as a signal), so setup effort per organization is unproven.
- No pricing, packaging, or build decision has been made. Whether this becomes a pilot deliverable, a demo, or neither is an owner decision.
- This note records an idea and its source; it does not authorize collection, outreach, or product changes.
