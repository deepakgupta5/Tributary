import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from tributary.core import Store, Invalid, digest, encode
from tributary.demo import seed, replay, replay_output, claim, demonstrate
from tributary.report import export, coverage


class ReviewCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.s = Store()
        seed(self.s)

    def tearDown(self):
        self.s.close()

    def test_exact_packet_survives_source_change_and_export(self):
        replay(self.s, 'o-cedar', 'before')
        packet = self.s.packet('o-cedar', 'fact_checker')
        saved = self.s.get_review('before:fact_checker')
        self.assertEqual(saved['packet'], packet)
        body = self.s.get('e-news')['body']
        body['paragraphs']['p1'] = 'Changed identity evidence.'
        self.s.put('e-news', 'evidence', body, 'collector:revision')
        self.assertEqual(self.s.get_review('before:fact_checker')['packet'], packet)
        self.assertEqual(packet['dependencies']['e-news']['version'], 1)
        self.assertIsNone(self.s.latest_review('o-cedar', 'fact_checker'))
        with tempfile.TemporaryDirectory() as directory:
            export(self.s, Path(directory), {})
            data = json.loads(Path(directory, 'records.json').read_text())
            exported = next(r for r in data['tables']['reviews'] if r['id'] == 'before:fact_checker')
            self.assertEqual(exported['packet'], packet)
            rows = [json.loads(line) for line in Path(directory, 'records.jsonl').read_text().splitlines()]
            exported_line = next(r['record'] for r in rows if r['group'] == 'reviews' and r['record']['id'] == 'before:fact_checker')
            self.assertEqual(exported_line['packet'], packet)

    def test_exact_packet_survives_upstream_review_change(self):
        replay(self.s, 'o-cedar', 'before')
        old = self.s.get_review('before:researcher')['packet']
        packet = self.s.packet('o-cedar', 'qc')
        output = replay_output(packet, 'replacement-qc')
        output['reason'] = 'Changed QC assessment.'
        self.s.review(packet, output)
        self.assertIsNone(self.s.latest_review('o-cedar', 'researcher'))
        saved = self.s.get_review('before:researcher')['packet']
        self.assertEqual(saved, old)
        self.assertEqual(saved['prior_reviews']['qc']['execution_id'], 'before:qc')
        self.assertEqual(self.s.packet('o-cedar', 'researcher')['prior_reviews']['qc']['execution_id'], 'replacement-qc')

    def test_packets_survive_database_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, 'store.sqlite')
            store = Store(path)
            seed(store)
            replay(store, 'o-cedar', 'persisted')
            saved = store.get_review('persisted:fact_checker')
            store.close()
            store = Store(path)
            try:
                self.assertEqual(store.get_review('persisted:fact_checker'), saved)
            finally:
                store.close()

    def test_legacy_schema_migrates_without_inventing_packets(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, 'legacy.sqlite')
            conn = sqlite3.connect(path)
            conn.execute('CREATE TABLE reviews(id TEXT PRIMARY KEY, subject TEXT, version INTEGER, stage TEXT, packet_hash TEXT, body TEXT, created TEXT)')
            conn.commit()
            conn.close()
            store = Store(path)
            try:
                seed(store)
                packet = store.packet('o-cedar', 'qc')
                output = replay_output(packet, 'legacy')
                store.db.execute('INSERT INTO reviews(id,subject,version,stage,packet_hash,body,created) VALUES(?,?,?,?,?,?,?)',
                    ('legacy', 'o-cedar', 2, 'qc', digest(packet), encode(output), 'historical'))
                store.db.commit()
                self.assertEqual(store.get_review('legacy')['input_state'], 'unavailable_legacy')
                self.assertIsNone(store.latest_review('o-cedar', 'qc'))
                with self.assertRaises(Invalid): store.review(packet, output)
                self.assertIsNone(store.get_review('legacy')['packet'])
                store.review(packet, replay_output(packet, 'new-execution'))
                self.assertEqual(store.latest_review('o-cedar', 'qc')['id'], 'new-execution')
            finally:
                store.close()

    def test_packet_integrity_failure_is_visible(self):
        replay(self.s, 'o-cedar', 'before')
        self.s.db.execute("UPDATE reviews SET packet='{}' WHERE id='before:qc'")
        with self.assertRaisesRegex(Invalid, 'hash mismatch'):
            self.s.get_review('before:qc')

    def test_partial_report_counts_submitted_completed_pending(self):
        # The reporting helper also accounts for absent entries before a checker runs.
        self.assertEqual(coverage([{'id': 'a'}, {'id': 'b'}], {'a': {'status': 'pending'}}),
                         {'eligible': 2, 'submitted': 1, 'completed': 0, 'pending': 2, 'unsubmitted': 1})
        other = Store()
        try:
            demonstration = demonstrate(other)
            packet = other.packet('f-campaign', 'fact_checker')
            output = replay_output(packet, 'partial')
            output['checks'][0]['status'] = 'pending'
            output['outcome'] = 'incomplete'
            other.review(packet, output)
            self.assertEqual(other.decide('f-campaign', 'partial')['state'], 'pending')
            with tempfile.TemporaryDirectory() as directory:
                export(other, Path(directory), demonstration)
                data = json.loads(Path(directory, 'records.json').read_text())
                self.assertEqual(data['claim_coverage']['f-campaign'],
                    {'eligible': 4, 'submitted': 4, 'completed': 3, 'pending': 1, 'unsubmitted': 0})
                self.assertIn('3/4 completed; 4 submitted; 1 pending', Path(directory, 'report.md').read_text())
        finally:
            other.close()

    def hypothesis_packet(self, material=False):
        body = self.s.get('o-cedar')['body']
        body['claims'].append(claim('hypothesis', 'Operational assistance might be useful.', 'e-news', 'hypothesis', material))
        self.s.put('o-cedar', 'organization', body, 'collector:hypothesis')
        for stage in ('qc', 'researcher', 'skeptic'):
            packet = self.s.packet('o-cedar', stage)
            self.s.review(packet, replay_output(packet, stage))
        return self.s.packet('o-cedar', 'fact_checker')

    def test_hypothesis_cannot_receive_factual_verdict(self):
        packet = self.hypothesis_packet()
        for status in ('verified', 'partly_verified', 'contradicted', 'unverifiable'):
            output = replay_output(packet, status)
            output['checks'][-1]['status'] = status
            with self.subTest(status=status), self.assertRaisesRegex(Invalid, 'Hypothesis'):
                self.s.review(packet, output)

    def test_reviewed_hypothesis_stays_nonfactual_in_report_and_json(self):
        packet = self.hypothesis_packet()
        self.s.review(packet, replay_output(packet, 'hypothesis-review'))
        self.assertEqual(self.s.decide('o-cedar', 'decision')['state'], 'admitted')
        with tempfile.TemporaryDirectory() as directory:
            export(self.s, Path(directory), {})
            text = Path(directory, 'report.md').read_text()
            self.assertIn('hypothesis — reviewed_hypothesis (not a verified fact)', text)
            data = json.loads(Path(directory, 'records.json').read_text())
            reviewed = next(r for r in data['tables']['reviews'] if r['id'] == 'hypothesis-review')
            self.assertEqual(reviewed['packet']['subject']['body']['claims'][-1]['type'], 'hypothesis')
            self.assertEqual(reviewed['body']['checks'][-1]['status'], 'reviewed_hypothesis')

    def test_material_hypothesis_cannot_satisfy_required_fact(self):
        packet = self.hypothesis_packet(material=True)
        self.s.review(packet, replay_output(packet, 'hypothesis-review'))
        result = self.s.decide('o-cedar', 'decision')
        self.assertEqual(result['state'], 'pending')
        self.assertIn('Material hypothesis cannot establish required fact: hypothesis', result['blockers'])

    def test_factual_claim_cannot_use_hypothesis_disposition(self):
        packet = self.hypothesis_packet()
        output = replay_output(packet, 'wrong-classification')
        output['checks'][0]['status'] = 'reviewed_hypothesis'
        with self.assertRaisesRegex(Invalid, 'Factual claim'):
            self.s.review(packet, output)

    def test_pending_hypothesis_remains_unperformed(self):
        packet = self.hypothesis_packet()
        output = replay_output(packet, 'pending-hypothesis')
        output['checks'][-1]['status'] = 'pending'
        output['outcome'] = 'incomplete'
        self.s.review(packet, output)
        self.assertIn('Claim not checked: hypothesis', self.s.blockers('o-cedar'))


if __name__ == '__main__':
    unittest.main()
