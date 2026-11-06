"""Regenerate the account-first, non-award research pass from reviewed public observations."""
import json
from datetime import date
from pathlib import Path
from .signals import ROOT, generate


def report(folder):
    def read(path):
        return path.read_text(encoding='utf-8')
    inputs = json.loads(read(folder/'pressure-inputs.json'))
    state = json.loads(read(folder/'state.json'))
    data = generate(state, state, json.loads(read(folder.parent/'day-3/worklist.json')),
                    json.loads(read(folder/'pilot-baseline.json')), date.fromisoformat(inputs['as_of']), inputs)
    accounts = data['accounts']
    coverage = inputs['coverage']
    if len(coverage) != len(accounts) or {c['account_id'] for c in coverage} != set(accounts):
        raise ValueError('Search coverage must reconcile to the entire account list')
    lines = ['# Account-first pressure and campaign review', '',
             'November 5, 2026 (Vancouver). One combined four-category search per existing account, plus targeted follow-up. Findings are candidate observations. A search without a finding establishes no conclusion about need. This is a supervised web pass; future source changes require fresh collection.', '',
             '## Findings', '', '| Account | Category | Published | Evidence | Assessment and next check |',
             '|---|---|---|---|---|']
    for eid in data['delta']['newly_observed_events']:
        e = data['events'][eid]
        a = data['assessments'][eid]
        v = next(iter(e['evidence'].values()))
        lines.append(f"| {accounts[e['account_id']]['name']} | {a['category']} | {v['publication_date']} | {v['fact']} [Source]({v['url']}) | {e['disposition']}. {a['next_action']} |")
    lines += ['', '## Search coverage', '', 'Selected page shown for each initial search. An unavailable page is a coverage gap. Only original-source or attributed, dated evidence selected for a finding enters the table above. No raw pages retained. GVFB first-party handling hold respected.', '',
              '| Account | Initial page | Outcome |', '|---|---|---|']
    for c in sorted(coverage, key=lambda c: accounts[c['account_id']]['name'].lower()):
        lines.append(f"| {accounts[c['account_id']]['name']} | [Selected result]({c['selected_page']}) | {c['status']} |")
    return '\n'.join(lines)+'\n'


if __name__ == '__main__':
    print(report(ROOT/'OutBound/evidence/day-4'), end='')
