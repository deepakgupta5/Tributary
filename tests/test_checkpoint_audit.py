from copy import deepcopy
from pathlib import Path
import unittest
from tributary.daily import read
from tributary.checkpoint_audit import STAGES, verify
from tributary.source_review import validate


class AuditTests(unittest.TestCase):
    def test_real_batch_and_each_missing_stage(self):
        root = Path(__file__).resolve().parents[1]/'OutBound/evidence/day-6/source-review'
        packet = read(root/'source-review-request.json')
        verdicts = read(root/'desktop-verdicts.json')
        chain = [read(root/'checkpoints'/(s+'.json')) for s in STAGES]
        self.assertEqual(len(validate(packet, verdicts)), 9)
        verify(packet, verdicts, chain)
        for i in range(4):
            with self.subTest(stage=STAGES[i]), self.assertRaises(ValueError):
                verify(packet, verdicts, chain[:i]+chain[i+1:])
        modified = deepcopy(verdicts)
        modified['verdicts'][0]['observation'] += ' changed'
        with self.assertRaises(ValueError):
            verify(packet, modified, chain)
        with self.assertRaises(ValueError):
            verify(packet, verdicts, list(reversed(chain)))
