"""Versioned candidate signals, distinct from factual and owner approval.

python3 -m tributary.signals STATE OUTPUT --baseline STATE --as-of YYYY-MM-DD
Only explicit event types map to rules. Keywords never establish a need.
"""
import argparse
from calendar import monthrange
from copy import deepcopy
from datetime import date, datetime
from zoneinfo import ZoneInfo
import hashlib
import json
from pathlib import Path

from tributary.resolution import ROOT, attach_award

VERSION = 'day4-v1'
RULES = {
    'fundraising_pressure': ('fundraising_pressure', 'Check whether supporter or renewal work could help.', 'A one-off timing or campaign change may explain the reported result.'),
    'campaign_comparison': ('campaign_improvement', 'Check whether comparable campaign results warrant supporter follow-through research.', 'Campaign scope, reporting periods or participant mix may differ.'),
    'financial_pressure': ('financial_pressure', 'Check the current operating position and whether outside support is feasible.', 'A planned drawdown or restricted-fund accounting may explain the reported pressure.'),
    'demand_change': ('operational_strain', 'Check whether demand has created a delivery or operating-capacity gap.', 'The organization may already have expanded capacity.'),
    'critical_vacancy': ('operational_strain', 'Check whether the vacancy creates a temporary leadership or execution gap.', 'Recruitment may be routine and internal coverage adequate.'),
    'funding_award': ('new_commitments', 'Check delivery obligations and whether operating or data work is relevant.', 'The award may fully fund delivery through the existing team.'),
    'funding_loss': ('financial_pressure', 'Check the current funding response and capacity for outside support.', 'Replacement funding or planned service changes may already resolve the loss.'),
    'campaign': ('new_commitments', 'Check campaign delivery and follow-through requirements.', 'An active campaign may be performing as planned.'),
    'new_program': ('new_commitments', 'Check delivery ownership and execution requirements.', 'The existing team may have adequate capacity.'),
    'new_geography': ('new_commitments', 'Check delivery requirements in the new geography.', 'The expansion may be routine and fully staffed.'),
    'partnership': ('new_commitments', 'Check which partner owns the delivery work.', 'Partners may supply all required capability.'),
    'facility_change': ('new_commitments', 'Check whether the change creates operating transition work.', 'The change may simplify operations or already be complete.'),
    'service_reduction': ('operational_strain', 'Check the current service position and cause of the reduction.', 'The change may be planned or demand-led rather than financially driven.'),
    'leadership_change': ('operational_strain', 'Check whether a transition creates a temporary execution requirement.', 'The successor and transition arrangements may already be in place.'),
    'modernization': ('campaign_improvement', 'Check the stated data or operating objective and delivery ownership.', 'An existing provider or internal team may already own the work.'),
    'sponsored_support': ('sponsored_support', 'Check eligibility, sponsor payment and application requirements.', 'The program may be closed or unsuitable for this organization or provider.'),
    'vendor_request': ('sponsored_support', 'Check the current deadline, scope and provider eligibility.', 'The request may be closed or outside the service scope.'),
}
# Explicit aliases preserve the observable event class, without keyword inference.
for alias, base in {'new_service':'new_program', 'usage_change':'demand_change',
                    'hiring_surge':'critical_vacancy', 'major_commitment':'partnership',
                    'facility_opening':'facility_change', 'facility_closure':'facility_change',
                    'relocation':'facility_change', 'data_modernization':'modernization',
                    'technology_modernization':'modernization', 'public_support_request':'vendor_request'}.items():
    RULES[alias] = RULES[base]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def months_before(day, count):
    month = day.year * 12 + day.month - 1 - count
    year, month = divmod(month, 12)
    return date(year, month + 1, min(day.day, monthrange(year, month + 1)[1]))


def assess(event, as_of):
    """A rule proposes a hypothesis, never purchasing capacity or factual approval."""
    rule = RULES.get(event['event_type'])
    dates = [e.get('event_date') or e.get('publication_date') for e in event['evidence'].values()]
    dates = [date.fromisoformat(d) for d in dates if d]
    latest = max(dates) if dates else None
    if latest and latest > as_of:
        freshness = 'future_date_needs_review'
    elif latest and latest >= months_before(as_of, 6):
        freshness = 'recent_development'
    elif latest:
        freshness = 'older_event'
    else:
        freshness = 'undated'
    # A fresh observation is a candidate investigation reason, not an ongoing-need claim.
    current = bool(rule and freshness == 'recent_development'
                   and event.get('disposition') not in ('positive_context','historical'))
    category, relevance, alternative = rule or ('unclassified', 'Relevance unassessed.', 'A mention alone may have no service relevance.')
    return dict(rule_version=VERSION, category=category, possible_relevance_hypothesis=relevance,
        alternative_explanation=alternative, freshness=freshness,
        freshness_basis='event date, otherwise publication date; retrieval is never a freshness proxy',
        current_reason_to_investigate=current, current_status='unknown',
        capacity_to_engage=dict(evidence='A funding award is restricted program context only.' if event['event_type']=='funding_award' else 'None established.',
                                consulting_budget='unknown', authority='unknown', willingness='unknown'),
        donor_retention='unknown', evidence_quality='candidate', review_status='pending',
        tier='investigate' if current else 'monitor',
        next_action=event.get('next') or 'Check the original evidence and current status, then resolve relevance and identity gaps.',
        contradictory_evidence=[], contradiction_check='pending',
        missing_facts=['Current status and any resolution', 'Service relevance', 'Capacity and procurement route', 'Contract payee where applicable'],
        version=digest([VERSION, event]))


def build(state, identities, pilot=None):
    inventory = {s['id']:s for s in json.loads((ROOT/'OutBound/data/day2-sources.json').read_text())}
    publishers = {'food':'Seattle Department of Neighborhoods','housing':'Seattle Office of Housing','housing-feed':'Seattle Office of Housing','contracts':'City of Vancouver','cra':'Canada Revenue Agency','irs':'Internal Revenue Service'}
    accounts = deepcopy(identities['accounts'])
    mapping = {k:v['account_id'] for k,v in identities['ledger'].items()}
    account_keys = {v['day2_account']:v['account_id'] for v in identities['ledger'].values()}
    events, documents, ledger = {}, {}, {}
    for old, name in state['accounts'].items():
        aid = account_keys.get(old, old)
        accounts.setdefault(aid, dict(name=name, basis='Publisher label; identity pending', registration='unchecked', question='Verify legal identity and eligibility.', inputs=[], events=[]))
    for aid, account in accounts.items():
        relationship = account.get('reviewed_relationship')
        account['official_id'] = (relationship.get('ein') if relationship and relationship['role'] in {'operating_entity','program_parent'} else aid if aid[:1].isdigit() else None)
        account['official_id_role'] = relationship['role'] if relationship else ('registry_entity' if account['official_id'] else None)
        account['official_id_entity'] = relationship['name'] if relationship and account['official_id'] else account['name'] if account['official_id'] else None
        account['identity_relationship'] = relationship
        account['headquarters'] = None
        account['area_served'] = None
    for key, history in sorted(state['items'].items()):
        version = history[-1]
        item = deepcopy(version['item'])
        aid = mapping.get(key, account_keys.get(item['account'], item['account']))
        sid = key.split('/')[0]
        src = inventory.get(sid,{})
        doc = documents.setdefault(item['url'], dict(url=item['url'], source=sid,
            publisher=publishers.get(sid), title=None, source_type=src.get('type'), geography=src.get('geography'), language='English',
            publication_date=item.get('publication_date'), title_status='not captured',
            response_sha256=state['sources'].get(sid,{}).get('checkpoint',{}).get('sha256'),
            last_successful_check=state['sources'].get(sid,{}).get('last_success'), items=[]))
        doc['items'].append(key)
        eid = None
        if sid not in {'irs','cra'}:
            round_key = {'food':'Seattle/Food Equity Fund/2026','housing':'Seattle/Urgent Operating Support/2026'}.get(sid)
            if round_key:
                eid = attach_award(events, aid, round_key, key, item)
                event = events[eid]
                event.update(event_type='funding_award', route=dict(name='Seattle Department of Neighborhoods' if sid=='food' else 'Seattle Office of Housing', evidence_url=item['url'], basis='Published funder-recipient relationship; no promised introduction'))
            else:
                eid = 'context-' + digest([aid,item['url']])[:24]
                event = events.setdefault(eid, dict(account_id=aid, event_type='unclassified_context', evidence={}, route=None))
            event['evidence'][key] = dict(item, first_seen_at=history[0]['retrieved_at'], retrieved_at=version['retrieved_at'], evidence_hash=digest(item), version=len(history))
            event['first_seen_at'] = min(e['first_seen_at'] for e in event['evidence'].values())
            event['contract_payee'] = None
        ledger[key] = dict(account_id=aid, event_id=eid, disposition='event' if eid else 'identity_only')
    # Earlier pilot observations are real prior evidence, not five newly discovered awards.
    for history in (pilot or {}).get('events',{}).values():
        item = history[-1]
        old = 'WA:' + item['account'].casefold()
        aid = account_keys.get(old, old)
        prior_at = pilot['attempts'][0]['at']
        evidence = dict(account=old, locator=item['locator'], fact=f"City announced USD {item['amount_usd']:,} in urgent operating support funding for {item['account']}.", url=item['source'], publication_date=item['announcement_date'], event_date=None)
        eid = attach_award(events, aid, 'Seattle/Urgent Operating Support/2026', 'pilot/'+item['account'], evidence)
        event = events[eid]
        event.update(event_type='funding_award', contract_payee=None, route=dict(name='Seattle Office of Housing', evidence_url=item['source'], basis='Published funder-recipient relationship; no promised introduction'))
        event['evidence']['pilot/'+item['account']].update(first_seen_at=prior_at, retrieved_at=prior_at, evidence_hash=digest(evidence), version=len(history))
        event['first_seen_at'] = min(e.get('first_seen_at',prior_at) for e in event['evidence'].values())
    for a in accounts.values():
        a['events'] = []
    for eid,e in events.items():
        accounts[e['account_id']]['events'].append(eid)
        event_dates = {v['event_date'] for v in e['evidence'].values() if v.get('event_date')}
        e['event_date'] = next(iter(event_dates)) if len(event_dates)==1 else None
        e['publication_dates'] = sorted({v['publication_date'] for v in e['evidence'].values() if v.get('publication_date')})
        e['last_retrieved_at'] = max(v['retrieved_at'] for v in e['evidence'].values())
        e['factual_observations'] = sorted({v['fact'] for v in e['evidence'].values()})
    return accounts, events, documents, ledger



def add_typed_events(accounts, events, inputs, documents=None, ledger=None):
    """Import bounded structured observations. No free-text inference or approval."""
    required = {'account_id','event_type','event_reference','fact','url','locator',
                'event_date','publication_date','first_seen_at','retrieved_at'}
    seen = set()
    for row in inputs:
        if not required <= row.keys():
            raise ValueError('Typed event lacks required provenance fields')
        if row['account_id'] not in accounts or row['event_type'] not in RULES:
            raise ValueError('Unknown account or event type')
        if not all(row[k] for k in ('event_reference','fact','url','locator','first_seen_at','retrieved_at')):
            raise ValueError('Empty typed-event provenance')
        for field in ('event_date','publication_date'):
            if row[field] is not None: date.fromisoformat(row[field])
        for field in ('first_seen_at','retrieved_at'):
            if datetime.fromisoformat(row[field]).tzinfo is None:
                raise ValueError('Observation timestamps need a timezone')
        eid = 'typed-' + digest([row['account_id'],row['event_reference']])[:24]
        if eid in seen: raise ValueError('Repeated typed event reference; group evidence before import')
        seen.add(eid)
        evidence = {k:row[k] for k in required-{'account_id','event_type','event_reference'}}
        evidence['evidence_hash'] = digest(evidence)
        evidence['version'] = 1
        events[eid] = dict(account_id=row['account_id'],event_type=row['event_type'],
            event_reference=row['event_reference'],event_date=row['event_date'],
            publication_dates=[row['publication_date']] if row['publication_date'] else [],
            first_seen_at=row['first_seen_at'],last_retrieved_at=row['retrieved_at'],
            factual_observations=[row['fact']],evidence={row['url']+'#'+row['locator']:evidence},
            route=None,contract_payee=None)
        accounts[row['account_id']]['events'].append(eid)
        if 'disposition' in row:
            if row['disposition'] not in ('positive_context','historical','investigate'):
                raise ValueError('Invalid reviewed disposition')
            events[eid].update(disposition=row['disposition'], next=row.get('next'))
        if documents is not None:
            doc=documents.setdefault(row['url'],dict(url=row['url'],source='typed_observation',publisher=None,title=None,source_type=None,geography=None,language='English',publication_date=row['publication_date'],response_sha256=None,last_successful_check=None,items=[],source_admission='pending'))
            doc['items'].append('typed/'+eid)
        if ledger is not None:
            ledger['typed/'+eid]=dict(account_id=row['account_id'],event_id=eid,disposition='event')


def generate(state, baseline, identities, pilot, as_of, event_inputs=None):
    accounts, events, documents, ledger = build(state,identities,pilot)
    old_accounts, old_events, _, _ = build(baseline,identities,pilot)
    event_inputs = event_inputs or {}
    add_typed_events(accounts,events,event_inputs.get('current',[]),documents,ledger)
    add_typed_events(old_accounts,old_events,event_inputs.get('baseline',[]))
    assessments = {}
    for eid, event in events.items():
        a = assess(event,as_of)
        a.update(event_id=eid, account_id=event['account_id'], newly_observed=eid not in old_events,
                 new_account=event['account_id'] not in old_accounts)
        # Compare actual item versions, not changing fetch/checkpoint timestamps.
        a['material_change'] = eid in old_events and digest(event['evidence']) != digest(old_events[eid]['evidence'])
        # A newly attached duplicate pilot row is extra coverage, not a material event change.
        if a['material_change'] and event['event_type']=='funding_award':
            def facts(e):
                return {(v['fact'],v.get('publication_date'),v.get('event_date')) for v in e['evidence'].values()}
            a['material_change'] = facts(event) != facts(old_events[eid])
        assessments[eid] = a
    new = sorted(set(accounts)-set(old_accounts))
    observed = [eid for eid,a in assessments.items() if a['newly_observed']]
    current = sorted({a['account_id'] for a in assessments.values() if a['current_reason_to_investigate']})
    known_new = sorted({a['account_id'] for a in assessments.values() if a['newly_observed'] and not a['new_account']})
    return dict(rule_version=VERSION, as_of=as_of.isoformat(), accounts=accounts, events=events,
        documents=documents, ledger=ledger, assessments=assessments,
        delta=dict(new_accounts=new, newly_observed_events=observed, known_accounts_with_new_events=known_new,
                   newly_signal_bearing_accounts=sorted({events[e]['account_id'] for e in observed if not old_accounts.get(events[e]['account_id'],{}).get('events')}),
                   accounts_with_current_reason=current),
        collection_runs=state['runs'][len(baseline['runs']):],
        limitations=['Candidate signals only. Separate researcher, skeptic and fact-checker execution is pending Day 5.',
            'No independent verification or owner usefulness judgment is claimed.',
            'BC and WA selected English-language endpoints only; other Canadian jurisdictions, local journalism and sector sources remain gaps.',
            'A recent six-month publication/event date supplies current candidate context, not proof that a need persists. Six months is review priority, not a discovery cutoff.',
            'Older observations remain visible. Current status requires fresh supporting evidence; a new retrieval alone does not establish continuation.'])


def render(data):
    d=data['delta']; events=data['events']; accounts=data['accounts']; assessments=data['assessments']
    attempts = [a for run in data['collection_runs'] for a in run['attempts']]
    local_dates = sorted({datetime.fromisoformat(a['at']).astimezone(ZoneInfo('America/Vancouver')).date().isoformat() for a in attempts})
    lines=['# Day 4 signal report', '', f"As of {data['as_of']} (UTC). Collection dates in Vancouver: {', '.join(local_dates) or 'none'}.", '',
           f"**{len(d['new_accounts'])} new accounts; {len(d['newly_observed_events'])} newly observed events; {len(d['accounts_with_current_reason'])} accounts with a current candidate reason to investigate.**", '',
           'New means absent from the Day 3 and earlier housing-pilot baseline. First observation and event recency are separate. Outreach remains manual.', '', '## New accounts', '']
    for aid in d['new_accounts']:
        lines.append(f"- **{accounts[aid]['name']}** (`{aid}`): legal identity and current eligibility pending; headquarters and area served unknown.")
    if not d['new_accounts']: lines.append('None.')
    lines += ['', '## Newly observed events', '', '| Account | Observation | Publication | Event date | First seen / retrieved (UTC) | Timing |', '|---|---|---|---|---|---|']
    for eid in d['newly_observed_events']:
        e=events[eid]; v=list(e['evidence'].values())[-1]; a=assessments[eid]
        lines.append(f"| {accounts[e['account_id']]['name']} | {v['fact']} [{v['locator']}]({v['url']}) | {v['publication_date'] or 'unknown'} | {v['event_date'] or 'unknown'} | {e['first_seen_at']} / {v['retrieved_at']} | {a['freshness']} |")
    if not d['newly_observed_events']: lines.append('| None | | | | | |')
    recent=[e for e in d['newly_observed_events'] if assessments[e]['freshness']=='recent_development']
    older=[e for e in d['newly_observed_events'] if assessments[e]['freshness']=='older_event']
    lines += ['', f"Recent developments newly observed: {len(recent)}. Older events discovered in this cycle: {len(older)}.",
              f"Known accounts with a new event: {len(d['known_accounts_with_new_events'])}. Newly signal-bearing accounts: {len(d['newly_signal_bearing_accounts'])}.", '', '## Current reasons to investigate', '']
    for aid in d['accounts_with_current_reason']:
        for eid,a in assessments.items():
            if a['account_id'] == aid and a['current_reason_to_investigate']:
                v=next(iter(events[eid]['evidence'].values()))
                lines.append(f"- **{accounts[aid]['name']}**: {v['fact']} [Source]({v['url']}). {a['possible_relevance_hypothesis']} {a['next_action']} Review pending.")
    if not d['accounts_with_current_reason']:
        lines.append('None established from this bounded collection. No older award is promoted as evidence of a current operating problem. This is a finding about the collected material, not proof that no current needs exist.')
    lines += ['', '## Older housing evidence and next checks', '',
              'The February announcement provides a route through Seattle Office of Housing and a hypothesis about operating-support relevance. These are monitor items with current-status checks pending. The three pilot awards are repeated coverage, not new events.', '',
              '| Account | USD announced | History | Next investigation |', '|---|---:|---|---|']
    for eid,e in events.items():
        if e.get('award_key')!='Seattle/Urgent Operating Support/2026': continue
        v=next(iter(e['evidence'].values())); a=assessments[eid]
        lines.append(f"| {accounts[e['account_id']]['name']} | {v['fact'].split('USD ')[1].split(' in ')[0]} | {'newly observed older award' if a['newly_observed'] else 'known pilot award, recollected'} | Check current delivery status and whether the award resolved the operating issue; verify legal identity and payee. |")
    lines += ['', 'Possible relevance is a hypothesis: operating or data support could matter if an unmet delivery requirement remains. Alternative: the grant and existing team may already cover the work. An award does not establish consulting budget, procurement authority, willingness to engage, or donor-retention difficulty. All remain unknown.', '',
              '## Collection and reconciliation', '', '| Source | Outcome | Added | Revised | Duplicate rows | Attempt (UTC) |', '|---|---|---:|---:|---:|---|']
    for run in data['collection_runs']:
        for a in run['attempts']:
            lines.append(f"| {a['source']} | {a['outcome']} | {len(a['additions'])} | {len(a['revisions'])} | {a['duplicates']} | {a['at']} |")
    lines += ['', f"Cumulative ledger: {len(ledger := data['ledger'])} items = {sum(v['disposition']=='identity_only' for v in ledger.values())} identity rows + {sum(v['disposition']=='event' for v in ledger.values())} event evidence rows; {len(events)} distinct events, including three pilot awards. No registry row becomes a commercial signal.", '',
              f"Collection additions: {sum(len(a['additions']) for a in attempts)}; revised rows: {sum(len(a['revisions']) for a in attempts)}; duplicate rows: {sum(a['duplicates'] for a in attempts)}. New distinct events: {len(d['newly_observed_events'])}; materially changed existing events: {sum(a['material_change'] for a in assessments.values())}. Backfill batch: {data['collection_runs'][-1]['batch'] if data['collection_runs'] else 'no new collection'}. The bounded inventory is not a complete 12-month archive.", '',
              'GVFB publication remains held under its previously recorded terms; the register remains available for historical identity. Current registration remains unchecked. Day 3 operating-entity, program-parent, fundraising-host and chapter relationships are preserved. Award contract payees remain unknown.', '', '## Review and limitations', '']
    lines += ['- '+x for x in data['limitations']]
    lines += ['', '[Structured signals, identities and item ledger](signals.json) · [Fresh collection state](state.json) · [Baseline pilot](pilot-baseline.json) · [Rules and reproduction](README.md)']
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('state',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--baseline',type=Path,required=True);p.add_argument('--as-of',type=date.fromisoformat,required=True)
    p.add_argument('--event-inputs',type=Path,help='JSON with current and baseline typed observation arrays')
    p.add_argument('--identities',type=Path,default=ROOT/'OutBound/evidence/day-3/worklist.json')
    p.add_argument('--pilot',type=Path,default=ROOT/'OutBound/evidence/day-4/pilot-baseline.json')
    args=p.parse_args()
    read=lambda path:json.loads(path.read_text())
    data=generate(read(args.state),read(args.baseline),read(args.identities),read(args.pilot),args.as_of,read(args.event_inputs) if args.event_inputs else None)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'signals.json').write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
    (args.output/'signal-report.md').write_text(render(data))
    print(json.dumps({k:len(v) for k,v in data['delta'].items()},sort_keys=True))


if __name__=='__main__': main()
