import json
from pathlib import Path
import unittest
from tributary.checks import amount_equal, shortfall, evaluate
from tributary.core import Invalid


class CheckTests(unittest.TestCase):
    def amount(self, value='40', **changes):
        return {'value': value, 'currency': 'CAD', 'unit': 'dollars', 'period': '2025', 'basis': 'actual', **changes}

    def test_numeric_context_mismatches(self):
        for changes in ({'currency': 'USD'}, {'unit': 'thousands'}, {'period': '2024'}, {'basis': 'target'}, {'value': '50'}):
            self.assertFalse(amount_equal(self.amount(), self.amount(**changes)))
        self.assertTrue(amount_equal(self.amount('40'), self.amount('40.00')))

    def test_arithmetic_and_nonfinite_values(self):
        self.assertEqual(shortfall(self.amount('50', basis='target'), self.amount()), '10')
        with self.assertRaises(Invalid): shortfall(self.amount('50', basis='target'), self.amount(currency='USD'))
        with self.assertRaises(Invalid): amount_equal(self.amount('NaN'), self.amount())

    def test_evaluator_counts_missing_false_verification_and_abstention(self):
        expected = json.loads(Path('OutBound/data/fixtures/expected.json').read_text())
        # Deliberately flawed saved results test scoring, not AI reasoning.
        observed = [{'id': 'correct', 'status': 'contradicted'}, {'id': 'target', 'status': 'verified'},
                    {'id': 'quote', 'status': 'contradicted'}, {'id': 'cause', 'status': 'unverifiable'},
                    {'id': 'missing', 'status': 'unverifiable'}]
        metrics = evaluate(expected, observed)
        self.assertEqual((metrics['defects'], metrics['caught'], metrics['missed']), (5, 2, 3))
        self.assertEqual((metrics['false_verification'], metrics['false_rejection'], metrics['checked']), (1, 1, 5))

    def test_evaluator_rejects_duplicate_or_unknown_ids(self):
        for rows in ([{'id': 'a', 'status': 'verified'}] * 2, [{'id': 'b', 'status': 'verified'}]):
            with self.assertRaises(Invalid): evaluate({'a': 'verified'}, rows)

    def test_expected_answers_are_separate_artifact(self):
        inputs = json.loads(Path('OutBound/data/fixtures/role_inputs.json').read_text())
        self.assertEqual({c['id'] for c in inputs['claims']}, set(json.loads(Path('OutBound/data/fixtures/expected.json').read_text())))
        self.assertNotIn('contradicted', json.dumps(inputs))
