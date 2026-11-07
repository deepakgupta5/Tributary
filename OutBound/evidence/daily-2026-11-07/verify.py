"""Offline integrity verification of the public recovery evidence; no collection."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from tributary.checkpoint_audit import STAGES, verify
from tributary.source_review import validate, render_owner

folder=Path(__file__).resolve().parent
read=lambda name:json.loads((folder/name).read_text())
proof=read('verification.json');packet=read('source-review-request.json');verdicts=read('desktop-verdicts.json');owner=read('worklist.json');run=read('run.json')
for name,expected in proof['artifact_sha256'].items():
    assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==expected,name
validate(packet,verdicts)
chain=[read('checkpoints/'+packet['id']+'/'+stage+'.json') for stage in STAGES]
verify(packet,verdicts,chain)
assert len(verdicts['verdicts'])==11
assert Counter(r['disposition'] for r in verdicts['verdicts'])==proof['verdict_dispositions']
assert owner['counts']==proof['owner_counts']
assert not owner['cards'] and owner['counts']['outstanding_research']==6
assert len(run['new_accounts'])==len(run['new_signals'])==len(run['changed_signals'])==0
assert render_owner(owner)==(folder/'worklist.md').read_text()
assert all(v.get('owner_decision') is None and v.get('owner_next_step') is None for v in verdicts['verdicts'])
assert all(sum(len(p.get('checking_excerpt','')) for p in group['passages'].values())<=1800 for group in packet['groups'])
print(json.dumps(dict(artifact_hashes='pass',linked_checkpoints='pass',verdicts=11,owner_attention=0,outstanding_research=6,new_accounts=0,new_signal_candidates=0,changed_signal_candidates=0,execution=proof['execution']),sort_keys=True))
