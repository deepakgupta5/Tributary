# Tributary evidence report

Synthetic source demonstration. No live-source coverage or independent human verification.

Evidence snapshot: `7dbd24303da7eb793d93e39f730b869708ede7e4f463fd2482e695ddbfd97d23`

## Execution records

- researcher: synthetic-fixture-author, synthetic_fixture, fixture-research-v1, 2026-11-03T12:00:00+00:00; `stage_498ad5dfb64c8c40cf05a9793f83591835ca3d5d722b796aac2c986f8820b7ee`.
- skeptic: synthetic-fixture-author, synthetic_fixture, fixture-skeptic-v1, 2026-11-03T12:01:00+00:00; `stage_8a2c3f6f244c3a3a1c75f949a0a0e71e6f652a2b320537373114a80f797b1dad`.
- fact-checker: synthetic-fixture-author, synthetic_fixture, fixture-factcheck-v1, 2026-11-03T12:02:00+00:00; `stage_adbe22c64be9f32443a7c34c9aab90089baa136452e4972b4288b0a0a8a96fd5`.

Same-assistant or fixture passes do not establish independent corroboration.

## DEMO_CA_001

Current status: unknown. Organizational route: not investigated.

### c1: contradicted (synthetic_fixture)

The 2026 campaign raised CAD 68,000.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `campaign`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The original says CAD 64,000, not CAD 68,000.

Correction: The 2026 campaign raised CAD 64,000.

### c2: verified (synthetic_fixture)

The 2026 target was CAD 80,000.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `campaign`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The source gives CAD 80,000 as the 2026 target; this is not the actual amount raised.

### c3: contradicted (synthetic_fixture)

The director said funding had collapsed.

Type: attributed_statement. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `leader`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The supplied quotation is not in the original and materially changes its meaning.

Correction: The director said: We are serving more households, but our funding mix has changed.

### c5: unverifiable (synthetic_fixture)

Supporter re-engagement may be worth investigating.

Type: hypothesis. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `demand`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

A commercial investigation hypothesis is not established by the source. Donor retention, budgets, and internal causes remain unknown.

Alternative: The funding mix, campaign design, or service demand may have changed; donor retention is unknown.

### c6: verified (synthetic_fixture)

Monthly service requests reached 300.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_184713993273eeef375e2a99` / `demand`. Event date: 2026-09-30.
Origins: fixture://demo-ca-report/2026-review (published 2026-10-12); fixture://demo-ca-syndication/reprint (published 2026-10-13)

The source reports 300 monthly requests. This does not prove a fundraising or donor-retention problem.

## DEMO_WA_001

Current status: unknown. Organizational route: not investigated.

### c4: partly verified (synthetic_fixture)

The campaign deadline was extended because donations were weak.

Type: observation. Source-faithfulness result only; independent corroboration not established.
Source: `ev_aa55f4680496e24d69b697aa` / `deadline`. Event date: unknown.
Origins: fixture://demo-wa-update/campaign-update (published 2026-10-15)

The extension is supported; weak donations are not. The source attributes the move to a venue closure. Event date remains unknown.

Correction: The deadline moved to accommodate a venue closure; no campaign total was published.

## Skeptic issues and dispositions

- high: Campaign actual differs from the source. (c1). corrected: Correct amount supplied alongside original claim; original remains in the audit history.
- high: The quotation changes the director's statement. (c3). corrected: Faithful quotation supplied.
- high: Deadline extension is assigned an unsupported fundraising cause. (c4). corrected: Stated venue explanation replaces unsupported cause.
- medium: A possible commercial hypothesis lacks donor-level evidence. (c5). limitation retained: Hypothesis remains unverified and separate from factual findings.

## Claim-check coverage

- contradicted: 2/6
- partly verified: 1/6
- pending: 0/6
- unverifiable: 1/6
- verified: 2/6
- Completed checks: 6/6

## Unknowns

- Donor retention is not disclosed.
- Consulting budget and willingness to engage are unknown.
- Current status has not been rechecked.
- No real sources have been integrated.

## Collection audit

- Run 1 (2026-11-04T00:53:09.142674+00:00): {"duplicate":1,"inserted":2,"rejected":1,"total":4}
