"""Grouped desktop source review, version-bound verdicts and owner queue gate.

Python collects originals and validates the structured output. The included desktop
assistant performs the reading/reasoning; no paid inference adapter or fake reviewer.
"""
import argparse
from copy import deepcopy
from datetime import datetime,timezone
from html.parser import HTMLParser
import json
import fcntl
import os
from pathlib import Path
import re

from tributary.daily import ROOT, Network, PATTERNS, canonical, digest, read, save, text_of
from tributary.checkpoint_audit import STAGES, verify

CONTRACT='source-review-v1'
FACTS={'supported_attributed','partly_supported','contradicted','insufficient','inaccessible'}
DISPOSITIONS={'supported_context','unsupported','contradicted','research_required','actionable'}
COMMERCIAL={'owner_investigate','monitor','not_relevant','research_required'}
CONTEXT=r'keeping (?:up|pace)|just enough|expanded|donor support rose|met both|surpassed|improv|successful|not .*declin|no .*shortfall|Dress Down'


def now(): return datetime.now(timezone.utc).isoformat()


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.skip=0;self.depth=0;self.parts=[];self.rows=[]
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style','nav','header','footer'}: self.skip+=1
        if tag in {'p','li','h1','h2','h3'} and not self.skip:
            if self.depth==0:self.parts=[]
            self.depth+=1
    def handle_data(self,value):
        if self.depth and not self.skip:self.parts.append(value)
    def handle_endtag(self,tag):
        if tag in {'script','style','nav','header','footer'}:self.skip=max(0,self.skip-1)
        if tag in {'p','li','h1','h2','h3'} and self.depth and not self.skip:
            self.depth-=1
            if self.depth==0:
                value=' '.join(''.join(self.parts).split())
                if value:self.rows.append(value)


def document(raw,url):
    html=raw.decode('utf8','replace')
    main=re.search(r'<article\b[^>]*>([\s\S]*?)</article>',html,re.I) or re.search(r'<main\b[^>]*>([\s\S]*?)</main>',html,re.I)
    parser=Paragraphs();parser.feed(main[1] if main else html)
    rows=parser.rows
    if not rows:
        rows=[line for line in text_of(main[1] if main else html).splitlines() if len(line)>35]
    if not rows:raise ValueError('No readable original; not a completed source review')
    dates={}
    for field,pattern in {'publication_date':r'(?:article:published_time|datePublished)[\s\S]{0,70}?(\d{4}-\d{2}-\d{2})',
                          'modified_date':r'(?:article:modified_time|dateModified)[\s\S]{0,70}?(\d{4}-\d{2}-\d{2})'}.items():
        match=re.search(pattern,html);dates[field]=match[1] if match else None
    paragraphs={}
    for index,text in enumerate(rows):
        h=digest(' '.join(text.casefold().split()))
        paragraphs['passage:'+h[:20]]=dict(hash=h,index=index+1,text=text)
    version=digest([dates,sorted(p['hash'] for p in paragraphs.values())])
    return dict(url=canonical(url),version=version,paragraphs=paragraphs,**dates)


def storage(state):
    return state.setdefault('source_review',dict(contract=CONTRACT,documents={},verdicts={},history=[],last_reviewed_owner=None))


def scope_for(signal,doc):
    pattern=PATTERNS.get(signal['category'],'(?!)')
    relevant={locator:p['hash'] for locator,p in doc['paragraphs'].items() if re.search(pattern,p['text'],re.I)}
    context={locator:p['hash'] for locator,p in doc['paragraphs'].items() if re.search(CONTEXT,p['text'],re.I)}
    return dict(category=signal['category'],relevant=relevant,context=context,
                publication_date=doc.get('publication_date'),modified_date=None)


def prepare(state,retrieve=None,cache_dir=None):
    """One original check per account+document, never one fetch per flag."""
    store=storage(state);retrieve=retrieve or Network();groups={};requests=[];reused=[];failures=[]
    for sid,signal in sorted(state['signals'].items()):
        key=digest([signal['account_id'],canonical(signal['url'])])[:24]
        groups.setdefault(key,dict(id=key,account_id=signal['account_id'],url=canonical(signal['url']),signals=[]))['signals'].append(signal)
    fetches=0;checked_at=now()
    for key,group in sorted(groups.items()):
        previous=store['documents'].get(key,{})
        try:
            fetches+=1
            code,raw,validators=retrieve(group['url'],previous.get('validators',{}))
            if code==304:
                if not previous.get('version'):raise ValueError('304 without a successful original version')
                doc=deepcopy(previous);doc['checked_at']=checked_at;doc['outcome']='unchanged'
            elif code==200:
                doc=document(raw,group['url']);raw=None
                doc.update(validators=dict(validators,raw_sha256=None),checked_at=checked_at,original_retrieved_at=checked_at,outcome='success')
            else:raise PermissionError('Original inaccessible, HTTP '+str(code))
            doc['available']=True
            if code==200 and cache_dir is not None:
                cache=Path(cache_dir)/key/(doc['version']+'.json')
                save(cache,dict(url=doc['url'],document_version=doc['version'],publication_date=doc.get('publication_date'),modified_date=doc.get('modified_date'),paragraphs=doc['paragraphs']))
                doc['original_cache']=str(cache.resolve())
            if code==200:
                doc['scopes']={s['category']:scope_for(s,doc) for s in group['signals']}
            # Persist only hashes and short necessary checking excerpts, not full pages.
            persisted=deepcopy(doc)
            for p in persisted['paragraphs'].values():p.pop('text',None)
            store['documents'][key]=persisted
            group_out=dict(id=key,account_id=group['account_id'],account_name=state['accounts'][group['account_id']]['name'],url=group['url'],
                           document_version=doc['version'],original_cache=doc.get('original_cache'),publication_date=doc.get('publication_date'),modified_date=doc.get('modified_date'),checked_at=checked_at,flags=[],passages={})
            for signal in group['signals']:
                sid=signal['id'];old=store['verdicts'].get(sid)
                # A 304 retains the previously computed category scopes. With 200,
                # scope hashes concern the relevant passages and counterevidence.
                scope=doc['scopes'].get(signal['category']) if code==304 else scope_for(signal,doc)
                if scope is None:raise ValueError('New category needs readable original after 304')
                scope_hash=digest(scope)
                refs=(old.get('evidence',[])+old.get('contradictory_evidence',[])) if old else []
                cited_unchanged=all(doc['paragraphs'].get(r['locator'],{}).get('hash')==r['hash'] for r in refs)
                if old and old.get('audit_ids') and cited_unchanged and old['scope_hash']==scope_hash and not old.get('invalidated'):
                    rebound=deepcopy(old);rebound.update(candidate_version=signal['version'],last_revalidated_at=checked_at,document_version=doc['version'])
                    if rebound['candidate_version']!=old['candidate_version']:
                        rebound['rebound_from']=old['candidate_version']
                    store['verdicts'][sid]=rebound;signal['review_status']=old['disposition']
                    for task in state['review_tasks'].values():
                        if task['signal_id']==sid and task['status']=='pending':task['status']=old['disposition']
                    reused.append(sid);continue
                if old: old['invalidated']=True
                signal['review_status']='pending_source_review'
                flag=dict(signal_id=sid,candidate_version=signal['version'],category=signal['category'],scope=scope,scope_hash=scope_hash,
                          original_candidate_note=signal['fact'])
                group_out['flags'].append(flag)
                locators=set(scope['relevant'])|set(scope['context'])
                # Include other paragraphs as hashed locators so the reader can cite
                # a corrected observation without being trapped by a wrong keyword.
                for locator,p in doc['paragraphs'].items():
                    item=dict(hash=p['hash'],index=p['index'])
                    if 'text' in p and (locator in locators or len(doc['paragraphs'])<10):
                        item['checking_excerpt']=p['text'][:420]
                    elif p.get('checking_excerpt'):item['checking_excerpt']=p['checking_excerpt']
                    group_out['passages'][locator]=item
            # Bound persisted excerpts. The desktop must inspect the original when
            # the necessary context is missing, and may return unfinished instead.
            remaining=1800
            for p in group_out['passages'].values():
                excerpt=p.get('checking_excerpt','')
                if remaining<=0:p.pop('checking_excerpt',None)
                else:p['checking_excerpt']=excerpt[:remaining];remaining-=len(p['checking_excerpt'])
            for locator,p in group_out['passages'].items():
                if p.get('checking_excerpt'):persisted['paragraphs'][locator]['checking_excerpt']=p['checking_excerpt']
            if group_out['flags']:requests.append(group_out)
        except Exception as exc:
            reason=type(exc).__name__+': '+str(exc)[:250]
            failures.append(dict(group_id=key,account_id=group['account_id'],url=group['url'],reason=reason,signal_ids=[s['id'] for s in group['signals']]))
            # Keep the last successful document/verdict and its original date.
            store.setdefault('unavailable',{})[key]=dict(reason=reason,checked_at=checked_at)
            for signal in group['signals']:signal['review_status']='source_unavailable'
            continue
        store.setdefault('unavailable',{}).pop(key,None)
    packet=dict(contract=CONTRACT,prepared_at=checked_at,groups=requests,reused=reused,source_failures=failures,
                summary=dict(grouped_documents=len(groups),original_fetches=fetches,flags_for_desktop=sum(len(g['flags']) for g in requests),reused_verdicts=len(reused),inaccessible_flags=sum(len(f['signal_ids']) for f in failures)))
    packet['id']=digest({k:v for k,v in packet.items() if k!='prepared_at'})
    return packet


def validate(packet,results):
    if results.get('contract')!=CONTRACT or results.get('packet_id')!=packet['id']:
        raise ValueError('Review packet contract/version mismatch')
    if not results.get('reviewed_at'):raise ValueError('Batch review timestamp required')
    expected={f['signal_id']:(g,f) for g in packet['groups'] for f in g['flags']}
    rows=results.get('verdicts',[])
    if len(rows)!=len({r['signal_id'] for r in rows}) or {r['signal_id'] for r in rows}!=set(expected):
        raise ValueError('Every requested flag needs exactly one disposition')
    for row in rows:
        group,flag=expected[row['signal_id']]
        if row.get('candidate_version')!=flag['candidate_version'] or row.get('document_version')!=group['document_version']:
            raise ValueError('Stale candidate or original document version')
        for field in ('observation','reporting_period','comparison_basis','fact_reason','commercial_reason','next_research_step'):
            if not isinstance(row.get(field),str) or not row[field].strip():raise ValueError('Missing substantive field: '+field)
        if row.get('fact_verdict') not in FACTS or row.get('disposition') not in DISPOSITIONS or row.get('commercial_relevance') not in COMMERCIAL:
            raise ValueError('Invalid factual, flag or commercial verdict')
        if type(row.get('source_checks_complete')) is not bool or row.get('time_status') not in {'current_supported','historical','undated'}:
            raise ValueError('Explicit check completion and time status required')
        if not isinstance(row.get('contradictory_evidence'),list):raise ValueError('Contradictory evidence must be explicit')
        if not row.get('original_read') or not row.get('reviewer') or not row.get('reviewed_at'):
            raise ValueError('Desktop original-reading attestation and reviewer identity required')
        if not all(row.get(stage) for stage in ('researcher_assessment','skeptic_assessment','fact_checker_assessment')):
            raise ValueError('Researcher, skeptic and fact-checker assessments required')
        evidence=row.get('evidence',[])
        if row['fact_verdict']=='supported_attributed' and not evidence:raise ValueError('Supported fact lacks exact source locator')
        for ref in evidence+row['contradictory_evidence']:
            locator=ref.get('locator');p=group['passages'].get(locator,{})
            if ref.get('hash')!=p.get('hash') or not p:raise ValueError('Evidence passage locator/hash mismatch')
            if not ref.get('note'):raise ValueError('Evidence reference needs interpretation')
        if row['commercial_relevance']=='owner_investigate':
            if (row['fact_verdict']!='supported_attributed' or row['disposition']!='actionable' or row.get('time_status')!='current_supported'
                or not row.get('source_checks_complete') or not row.get('owner_decision') or not row.get('owner_next_step')):
                raise ValueError('Owner gate: complete supported current evidence and a commercial decision required')
        elif row['disposition']=='actionable':raise ValueError('Actionable disposition needs an explicit commercial verdict')
    return rows


def apply(state,packet,results,chain=()):
    rows=validate(packet,results);store=storage(state)
    if not rows:return 0
    verify(packet,results,chain)
    for row in rows:
        group,flag=next((g,f) for g in packet['groups'] for f in g['flags'] if f['signal_id']==row['signal_id'])
        current=state['signals'].get(row['signal_id'],{})
        doc=store['documents'].get(group['id'],{})
        if current.get('version')!=row['candidate_version'] or doc.get('version')!=row['document_version']:
            raise ValueError('State changed after desktop reading; reprepare affected claims')
    # Validate the entire batch before applying any verdict.
    for row in rows:
        group,flag=next((g,f) for g in packet['groups'] for f in g['flags'] if f['signal_id']==row['signal_id'])
        ids=[r['execution_id'] for r in chain]
        record=dict(row,scope=flag['scope'],scope_hash=flag['scope_hash'],group_id=group['id'],url=group['url'],invalidated=False,audit_ids=ids)
        old=store['verdicts'].get(row['signal_id'])
        if old and all(old.get(k)==v for k,v in record.items()):continue
        store['history'].append(record);store['verdicts'][row['signal_id']]=record
        state['signals'][row['signal_id']]['review_status']=row['disposition']
        for task in state['review_tasks'].values():
            if task['signal_id']==row['signal_id'] and task['status']=='pending':
                task.update(status=row['disposition'],source_review_id=digest(record))
    store['last_desktop_review_at']=results['reviewed_at']
    store.setdefault('audit_records',{}).update({r['execution_id']:r for r in chain})
    store.setdefault('audit_packets',{})[digest(packet)]=packet
    return len(rows)


def owner_view(state,collection,packet,reviewer_ran=False):
    store=storage(state);eligible={};research=[];history=[]
    unavailable={sid for f in packet.get('source_failures',[]) for sid in f['signal_ids']}
    outstanding=[]
    for sid,signal in state['signals'].items():
        verdict=store['verdicts'].get(sid)
        audit=store.get('audit_records',{})
        ids=verdict.get('audit_ids',[]) if verdict else []
        audited=len(ids)==4 and all(audit.get(i,{}).get('stage')==stage for i,stage in zip(ids,STAGES))
        valid=bool(audited and not verdict.get('invalidated') and sid not in unavailable and verdict['candidate_version']==signal['version'])
        reason='Original source unavailable' if sid in unavailable else 'Desktop review unfinished or evidence changed' if not valid else verdict['fact_reason']
        row=dict(signal_id=sid,account_id=signal['account_id'],url=signal['url'],status=verdict['disposition'] if valid else 'unfinished',reason=reason,
                 reviewed_at=verdict.get('reviewed_at') if verdict else None)
        research.append(row)
        if not valid or verdict['disposition']=='research_required':outstanding.append(row)
        if not valid:continue
        history.append(dict(verdict,account_name=state['accounts'][signal['account_id']]['name']))
        if verdict['disposition']!='actionable' or verdict['commercial_relevance']!='owner_investigate':continue
        aid=signal['account_id'];card=eligible.setdefault(aid,dict(account_id=aid,name=state['accounts'][aid]['name'],recommended_tier='investigate',findings=[],requires_attention=True))
        card['findings'].append(verdict)
    for card in eligible.values():
        card['fingerprint']=digest([(v['signal_id'],v['scope_hash'],v['observation'],v['owner_decision']) for v in card['findings']])
        card['review_status']='reviewed source evidence; commercial judgment reserved for owner'
    failed_sources=[a for a in collection.get('collection',[]) if a['outcome'] in {'failed','blocked','held'}]
    counts=dict(owner_attention_accounts=len(eligible),reviewed_flags=len(history),unfinished_or_research_flags=len(outstanding),
                unsupported_or_contradicted_flags=sum(v['disposition'] in {'unsupported','contradicted'} for v in history),
                source_checks_outstanding=len(failed_sources),outstanding_research=len(outstanding)+len(failed_sources))
    last=store.get('last_reviewed_owner')
    if reviewer_ran or (not packet.get('groups') and not packet.get('source_failures') and history):
        data=dict(as_of=collection['as_of'],collection_run_id=collection['run_id'],collection_status=collection['run_status'],
                  verification='desktop_review_completed' if reviewer_ran else 'unchanged_verdicts_reused',
                  last_reviewed_at=store.get('last_desktop_review_at'),cards=list(eligible.values()),counts=counts,
                  research_queue=research,source_issues=failed_sources,review_history=history,collection_counts=collection.get('counts',{}))
        if reviewer_ran:store['last_reviewed_owner']=deepcopy(data)
    else:
        data=dict(as_of=collection['as_of'],collection_run_id=collection['run_id'],collection_status=collection['run_status'],
                  verification='reviewer_unavailable_or_incomplete',last_reviewed_at=last.get('last_reviewed_at') if last else None,
                  cards=list(eligible.values()),counts=counts,research_queue=research,source_issues=failed_sources,review_history=history,
                  last_reviewed_worklist=deepcopy(last),legacy_reviewed_reference='OutBound/evidence/day-5/worklist.md' if last is None else None,collection_counts=collection.get('counts',{}))
    return data


def render_owner(data):
    n=data['counts'];lines=['# Reviewed owner worklist','',f"Collection: {data['as_of']}, {data['collection_status']}. Review status: **{data['verification']}**.",
        f"Last desktop review: {data.get('last_reviewed_at') or 'not available in this run; see dated previous review'}. Outreach stays manual.",'',
        f"**Owner attention: {n['owner_attention_accounts']} accounts. Outstanding research: {n['outstanding_research']} items** ({n['unfinished_or_research_flags']} claim checks, {n['source_checks_outstanding']} source-access/handling checks).",'',
        'Unsupported interpretations and unfinished checks remain in the internal research queue. These are system research tasks, not requests for commercial judgment.','', '## Act','','None.','','## Investigate','']
    if not data['cards']:lines+=['None. The reviewed batch does not yet support a current commercial decision or investigation step.','']
    for c in data['cards']:
        lines+=['### '+c['name'],'']
        if c.get('owner_feedback'):
            lines += ['Private decision: '+c['owner_feedback']['decision']+'. '+c['owner_feedback']['reason'], 'Decision needs review: '+str(c.get('decision_needs_review')), '']
        for v in c['findings']:
            lines += [v['observation']+' [Source]('+v['url']+').', '[Four checkpoint records](checkpoint-audit.json): '+', '.join(v['audit_ids']), 'Period: '+v['reporting_period']+'.',
                      'Why it may matter, hypothesis: '+v['commercial_reason'], 'Decision: '+v['owner_decision'], 'Next step: '+v['owner_next_step'],'']
    lines+=['## Monitor','',f"{n['reviewed_flags']} flags have recorded source dispositions. Historical/positive context remains in the review ledger; it is not an owner attention request.",'',
            '## Suppress','',f"{n['unsupported_or_contradicted_flags']} unsupported or contradicted interpretations are retained internally with reasons. Accounts are not deleted.",'']
    monitors=[v for v in data['review_history'] if v['disposition']=='supported_context']
    if monitors:
        where=lines.index('## Suppress')
        detail=[]
        for v in monitors:
            detail += ['- **'+v.get('account_name',v['signal_id'])+':** '+v['observation']+' [Source]('+v['url']+'). '+v['reporting_period']+'. '+v['commercial_reason']+' Research next step: '+v['next_research_step'],'']
        lines[where:where]=detail
    if data['verification']=='reviewer_unavailable_or_incomplete':
        lines+=['## Reviewer unavailable / unfinished','','Collection status is current. The last reviewed worklist and its dates are preserved; this run is not freshly verified.',
                '[Last reviewed worklist](last-reviewed-worklist.md), with its original review date. Previous-format baseline: '+str(data.get('legacy_reviewed_reference') or 'saved last-reviewed-worklist.json')+'.','']
    lines+=['[Nine-flag dispositions](dispositions.md) · [Internal research queue](research-queue.json) · [Structured owner worklist](owner-worklist.json)','']
    return '\n'.join(lines)


def publish(state,collection,packet,directory,reviewer_ran=False):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    data=owner_view(state,collection,packet,reviewer_ran)
    audit_store=storage(state)
    save(directory/'checkpoint-audit.json',dict(records=audit_store.get('audit_records',{}),packets=audit_store.get('audit_packets',{})))
    save(directory/'owner-worklist.json',data)
    (directory/'owner-worklist.md').write_text(render_owner(data))
    # Separate internal queue, including closed unsupported flags and live access gaps.
    save(directory/'research-queue.json',dict(flags=data['research_queue'],source_checks=data['source_issues']))
    if data.get('last_reviewed_worklist'):
        save(directory/'last-reviewed-worklist.json',data['last_reviewed_worklist'])
        (directory/'last-reviewed-worklist.md').write_text(render_owner(data['last_reviewed_worklist']))
    lines=['# Source-review dispositions','','| Flag | Account | Fact verdict | Flag disposition | Period / comparison | Commercial treatment |','|---|---|---|---|---|---|']
    for sid,signal in sorted(state['signals'].items()):
        v=storage(state)['verdicts'].get(sid,{})
        if v.get('invalidated'):v=dict(v,fact_verdict='reopened: evidence changed',disposition='unfinished')
        lines.append(f"| `{sid}` | {state['accounts'][signal['account_id']]['name']} | {v.get('fact_verdict','unfinished')} | {v.get('disposition','unfinished')} | {v.get('reporting_period','unknown')}; {v.get('comparison_basis','unchecked')} | {v.get('commercial_relevance','research_required')} |")
        if v:lines+=[]
    lines+=['']
    for sid,v in sorted(storage(state)['verdicts'].items()):
        lines+=['## '+sid,'',v['observation'], 'Source: '+v['url'], 'Factual verdict: '+v['fact_verdict']+'. '+v['fact_reason'],
                'Commercial verdict: '+v['commercial_relevance']+'. '+v['commercial_reason'], 'System research step: '+v['next_research_step'],'']
    (directory/'dispositions.md').write_text('\n'.join(lines))
    return data


def private_owner(directory,data,feedback_db):
    from tributary.daily_worklist import Feedback, private_destination
    if not Path(feedback_db).exists():return
    store=Feedback(feedback_db)
    try:
        private=store.overlay(data);private['queue_counts']=private['counts'];private['counts']=deepcopy(data['counts'])
    finally:store.close()
    dest=private_destination(Path(directory)/'private-latest');dest.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(dest,0o700)
    save(dest/'worklist.json',private);(dest/'worklist.md').write_text(render_owner(private))
    for name in ('worklist.json','worklist.md'):os.chmod(dest/name,0o600)


def _main(args):
    out=args.out or args.state_dir/'latest';state=read(args.state_dir/'state.json')
    collection=read(out/'collection-worklist.json') if (out/'collection-worklist.json').exists() else read(out/'worklist.json')
    packet_path=out/'source-review-request.json'
    if args.action=='prepare':
        packet=prepare(state,cache_dir=args.state_dir/'source-cache');save(packet_path,packet);save(args.state_dir/'state.json',state)
        print(json.dumps(packet['summary'],sort_keys=True));return
    packet=read(packet_path)
    if args.action=='complete':
        if not args.verdicts:raise ValueError('--verdicts required')
        chain=[read(out/'checkpoints'/packet['id']/(s+'.json')) for s in STAGES] if packet['groups'] else []
        count=apply(state,packet,read(args.verdicts),chain)
        data=publish(state,collection,packet,out,bool(count))
    else:
        count=0;data=publish(state,collection,packet,out,False)
    save(args.state_dir/'state.json',state)
    settings=read(ROOT/'out/schedule/config.json') if (ROOT/'out/schedule/config.json').exists() else {}
    feedback=os.environ.get('TRIBUTARY_FEEDBACK_DB') or settings.get('feedback_db')
    if feedback:private_owner(args.state_dir,data,feedback)
    # The owner view is the default publication; raw flags keep their own file.
    save(out/'worklist.json',data);(out/'worklist.md').write_text(render_owner(data))
    print(json.dumps(dict(verdicts_applied=count,**data['counts']),sort_keys=True))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['prepare','complete','publish'])
    p.add_argument('--state-dir',type=Path,default=ROOT/'out/daily')
    p.add_argument('--out',type=Path);p.add_argument('--verdicts',type=Path)
    args=p.parse_args();args.state_dir.mkdir(parents=True,exist_ok=True)
    with (args.state_dir/'runner.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);_main(args)

if __name__=='__main__':main()
