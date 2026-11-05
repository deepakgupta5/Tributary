import json
from pathlib import Path
import tempfile
import unittest

from tributary.core import Invalid, Store
from tributary.report import export


class LiveBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.source = {'live': True, 'name': 'Public register', 'claims': [], 'dependencies': [],
                       'details': {'identity': 'resolved', 'access': 'resolved', 'handling': 'resolved',
                                   'utility': 'resolved'}, 'endpoint': 'https://example.test/data'}
        self.store.put('s-live', 'source', self.source, 'collection:live')

    def tearDown(self):
        self.store.close()

    def evidence(self):
        return {'live': True, 'source': 's-live', 'dependencies': [], 'available': True,
                'publication_date': '2026-11-05', 'paragraphs': {'row': 'Selected public fields.'},
                'source_url': 'https://example.test/data.csv', 'retrieved_at': '2026-11-05',
                'retention': 'sanitized_excerpt_and_factual_notes', 'whole_document_stored': False}

    def test_live_evidence_requires_bounded_retention_metadata(self):
        body = self.evidence()
        self.store.put('e-live', 'evidence', body, 'collection:live')
        for field in ('source_url', 'retrieved_at', 'retention', 'whole_document_stored'):
            changed = self.evidence()
            changed.pop(field)
            with self.subTest(field=field), self.assertRaises(Invalid):
                self.store.put('e-bad-' + field, 'evidence', changed, 'collection:live')

    def test_scope_must_be_explicit_and_exclusive(self):
        for flags in ({}, {'synthetic': True, 'live': True}):
            body = {**self.source, **flags}
            body.pop('live', None) if not flags else None
            with self.assertRaisesRegex(Invalid, 'exactly one'):
                self.store.put('bad-' + str(len(flags)), 'source', body, 'collection:live')

    def test_live_report_labels_scope_and_does_not_claim_fiction(self):
        self.store.put('e-live', 'evidence', self.evidence(), 'collection:live')
        with tempfile.TemporaryDirectory() as directory:
            export(self.store, Path(directory), {})
            data = json.loads(Path(directory, 'records.json').read_text())
            report = Path(directory, 'report.md').read_text()
            self.assertEqual(data['data_scopes'], ['live_sanitized'])
            self.assertFalse(data['synthetic_only'])
            self.assertIn('# Bounded live Tributary report', report)
            self.assertIn('whole source documents are not stored', report)
            self.assertIn('supervised bounded retrieval', report)
            self.assertIn('## Retained live evidence catalog', report)
            self.assertIn('https://example.test/data.csv', report)
            self.assertNotIn('All names and evidence are fictional', report)
            self.assertNotIn('No real endpoint was attempted', report)

    def test_live_excerpt_size_is_bounded(self):
        body = self.evidence()
        body['paragraphs']['row'] = 'x' * 2001
        with self.assertRaisesRegex(Invalid, 'excerpt limit'):
            self.store.put('e-too-large', 'evidence', body, 'collection:live')


if __name__ == '__main__':
    unittest.main()
