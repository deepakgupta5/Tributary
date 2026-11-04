# Tributary evidence report

Synthetic source demonstration. No live-source coverage or independent human verification.

Evidence snapshot: `7dbd24303da7eb793d93e39f730b869708ede7e4f463fd2482e695ddbfd97d23`

## Execution records

- researcher: Codex current coding session, same assistant for all roles, model_checked, coding-session-2026-11-03-researcher, 2026-11-04T00:53:09.071873+00:00; `stage_752175f26099cbb9f3426b6af81b3b1b5a42852febf89a1ebda21815e7917624`.
- skeptic: Codex current coding session, same assistant for all roles, model_checked, coding-session-2026-11-03-skeptic, 2026-11-04T00:53:09.077524+00:00; `stage_7ac8443f194496390674919ac274c063762989545db75b30871d1b321d2c1114`.
- fact-checker: Codex current coding session, same assistant for all roles, model_checked, coding-session-2026-11-03-fact-checker, 2026-11-04T00:53:09.084449+00:00; `stage_2d5f4f4a6a3d9972a677c77b0c1bc2cf95dcc33e7c989830c34cbfae76f2a5ee`.

Same-assistant or fixture passes do not establish independent corroboration.

## DEMO_CA_001

Current status: unknown. Organizational route: not investigated.

### c1: verified (model_checked)

The synthetic 2026 campaign raised CAD 64,000.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `campaign`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The source says CAD 64,000 for the 2026 actual amount and separately gives the CAD 80,000 target.

### c2: verified (model_checked)

The 2026 target was CAD 80,000.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `campaign`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The source gives CAD 80,000 as the 2026 target; this is not the actual amount raised.

### c3: verified (model_checked)

The director described serving more households and a changed funding mix.

Type: attributed_statement. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `leader`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The quotation matches the director statement in the source. It is an attributed statement, not independent proof of the funding situation.

### c5: unverifiable (model_checked)

Supporter re-engagement may be worth investigating.

Type: hypothesis. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `demand`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

A commercial investigation hypothesis is not established by the source. Donor retention, budgets, and internal causes remain unknown.

Alternative: The funding mix, campaign design, or service demand may have changed; donor retention is unknown.

### c6: verified (model_checked)

Monthly service requests reached 300.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `demand`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The source reports 300 monthly requests. This does not prove a fundraising or donor-retention problem.

## DEMO_WA_001

Current status: unknown. Organizational route: not investigated.

### c4: verified (model_checked)

The deadline moved from September 30 to October 14 because of a venue closure. The source does not publish a campaign total.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_aa55f4680496e24d69b697aa` / `deadline`. Event date: unknown.
Origins: fixture://demo-wa-update/campaign-update (published 2026-10-15)

The source explicitly gives the venue closure as the reason and says no campaign total is published. Publication date is known; event date remains unknown.

## Skeptic issues and dispositions

- medium: A possible commercial hypothesis lacks donor-level evidence. (c5). limitation retained: The commercial hypothesis remains unverifiable; donor retention is not disclosed.
- medium: The packets do not establish independent corroboration or a current-status update. (c1, c2, c3, c4, c6). unresolved: No independent corroborating record or subsequent update is in these synthetic sources.

## Claim-check coverage

- contradicted: 0/6
- partly verified: 0/6
- pending: 0/6
- unverifiable: 1/6
- verified: 5/6
- Completed checks: 6/6

## Unknowns

- Donor retention is not disclosed.
- Consulting budget and willingness to engage are unknown.
- Current status has not been rechecked.
- No real sources have been integrated.

## Collection audit

- Run 1 (2026-11-04T00:53:09.070227+00:00): {"duplicate":1,"inserted":2,"rejected":1,"total":4}
