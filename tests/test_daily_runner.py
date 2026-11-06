from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tributary.daily import ROOT, TZ, VERSION, Network, alias_map, candidates, digest, documents, execute, fetched, initial_state, run, worklist
from tributary.daily_worklist import Feedback

AT=datetime(2026,11,6,6,tzinfo=timezone.utc)
SOURCE=dict(id='synthetic-feed',kind='feed',url='https://example.test/feed',account_id='911090450',account_ids=['911090450'])

def feed(text='Food Lifeline reports growing demand and more clients.',date='Thu, 05 Nov 2026 12:00:00 GMT'):
    return f'<rss><channel><item><title>Organization update</title><link>https://example.test/update</link><pubDate>{date}</pubDate><description>{text}</description></item></channel></rss>'.encode()


class DailyRunnerTests(unittest.TestCase):
    def setUp(self): self.state=initial_state()

    def test_each_of_four_categories_produces_pending_candidates(self):
        examples={'fundraising_pressure':'Donations declined this year.', 'financial_pressure':'We lost public funding.', 'campaign_performance':'Our fundraising campaign raised more than the goal.', 'operational_strain':'Demand increased this year.'}
        for category,text in examples.items():
            result=list(candidates(SOURCE,feed(text),self.state['accounts'],AT.date()))
            self.assertIn(category,{c['category'] for c in result})
            self.assertTrue(all(c['review_status']=='pending' for c in result))

    def test_entities_and_empty_valid_feed_are_not_parse_failures(self):
        result=list(documents(SOURCE,feed('Growing&nbsp;demand.')))
        self.assertIn('Growing',result[0]['text'])
        self.assertEqual(list(documents(SOURCE,b'<rss><channel/></rss>')),[])
        with self.assertRaises(ValueError): list(documents(SOURCE,b'<html><body>No feed</body></html>'))

    def test_repeat_unchanged_content_does_not_duplicate_signal_task_or_card(self):
        retrieve=lambda *_:(200,feed(),{'etag':'same'})
        first=run(self.state,[SOURCE],retrieve,AT)
        count=len(self.state['review_tasks'])
        second=run(self.state,[SOURCE],retrieve,AT)
        self.assertEqual(len(first['new_signals']),1)
        self.assertEqual(second['new_signals'],[])
        self.assertEqual(second['changed_signals'],[])
        self.assertEqual(second['attempts'][0]['outcome'],'unchanged')
        self.assertEqual(len(self.state['review_tasks']),count)
        cards=worklist(self.state,second)['cards']
        self.assertEqual(len(cards),len({c['account_id'] for c in cards}))

    def test_changed_claim_version_reopens_review_without_new_event_id(self):
        run(self.state,[SOURCE],lambda *_:(200,feed(),{}),AT)
        second=run(self.state,[SOURCE],lambda *_:(200,feed('Food Lifeline reports demand increased by 25 percent.'),{}),AT)
        self.assertEqual(len(second['changed_signals']),1)
        self.assertEqual(second['new_signals'],[])
        self.assertEqual(len(self.state['signals']),1)
        self.assertEqual(len(self.state['review_tasks']),2)

    def test_historical_day5_observation_is_not_new_today(self):
        s=dict(SOURCE,url='https://foodlifeline.org/article/food-frenzy-2026-results',kind='page')
        raw=b'<article><p>Food Frenzy fundraising results raised more than the goal.</p></article>'
        first=run(self.state,[s],lambda *_:(200,raw,{}),AT)
        self.assertEqual(first['new_signals'],[])
        self.assertEqual(len(first['source_rechecks']),1)

    def test_old_or_undated_first_observation_is_labelled_separately(self):
        first=run(self.state,[SOURCE],lambda *_:(200,feed(date='Thu, 01 Jan 2026 12:00:00 GMT'),{}),AT)
        self.assertEqual(len(first['new_signals']),1)
        self.assertEqual(len(first['historical_first_observed']),1)
        c=next(iter(self.state['signals'].values()))
        self.assertEqual(c['publication_date'],'2026-01-01')
        self.assertNotEqual(c['publication_date'],AT.date().isoformat())

    def test_failure_does_not_advance_last_success_and_recovers(self):
        run(self.state,[SOURCE],lambda *_:(200,feed(),{'etag':'saved'}),AT)
        before=deepcopy(self.state['checkpoints'][SOURCE['id']])
        failed=run(self.state,[SOURCE],lambda *_:(503,b'',{}),AT)
        self.assertEqual(failed['attempts'][0]['outcome'],'failed')
        for field in ('last_success','raw_sha256','etag','semantic_sha256'):
            self.assertEqual(self.state['checkpoints'][SOURCE['id']][field],before[field])
        recovered=run(self.state,[SOURCE],lambda *_:(304,b'',{}),AT)
        self.assertEqual(recovered['attempts'][0]['outcome'],'unchanged')
        self.assertEqual(recovered['new_signals'],[])

    def test_missed_partial_day_is_visible_on_catchup(self):
        self.state['last_attempt_date']='2026-11-02'
        result=run(self.state,[SOURCE],lambda *_:(200,feed(),{}),AT)
        self.assertEqual(result['missed_dates'],['2026-11-03','2026-11-04'])
        self.assertIn('cannot guarantee',result['coverage_gap'])

    def test_304_without_checkpoint_is_failure_not_unchanged(self):
        self.assertEqual(fetched(SOURCE,{},lambda *_:(304,b'',{}))['outcome'],'failed')

    def test_saved_discovery_validators_are_used(self):
        cp=self.state['checkpoints']['irs']
        self.assertTrue(cp['raw_sha256'])
        self.assertEqual(cp.get('etag'),self.state['collection']['sources']['irs']['checkpoint'].get('etag'))

    def test_registry_discovers_a_new_account_once(self):
        src=dict(id='irs',kind='discovery',url='https://example.test/register',geography='WA',account_ids=[])
        body=b'EIN,NAME,CITY,STATE,TAX_PERIOD\n123456789,SYNTHETIC FOOD BANK,SEATTLE,WA,202606\n'
        first=run(self.state,[src],lambda *_:(200,body,{}),AT)
        self.assertEqual(first['new_accounts'],['123456789'])
        self.assertEqual(first['new_signals'],[])
        second=run(self.state,[src],lambda *_:(200,body,{}),AT)
        self.assertEqual(second['new_accounts'],[])

    def test_interrupted_run_resumes_without_reprocessing_completed_sources(self):
        saved=[]
        def interrupt(state):
            saved.append(deepcopy(state))
            if len(state['active_run']['attempts'])==1: raise RuntimeError('synthetic interruption')
        second=dict(SOURCE,id='synthetic-feed-2',url='https://example.test/feed2')
        with self.assertRaises(RuntimeError): run(self.state,[SOURCE,second],lambda *_:(200,feed(),{}),AT,interrupt,jobs=1)
        interrupted=saved[-1]
        done=interrupted['active_run']['attempts'][0]['source']
        calls=[]
        def retrieve(url,cp): calls.append(url);return 200,feed(),{}
        result=run(interrupted,[SOURCE,second],retrieve,AT)
        self.assertEqual(len(calls),1)
        self.assertEqual(len(result['attempts']),2)
        self.assertEqual(len(interrupted['signals']),1)

    def test_robots_denial_is_blocked_and_body_not_requested(self):
        net=Network();calls=[]
        def get(url,cp): calls.append(url);return 200,b'User-agent: *\nDisallow: /private',{}
        with patch('tributary.collect.fetch',get):
            with self.assertRaises(PermissionError): net('https://example.test/private',{})
        self.assertEqual(calls,['https://example.test/robots.txt'])

    def test_public_run_does_not_contain_private_reasons(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);db=base/'feedback.sqlite';store=Feedback(db)
            c=self.state['reviewed_cards'][0]
            store.record(c['account_id'],'monitor','SYNTHETIC_PRIVATE_DAILY',c['fingerprint']);store.close()
            data=execute(base/'state',base/'public',db,lambda *_:(200,feed(),{}),AT,[SOURCE],jobs=1)
            self.assertNotIn('SYNTHETIC_PRIVATE_DAILY',(base/'public/worklist.md').read_text())
            self.assertNotIn('SYNTHETIC_PRIVATE_DAILY',(base/'public/worklist.json').read_text())
            # A source-research card is no longer published to the owner.
            self.assertEqual(json.loads((base/'state/private-latest/worklist.json').read_text())['cards'],[])
            saved=Feedback(db)
            self.assertEqual(saved.latest(c['account_id'])['reason'],'SYNTHETIC_PRIVATE_DAILY');saved.close()
            self.assertEqual((base/'state/private-latest').stat().st_mode & 0o777,0o700)

    def test_failure_invalidates_reuse_without_erasing_original_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Feedback(Path(directory)/'private.sqlite')
            original=self.state['reviewed_cards'][0]
            store.record(original['account_id'],'dismiss','SYNTHETIC_HOLD',original['fingerprint'])
            log=run(self.state,[SOURCE],lambda *_:(503,b'',{}),AT)
            data=store.overlay(worklist(self.state,log))
            card=next(c for c in data['cards'] if c['account_id']==original['account_id'])
            self.assertTrue(card['decision_needs_review'])
            self.assertEqual(card['owner_feedback']['decision'],'dismiss')
            self.assertEqual(card['effective_tier'],card['recommended_tier'])
            store.close()

    def test_vancouver_daily_guard_and_interrupted_catchup(self):
        from tributary.daily import scheduled_due
        before=datetime(2026,11,6,7,59,tzinfo=TZ)  # 07:59 PST
        after=datetime(2026,11,6,8,5,tzinfo=TZ)   # 08:05 PST
        self.assertFalse(scheduled_due(self.state,before))
        self.assertTrue(scheduled_due(self.state,after))
        self.state['last_attempt_date']='2026-11-06'
        self.assertFalse(scheduled_due(self.state,after))
        self.state['active_run']={'status':'running'}
        self.assertTrue(scheduled_due(self.state,before))

    def test_native_schedule_preserves_unrelated_entries_and_is_idempotent(self):
        from tributary.schedule import block,replace
        existing='MAILTO=""\n10 9 * * * /usr/bin/true # unrelated\n'
        entry=block(Path('/tmp/Tributary project'),'/usr/bin/python3')
        result=replace(existing,entry)
        self.assertTrue(result.startswith(existing))
        self.assertEqual(replace(result,entry),result)
        self.assertEqual(result.count('BEGIN TRIBUTARY'),1)
        self.assertIn("'",entry)  # path with spaces is shell-quoted

    def test_scheduled_skip_performs_no_collection(self):
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            def unexpected(*_): self.fail('Collection must not run before the daily window')
            result=execute(base/'state',base/'public',retrieve=unexpected,at=datetime(2026,11,6,7,tzinfo=TZ),sources=[SOURCE],execution='scheduled_local')
            self.assertTrue(result['skipped'])
            self.assertFalse((base/'public/worklist.md').exists())

    def test_feed_and_page_coverage_do_not_oscillate_event_versions(self):
        page=dict(SOURCE,id='synthetic-page',kind='page',url='https://example.test/update')
        def retrieve(url,cp):
            return (200,feed() if url.endswith('/feed') else b'<article><p>Demand increased for Food Lifeline.</p></article>',{})
        first=run(self.state,[SOURCE,page],retrieve,AT)
        self.assertEqual(len(first['new_signals']),1)
        self.assertEqual(first['changed_signals'],[])
        version=next(iter(self.state['signals'].values()))['version']
        second=run(self.state,[SOURCE,page],retrieve,AT)
        self.assertEqual(second['new_signals'],[])
        self.assertEqual(second['changed_signals'],[])
        self.assertEqual(next(iter(self.state['signals'].values()))['version'],version)
        self.assertEqual(sum(t['status']=='pending' for t in self.state['review_tasks'].values()),1)
