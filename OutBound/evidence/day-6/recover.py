"""Reproduce controlled recovery using copied live state; never alters production.

The HTTP 503 and missed-date bookmark are injected. The recovery request is live.
"""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from tributary.daily import Network, TZ, execute, inventory, read, save


def prove():
    current=read(ROOT/'out/operations-v2/state.json')
    source=next(s for s in inventory() if s['id']=='compass-news')
    copied=deepcopy(current)
    today=datetime.now(TZ).date()
    copied['last_attempt_date']=(today-timedelta(days=2)).isoformat()
    target=ROOT/'out/recovery-proof'
    save(target/'state.json',copied)
    before=deepcopy(copied['checkpoints'][source['id']])
    failed=execute(target,ROOT/'OutBound/evidence/day-6/recovery-failed',retrieve=lambda *_:(503,b'',{}),sources=[source],jobs=1,execution='controlled_failure_injection')
    after=read(target/'state.json')['checkpoints'][source['id']]
    for field in ('raw_sha256','last_success'):
        assert before[field]==after[field]
    recovered=execute(target,ROOT/'OutBound/evidence/day-6/recovery-live',retrieve=Network(),sources=[source],jobs=1,execution='manual_live_recovery')
    outcome=recovered['collection'][0]['outcome']
    assert outcome in {'success','unchanged'},outcome
    assert recovered['counts']['new_signal_candidates']==0
    assert recovered['counts']['changed_signal_candidates']==0
    proof=dict(test='copied real state, injected 503 and simulated missed-date bookmark, followed by a real live request',
        source=source['id'],injected_outcome=failed['collection'][0]['outcome'],successful_checkpoint_preserved_after_failure=True,
        recovery_outcome=outcome,recovery_http=recovered['collection'][0].get('http'),missed_dates_simulated=failed['missed_dates'],
        recovered_counts=recovered['counts'],production_state_modified=False)
    save(ROOT/'OutBound/evidence/day-6/recovery-proof.json',proof)
    print(proof)


if __name__=='__main__': prove()
