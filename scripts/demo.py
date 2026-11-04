"""Replay synthetic role artifacts. This does not run or evaluate a model."""
import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tributary.core import ROLES, Store

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / 'fixtures' / name).read_text())


def bind(template, packet):
    """Bind explicit fixture source references to current immutable evidence IDs."""
    output = copy.deepcopy(template)
    output['input_digest'] = packet['input_digest']
    lookup = {origin['source_id']: row['id'] for row in packet['evidence'] for origin in row['origins']}
    if output['role'] == 'researcher':
        for claim in output['claims']:
            claim['evidence_id'] = lookup[claim.pop('source_id')]
    if output['role'] == 'fact-checker':
        claims = {c['claim_id']: c for c in packet['researcher']['claims']}
        for check in output['checks']:
            original = claims[check['claim_id']]
            check['evidence_id'] = original['evidence_id']
            check['locator'] = original['locator']
    return output


def run(db, directory):
    directory.mkdir(parents=True, exist_ok=True)
    store = Store(db)
    try:
        audit = store.collect(read('sources.json'))
        (directory/'collection.json').write_text(json.dumps(audit, indent=2)+'\n')
        for role in ROLES:
            packet = store.role_input(role)
            output = bind(read(role+'.json'), packet)
            store.submit(output)
            (directory/(role+'-input.json')).write_text(json.dumps(packet, indent=2)+'\n')
            (directory/(role+'-output.json')).write_text(json.dumps(output, indent=2)+'\n')
        (directory/'report.md').write_text(store.report())
        print(json.dumps({'report': str(directory/'report.md'), 'counts': audit['counts'], 'execution': 'synthetic fixture replay; no model execution'}))
    finally:
        store.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='tributary.sqlite')
    parser.add_argument('--output', type=Path, default=Path('output'))
    args = parser.parse_args()
    run(args.db, args.output)
