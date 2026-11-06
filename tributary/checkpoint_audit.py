"""Record ordered review executions. Work in a fresh directory per packet."""
import argparse
from datetime import datetime, timezone
from pathlib import Path

from .daily import digest, read, save

STAGES = ('qc', 'researcher', 'skeptic', 'fact_checker')


def execute(stage, packet, responses, previous=None, verdicts=None):
    index = STAGES.index(stage)
    flags = {f['signal_id']: (g, f) for g in packet['groups'] for f in g['flags']}
    if set(responses) != set(flags):
        raise ValueError('A response is required for each flag')
    if index and (not previous or previous['stage'] != STAGES[index-1]
                  or previous['packet_hash'] != digest(packet)):
        raise ValueError('Missing or stale predecessor')
    results = {}
    for sid, (group, flag) in flags.items():
        answer = responses[sid]
        if answer.get('result') not in ('pass', 'hold') or not answer.get('reason','').strip():
            raise ValueError('Each checkpoint needs an outcome and reason')
        if not answer.get('actor','').strip():
            raise ValueError('Missing reviewer identity')
        results[sid] = dict(answer, candidate_version=flag['candidate_version'],
                            document_version=group['document_version'], source=group['url'])
    record = dict(stage=stage, packet_hash=digest(packet), packet_id=packet['id'],
                  executed_at=datetime.now(timezone.utc).isoformat(), outputs=results,
                  predecessor=previous['execution_id'] if previous else None)
    if stage == 'fact_checker':
        from .source_review import validate
        validate(packet, verdicts)
        record['verdict_hash'] = digest(verdicts)
    record['execution_id'] = digest(record)
    return record


def verify(packet, verdicts, chain):
    if len(chain) != len(STAGES):
        raise ValueError('Four checkpoint executions required')
    previous = None
    for stage, record in zip(STAGES, chain):
        if (record['stage'] != stage or record['packet_hash'] != digest(packet)
                or record['predecessor'] != previous
                or record['execution_id'] != digest({k:v for k,v in record.items() if k != 'execution_id'})):
            raise ValueError('Checkpoint audit mismatch')
        previous = record['execution_id']
    if chain[-1]['verdict_hash'] != digest(verdicts):
        raise ValueError('Fact check belongs to another verdict version')
    for v in verdicts['verdicts']:
        for record in chain:
            out = record['outputs'][v['signal_id']]
            if out['candidate_version'] != v['candidate_version'] or out['document_version'] != v['document_version']:
                raise ValueError('Stale checkpoint output')
            if v['disposition'] == 'actionable' and out['result'] != 'pass':
                raise ValueError('A held checkpoint prevents promotion')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=STAGES)
    for field in ('packet','responses','directory'):
        parser.add_argument(field, type=Path)
    parser.add_argument('--verdicts', type=Path)
    args = parser.parse_args()
    idx = STAGES.index(args.stage)
    target = args.directory / (args.stage+'.json')
    if target.exists():
        parser.error('Existing execution; use a new directory to rerun')
    prior = read(args.directory/(STAGES[idx-1]+'.json')) if idx else None
    save(target, execute(args.stage, read(args.packet), read(args.responses), prior,
                         read(args.verdicts) if args.verdicts else None))
