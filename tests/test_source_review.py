from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from tributary import source_review as sr
from tributary.daily import initial_state, digest, execute

HTML=b'<article><p>Donations declined 20% in October 2026 compared with October 2025.</p><p>Demand increased 10% in October 2026.</p></article>'

def state():
    s=initial_state();s['signals']={};s['review_tasks']={}
    for category in ('fundraising_pressure','operational_strain'):
        sid=category;s['signals'][sid]=dict(id=sid,account_id='911090450',url='https://example.test/original',category=category,version='candidate-v1',fact='Machine keyword candidate, unverified')
        s['review_tasks'][sid]=dict(signal_id=sid,status='pending')
    return s

def verdicts(p,owner=False):
    rows=[]
    for g in p['groups']:
        for f in g['flags']:
            locator=next(iter(f['scope']['relevant']),next(iter(g['passages'])))
            rows.append(dict(signal_id=f['signal_id'],candidate_version=f['candidate_version'],document_version=g['document_version'],
                observation='Source reports an attributed October change.',reporting_period='October 2026',comparison_basis='October 2025, absolute baseline unknown',
                fact_verdict='supported_attributed',fact_reason='Attributed change matches the original passage.',commercial_reason='A dated supporter revenue decision can be investigated.' if owner else 'No present commercial decision established.',
                disposition='actionable' if owner else 'supported_context',commercial_relevance='owner_investigate' if owner else 'monitor',
                time_status='current_supported',source_checks_complete=True,owner_decision='Assess whether supporter segmentation can address this gap.' if owner else None,
                owner_next_step='Owner selects an account discovery hypothesis.' if owner else None,next_research_step='Monitor a dated follow-up.',
                original_read=True,reviewer='synthetic desktop reviewer for deterministic tests',reviewed_at='2026-11-06T08:00:00Z',
                researcher_assessment='Observed change.',skeptic_assessment='Baseline limitation retained.',fact_checker_assessment='Original locator checked.',
                evidence=[dict(locator=locator,hash=g['passages'][locator]['hash'],note='Original exact paragraph.')],contradictory_evidence=[]))
    return dict(contract=sr.CONTRACT,packet_id=p['id'],reviewed_at='2026-11-06T08:00:00Z',verdicts=rows)

def collection():return dict(as_of='2026-11-06',run_id='test',run_status='complete',collection=[],counts={})

def apply_review(s,p,r):
    from tributary.checkpoint_audit import execute, STAGES
    sr.validate(p,r)
    chain=[]
    if not r['verdicts']:return sr.apply(s,p,r)
    for stage in STAGES:
        answers={v['signal_id']:dict(actor='fixture',reason='synthetic check',result='pass') for v in r['verdicts']}
        chain.append(execute(stage,p,answers,chain[-1] if chain else None,r))
    if s.get('_test_chain_key')==digest([p,r]):chain=s['_test_chain']
    s['_test_chain_key']=digest([p,r]);s['_test_chain']=chain
    return sr.apply(s,p,r,chain)

class SourceReviewTests(unittest.TestCase):
    def test_missing_checkpoint_blocks_actionable_owner_card(self):
        from tributary.checkpoint_audit import STAGES, execute
        s=state(); p=sr.prepare(s,lambda *_:(200,HTML,{})); r=verdicts(p,True)
        checks=[]
        answers={v['signal_id']:dict(actor='fixture',reason='case-specific check',result='pass') for v in r['verdicts']}
        for stage in STAGES:
            checks.append(execute(stage,p,answers,checks[-1] if checks else None,r))
        for i in range(4):
            with self.subTest(stage=STAGES[i]), self.assertRaises(ValueError):
                sr.apply(s,p,r,checks[:i]+checks[i+1:])
            self.assertEqual(sr.owner_view(s,collection(),p)['cards'],[])
        held=dict(answers)
        held[r['verdicts'][0]['signal_id']]=dict(actor='fixture',reason='Unresolved contradiction',result='hold')
        fourth=execute('fact_checker',p,held,checks[2],r)
        with self.assertRaises(ValueError):
            sr.apply(s,p,r,checks[:3]+[fourth])
        sr.apply(s,p,r,checks)
        self.assertEqual(len(sr.owner_view(s,collection(),p)['cards']),1)

    def test_one_original_two_independent_claims(self):
        s=state();calls=[]
        p=sr.prepare(s,lambda u,c:(calls.append(u) or 200,HTML,{}))
        self.assertEqual(len(calls),1);self.assertEqual(p['summary']['flags_for_desktop'],2)
        apply_review(s,p,verdicts(p));self.assertEqual(len(s['source_review']['verdicts']),2)

    def test_unchanged_200_and_304_reuse_without_duplicate_cards_or_history(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{'etag':'v1'}));apply_review(s,p,verdicts(p,True))
        first=sr.owner_view(s,collection(),p,True);history=deepcopy(s['source_review']['history'])
        for code in (200,304):
            p=sr.prepare(s,lambda *_:(code,HTML if code==200 else b'',{}))
            self.assertEqual(p['summary']['reused_verdicts'],2);self.assertEqual(p['groups'],[])
            second=sr.owner_view(s,collection(),p)
            self.assertEqual([c['fingerprint'] for c in second['cards']],[c['fingerprint'] for c in first['cards']]);self.assertEqual(second['last_reviewed_at'],first['last_reviewed_at'])
        self.assertEqual(s['source_review']['history'],history)

    def test_changed_claim_only_reopens_affected_category(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p))
        p=sr.prepare(s,lambda *_:(200,HTML.replace(b'20%',b'30%'),{}))
        self.assertEqual(p['reused'],['operational_strain'])
        self.assertEqual([f['signal_id'] for g in p['groups'] for f in g['flags']],['fundraising_pressure'])

    def test_changed_cited_passage_outside_regex_reopens(self):
        s=state();raw=HTML.replace(b'</article>',b'<p>The annual ledger records a gap of USD100.</p></article>')
        p=sr.prepare(s,lambda *_:(200,raw,{}));r=verdicts(p)
        g=p['groups'][0];k=next(k for k,v in g['passages'].items() if v['index']==3)
        r['verdicts'][0]['evidence'].append(dict(locator=k,hash=g['passages'][k]['hash'],note='Important ledger basis.'))
        apply_review(s,p,r);p=sr.prepare(s,lambda *_:(200,raw.replace(b'USD100',b'USD200'),{}))
        self.assertIn(r['verdicts'][0]['signal_id'],[f['signal_id'] for g in p['groups'] for f in g['flags']])

    def test_new_contradiction_reopens_then_removes_owner_claim(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p,True));sr.owner_view(s,collection(),p,True)
        changed=HTML.replace(b'</article>',b'<p>Updated: donations are keeping pace; no remaining shortfall.</p></article>')
        p=sr.prepare(s,lambda *_:(200,changed,{}));self.assertEqual(p['summary']['flags_for_desktop'],2)
        r=verdicts(p)
        for row in r['verdicts']:
            row.update(fact_verdict='contradicted',disposition='contradicted',commercial_relevance='not_relevant',fact_reason='Updated source contradicts prior gap.')
            g=p['groups'][0];k=next(k for k,v in g['passages'].items() if v['index']==3)
            row['contradictory_evidence']=[dict(locator=k,hash=g['passages'][k]['hash'],note='Explicit contrary update.')]
        apply_review(s,p,r);v=sr.owner_view(s,collection(),p,True)
        self.assertEqual(v['counts']['owner_attention_accounts'],0);self.assertEqual(v['counts']['unsupported_or_contradicted_flags'],2)

    def test_inaccessible_retains_last_reviewed_worklist_with_its_date(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p,True));first=sr.owner_view(s,collection(),p,True)
        p=sr.prepare(s,lambda *_:(403,b'',{}));v=sr.owner_view(s,collection(),p)
        self.assertEqual(p['summary']['original_fetches'],1);self.assertEqual(p['summary']['inaccessible_flags'],2)
        self.assertEqual(v['cards'],[]);self.assertEqual(v['verification'],'reviewer_unavailable_or_incomplete')
        self.assertEqual(v['last_reviewed_worklist'],first);self.assertEqual(v['last_reviewed_at'],first['last_reviewed_at'])
        self.assertEqual(len(s['source_review']['history']),2)
        p=sr.prepare(s,lambda *_:(304,b'',{}));self.assertEqual(len(p['reused']),2)

    def test_missing_reviewer_publishes_status_not_raw_cards(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));v=sr.owner_view(s,collection(),p)
        self.assertEqual(v['cards'],[]);self.assertEqual(v['counts']['unfinished_or_research_flags'],2)
        self.assertIn('not freshly verified',sr.render_owner(v))

    def test_incomplete_stale_and_bad_locator_rejected_atomically(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}))
        for change in ('missing','stale','locator','period','gate'):
            r=verdicts(p,True)
            if change=='missing':r['verdicts'].pop()
            elif change=='stale':r['verdicts'][0]['candidate_version']='old'
            elif change=='locator':r['verdicts'][0]['evidence'][0]['hash']='wrong'
            elif change=='period':r['verdicts'][0]['reporting_period']=''
            else:r['verdicts'][0]['source_checks_complete']=False
            with self.assertRaises(ValueError):apply_review(s,p,r)
            self.assertEqual(s['source_review']['verdicts'],{})

    def test_donation_page_and_campaign_success_do_not_establish_pressure(self):
        s=state();p=sr.prepare(s,lambda *_:(200,b'<article><p>Donate today. Our campaign raised USD1000 and surpassed its goal.</p></article>',{}))
        r=verdicts(p)
        for row in r['verdicts']:row.update(fact_verdict='insufficient',disposition='unsupported',commercial_relevance='not_relevant',fact_reason='Donation request and successful performance do not establish financial pressure.')
        apply_review(s,p,r);v=sr.owner_view(s,collection(),p,True)
        self.assertEqual(v['cards'],[]);self.assertEqual(v['counts']['unsupported_or_contradicted_flags'],2)

    def test_new_flag_on_304_needs_readable_original_not_silent_approval(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p))
        s['signals']['financial_pressure']=dict(s['signals']['fundraising_pressure'],id='financial_pressure',category='financial_pressure')
        p=sr.prepare(s,lambda *_:(304,b'',{}))
        self.assertEqual(p['summary']['inaccessible_flags'],3)
        self.assertEqual(sr.owner_view(s,collection(),p)['cards'],[])

    def test_reapply_same_results_is_idempotent(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));r=verdicts(p)
        apply_review(s,p,r);apply_review(s,p,r);self.assertEqual(len(s['source_review']['history']),2)

    def test_cached_original_allows_desktop_reading_without_second_fetch(self):
        s=state()
        with tempfile.TemporaryDirectory() as directory:
            calls=[];p=sr.prepare(s,lambda u,c:(calls.append(u) or 200,HTML,{}),Path(directory))
            cache=Path(p['groups'][0]['original_cache'])
            self.assertTrue(cache.exists());self.assertEqual(len(calls),1)
            original=__import__('json').loads(cache.read_text())
            self.assertTrue(all('text' in row for row in original['paragraphs'].values()))
            self.assertFalse(any('text' in row for doc in s['source_review']['documents'].values() for row in doc['paragraphs'].values()))
            p=sr.prepare(s,lambda *_:(304,b'',{}),Path(directory))
            self.assertIsNone(p['groups'][0]['original_cache'])  # 304 metadata never revives a full-original cache path

    def test_private_feedback_survives_reuse_and_changed_evidence(self):
        from tributary.daily_worklist import Feedback
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p,True));v=sr.owner_view(s,collection(),p,True)
        with tempfile.TemporaryDirectory() as directory:
            db=Path(directory)/'private.sqlite';store=Feedback(db)
            card=v['cards'][0];store.record(card['account_id'],'monitor','PRIVATE_ONLY',card['fingerprint']);store.close()
            before=db.read_bytes();p=sr.prepare(s,lambda *_:(304,b'',{}));v=sr.owner_view(s,collection(),p)
            sr.private_owner(directory,v,db)
            private=__import__('json').loads((Path(directory)/'private-latest/worklist.json').read_text())
            self.assertFalse(private['cards'][0]['decision_needs_review']);self.assertNotIn('PRIVATE_ONLY',sr.render_owner(v))
            self.assertEqual(db.read_bytes(),before)
            p=sr.prepare(s,lambda *_:(200,HTML.replace(b'20%',b'30%'),{}));apply_review(s,p,verdicts(p,True));v=sr.owner_view(s,collection(),p,True)
            store=Feedback(db);self.assertTrue(store.overlay(v)['cards'][0]['decision_needs_review']);store.close()

    def test_empty_completion_cannot_refresh_review_date(self):
        s=state();p=sr.prepare(s,lambda *_:(200,HTML,{}));apply_review(s,p,verdicts(p))
        old=s['source_review']['last_desktop_review_at']
        p=sr.prepare(s,lambda *_:(304,b'',{}));r=verdicts(p);r['reviewed_at']='2026-12-01T00:00:00Z'
        self.assertEqual(apply_review(s,p,r),0);self.assertEqual(s['source_review']['last_desktop_review_at'],old)

if __name__=='__main__':unittest.main()
