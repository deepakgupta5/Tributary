"""Software checks of saved output transport, not additional role executions."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tributary.core import Store, STAGES, Invalid

ROOT = Path(__file__).resolve().parents[1] / 'OutBound/evidence/evaluations/session-001'
spec = importlib.util.spec_from_file_location('session_reproduce', ROOT / 'reproduce.py')
session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(session)


class SessionEvaluationTests(unittest.TestCase):
    def test_frozen_packets_reconstruct_and_reports_reconcile(self):
        session.verify_freeze()
        store = Store()
        try:
            session.initialize(store)
            for stage in STAGES:
                self.assertEqual(session.packet_bundle(store, stage), session.read(ROOT / 'packets' / (stage + '.json')))
                session.record(store, stage)
            with tempfile.TemporaryDirectory() as directory:
                out = Path(directory)
                session.render(store, out, 'Software test transport replay; no new inference')
                report = (out / 'report.md').read_text()
                self.assertIn('coding_session', report)
                self.assertNotIn('Semantic verdicts here are scripted', report)
                self.assertNotIn('Washington funder record', report)
                self.assertIn('Open-book/contaminated', report)
                self.assertIn('hypothesis — reviewed_hypothesis (not a verified fact)', report)
                score = session.score(out)
                original = session.read(ROOT / 'reports/scores.json')
                for key in ('tracks', 'coverage', 'stages', 'hypotheses', 'admission', 'collection', 'qc', 'reconciliation'):
                    self.assertEqual(score[key], original[key])
                self.assertEqual(score['tracks']['reviewer_challenge']['fact_checker']['mismatches'],
                                 [{'id': 'f-challenge/c7', 'expected': 'unverifiable', 'actual': 'contradicted'}])
                # Preserve existing score records instead of silently replacing a run.
                with self.assertRaises(FileExistsError):
                    session.score(out)
                exported = session.read(out / 'records.json')
                jsonl = [json.loads(line) for line in (out / 'records.jsonl').read_text().splitlines()]
                for table, rows in exported['tables'].items():
                    self.assertEqual(rows, [row['record'] for row in jsonl if row['group'] == table])
        finally:
            store.close()

    def test_changed_frozen_output_cannot_be_scored(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'case'
            shutil.copytree(ROOT, copy)
            file = copy / 'outputs/fact_checker.json'
            file.write_text(file.read_text() + '\n')
            with patch.object(session, 'ROOT', copy):
                with self.assertRaisesRegex(Invalid, 'Frozen input/output changed'):
                    session.verify_freeze()

    def test_pending_and_absent_results_stay_in_denominators(self):
        score = session.scored({'bad': 'contradicted', 'good': 'verified'}, [{'id': 'bad', 'status': 'pending'}])
        self.assertEqual((score['eligible'], score['submitted'], score['checked'], score['pending']), (2, 1, 0, 2))
        self.assertEqual((score['caught'], score['missed'], score['false_verification']), (0, 1, 0))

    def test_expected_answer_records_are_not_in_saved_packets(self):
        # Packet separation is a data-layout check, never a claim of blind context.
        for stage in STAGES:
            packets = session.read(ROOT / 'packets' / (stage + '.json'))
            for packet in packets.values():
                self.assertEqual(set(packet), {'contract_version', 'subject', 'stage', 'fingerprint',
                                                'dependencies', 'prior_reviews', 'required_details'})
                self.assertNotIn('expected', packet['dependencies'])
        self.assertTrue(session.read(ROOT / 'context.json')['expected_answers_seen'])
        self.assertFalse(session.read(ROOT / 'context.json')['context_isolation'])

    def test_changed_collection_cannot_silently_replace_replay(self):
        store = Store()
        try:
            session.initialize(store)
            with self.assertRaisesRegex(Invalid, 'empty database'):
                session.initialize(store)
        finally:
            store.close()


if __name__ == '__main__':
    unittest.main()
