from copy import deepcopy
from datetime import date
import json
from pathlib import Path
import unittest

from tributary.signals import RULES, assess, generate, render
from tributary.collect import run

ROOT = Path(__file__).resolve().parents[1]
read = lambda p: json.loads((ROOT/p).read_text())


class SignalsTests(unittest.TestCase):
    def setUp(self):
        self.baseline = read('OutBound/evidence/day-2/state.json')
        self.state = read('OutBound/evidence/day-4/state.json')
        self.identities = read('OutBound/evidence/day-3/worklist.json')
        self.pilot = read('OutBound/evidence/day-4/pilot-baseline.json')

    def generate(self, state=None, baseline=None):
        return generate(state or self.state, baseline or self.baseline, self.identities, self.pilot, date(2026,11,6))

    def test_live_delta_counts_pilot_awards_once_and_keeps_old_dates(self):
        data = self.generate()
        self.assertEqual({data['accounts'][a]['name'] for a in data['delta']['new_accounts']}, {'Solid Ground','Plymouth Housing Group'})
        self.assertEqual(len(data['delta']['newly_observed_events']),2)
        self.assertEqual(data['delta']['known_accounts_with_new_events'],[])
        self.assertEqual(data['delta']['accounts_with_current_reason'],[])
        self.assertEqual(len(data['events']),28)
        self.assertEqual(sum(a['material_change'] for a in data['assessments'].values()),0)
        for eid in data['delta']['newly_observed_events']:
            self.assertEqual(data['assessments'][eid]['freshness'],'older_event')
            e=data['events'][eid]
            self.assertTrue(e['first_seen_at'].startswith('2026-11-06'))
            for v in e['evidence'].values():
                self.assertIsNone(v['event_date'])
                self.assertEqual(v['publication_date'],'2026-02-06')

    def test_registries_never_produce_commercial_signals_and_ledger_reconciles(self):
        d=self.generate()
        self.assertEqual(len(d['ledger']),40)
        self.assertEqual(sum(v['disposition']=='identity_only' for v in d['ledger'].values()),12)
        for k,v in d['ledger'].items():
            if k.startswith(('irs/','cra/')): self.assertIsNone(v['event_id'])
        self.assertIn('107449787RR0001',d['accounts'])
        self.assertEqual(d['accounts']['107449787RR0001']['registration'],'unchecked')

    def test_host_ein_stays_on_relationship_and_provisional_ids_survive(self):
        d=self.generate()
        for aid,row in self.identities['accounts'].items():
            self.assertEqual(d['accounts'][aid]['identity_relationship'],row.get('reviewed_relationship'))
        host=d['accounts']['WA:tongan community food pantry']
        self.assertIsNone(host['official_id'])
        self.assertEqual(host['identity_relationship']['ein'],'31-1580932')
        for e in d['events'].values(): self.assertIsNone(e['contract_payee'])

    def test_every_category_has_rules_and_capacity_is_not_inferred(self):
        self.assertEqual({r[0] for r in RULES.values()}, {'fundraising_pressure','campaign_improvement','financial_pressure','operational_strain','new_commitments','sponsored_support'})
        for event_type in RULES:
            with self.subTest(event_type=event_type):
                event=dict(event_type=event_type,evidence={'a':{'event_date':None,'publication_date':'2026-10-01'}})
                a=assess(event,date(2026,11,6))
                self.assertEqual(a['review_status'],'pending')
                for field in ('consulting_budget','authority','willingness'):
                    self.assertEqual(a['capacity_to_engage'][field],'unknown')
                self.assertEqual(a['donor_retention'],'unknown')
                self.assertTrue(a['alternative_explanation'])

    def test_recency_uses_event_then_publication_never_retrieval(self):
        event=dict(event_type='funding_award',evidence={'x':dict(event_date='2025-12-01',publication_date='2026-11-01',retrieved_at='2026-11-06')})
        self.assertEqual(assess(event,date(2026,11,6))['freshness'],'older_event')
        event['evidence']['x'].update(event_date=None,publication_date=None)
        self.assertFalse(assess(event,date(2026,11,6))['current_reason_to_investigate'])
        event['evidence']['x']['publication_date']='2027-01-01'
        self.assertEqual(assess(event,date(2026,11,6))['freshness'],'future_date_needs_review')

    def test_repeat_no_new_accounts_events_or_material_change(self):
        data=self.generate(baseline=self.state)
        for values in data['delta'].values(): self.assertEqual(values,[])
        self.assertFalse(any(a['material_change'] for a in data['assessments'].values()))
        self.assertEqual(data,self.generate(baseline=self.state))

    def test_changed_fact_at_known_account_reopens_candidate_version(self):
        s=deepcopy(self.state)
        k='housing/Bellwether Housing'
        v=deepcopy(s['items'][k][-1]);v['item']['fact']='Revised operating award amount; synthetic test.'
        v['retrieved_at']='2026-11-07T01:00:00+00:00';s['items'][k].append(v)
        d=self.generate(s,self.state)
        changed=[a for a in d['assessments'].values() if a['material_change']]
        self.assertEqual(len(changed),1)
        self.assertFalse(changed[0]['new_account']);self.assertFalse(changed[0]['newly_observed'])
        self.assertEqual(changed[0]['review_status'],'pending')

    def test_new_event_at_known_account_does_not_become_new_account(self):
        s=deepcopy(self.state)
        k='housing/Bellwether Housing'
        v=deepcopy(s['items'][k][0]);v['item'].update(url='https://example.test/new-program',publication_date='2026-11-01')
        s['items']['housing-feed/new-program']=[v]
        d=self.generate(s,self.state)
        self.assertEqual(d['delta']['new_accounts'],[])
        self.assertEqual(len(d['delta']['known_accounts_with_new_events']),1)
        self.assertEqual(len(d['delta']['newly_observed_events']),1)
        # Unclassified feed mentions stay visible without automatic relevance.
        a=next(a for a in d['assessments'].values() if a['newly_observed'])
        self.assertFalse(a['current_reason_to_investigate'])

    def test_partial_failure_keeps_checkpoint_during_next_batch(self):
        s=deepcopy(self.baseline)
        old=deepcopy(s['sources']['housing'])
        inventory=read('OutBound/data/day2-sources.json')
        run(s,inventory,lambda *_:(503,b'',{}),advance=True)
        self.assertEqual(s['batch'],2)
        self.assertEqual(s['sources']['housing']['checkpoint'],old['checkpoint'])
        self.assertEqual(s['sources']['housing']['last_success'],old['last_success'])
        d=self.generate(s)
        self.assertEqual(d['delta']['newly_observed_events'],[])
        self.assertTrue(any(a['outcome']=='failed' for a in d['collection_runs'][-1]['attempts']))

    def test_report_links_and_pending_review_are_visible(self):
        text=render(self.generate())
        for term in ('2 new accounts','2 newly observed events','0 accounts with a current','older_event','pending Day 5','signals.json','state.json'):
            self.assertIn(term,text)

    def test_typed_event_pipeline_at_known_account_and_repeat(self):
        row=dict(account_id='911090450',event_type='demand_change',event_reference='synthetic-demand-1',
                 fact='Synthetic test observation, not live evidence.',url='https://example.test/demand',
                 locator='test-row',event_date='2026-10-01',publication_date='2026-10-02',
                 first_seen_at='2026-11-06T02:00:00+00:00',retrieved_at='2026-11-06T02:00:00+00:00')
        args=(self.state,self.state,self.identities,self.pilot,date(2026,11,6))
        data=generate(*args,event_inputs={'current':[row]})
        self.assertEqual(data['delta']['new_accounts'],[])
        self.assertEqual(data['delta']['accounts_with_current_reason'],['911090450'])
        self.assertEqual(data['delta']['known_accounts_with_new_events'],['911090450'])
        a=next(a for a in data['assessments'].values() if a['newly_observed'])
        self.assertEqual(a['category'],'operational_strain')
        repeated=generate(*args,event_inputs={'current':[row],'baseline':[row]})
        self.assertEqual(repeated['delta']['newly_observed_events'],[])
        self.assertFalse(any(a['material_change'] for a in repeated['assessments'].values()))
        bad=dict(row,account_id='unknown')
        with self.assertRaises(ValueError): generate(*args,event_inputs={'current':[bad]})
        with self.assertRaises(ValueError): generate(*args,event_inputs={'current':[row,row]})
