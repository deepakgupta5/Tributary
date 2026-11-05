"""Persist/replay saved session outputs and score only after a hash freeze.

No reviewer inference occurs in this program. No network or external dependencies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[3]))
from tributary.core import Store, STAGES, now, require
from tributary.report import export
from tributary.checks import evaluate


def read(path):
    return json.loads(path.read_text())


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def initialize(store):
    require(not store.current(), 'Use an empty database')
    collected = read(ROOT / 'outputs/collection.json')
    for row in collected['seed_sources']:
        store.put(row['id'], row['kind'], row['body'], collected['execution_id'])
    audit = store.ingest('session-001:collection', collected['evidence'])
    require(audit['status'] == 'complete', 'Collection persistence failed')
    for row in collected['subjects']:
        store.put(row['id'], row['kind'], row['body'], collected['execution_id'])
    for row in collected['discoveries']:
        store.discover(row['parent'], row['child'], row['method'], collected['execution_id'])


def subjects():
    return [r['id'] for r in read(ROOT / 'outputs/collection.json')['subjects']]


def packet_bundle(store, stage):
    return {rid: store.packet(rid, stage) for rid in subjects()}


def record(store, stage):
    packets = read(ROOT / 'packets' / (stage + '.json'))
    outputs = read(ROOT / 'outputs' / (stage + '.json'))
    require(set(packets) == set(outputs) == set(subjects()), 'Subject mismatch')
    for rid in subjects():
        store.review(packets[rid], outputs[rid])


def render(store, out, mode):
    decisions = [store.decide(rid, 'session-001:decisions') for rid in subjects()]
    audit = store.reconcile({'states': {}, 'cursor': 0})
    metadata = {'run': 'session-001', 'execution': mode,
                'tracks': {'complete_chain': [s for s in subjects() if s != 'f-challenge'],
                           'reviewer_challenge': ['f-challenge']},
                'context': read(ROOT / 'context.json'),
                'decisions': decisions, 'reconciliation': audit}
    out.mkdir(parents=True, exist_ok=True)
    export(store, out, metadata)


def frozen_paths():
    return [ROOT / 'context.json', *sorted((ROOT / 'inputs').glob('*.json')),
            *sorted((ROOT / 'outputs').glob('*.json')), *sorted((ROOT / 'packets').glob('*.json'))]


def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths()}


def verify_freeze():
    require(hashes() == read(ROOT / 'frozen.json')['sha256'], 'Frozen input/output changed')


def scored(expected, observed):
    score = evaluate(expected, observed)
    actual = {x['id']: x['status'] for x in observed}
    score.update(submitted=len(observed), pending=len(expected) - score['checked'],
                 abstentions=sum(v == 'unverifiable' for v in actual.values()),
                 mismatches=[{'id': k, 'expected': v, 'actual': actual.get(k, 'pending')}
                             for k, v in expected.items() if actual.get(k, 'pending') != v])
    return score


def score(out):
    verify_freeze()  # Expected answers are opened only in this scoring operation.
    expected = read(ROOT / 'inputs/expected.json')
    fact = read(ROOT / 'outputs/fact_checker.json')
    researcher = read(ROOT / 'outputs/researcher.json')
    skeptic = read(ROOT / 'outputs/skeptic.json')
    result = {'basis': 'Open-book, contaminated, same assistant; descriptive case counts only.',
              'frozen_at': read(ROOT / 'frozen.json')['created'], 'scored_at': now(), 'tracks': {}}
    for track, keys in [('complete_chain', expected['chain']),
                        ('reviewer_challenge', {'f-challenge': expected['challenge']})]:
        flat = {rid + '/' + cid: status for rid, claims in keys.items() for cid, status in claims.items()}
        role_scores = {}
        for role, outputs, field in [('researcher', researcher, 'assessments'), ('fact_checker', fact, 'checks')]:
            observations = [{'id': rid + '/' + c['claim_id'], 'status': c['status']}
                            for rid in keys for c in outputs[rid][field] if c['status'] != 'reviewed_hypothesis']
            role_scores[role] = scored(flat, observations)
        defects = {k for k, v in flat.items() if v != 'verified'}
        flagged = {rid + '/' + i['claim_id'] for rid in keys for i in skeptic[rid]['issues']
                   if 'claim_id' in i and i['material']}
        role_scores['skeptic'] = {'defects': len(defects), 'caught': len(defects & flagged),
                                  'missed': len(defects - flagged),
                                  'correct_controls': len(flat) - len(defects),
                                  'material_false_alarms': len((flagged & set(flat)) - defects)}
        result['tracks'][track] = role_scores
    exported = read(out / 'records.json')
    result['coverage'] = {key: sum(c[key] for c in exported['claim_coverage'].values())
                          for key in ('eligible', 'submitted', 'completed', 'pending', 'unsubmitted')}
    result['stages'] = {'eligible': len(subjects()) * len(STAGES),
                        'submitted': len(exported['tables']['reviews']),
                        'completed': sum(r['body']['completed'] for r in exported['tables']['reviews']),
                        'pending': sum(not r['body']['completed'] for r in exported['tables']['reviews'])}
    hyp = [('f-chain', 'f6'), ('f-challenge', 'c12')]
    result['hypotheses'] = {'eligible': len(hyp), 'retained_nonfactual': sum(
        next(c for c in fact[rid]['checks'] if c['claim_id'] == cid)['status'] == 'reviewed_hypothesis'
        for rid, cid in hyp)}
    states = exported['current_status']
    result['admission'] = {'eligible': len(subjects()), 'expected_active': len(expected['required_admitted']),
        'actual_active': sum(s['state'] in {'approved', 'admitted', 'approved_for_collection'} for s in states.values()),
        'false_approval': [rid for rid in expected['required_pending'] if states[rid]['state'] != 'pending'],
        'false_block': [rid for rid in expected['required_admitted'] if states[rid]['state'] not in {'approved', 'admitted', 'approved_for_collection'}]}
    collection = read(ROOT / 'outputs/collection.json')
    originals = {d['id']: {k: v for k, v in d.items() if k != 'id'}
                 for d in read(ROOT / 'inputs/source_documents.json')['documents']}
    result['collection'] = {'documents_expected': len(originals), 'documents_stored': len(collection['evidence']),
        'exact_document_preservation': sum({k: v for k, v in e['body'].items() if k != 'synthetic'} == originals[e['id']]
                                           for e in collection['evidence']),
        'directions': sorted({x['record']['body']['direction'] for x in
            [json.loads(line) for line in (out / 'records.jsonl').read_text().splitlines()]
            if x['group'] == 'history' and x['record']['type'] == 'discovery'})}
    result['qc'] = {'subjects': len(subjects()), 'completed': sum(x['completed'] for x in read(ROOT / 'outputs/qc.json').values()),
                    'note': 'QC assessed faithful storage and proposal labelling; it did not confer factual or admission approval.'}
    result['reconciliation'] = exported['demonstration']['reconciliation']
    write_new(out / 'scores.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['initialize', 'prepare', 'record', 'render', 'freeze', 'score', 'replay'])
    parser.add_argument('--stage', choices=STAGES)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.action == 'freeze':
        require(all((ROOT / folder / (stage + '.json')).exists() for stage in STAGES for folder in ('packets', 'outputs')), 'Stages missing')
        write_new(ROOT / 'frozen.json', {'created': now(), 'sha256': hashes(),
                  'meaning': 'Byte freeze before scoring, not a signature or isolation guarantee.'})
        return
    if args.action == 'score':
        print(json.dumps(score(args.out), indent=2))
        return
    store = Store(args.out / 'evaluation.sqlite')
    try:
        if args.action == 'initialize':
            initialize(store)
        elif args.action == 'prepare':
            require(args.stage is not None, 'Stage required')
            write_new(ROOT / 'packets' / (args.stage + '.json'), packet_bundle(store, args.stage))
        elif args.action == 'record':
            require(args.stage is not None, 'Stage required')
            record(store, args.stage)
        elif args.action == 'render':
            render(store, args.out, 'original recorded coding session')
        elif args.action == 'replay':
            verify_freeze()
            initialize(store)
            for stage in STAGES:
                require(packet_bundle(store, stage) == read(ROOT / 'packets' / (stage + '.json')), 'Reconstructed packet differs')
                record(store, stage)
            render(store, args.out, 'Transport replay of frozen coding-session outputs; no new inference')
            score(args.out)
    finally:
        store.close()


if __name__ == '__main__':
    main()
