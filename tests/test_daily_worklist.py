from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tributary.daily_worklist import ROOT, Feedback, build, export, load_evidence, render, private_destination, digest


class DailyWorklistTests(unittest.TestCase):
    def setUp(self):
        self.args=load_evidence(ROOT/'OutBound/evidence/day-5')
        self.worklist=build(*self.args)

    def test_six_original_observations_reconcile_to_four_unique_cards(self):
        self.assertEqual(len([r for r in self.args[0]['observations'] if r['origin']=='day4']),6)
        self.assertEqual(len(self.worklist['cards']),4)
        self.assertEqual(len({c['account_id'] for c in self.worklist['cards']}),4)
        self.assertEqual(sum(len(c['observations']) for c in self.worklist['cards']),8)
        self.assertEqual(self.worklist['counts'],dict(act=0,investigate=1,monitor=3,suppress=0))

    def test_every_rendered_claim_has_completed_source_qualified_check(self):
        data,reviews,sources=self.args
        for row in data['observations']:
            checked=reviews[-1]['claim_checks'][row['id']]
            self.assertEqual(len(checked),len(row['claims']))
            self.assertTrue(all(c['status']=='supported_attributed' and c['locator'] and c['source_sha256'] for c in checked))

    def test_stale_data_source_or_prior_stage_is_rejected(self):
        for position in range(3):
            args=deepcopy(self.args)
            if position==0: args[0]['observations'][0]['fact']='Changed fact'
            elif position==1: args[1][1]['reason']='Changed researcher assessment'
            else: args[2][0]['response_sha256']='different source version'
            with self.subTest(position=position),self.assertRaises(ValueError): build(*args)

    def test_missing_and_incomplete_reviews_are_rejected(self):
        data,reviews,sources=deepcopy(self.args)
        with self.assertRaises(ValueError): build(data,reviews[:-1],sources)
        reviews[2]['completed']=False
        with self.assertRaises(ValueError): build(data,reviews,sources)

    def test_tampered_claim_coverage_rejected(self):
        data,reviews,sources=deepcopy(self.args)
        rid=data['observations'][0]['id']
        reviews[-1]['claim_checks'][rid].pop()
        with self.assertRaises(ValueError): build(data,reviews,sources)

    def test_partial_surrey_link_stays_visible_and_does_not_become_act(self):
        c=next(c for c in self.worklist['cards'] if c['account_id']=='132168162RR0001')
        self.assertTrue(c['material_pending'])
        self.assertEqual(c['recommended_tier'],'investigate')
        text=render(self.worklist)
        self.assertIn('evidence ends on June 11, 2026',text)
        self.assertIn('primary operator confirmation remains pending',text)
        self.assertIn('2024 to September 30, 2025',text)
        self.assertNotIn('Surrey needs consulting',text)

    def test_repeat_build_is_byte_identical_and_does_not_duplicate_cards(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            export(self.worklist,p)
            first={n:(p/n).read_bytes() for n in ('worklist.md','worklist.json')}
            export(build(*self.args),p)
            self.assertEqual(first,{n:(p/n).read_bytes() for n in first})
            self.assertEqual(len(json.loads((p/'worklist.json').read_text())['cards']),4)

    def test_private_decision_survives_rerun_and_database_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'owner.sqlite'
            c=self.worklist['cards'][0]
            store=Feedback(path)
            record=store.record(c['account_id'],'dismiss','SYNTHETIC PRIVATE REASON',c['fingerprint'])
            same=store.record(c['account_id'],'dismiss','SYNTHETIC PRIVATE REASON',c['fingerprint'])
            self.assertEqual(record,same)
            first=store.overlay(self.worklist)
            store.close()
            store=Feedback(path)
            second=store.overlay(build(*self.args))
            self.assertEqual(first,second)
            self.assertEqual(second['counts']['suppress'],1)
            self.assertEqual(store.db.execute('SELECT count(*) FROM owner_decisions').fetchone()[0],1)
            store.close()

    def test_changed_evidence_preserves_decision_but_requires_rereview(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Feedback(Path(directory)/'private.sqlite')
            c=self.worklist['cards'][0]
            store.record(c['account_id'],'dismiss','SYNTHETIC HISTORY',c['fingerprint'])
            changed=deepcopy(self.worklist);changed['cards'][0]['fingerprint']='new reviewed version'
            result=store.overlay(changed)['cards'][0]
            self.assertEqual(result['owner_feedback']['reason'],'SYNTHETIC HISTORY')
            self.assertTrue(result['decision_needs_review'])
            self.assertEqual(result['effective_tier'],result['recommended_tier'])
            store.close()

    def test_private_notes_never_enter_public_export(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);store=Feedback(p/'private.sqlite');c=self.worklist['cards'][0]
            store.record(c['account_id'],'monitor','SYNTHETIC_SECRET_MARKER',c['fingerprint'])
            private=store.overlay(self.worklist)
            export(private,p/'private-view')
            export(self.worklist,p/'public-view')
            self.assertIn('SYNTHETIC_SECRET_MARKER',(p/'private-view/worklist.md').read_text())
            for filename in ('worklist.md','worklist.json'):
                self.assertNotIn('SYNTHETIC_SECRET_MARKER',(p/'public-view'/filename).read_text())
                self.assertNotIn('owner_feedback',(p/'public-view'/filename).read_text())
            store.close()

    def test_private_output_cannot_overwrite_public_evidence(self):
        with self.assertRaises(ValueError): private_destination(ROOT/'OutBound/evidence/day-5')
        self.assertEqual(private_destination(ROOT/'out/private-view'),ROOT/'out/private-view')

    def test_unknown_feedback_and_empty_reason_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Feedback(Path(directory)/'decisions.sqlite')
            with self.assertRaises(ValueError): store.record('synthetic','send','reason','version')
            with self.assertRaises(ValueError): store.record('synthetic','monitor','','version')
            store.close()
