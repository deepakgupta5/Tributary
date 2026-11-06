import json
import unittest
from datetime import date
from tributary.pressure_report import report
from tributary.signals import ROOT, generate


class PressurePass(unittest.TestCase):
    def test_reviewed_signals_and_repeat(self):
        folder = ROOT / 'OutBound/evidence/day-4'
        load = lambda path: json.loads(path.read_text())
        inputs = load(folder / 'pressure-inputs.json')
        state = load(folder / 'state.json')
        args = (state, state, load(folder.parent / 'day-3/worklist.json'),
                load(folder / 'pilot-baseline.json'), date.fromisoformat(inputs['as_of']))
        delta = generate(*args, inputs)['delta']
        self.assertEqual(delta['new_accounts'], [])
        self.assertEqual(len(delta['newly_observed_events']), 6)
        self.assertEqual(delta['accounts_with_current_reason'], ['132168162RR0001'])
        repeat = generate(*args, dict(inputs, baseline=inputs['current']))['delta']
        self.assertEqual(repeat['newly_observed_events'], [])
        self.assertEqual(report(folder), (folder / 'pressure-report.md').read_text())
