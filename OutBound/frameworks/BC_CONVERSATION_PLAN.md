# BC conversation plan: from the archived BC charity list to owner conversations

Owner: Deepak Gupta
Status: Approved by the owner on 2026-11-06 and recorded at his instruction. This document is the operating plan for BC nonprofit outbound. It sits above the build plan: [PROJECT_PLAN.md](PROJECT_PLAN.md) governs the Tributary system; this plan governs the market objective the system serves. Target definition: [PRD.md](PRD.md), "Current outbound target: mid-sized BC nonprofits." Trigger evidence rules: [BC_TRIGGER_SCREEN.md](BC_TRIGGER_SCREEN.md).

## Objective

Have actual conversations with BC nonprofit people by **Friday, November 13, 2026**, starting from the archived list of 12,040 BC charity records (`OutBound/data/archive/BC-charity-candidates-2024.txt`; historical CRA 2024 identification data, eligibility and current status unchecked, archived and not enabled for collection or outreach until screened — see Step 4 of the repo-update program below).

Success test: **5 conversations held or firmly booked by November 13.** Under 2 means the problem is trigger quality or channel; fix that before adding volume. Funnel counts are recorded at each step (cards → contact-ready → attempts → conversations); a step does not start until the step above it has produced its output.

## Working pitch (owner correction, 2026-11-06)

The pitch used in conversations is the tight pitch, not the website framing:

> Help nonprofits raise more money from their **existing donors**, and fine-tune how they do that using analytics and systems.

Known mismatch, recorded: autonomybridge.com/nonprofits frames the offer as operational leadership and states that the nonprofit team retains fundraising strategy, donor relationships, and solicitation. A prospect who checks the site after hearing the tight pitch will see a different offer. Correcting the PRD to the tight pitch is Step 2 of the repo-update program below. Revising the website is a separate owner decision, not yet made.

Buyer order under the tight pitch: development/fundraising lead first, Executive Director second.

## Target (as recorded in the PRD, commit `1fd7cf2`)

A mid-sized BC nonprofit with roughly **$1M–$5M in annual revenue and 10–50 paid staff**, and at least one live trigger. Working definitions for the BC pilot: **CAD annual revenue** (latest available) and **paid staff headcount**.

Practical test for every outbound candidate: **What decision or delivery milestone is at risk, by when, and what evidence says it is still open?** An award announcement or ED job posting is a reason to investigate; qualification requires the link to a live decision or delivery obligation.

Size fit and trigger evidence are assessed **separately**:

- Size fit, no live trigger → **Monitor**
- Plausible trigger with a material evidence gap → **Investigate**
- Supported size fit plus a live trigger → qualified for **outbound preparation**

The archived 12,040 records still need to be screened against this target (Step 4 below). The size screen's historical result — 754 revenue/staff-proxy matches, plus 414 revenue matches with incomplete staffing retained for enrichment — is recorded in BC_TRIGGER_SCREEN.md; the dataset behind it is not yet a repository artifact (Step 4 closes this).

## Decisions taken (owner, 2026-11-06)

| # | Decision | Detail |
| --- | --- | --- |
| 1 | Warmth inventory is zero | No existing contacts in the BC nonprofit/funder world. Warmth must be manufactured (events, intermediaries, social engagement). Direct outreach is the starting route; warmth-building runs in parallel. |
| 2 | All channels in, for this work | LinkedIn, Facebook, Twitter/X, Threads, Instagram. This is specific to BC nonprofit outbound; it does not change channel boundaries set for other work. |
| 3 | In-person geography | West Vancouver to Abbotsford — roughly one hour's drive from Coquitlam (incl. Port Coquitlam, Port Moody, Burnaby, Vancouver, North Vancouver, New Westminster, Richmond, Surrey, Langley, Maple Ridge/Pitt Meadows). Outside that corridor: remote/monitor only for the pilot. |
| 4 | Event rule | **Pay for in-person networking.** Paid virtual events are not proposed. Free virtual events are acceptable. |
| 5 | Events: attend | AFP National Philanthropy Day, Fri Nov 13, River Rock, Richmond — $130 non-member (registration closes Wed Nov 11; buy decision pending). CAGP Greater Vancouver Watch Party, Wed Nov 25, and Radically Reciprocal, Thu Nov 26, Vancouver Foundation — fees not published; one enquiry to the chapter settles both. AFP Greater Vancouver AGM, Wed Nov 25, virtual — free. Coquitlam Foundation Christmas Benefit Breakfast, Thu Dec 3 — $30; ticket purchase channel still to be found. |
| 6 | Events: skipped, do not re-propose | Housing Central Conference, Nov 16–18 ($1,550 non-member; room is mostly government-funded housing organizations — weak existing-donor base). Crisis Comms Lab, Dec 1 ($121.85; comms audience, not the donor-revenue owner). AFP Global sponsored webinar, Dec 9 (paid virtual). |
| 7 | Governance | No unilateral changes. Every material decision is stated, decided by the owner, and recorded in `decisions/DECISIONS.md` per its change procedure, with affected documents updated in the same change where practical. Assistant reviews and proposals stay in owner chat until the owner approves them for the repository record. |
| 8 | Shared workspace | This repository is the shared workspace for the owner, Codex, Bertie (Muse), and ChatGPT. Work is coordinated through repository artifacts (documents, issues, pull requests); each contributor verifies against the recorded plan and decisions. |

## Execution steps (November 6–13, 2026)

| Step | When | Action | Output |
| --- | --- | --- | --- |
| 1 | Fri Nov 6 | Geography + form cut of the 754 size-fit and 414 enrichment records against the Decision 3 corridor. Foundations (designations A/B) split to a funder/intermediary list. | Pool A, with a real count computed from the data — no count is stated before it is computed. |
| 2 | Sat Nov 7 – Sun Nov 8 | Trigger screen on a bounded batch (~60–80 accounts): shared sources across Pool A first; account-specific probes only where an anchor appears. Evidence rules per BC_TRIGGER_SCREEN.md. | Cards classified inferred live trigger / watch / monitor / resolved. |
| 3 | Mon Nov 9 (morning) | Owner review of batch cards: worth a conversation, yes/no, one-line reason (this is the screen's quality test). | Top 15 accounts, ranked. |
| 4 | Mon Nov 9 | People and contact routes for the 15 only: development/fundraising lead, ED, board chair. Sources in order: organization website → annual report → CRA directors list → LinkedIn (title/currency check). Published, verified contact details only — never guessed email patterns. | 15 contact-ready accounts, ~30–45 named people. |
| 5 | Mon Nov 9 | Outreach scripts (phone opener, 30-second voicemail, 4-line email, LinkedIn note), all built from each card's one neutral discovery question. The trigger is an inference and is presented as a question, not a claim. Warmth in parallel: BC Non-Profit Network updates signup, follow the 15 organizations, event registrations per Decision 5. | Scripts approved by owner before use. |
| 6 | Tue Nov 10 – Wed Nov 11 | Outreach wave 1: one primary channel per account, in order — phone, then email, then LinkedIn. Every attempt logged. (Nov 10 starts late: owner is driving a 3:30 AM airport drop-off.) | Attempts and responses logged per account. |
| 7 | Thu Nov 12 | One follow-up to wave-1 non-responders, different channel, same question. Intermediary conversations in parallel (Vantage Point; in-corridor BCNN steering-committee organizations). | Follow-ups logged; intermediary outcomes recorded. |
| 8 | Fri Nov 13 | Hold booked conversations (afternoon; owner's morning is committed). Close the loop: per conversation — trigger confirmed or refuted, their exact words, any past-buying evidence. | Conversation log + funnel numbers against the success test. |

## Repo-update program (owner instruction, 2026-11-06)

| Step | Work | Status |
| --- | --- | --- |
| 1 | Record this plan, the objective, the steps, and the decisions in the repository. | This document; decisions also entered in `decisions/DECISIONS.md`. |
| 2 | Correct the pitch in the PRD (donor-base gate, buyer order, donor-side triggers) and sync the PRD with PROJECT_PLAN.md (single status source). | Pending — draft goes to the owner for approval before landing. |
| 3 | Decide the PRD Q1 categories (hospitals, universities, religious organizations, advocacy groups) and record each decision with rationale in DECISIONS.md. Owner decision per category; nothing is cut unilaterally. | **Decided 2026-11-06: all four categories excluded as buyers for the pilot** (hospital foundations remain eligible as separate entities). Recorded as DECISIONS.md entry D062. |
| 4 | Screen the archived 12,040 against the target and the Step 3 decisions; commit the output dataset and a reconciliation table (12,040 in → excluded by reason, with counts → 754 size-fit → 414 enrichment). Verify the 754/414 reproduce, or document the variance. | Issue opened 2026-11-06: [Issue #9](https://github.com/deepakgupta5/Tributary/issues/9) — Codex to execute; Bertie verifies counts on completion. |

## Boundaries

- Outreach is manual. Tributary does not send outreach and does not infer need, budget, authority, or willingness to engage without direct evidence.
- Private pursuit data — named-prospect judgments, relationship notes, outreach status — stays outside this public repository (per PRD). This plan records objectives, steps, decisions, and funnel counts, not private pursuit detail.
- Board/director overlap analysis is private-layer only and is never part of shared or public material.
- Do not bypass access controls; published sources only.

## Status log

- 2026-11-06 — Plan, objective, steps, and Decisions 1–8 recorded at the owner's instruction. Repo-update program Steps 2–4 pending as tabled above. AFP Philanthropy Day buy decision outstanding (deadline Wed Nov 11).
- 2026-11-06 — Repo-update program Step 4 issued: GitHub Issue #9 tasks Codex with screening the archived 12,040 against the target and the D062 exclusions, committing the population dataset and reconciliation table, and verifying the 754/414 gate numbers reproduce or documenting the variance.
- 2026-11-06 — Q1 decided (program Step 3): hospitals, universities, religious organizations, and advocacy groups excluded as buyers for the pilot; hospital foundations remain eligible. DECISIONS.md entries D058–D062 recorded. This document, the frameworks index, and the decision entries landed on main on 2026-11-06 (commits 3000a1e, f1983e3, ff6c341) after the owner installed the Muse GitHub App on the deepakgupta5 account with Tributary selected — earlier pushes had failed with 403 because the app was not installed.
