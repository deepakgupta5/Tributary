import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_live_runner():
    path = ROOT / 'live_runs' / 'session-001' / 'run.py'
    spec = importlib.util.spec_from_file_location('tributary_live_session_001', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorklistTests(unittest.TestCase):
    def test_existing_live_accounts_are_visible_with_separate_states(self):
        runner = load_live_runner()
        session = ROOT / 'live_runs' / 'session-001'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'result'
            runner.run(session, output)
            worklist = json.loads((output / 'worklist.json').read_text())
            accounts = {card['account_id']: card for card in worklist['accounts']}

            self.assertEqual(set(accounts), {'o-foodlifeline', 'o-gvfb', 'o-nurturing'})
            self.assertEqual(accounts['o-gvfb']['discovery_state'], 'discovered')
            self.assertEqual(accounts['o-gvfb']['identity_state'], 'verified')
            self.assertEqual(accounts['o-gvfb']['eligibility_state'], 'open')
            self.assertEqual(accounts['o-gvfb']['signal_review_state'], 'no_signal_identified')
            self.assertEqual(accounts['o-gvfb']['business_relevance'], 'unreviewed_private')

            self.assertEqual(accounts['o-foodlifeline']['signal_review_state'], 'reviewed_signal')
            self.assertEqual(accounts['o-nurturing']['signal_review_state'], 'signal_under_review')

    def test_markdown_is_compact_default_and_keeps_uncertainty_visible(self):
        runner = load_live_runner()
        session = ROOT / 'live_runs' / 'session-001'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'result'
            runner.run(session, output)
            worklist = (output / 'worklist.md').read_text()
            audit = (output / 'report.md').read_text()

            self.assertIn('Greater Vancouver Food Bank Society', worklist)
            self.assertIn('current status', worklist)
            self.assertIn('Hypothesis:', worklist)
            self.assertLess(len(worklist.splitlines()), len(audit.splitlines()))


if __name__ == '__main__':
    unittest.main()
