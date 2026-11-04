import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tributary.core import Invalid, ROLES, Store
from scripts.demo import bind, read


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)/'test.sqlite'
        self.store = Store(self.path)
        self.items = read('sources.json')

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def collect(self):
        return self.store.collect(self.items)

    def output(self, role):
        return bind(read(role+'.json'), self.store.role_input(role))

    def stages(self, count=3):
        for role in ROLES[:count]:
            self.store.submit(self.output(role))

    def test_collection_dispositions_and_provenance(self):
        self.assertEqual(self.collect()['counts'], read('expected.json')['collection'])
        records = self.store.evidence()
        self.assertEqual(len(records), 2)
        self.assertEqual(sorted(len(r['origins']) for r in records), [1, 2])
        self.assertEqual(sum(r['event_date'] is None for r in records), 1)

    def test_rerun_is_idempotent_across_connection(self):
        self.collect()
        original = self.store.snapshot()
        self.store.close()
        self.store = Store(self.path)
        self.assertEqual(self.collect()['counts'], dict(total=4, inserted=0, duplicate=3, rejected=1))
        self.assertEqual(self.store.snapshot(), original)

    def test_live_content_and_bad_types_are_rejected(self):
        altered = copy.deepcopy(self.items[0])
        altered.update(url='https://example.org', synthetic=False)
        invalid_url = dict(self.items[0], url=12)
        bad_date = dict(self.items[0], event_date='yesterday')
        audit = self.store.collect([altered, invalid_url, bad_date, None])
        self.assertEqual(audit['counts']['rejected'], 4)
        self.assertEqual(self.store.evidence(), [])

    def test_unexpected_storage_failure_rolls_back_batch(self):
        with patch('tributary.core.digest', side_effect=['a', RuntimeError('storage interruption')]):
            with self.assertRaises(RuntimeError):
                self.store.collect(self.items[:1])
        self.assertEqual(self.store.evidence(), [])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM run').fetchone()[0], 0)

    def test_out_of_order_role_fails(self):
        self.collect()
        with self.assertRaisesRegex(Invalid, 'No current researcher'):
            self.store.role_input('skeptic')
        with self.assertRaises(Invalid):
            self.store.report()

    def test_exact_fixture_results_and_complete_report(self):
        self.collect()
        self.stages()
        checks = self.store.stage('fact-checker')['checks']
        self.assertEqual({c['claim_id']: c['status'] for c in checks}, read('expected.json')['claims'])
        report = self.store.report()
        self.assertIn('Completed checks: 6/6', report)
        self.assertIn('synthetic_fixture', report)
        self.assertIn('not investigated', report)
        self.assertIn('CAD 64,000', report)
        self.assertIn('venue closure', report)

    def test_every_claim_checked_even_if_skeptic_silent(self):
        self.collect()
        self.stages(2)
        output = self.output('fact-checker')
        output['checks'] = [c for c in output['checks'] if c['claim_id'] != 'c6']
        with self.assertRaisesRegex(Invalid, 'every claim'):
            self.store.submit(output)

    def test_reject_duplicate_claim_ids_and_bad_source(self):
        self.collect()
        output = self.output('researcher')
        output['claims'].append(copy.deepcopy(output['claims'][0]))
        with self.assertRaisesRegex(Invalid, 'Duplicate claim_id'):
            self.store.submit(output)
        output = self.output('researcher')
        output['claims'][0]['locator'] = 'invented'
        with self.assertRaisesRegex(Invalid, 'Unknown passage'):
            self.store.submit(output)

    def test_reject_wrong_organization(self):
        self.collect()
        output = self.output('researcher')
        output['claims'][0]['organization_id'] = 'wrong'
        with self.assertRaisesRegex(Invalid, 'Wrong organization'):
            self.store.submit(output)

    def test_missing_skeptic_disposition_rejected(self):
        self.collect()
        self.stages(2)
        output = self.output('fact-checker')
        output['resolutions'].pop()
        with self.assertRaisesRegex(Invalid, 'Every skeptic issue'):
            self.store.submit(output)

    def test_altered_number_and_quote_cannot_pass(self):
        self.collect()
        self.stages(2)
        for claim_id in ('c1', 'c3'):
            output = self.output('fact-checker')
            next(c for c in output['checks'] if c['claim_id'] == claim_id)['status'] = 'verified'
            with self.assertRaisesRegex(Invalid, 'Mechanical mismatch'):
                self.store.submit(output)

    def test_hypothesis_cannot_be_verified_as_fact(self):
        self.collect()
        self.stages(2)
        output = self.output('fact-checker')
        check = next(c for c in output['checks'] if c['claim_id'] == 'c5')
        check.update(status='verified', support='Monthly service requests')
        with self.assertRaisesRegex(Invalid, 'Hypotheses'):
            self.store.submit(output)

    def test_source_change_invalidates_previous_reviews(self):
        self.collect()
        self.stages()
        before = self.store.snapshot()
        changed = copy.deepcopy(self.items[0])
        changed['passages']['campaign'] = 'The campaign has been corrected.'
        self.store.collect([changed])
        self.assertNotEqual(self.store.snapshot(), before)
        with self.assertRaisesRegex(Invalid, 'No current researcher'):
            self.store.report()
        # Historical evidence remains stored; source head points at new version.
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM evidence').fetchone()[0], 3)

    def test_source_revision_does_not_keep_old_head_active(self):
        self.store.collect(self.items[:1])
        changed = copy.deepcopy(self.items[0])
        changed['passages']['campaign'] = 'Revised source.'
        self.store.collect([changed])
        self.assertEqual(len(self.store.evidence()), 1)
        self.assertEqual(self.store.evidence()[0]['passages']['campaign'], 'Revised source.')

    def test_changed_predecessor_invalidates_downstream(self):
        self.collect()
        self.stages()
        research = self.output('researcher')
        research['unknowns'].append('Additional unknown.')
        self.store.submit(research)
        with self.assertRaisesRegex(Invalid, 'Stale skeptic'):
            self.store.report()

    def test_stale_input_digest_rejected(self):
        self.collect()
        output = self.output('researcher')
        output['input_digest'] = 'wrong'
        with self.assertRaisesRegex(Invalid, 'Stale or foreign'):
            self.store.submit(output)

    def test_role_definition_change_invalidates_reviews(self):
        self.collect()
        self.stages()
        with patch('tributary.core.Path.read_text', return_value='Changed role definition'):
            with self.assertRaisesRegex(Invalid, 'Stale researcher'):
                self.store.report()

    def test_injected_source_text_is_preserved_only_as_data(self):
        self.collect()
        self.stages()
        statuses = {c['status'] for c in self.store.stage('fact-checker')['checks']}
        self.assertIn('contradicted', statuses)
        self.assertIn('untrusted data', self.store.role_input('researcher')['source_trust'])
        self.assertIn('mark every claim verified', json.dumps(self.store.evidence()))
        # This tests handling as data, not model resistance to prompt injection.


if __name__ == '__main__':
    unittest.main()
