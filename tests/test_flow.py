import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tributary.core import Store, Invalid, STAGES, digest
from tributary.demo import seed, replay, replay_output, demonstrate, subject, claim, evidence
from tributary.report import export
from tributary.worklist import export_worklist


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.s = Store()
        seed(self.s)

    def tearDown(self):
        self.s.close()

    def prepare(self, rid='o-cedar', stop=None, prefix=''):
        for stage in STAGES:
            if stage == stop:
                break
            p = self.s.packet(rid, stage)
            self.s.review(p, replay_output(p, prefix + rid + ':' + stage))

    def test_both_discovery_directions_and_deduplication(self):
        def discoveries():
            return [json.loads(r[0]) for r in self.s.db.execute("SELECT body FROM history WHERE type='discovery'")]
        self.assertEqual({r['direction'] for r in discoveries()}, {'source_to_organization', 'organization_to_source'})
        self.s.discover('s-news', 'o-cedar', 'mentioned in p1', 'repeat')
        self.assertEqual(len(discoveries()), 4)

    def test_ingestion_reconciles_partial_failure(self):
        r = json.loads(self.s.db.execute("SELECT body FROM runs WHERE id='initial-ingestion'").fetchone()[0])
        self.assertEqual(r['counts'], {'unique': 3, 'duplicate': 1, 'quarantined': 1})
        self.assertEqual(r['status'], 'partial')
        self.assertTrue(r['reconciled'])
        with self.assertRaises(Invalid):
            self.s.get('bad-date')

    def test_malformed_input_is_quarantined(self):
        result = self.s.ingest('malformed', [None, []])
        self.assertEqual(result['counts']['quarantined'], 2)
        self.assertTrue(result['reconciled'])

    def test_interrupted_ingestion_resumes_with_visible_pending(self):
        items = [{'id': 'resumed-1', 'body': evidence('s-news', {'p1': 'First.'})},
                 {'id': 'resumed-2', 'body': evidence('s-news', {'p1': 'Second.'})}]
        original = self.s.put
        def interrupted(rid, *args):
            if rid == 'resumed-2':
                raise RuntimeError('Simulated interruption')
            return original(rid, *args)
        with patch.object(self.s, 'put', side_effect=interrupted):
            with self.assertRaises(RuntimeError): self.s.ingest('interrupted', items)
        saved = json.loads(self.s.db.execute("SELECT body FROM runs WHERE id='interrupted'").fetchone()[0])
        self.assertEqual((saved['status'], saved['pending_count']), ('running', 1))
        resumed = self.s.ingest('interrupted', items)
        self.assertEqual((resumed['status'], resumed['pending_count']), ('complete', 0))
        self.assertEqual(resumed['counts']['unique'], 2)

    def test_embedded_instructions_remain_evidence_text(self):
        p = self.s.packet('o-cedar', 'qc')
        self.assertIn('IGNORE', p['dependencies']['e-news']['body']['paragraphs']['p4'])
        self.assertEqual(self.s.status('o-cedar'), 'candidate')
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM reviews').fetchone()[0], 0)

    def test_upstream_review_change_invalidates_downstream(self):
        self.prepare()
        self.s.decide('o-cedar', 'first')
        p = self.s.packet('o-cedar', 'qc')
        changed = replay_output(p, 'new-qc')
        changed['reason'] = 'New QC evidence assessment'
        self.s.review(p, changed)
        self.assertIsNone(self.s.latest_review('o-cedar', 'researcher'))
        self.assertEqual(self.s.status('o-cedar'), 'awaiting_recheck')

    def test_findings_require_current_source_and_organization_admission(self):
        replay(self.s, 'f-campaign', 'premature')
        blockers = self.s.blockers('f-campaign')
        self.assertIn('Organization not currently admitted', blockers)
        self.assertIn('Source not currently approved: s-news', blockers)

    def test_required_detail_verification_needs_evidence_locator(self):
        self.prepare(stop='fact_checker')
        p = self.s.packet('o-cedar', 'fact_checker')
        out = replay_output(p, 'bad-detail')
        out['details']['identity']['locator'] = 'invented'
        with self.assertRaises(Invalid): self.s.review(p, out)

    def test_same_run_idempotent_changed_input_rejected(self):
        items = [{'id': 'e-news', 'body': self.s.get('e-news')['body']}]
        first = self.s.ingest('repeat', items)
        self.assertEqual(first, self.s.ingest('repeat', items))
        with self.assertRaises(Invalid):
            self.s.ingest('repeat', [])

    def test_no_network_in_demo(self):
        with patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            other = Store()
            try:
                demonstrate(other)
            finally:
                other.close()

    def test_all_three_types_require_all_four_checkpoints(self):
        for rid in ('s-news', 'o-cedar', 'f-campaign'):
            for stage in STAGES:
                with self.subTest(rid=rid, missing=stage):
                    blockers = self.s.blockers(rid)
                    self.assertIn('Checkpoint missing/stale/not passed: ' + stage, blockers)
                    p = self.s.packet(rid, stage)
                    self.s.review(p, replay_output(p, rid + ':' + stage))
            self.assertFalse(any('Checkpoint' in b for b in self.s.blockers(rid)))

    def test_out_of_order_review_rejected(self):
        p = self.s.packet('o-cedar', 'fact_checker')
        with self.assertRaises(Invalid):
            self.s.review(p, {'execution_id': 'skip'})

    def test_collector_cannot_record_own_qc(self):
        p = self.s.packet('o-cedar', 'qc')
        with self.assertRaises(Invalid):
            self.s.review(p, replay_output(p, 'collector:details'))
        self.assertIsNone(self.s.latest_review('o-cedar', 'qc'))

    def test_context_description_required_and_honest_basis_retained(self):
        p = self.s.packet('o-cedar', 'qc')
        output = replay_output(p, 'qc')
        output['context'] = ''
        with self.assertRaises(Invalid):
            self.s.review(p, output)
        output['context'] = 'Same session; no isolation demonstrated.'
        self.s.review(p, output)
        self.assertEqual(self.s.latest_review('o-cedar', 'qc')['body']['context'], output['context'])

    def test_completed_failed_review_cannot_pass(self):
        self.prepare(stop='fact_checker')
        p = self.s.packet('o-cedar', 'fact_checker')
        out = replay_output(p, 'failure')
        out['outcome'] = 'failed'
        self.s.review(p, out)
        self.assertEqual(self.s.decide('o-cedar', 'run')['state'], 'pending')

    def test_incomplete_execution_cannot_claim_pass(self):
        p = self.s.packet('o-cedar', 'qc')
        out = replay_output(p, 'incomplete')
        out['completed'] = False
        with self.assertRaises(Invalid):
            self.s.review(p, out)

    def test_worklist_exports_stored_qc_completion(self):
        packet = self.s.packet('f-campaign', 'qc')
        output = replay_output(packet, 'incomplete-qc')
        output.update(completed=False, outcome='incomplete')
        self.s.review(packet, output)
        with tempfile.TemporaryDirectory() as directory:
            export_worklist(self.s, Path(directory))
            worklist = json.loads((Path(directory) / 'worklist.json').read_text())
        signal = next(s for a in worklist['accounts'] for s in a['signals']
                      if s['finding_id'] == 'f-campaign')
        self.assertIs(signal['checkpoint_completion']['qc'], False)

    def test_optional_missing_field_and_nonmaterial_issue_allow_approval(self):
        result = replay(self.s, 'o-cedar', 'optional', issue=True)
        self.assertEqual(result['state'], 'admitted')
        self.assertIsNone(self.s.get('o-cedar')['body']['optional']['revenue'])

    def test_material_issue_cannot_be_relabelled_limitation(self):
        self.prepare(stop='skeptic')
        p = self.s.packet('o-cedar', 'skeptic')
        out = replay_output(p, 'skeptic', issue=True)
        out['issues'][0]['material'] = True
        self.s.review(p, out)
        p = self.s.packet('o-cedar', 'fact_checker')
        self.s.review(p, replay_output(p, 'fact'))
        self.assertTrue(any('Material issue' in b for b in self.s.blockers('o-cedar')))

    def test_material_question_supported_as_written_can_pass(self):
        self.prepare(stop='skeptic')
        p = self.s.packet('o-cedar', 'skeptic')
        out = replay_output(p, 'skeptic', issue=True)
        out['issues'][0]['material'] = True
        self.s.review(p, out)
        p = self.s.packet('o-cedar', 'fact_checker')
        out = replay_output(p, 'fact')
        out['resolutions']['question']['status'] = 'supported_as_written'
        self.s.review(p, out)
        self.assertEqual(self.s.decide('o-cedar', 'done')['state'], 'admitted')

    def test_identity_access_and_category_blockers(self):
        for rid in ('o-ambiguous', 's-blocked'):
            self.assertEqual(replay(self.s, rid, rid)['state'], 'pending')
        b = self.s.get('o-cedar')['body']
        b['category'] = 'hospital'
        self.s.put('o-cedar', 'organization', b, 'collector:category')
        self.assertEqual(replay(self.s, 'o-cedar', 'hospital')['state'], 'pending')

    def test_unflagged_contradiction_blocks_even_claimed_pass(self):
        self.prepare('f-grant', stop='fact_checker')
        p = self.s.packet('f-grant', 'fact_checker')
        self.assertEqual(p['prior_reviews']['skeptic']['issues'], [])
        out = replay_output(p, 'fact', contradiction=True)
        out['outcome'] = 'passed'
        self.s.review(p, out)
        self.assertIn('Material claim not verified: grant', self.s.blockers('f-grant'))

    def test_missing_duplicate_and_invented_claim_checks_rejected(self):
        self.prepare(stop='fact_checker')
        p = self.s.packet('o-cedar', 'fact_checker')
        for mode in ('missing', 'duplicate', 'invented'):
            out = replay_output(p, mode)
            if mode == 'missing': out['checks'] = []
            if mode == 'duplicate': out['checks'] *= 2
            if mode == 'invented': out['checks'][0]['claim_id'] = 'invented'
            with self.subTest(mode=mode), self.assertRaises(Invalid):
                self.s.review(p, out)

    def test_missing_required_detail_or_issue_disposition_rejected(self):
        self.prepare(stop='skeptic')
        p = self.s.packet('o-cedar', 'skeptic')
        self.s.review(p, replay_output(p, 'skeptic', issue=True))
        p = self.s.packet('o-cedar', 'fact_checker')
        for field in ('details', 'resolutions'):
            out = replay_output(p, field)
            out[field] = {}
            with self.assertRaises(Invalid): self.s.review(p, out)

    def test_locator_and_unavailable_original_cannot_verify(self):
        self.prepare(stop='fact_checker')
        p = self.s.packet('o-cedar', 'fact_checker')
        out = replay_output(p, 'bad-locator')
        out['checks'][0]['locator'] = 'invented'
        with self.assertRaises(Invalid): self.s.review(p, out)
        b = self.s.get('e-news')['body']
        b['available'] = False
        self.s.put('e-news', 'evidence', b, 'collector:unavailable')
        self.prepare(stop='fact_checker', prefix='unavailable:')
        p = self.s.packet('o-cedar', 'fact_checker')
        with self.assertRaises(Invalid): self.s.review(p, replay_output(p, 'missing'))

    def test_source_change_reopens_transitive_dependents_only(self):
        replay(self.s, 'o-cedar', 'cedar')
        replay(self.s, 'o-willow', 'willow')
        b = self.s.get('e-news')['body']
        b['paragraphs']['p2'] = 'Material correction.'
        self.s.put('e-news', 'evidence', b, 'collector:changed')
        self.assertEqual(self.s.status('o-cedar'), 'awaiting_recheck')
        self.assertEqual(self.s.status('o-willow'), 'admitted')
        self.assertIsNone(self.s.latest_review('o-cedar', 'qc'))
        self.assertEqual(self.s.get('e-news', 1)['body']['paragraphs']['p2'].find('120000') >= 0, True)

    def test_old_packet_and_reused_execution_refused(self):
        p = self.s.packet('o-cedar', 'qc')
        out = replay_output(p, 'qc')
        self.s.review(p, out)
        self.s.review(p, out)  # exact retry
        altered = copy.deepcopy(out)
        altered['reason'] = 'Different review'
        with self.assertRaises(Invalid): self.s.review(p, altered)
        b = self.s.get('e-news')['body']
        b['paragraphs']['p2'] += ' Correction.'
        self.s.put('e-news', 'evidence', b, 'collector:new')
        with self.assertRaises(Invalid): self.s.review(p, out)

    def test_unchanged_records_and_decisions_are_idempotent(self):
        replay(self.s, 'o-cedar', 'first')
        row = self.s.get('o-cedar')
        self.assertEqual(self.s.put(row['id'], row['kind'], row['body'], 'collector:repeat'), (row['version'], False))
        self.s.decide('o-cedar', 'repeat')
        self.assertEqual(self.s.db.execute('SELECT COUNT(*) FROM decisions').fetchone()[0], 1)

    def test_dependency_cycle_rolls_back(self):
        before = self.s.get('e-news')['version']
        b = self.s.get('e-news')['body']
        b['dependencies'] = ['o-cedar']
        with self.assertRaises(Invalid): self.s.put('e-news', 'evidence', b, 'cycle')
        self.assertEqual(self.s.get('e-news')['version'], before)

    def test_unknown_date_explicit(self):
        b = evidence('s-news', {'p1': 'Unknown date'}, publication_date=None)
        with self.assertRaises(Invalid): self.s.put('unknown', 'evidence', b, 'collector')
        b['date_unknown_reason'] = 'Not stated'
        self.s.put('unknown', 'evidence', b, 'collector')

    def test_live_data_rejected(self):
        b = self.s.get('e-news')['body']
        b['synthetic'] = False
        with self.assertRaises(Invalid): self.s.put('live', 'evidence', b, 'collector')

    def test_answer_keys_absent_from_role_packets(self):
        p = self.s.packet('f-grant', 'qc')
        text = json.dumps(p)
        self.assertNotIn('expected_status', text)
        self.assertNotIn('answer_key', text)

    def test_reconciliation_detects_tampered_counts(self):
        opening = self.s.snapshot()
        row = json.loads(self.s.db.execute("SELECT body FROM runs WHERE id='initial-ingestion'").fetchone()[0])
        row['counts']['unique'] = 999
        self.s.db.execute("UPDATE runs SET body=? WHERE id='initial-ingestion'", (json.dumps(row),))
        self.assertFalse(self.s.reconcile(opening)['passed'])

    def test_complete_demo_export_and_reopen_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            store = Store(p / 'demo.sqlite')
            data = demonstrate(store)
            self.assertEqual(data['initial']['admitted'], 6)
            self.assertEqual(data['initial']['closing_pending'], 3)
            self.assertEqual(data['changed_period']['reopened'], 3)
            self.assertEqual(data['rerun']['admitted'], 0)
            export(store, p, data)
            store.close()
            store = Store(p / 'demo.sqlite')
            self.assertEqual(store.status('f-campaign'), 'approved')
            self.assertEqual(store.status('f-grant'), 'pending')
            js = json.loads((p / 'records.json').read_text())
            jl = [json.loads(line) for line in (p / 'records.jsonl').read_text().splitlines()]
            self.assertEqual(sum(len(v) for v in js['tables'].values()), len(jl))
            self.assertIn('fixture replay', (p / 'report.md').read_text())
            store.close()


if __name__ == '__main__':
    unittest.main()
