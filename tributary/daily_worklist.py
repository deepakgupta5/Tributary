"""Reviewed account worklist. Replays saved supervised reviews; never auto-verifies.

Public build does not open private feedback. Private decisions stay in a local SQLite
journal, and must be requested explicitly for a local, ignored output directory.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('collection-qc', 'researcher', 'skeptic', 'fact-checker')
TIERS = ('act', 'investigate', 'monitor', 'suppress')


def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def review_packet(data, sources, prior, stage):
    return dict(stage=stage,subject_data=data,source_checks=sources,prior_outputs=prior)


def load_evidence(folder):
    data=json.loads((folder/'observations.json').read_text())
    reviews=[json.loads((folder/(stage+'.json')).read_text()) for stage in STAGES]
    sources=json.loads((folder/'source-checks.json').read_text())
    for i,stage in enumerate(('qc','researcher','skeptic','fact_checker')):
        packet=json.loads((folder/'packets'/(stage+'.json')).read_text())
        if packet!=review_packet(data,sources,reviews[:i],stage):
            raise ValueError('Stored role packet differs from current input')
    return data,reviews,sources


def build(data, reviews, sources):
    """Only valid, version-matched full-ledger checks enter the reviewed view."""
    observations={}
    for row in data['observations']:
        old=observations.get(row['id'])
        if old is not None and old != row:
            raise ValueError('Conflicting observation versions: '+row['id'])
        observations[row['id']]=row
    fingerprints={rid:digest(row) for rid,row in observations.items()}
    parent=digest(data)
    prior=[]
    expected_stages=('qc','researcher','skeptic','fact_checker')
    if len(reviews)!=4: raise ValueError('All four review outputs required')
    for stage, review in zip(expected_stages,reviews):
        if (review['stage']!=stage or not review['completed'] or review['subjects']!=fingerprints
                or review['input_hash']!=digest(review_packet(data,sources,prior,stage))):
            raise ValueError('Missing, stale or altered review: '+stage)
        parent=digest(review)
        prior.append(review)
    source_map={s['url']:s for s in sources}
    checks=reviews[-1]['claim_checks']
    if set(checks)!=set(observations): raise ValueError('Full claim ledger not checked')
    for rid,row in observations.items():
        expected={c['id']:c for c in row['claims']}
        actual={c['claim_id']:c for c in checks[rid]}
        if len(actual)!=len(checks[rid]) or set(actual)!=set(expected):
            raise ValueError('Every claim requires exactly one check')
        for cid,claim in expected.items():
            check=actual[cid]
            source=source_map.get(claim['source'],{})
            if (check['status'] not in {'supported_attributed','pending','contradicted','insufficient'}
                    or check['source']!=claim['source'] or check['locator']!=claim['locator']
                    or check['source_sha256']!=source.get('response_sha256')
                    or check['source_sha256']!=row['claim_source_version'][cid]):
                raise ValueError('Claim source or version mismatch: '+rid+'/'+cid)
    context = {c['id']:c for c in data.get('context_claims',[])}
    context_checks = reviews[-1].get('context_checks',{})
    if set(context)!=set(context_checks): raise ValueError('Context claim coverage incomplete')
    for cid,claim in context.items():
        check=context_checks[cid]
        if check!=claim or check['source_sha256']!=source_map.get(check['source'],{}).get('response_sha256'):
            raise ValueError('Context check source/version mismatch')
    pending={r['observation_id'] for r in reviews[-1].get('material_pending',[])}
    cards={}
    for row in data['cards']:
        aid=row['account_id']
        if aid in cards: raise ValueError('Duplicate account card')
        if row['recommended_tier'] not in TIERS: raise ValueError('Invalid tier')
        if len(row['observation_ids'])!=len(set(row['observation_ids'])):
            raise ValueError('Duplicate observation on card')
        evidence=[observations[rid] for rid in row['observation_ids']]
        if any(r['account_id']!=aid for r in evidence): raise ValueError('Wrong-account evidence')
        incomplete=any(c['status']!='supported_attributed' for r in evidence for c in checks[r['id']])
        material=incomplete or bool(pending & set(row['observation_ids']))
        if row['recommended_tier']=='act' and material:
            raise ValueError('Act blocked by incomplete or material pending checks')
        card=deepcopy(row)
        card.update(observations=evidence,review_status='source-faithfulness checked; material link pending' if material else 'source-faithfulness checked',
                    evidence_quality='partial' if material else 'supported_attributed',
                    material_pending=material,scope='Existing account; no new admission or current-registration approval',
                    capacity=dict(consulting_budget='unknown',authority='unknown',willingness='unknown'),
                    business_relevance='unreviewed_private')
        # Excludes retrieval/check timestamps so an unchanged factual rerun does not
        # make a private decision stale; changed facts, dates or reasoning do.
        semantic=[{k:r.get(k) for k in ('id','fact','claims','event_date','event_date_text','publication_date','source_versions')} for r in evidence]
        card['fingerprint']=digest([row,semantic,card['evidence_quality'],card['material_pending']])
        cards[aid]=card
    covered=[rid for c in cards.values() for rid in c['observation_ids']]
    if len(covered)!=len(set(covered)) or set(covered)!=set(observations):
        raise ValueError('Observations must reconcile to exactly one account card')
    result=dict(contract_version=1,as_of=data['as_of'],reviewed_at=data['reviewed_at'],cards=list(cards.values()),
                review_basis='Supervised same-assistant source checks, not independent human verification.',
                surrey_followup=data['surrey_followup'],suppressed_interpretations=data['suppressed_interpretations'],
                limitations=data['limitations'],review_chain_hash=parent)
    result['counts']={tier:sum(c['recommended_tier']==tier for c in cards.values()) for tier in TIERS}
    return result


class Feedback:
    """Append-only owner decisions, separate from evidence review and public data."""
    def __init__(self,path):
        path=Path(path)
        path.parent.mkdir(parents=True,exist_ok=True)
        fresh=not path.exists()
        self.db=sqlite3.connect(path)
        self.db.row_factory=sqlite3.Row
        if fresh: os.chmod(path,0o600)
        self.db.execute('CREATE TABLE IF NOT EXISTS owner_decisions (id INTEGER PRIMARY KEY, account_id TEXT NOT NULL, decision TEXT NOT NULL, reason TEXT NOT NULL, fingerprint TEXT NOT NULL, created_at TEXT NOT NULL)')
        self.db.commit()

    def close(self): self.db.close()

    def latest(self,account_id):
        row=self.db.execute('SELECT * FROM owner_decisions WHERE account_id=? ORDER BY id DESC LIMIT 1',(account_id,)).fetchone()
        return dict(row) if row else None

    def record(self,account_id,decision,reason,fingerprint):
        if decision not in {'investigate','monitor','dismiss'} or not reason.strip() or not fingerprint:
            raise ValueError('Decision, reason and reviewed fingerprint required')
        previous=self.latest(account_id)
        if previous and all(previous[k]==v for k,v in dict(decision=decision,reason=reason,fingerprint=fingerprint).items()):
            return previous
        with self.db:
            self.db.execute('INSERT INTO owner_decisions(account_id,decision,reason,fingerprint,created_at) VALUES(?,?,?,?,?)',
                (account_id,decision,reason,fingerprint,datetime.now(timezone.utc).isoformat()))
        return self.latest(account_id)

    def overlay(self,worklist):
        result=deepcopy(worklist)
        result['private_output']=True
        for card in result['cards']:
            decision=self.latest(card['account_id'])
            card['owner_feedback']=decision
            card['decision_needs_review']=bool(decision and decision['fingerprint']!=card['fingerprint'])
            card['effective_tier']=(dict(investigate='investigate',monitor='monitor',dismiss='suppress')[decision['decision']]
                if decision and not card['decision_needs_review'] else card['recommended_tier'])
        result['counts']={tier:sum(c['effective_tier']==tier for c in result['cards']) for tier in TIERS}
        return result


def render(worklist):
    observations=[r for c in worklist['cards'] for r in c['observations']]
    originals=sum(r['origin']=='day4' for r in observations)
    followups=sum(r['origin']=='day5_followup' for r in observations)
    lines=['# Reviewed daily worklist','',f"Reviewed {worklist['as_of']} (Vancouver). "+worklist['review_basis'],
           '', 'Existing accounts; current identity and eligibility checks remain separate. Budget, authority and willingness are unknown throughout. Outreach is manual. Exact event dates are unknown unless qualified below; dates shown are publication dates. Private feedback stays local.', '',
           ' | '.join(t.title()+': '+str(worklist['counts'][t]) for t in TIERS),'',
           f"Reviewed {originals} Day 4 non-award observations across {len(worklist['cards'])} accounts, plus {followups} follow-ups. Other accounts remain in the prior monitoring ledgers.",'']
    for tier in TIERS:
        lines+=['## '+tier.title(),'']
        cards=sorted((c for c in worklist['cards'] if c.get('effective_tier',c['recommended_tier'])==tier),key=lambda c:c['name'])
        if not cards: lines+=['None.','']
        for c in cards:
            lines += ['### '+c['name'],'',f"Account `{c['account_id']}`. {c['review_status']}.", '']
            for r in c['observations']:
                event=r.get('event_date') or r.get('event_date_text') or 'unknown; reporting period follows the source context'
                pub=r.get('publication_date') or 'unknown'
                date_note = '; event: '+event if r.get('event_date') or r.get('event_date_text') else ''
                lines.append(f"- **{pub}{date_note}:** {r['fact']} [Source]({r['url']})")
            lines += ['', '**Why it may matter, hypothesis:** '+c['why_hypothesis'], '', '**Alternative:** '+c['alternative'], '',
                      '**Unknown:** '+c['unknowns'], '', '**Route:** '+c['route'], '', '**Next step:** '+c['next_step'],'']
            if worklist.get('private_output') and c.get('owner_feedback'):
                f=c['owner_feedback']
                lines+=['**Private owner decision:** '+f['decision']+'. '+f['reason'],
                        'Decision needs re-review after changed evidence.' if c['decision_needs_review'] else 'Decision preserved for unchanged evidence.','']
    lines+=['Suppressed interpretations, not suppressed accounts:','']
    lines+=['- '+x for x in worklist['suppressed_interpretations']]
    lines+=['','## Surrey evidence cutoff','',worklist['surrey_followup']['conclusion'],
            'An October story and recruitment figures recycle the FY2025 report, covering October 1, 2024 to September 30, 2025. They do not update summer or autumn 2026 demand or donations. The Delview partner report adds newer qualitative distribution evidence, with the operator link and exact year visibly pending.',
            '', '## Review limits','']
    lines+=['- '+x for x in worklist['limitations']]
    lines+=['','[Claim checks and skeptic resolutions](fact-checker.json) · [Source retrieval metadata](source-checks.json) · [Full observations and follow-up](observations.json) · [Run and private-feedback instructions](README.md)','']
    return '\n'.join(lines)


def private_destination(path):
    """Prevent writing private views into the tracked/public repository tree."""
    path=Path(path).resolve()
    if path==ROOT or ROOT in path.parents:
        rel=path.relative_to(ROOT)
        result=subprocess.run(['git','check-ignore','--quiet',str(rel/'worklist.json')],cwd=ROOT)
        if result.returncode!=0: raise ValueError('Private output must be outside the repo or in an ignored directory')
    return path


def export(worklist,path):
    path=Path(path)
    if worklist.get('private_output'): path=private_destination(path)
    path.mkdir(parents=True,exist_ok=True)
    for filename,content in [('worklist.json',json.dumps(worklist,indent=2,ensure_ascii=False,sort_keys=True)+'\n'),('worklist.md',render(worklist))]:
        target=path/filename
        temp=target.with_suffix(target.suffix+'.tmp')
        temp.write_text(content);temp.replace(target)
        if worklist.get('private_output'): os.chmod(target,0o600)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    default=ROOT/'OutBound/evidence/day-5'
    build_cli=sub.add_parser('build')
    build_cli.add_argument('--evidence',type=Path,default=default)
    build_cli.add_argument('--out',type=Path,default=ROOT/'out/day5')
    build_cli.add_argument('--private',action='store_true')
    feedback_cli=sub.add_parser('feedback')
    feedback_cli.add_argument('account_id');feedback_cli.add_argument('decision',choices=['investigate','monitor','dismiss'])
    feedback_cli.add_argument('--reason',required=True);feedback_cli.add_argument('--worklist',type=Path,required=True)
    for cli in (build_cli,feedback_cli):
        cli.add_argument('--feedback-db',type=Path,default=Path(os.environ.get('TRIBUTARY_FEEDBACK_DB',ROOT/'out/private/owner-feedback.sqlite')))
    args=parser.parse_args()
    if args.command=='feedback':
        data=json.loads(args.worklist.read_text())
        card=next(c for c in data['cards'] if c['account_id']==args.account_id)
        store=Feedback(args.feedback_db)
        try: store.record(args.account_id,args.decision,args.reason,card['fingerprint'])
        finally: store.close()
        print('Private decision saved. No reason or private content exported.')
    else:
        data=build(*load_evidence(args.evidence))
        if args.private:
            private_destination(args.out)
            store=Feedback(args.feedback_db)
            try: data=store.overlay(data)
            finally: store.close()
        export(data,args.out)
        print(json.dumps(data['counts'],sort_keys=True))


if __name__=='__main__': main()
