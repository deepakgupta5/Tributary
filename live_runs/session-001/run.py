#!/usr/bin/env python3
"""Reproduce the bounded supervised live session from preserved inputs."""
import argparse
from decimal import Decimal
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tributary.core import Store  # noqa: E402
from tributary.report import export  # noqa: E402


STAGES = ('qc', 'researcher', 'skeptic', 'fact_checker')


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def review_output(subject, stage, assessment, context, run_id):
    source = assessment['fact' if stage == 'fact_checker' else stage]
    result = {
        'execution_id': f'{run_id}:{stage}:{subject["id"]}',
        'actor': 'Codex assistant',
        'basis': 'coding_session',
        'context': context,
        'completed': True,
        'outcome': source['outcome'],
        'reason': source['reason'],
    }
    if stage == 'researcher':
        result['claim_ids'] = [claim['id'] for claim in subject['body']['claims']]
        result['unknowns'] = source.get('unknowns', [])
    elif stage == 'skeptic':
        result['issues'] = source['issues']
    elif stage == 'fact_checker':
        result['checks'] = [source['checks'][claim['id']]
                            | {'claim_id': claim['id']}
                            for claim in subject['body']['claims']]
        result['details'] = source['details']
        result['resolutions'] = source['resolutions']
    return result


def validate_session(records, assessments):
    organizations = [s for s in records['subjects'] if s['kind'] == 'organization']
    if len(organizations) > 3:
        raise ValueError('The live prototype is limited to three organizations')
    if set(assessments['subjects']) != {s['id'] for s in records['subjects']}:
        raise ValueError('Assessment and subject ledgers differ')
    difference = 16_001_264 - 10_755_509
    percentage = (Decimal(difference) / Decimal(10_755_509) * Decimal(100)).quantize(Decimal('0.01'))
    if difference != 5_245_755 or percentage != Decimal('48.77'):
        raise ValueError('Food Lifeline calculation regression')
    for evidence in records['evidence']:
        body = evidence['body']
        if body.get('whole_document_stored') is not False:
            raise ValueError('Whole live documents are forbidden')


def run(session_dir, output_dir):
    records = read_json(session_dir / 'records.json')
    assessments = read_json(session_dir / 'assessments.json')
    validate_session(records, assessments)
    if output_dir.exists():
        raise FileExistsError(f'Refusing to overwrite existing output: {output_dir}')
    output_dir.mkdir(parents=True)

    database = output_dir / 'session.sqlite'
    store = Store(database)
    try:
        opening = store.snapshot()
        for source in records['seed_sources']:
            store.put(source['id'], source['kind'], source['body'], 'collection:live-session-001')

        ingestion = store.ingest(records['run_id'] + ':collection', records['evidence'])
        if ingestion['status'] != 'complete':
            raise ValueError('Live evidence ingestion did not reconcile')

        for subject in records['subjects']:
            store.put(subject['id'], subject['kind'], subject['body'], 'collection:live-session-001')
        for discovery in records['discoveries']:
            store.discover(discovery['parent'], discovery['child'], discovery['method'], records['run_id'])

        for subject in records['subjects']:
            assessment = assessments['subjects'][subject['id']]
            for stage in STAGES:
                packet = store.packet(subject['id'], stage)
                output = review_output(subject, stage, assessment, assessments['context'], records['run_id'])
                write_json(output_dir / 'packets' / stage / f'{subject["id"]}.json', packet)
                write_json(output_dir / 'outputs' / stage / f'{subject["id"]}.json', output)
                store.review(packet, output)

        decisions = []
        for kind in ('source', 'organization', 'finding'):
            for subject in records['subjects']:
                if subject['kind'] == kind:
                    decisions.append(store.decide(subject['id'], records['run_id']))

        reconciliation = store.reconcile(opening)
        demonstration = {
            'run_id': records['run_id'],
            'retrieved_at': records['retrieved_at'],
            'purpose': records['purpose'],
            'organization_count': len([s for s in records['subjects'] if s['kind'] == 'organization']),
            'collection': ingestion,
            'decisions': decisions,
            'reconciliation': reconciliation,
            'transient_downloads': records['transient_downloads'],
            'whole_documents_stored': 0,
            'context_limitation': assessments['context'],
        }
        export(store, output_dir, demonstration)
        write_json(output_dir / 'run.json', demonstration)
        return demonstration
    finally:
        store.close()
        database.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path(__file__).with_name('results'))
    args = parser.parse_args()
    session_dir = Path(__file__).resolve().parent
    result = run(session_dir, args.out.resolve())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
