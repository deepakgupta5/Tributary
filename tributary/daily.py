"""Free local daily collection, review handoff and dated public/private worklists.

python3 -m tributary.daily --state-dir out/daily
No model/API calls, automatic review, login, outreach or automatic Git push.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import fcntl
import hashlib
from html.entities import name2codepoint
import threading
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo

from tributary import collect
from tributary.daily_worklist import Feedback, build as reviewed_build, load_evidence, private_destination
from tributary.resolution import normalize

ROOT=Path(__file__).resolve().parents[1]
TZ=ZoneInfo('America/Vancouver')
VERSION='day6-v2'
PATTERNS={
 'fundraising_pressure':r'(?:donations?|fundraising|funding)\b.{0,70}\b(?:declin\w*|shortfall|drop\w*|fell|down|falling|struggl\w*)|(?:declin\w*|shortfall)\b.{0,50}\b(?:donations?|fundraising)|donor retention',
 'campaign_performance':r'(?:campaign|food frenzy|fundrais\w*|matching)\b.{0,100}\b(?:raised|results?|goal|target|match|total)|(?:raised|surpassed|exceeded)\b.{0,70}\b(?:goal|campaign|fundrais\w*)',
 'financial_pressure':r'(?:loss|lost|cut\w*)\b.{0,70}\b(?:funding|revenue)|(?:funding|revenue)\b.{0,60}\b(?:loss|lost|cut\w*)|(?:operating|budget|financial)\s+(?:deficit|shortfall|gap)|reserves?\b.{0,40}\b(?:declin\w*|deplet\w*)',
 'operational_strain':r'(?:demand|clients?|visits?|usage)\b.{0,70}\b(?:increas\w*|ris\w*|grew|growth|record|surge)|(?:increas\w*|ris\w*|growing|record|surge)\b.{0,60}\b(?:demand|clients?|visits?|usage)|staff\w*\s+(?:shortage|gap)|distribution\s+(?:capacity|depot)|(?:new|inaugural)\b.{0,35}\b(?:depot|distribution)',
}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+'\n');temp.replace(path)


def read(path): return json.loads(Path(path).read_text())


def canonical(url):
    u=urlsplit(url)
    return urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path.rstrip('/') or '/',u.query,''))


class Text(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in {'script','style','nav','footer','header'}: self.skip+=1
        if tag in {'p','div','h1','h2','li','br'} and not self.skip: self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in {'script','style','nav','footer','header'}: self.skip=max(0,self.skip-1)
        if tag in {'p','div','h1','h2','li'} and not self.skip: self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)


def text_of(raw):
    parser=Text();parser.feed(raw if isinstance(raw,str) else raw.decode('utf8','replace'))
    return '\n'.join(' '.join(line.split()) for line in ''.join(parser.parts).splitlines() if line.strip())


def alias_map(accounts):
    result={}
    for aid,a in accounts.items():
        for n in [a['name'],*a.get('aliases',[])]: result[normalize(n)]=aid
    for alias,aid in {'Surrey Food Bank':'132168162RR0001','Food Lifeline':'911090450','Clark County Food Bank':'911307564','Compass Housing Alliance':'WA:compass housing alliance'}.items():
        if aid in accounts: result[normalize(alias)]=aid
    return result


def inventory():
    sources=[dict(s,kind='discovery') for s in read(ROOT/'OutBound/data/day2-sources.json')]
    sources+=read(ROOT/'OutBound/data/day6-sources.json')
    # Day 4 provides inspected candidate pages for all 39 known accounts. Registry
    # and giving-directory pages are checks, not claims of comprehensive news cover.
    pressure=read(ROOT/'OutBound/evidence/day-4/pressure-inputs.json')
    for c in pressure['coverage']:
        sources.append(dict(id='account-'+digest(c['account_id'])[:12],kind='page',url=c['selected_page'],account_id=c['account_id'],publisher='Selected account source',geography='BC/WA',
            hold='GVFB first-party content remains held.' if c['account_id']=='107449787RR0001' and 'foodbank.bc.ca' in c['selected_page'] else None))
    # Recheck every exact source used by the reviewed Day 5 cards, including two
    # older Surrey articles; they are historical context, never fresh by retrieval.
    for s in read(ROOT/'OutBound/evidence/day-5/source-checks.json'):
        if s['url'].endswith('.pdf'): continue  # annual PDF is historical context
        existing=next((x for x in sources if canonical(x['url'])==canonical(s['url'])),None)
        if existing: continue
        aid=next((r['account_id'] for r in read(ROOT/'OutBound/evidence/day-5/observations.json')['observations'] if canonical(r['url'])==canonical(s['url'])),'132168162RR0001')
        sources.append(dict(id='review-source-'+digest(s['url'])[:12],kind='page',url=s['url'],account_id=aid,publisher='Reviewed source',geography='BC/WA'))
    # Several accounts share a page; fetch once and retain every account scope.
    unique={}
    for s in sources:
        key=canonical(s['url'])
        if key in unique:
            ids=set(unique[key].get('account_ids',[]))|set(s.get('account_ids',[]))
            if s.get('account_id'): ids.add(s['account_id'])
            unique[key]['account_ids']=sorted(ids)
        else:
            s['account_ids']=[s['account_id']] if s.get('account_id') else []
            s['handling']='Bounded free public endpoint; transient processing, retained URLs/dates/hashes and organization-level candidate notes only. No whole source content retained.'
            unique[key]=s
    return list(unique.values())


def initial_state():
    d5=reviewed_build(*load_evidence(ROOT/'OutBound/evidence/day-5'))
    # Use the Day 3 resolved account IDs rather than duplicating aliases from the
    # collection ledger under old provisional keys.
    from tributary.signals import build as resolved
    accounts,_,_,_=resolved(read(ROOT/'OutBound/evidence/day-4/repeat-state.json'),read(ROOT/'OutBound/evidence/day-3/worklist.json'),read(ROOT/'OutBound/evidence/day-4/pilot-baseline.json'))
    seeded={sid:dict(value.get('checkpoint',{}),raw_sha256=value.get('checkpoint',{}).get('sha256'),last_success=value.get('last_success')) for sid,value in read(ROOT/'OutBound/evidence/day-4/repeat-state.json')['sources'].items()}
    return dict(version=VERSION,accounts=accounts,collection=read(ROOT/'OutBound/evidence/day-4/repeat-state.json'),
        checkpoints=seeded,signals={},review_tasks={},reviewed_cards=d5['cards'],runs=[],last_complete_date=None,
        baseline_sources={canonical(s['url']):s for s in read(ROOT/'OutBound/evidence/day-5/source-checks.json')},
        # A matching reviewed source/category is carry-forward, not a new finding.
        baseline_observations=read(ROOT/'OutBound/evidence/day-5/observations.json')['observations'])


def fetched(source,checkpoint,retrieve):
    if source.get('hold'): return dict(outcome='held',reason=source['hold'])
    try:
        code,raw,validators=retrieve(source['url'],checkpoint)
        if code==304:
            if not checkpoint.get('raw_sha256') and not checkpoint.get('sha256'): raise ValueError('304 without prior checkpoint')
            return dict(outcome='unchanged',http=code,validators=validators,raw=None)
        if code in {401,403,429}: return dict(outcome='blocked',http=code,reason='HTTP '+str(code))
        if code!=200: raise ValueError('HTTP '+str(code))
        return dict(outcome='fetched',http=code,raw=raw,validators=validators,raw_sha256=hashlib.sha256(raw).hexdigest())
    except Exception as exc:
        # Never log response bodies or private inputs on failure.
        return dict(outcome='blocked' if isinstance(exc,PermissionError) else 'failed',reason=type(exc).__name__+': '+str(exc)[:300])


def documents(source,raw):
    if source['kind']=='feed':
        # Some publisher RSS contains HTML named entities outside CDATA.
        xml=raw.decode('utf8','replace')
        xml=re.sub(r'&([A-Za-z][A-Za-z0-9]+);',lambda m:m[0] if m[1] in {'amp','lt','gt','quot','apos'} else '&#'+str(name2codepoint[m[1]])+';' if m[1] in name2codepoint else m[0],xml)
        tree=ET.fromstring(xml)
        entries=tree.findall('.//item')
        if not entries: entries=tree.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries and tree.tag not in {'rss','{http://www.w3.org/2005/Atom}feed'}:
            raise ValueError('Not a recognized feed; source history unavailable')
        for e in entries[:50]:
            link=e.findtext('link')
            if not link:
                node=e.find('{http://www.w3.org/2005/Atom}link');link=node.get('href') if node is not None else None
            title=e.findtext('title') or e.findtext('{http://www.w3.org/2005/Atom}title') or ''
            pub=e.findtext('pubDate') or e.findtext('{http://www.w3.org/2005/Atom}published')
            if not link: continue
            if pub:
                try: pub=parsedate_to_datetime(pub).date().isoformat()
                except (ValueError,TypeError): pub=pub[:10];date.fromisoformat(pub)
            summary=' '.join(e.findtext(k,'') for k in ('description','{http://purl.org/rss/1.0/modules/content/}encoded','{http://www.w3.org/2005/Atom}summary'))
            yield dict(url=canonical(link),publication_date=pub,text=text_of(title+'\n'+summary),locator='RSS/Atom item '+link)
    else:
        html=raw.decode('utf8','replace')
        match=re.search(r'(?:article:published_time|datePublished)[\s\S]{0,60}?(\d{4}-\d{2}-\d{2})',html)
        main=re.search(r'<article\b[^>]*>([\s\S]*?)</article>',html,re.I) or re.search(r'<main\b[^>]*>([\s\S]*?)</main>',html,re.I)
        text=text_of(main[1] if main else html)
        if len(text)<40: raise ValueError('No usable text; not a no-findings result')
        yield dict(url=canonical(source['url']),publication_date=match[1] if match else None,text=text,locator='Published page, matched category wording')


def candidates(source,raw,accounts,today):
    aliases=alias_map(accounts)
    for doc in documents(source,raw):
        if doc['publication_date'] and not (today-timedelta(days=366)<=date.fromisoformat(doc['publication_date'])<=today): continue
        scopes=source['account_ids'] if source['kind']=='page' or source.get('account_id') else []
        if not scopes:
            normalized=' '+normalize(doc['text'])+' '
            scopes=sorted({aid for alias,aid in aliases.items() if ' '+alias+' ' in normalized})
        for category,pattern in PATTERNS.items():
            hits=[]
            for line in doc['text'].splitlines():
                if re.search(pattern,line,re.I):
                    # Keep hashes of relevant text, not incidental personal data.
                    hits.append(digest(' '.join(line.casefold().split())))
            if not hits: continue
            for aid in scopes:
                yield dict(id='signal-'+digest([aid,doc['url'],category])[:24],account_id=aid,category=category,url=doc['url'],
                    publication_date=doc['publication_date'],event_date=None,locator=doc['locator'],
                    fact='Publication contains wording potentially relevant to '+category.replace('_',' ')+'. Original-source review is required before promoting a substantive claim.',
                    evidence_fingerprint=digest(sorted(set(hits))),rule_version=VERSION,
                    review_status='pending',evidence_quality='unreviewed',first_seen=None,source_id=source['id'])


def historical_match(state,candidate):
    category_map={'campaign_comparison':'campaign_performance','demand_change':'operational_strain','funding_loss':'financial_pressure'}
    return any(r['account_id']==candidate['account_id'] and canonical(r['url'])==candidate['url'] and True for r in state['baseline_observations'])


def run(state, sources, retrieve=collect.fetch, at=None, checkpoint=None, execution='manual_live', jobs=6):
    at=at or datetime.now(timezone.utc);today=at.astimezone(TZ).date();stamp=at.isoformat()
    run_id=stamp.replace(':','-')
    # Resume the same interrupted invocation without erasing successful attempts.
    active=state.get('active_run')
    if active:
        log=active;run_id=log['id']
    else:
        prior=state.get('last_attempt_date') or state.get('last_complete_date')
        missed=[]
        if prior:
            cursor=date.fromisoformat(prior)+timedelta(days=1)
            while cursor<today: missed.append(cursor.isoformat());cursor+=timedelta(days=1)
        log=dict(id=run_id,started_at=stamp,local_date=today.isoformat(),execution=execution,status='running',attempts=[],
            new_accounts=[],new_signals=[],changed_signals=[],historical_first_observed=[],source_rechecks=[],missed_dates=missed,
            coverage_gap='Feeds/indexes are bounded. Catch-up checks last successful checkpoints but cannot guarantee every missed publication is recoverable.')
        state['active_run']=log
        if checkpoint: checkpoint(state)
    finished={a['source'] for a in log['attempts'] if a['outcome'] not in {'failed','blocked','held'}}
    pending=[s for s in sources if s['id'] not in finished]
    # Independent fetches run concurrently. All state mutations and durable commits
    # happen in this thread, one source at a time, under the CLI single-writer lock.
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures={pool.submit(fetched,s,state['checkpoints'].get(s['id'],{}),retrieve):s for s in pending}
        for future in as_completed(futures):
            source=futures[future];sid=source['id'];result=future.result();raw=result.pop('raw',None)
            attempt=dict(source=sid,url=source['url'],at=stamp,**result)
            cp=state['checkpoints'].setdefault(sid,{})
            cp['last_attempt']=stamp
            if result['outcome'] in {'failed','blocked','held'}:
                log['attempts'].append(attempt)
                if checkpoint: checkpoint(state)
                continue
            try:
                if source['kind']=='discovery':
                    # Existing collector keeps its successful validators/checkpoints.
                    prior_accounts=set(state['collection']['accounts'])
                    collect.run(state['collection'],[source],retrieve=lambda *_:(result.get('http',200),raw or b'',result.get('validators',{})))
                    legacy=state['collection']['runs'][-1]['attempts'][0]
                    if legacy['outcome'] in {'failed','blocked'}: raise ValueError(legacy.get('reason','Discovery parse failed'))
                    attempt['outcome']=legacy['outcome'];attempt['discovery_items_added']=len(legacy['additions'])
                    for aid in set(state['collection']['accounts'])-prior_accounts:
                        name=state['collection']['accounts'][aid]
                        if aid not in state['accounts']:
                            state['accounts'][aid]=dict(name=name,question='Resolve identity and eligibility; registry listing alone is not a signal.',events=[])
                            log['new_accounts'].append(aid)
                    # Resolve known collection aliases without auto-merging new names.
                elif result['outcome']=='fetched':
                    proposed=list(candidates(source,raw,state['accounts'],today))
                    fingerprint=digest(sorted((c['id'],c['evidence_fingerprint'],c['publication_date']) for c in proposed))
                    attempt['outcome']='unchanged' if cp.get('semantic_sha256')==fingerprint else 'success'
                    attempt['candidate_count']=len(proposed)
                    for c in proposed:
                        cid=c['id'];old=state['signals'].get(cid)
                        source_version=digest({k:v for k,v in c.items() if k not in {'first_seen','source_id'}})
                        evidence=deepcopy(old.get('evidence_by_source',{})) if old else {}
                        previous_source=evidence.get(sid)
                        if previous_source==source_version:
                            old['last_seen']=stamp
                            old.pop('missing_from_latest',None)
                            continue
                        historical=historical_match(state,c)
                        if historical and not old and result.get('raw_sha256')==state['baseline_sources'].get(canonical(c['url']),{}).get('response_sha256'):
                            continue
                        evidence[sid]=source_version
                        version=digest(evidence)
                        c.update(first_seen=old['first_seen'] if old else stamp,last_seen=stamp,version=version,
                                 evidence_by_source=evidence,
                                 prior_versions=old.get('prior_versions',[])+[old['version']] if old else [],
                                 baseline_replay=historical)
                        state['signals'][cid]=c
                        if old and previous_source and previous_source!=source_version:
                            if cid not in log['new_signals']: log['changed_signals'].append(cid)
                        elif historical:
                            log['source_rechecks'].append(cid)
                        elif not old:
                            log['new_signals'].append(cid)
                            if not c['publication_date'] or (today-date.fromisoformat(c['publication_date'])).days>183:
                                log['historical_first_observed'].append(cid)
                        # One current pending review per event version; older review
                        # tasks stay in the audit as superseded, not duplicate work.
                        for task in state['review_tasks'].values():
                            if task['signal_id']==cid and task['status']=='pending': task['status']='superseded'
                        task_id=cid+'/'+version
                        state['review_tasks'].setdefault(task_id,dict(id=task_id,signal_id=cid,version=version,account_id=c['account_id'],status='pending',reason='Changed or newly observed evidence requires researcher, skeptic and fact-checker review; never auto-approved.',created_at=stamp))
                    # A disappearing old candidate is a material recheck, not proof
                    # the underlying need resolved. Keep history and reopen review.
                    visible={c['id'] for c in proposed}
                    for cid,c in state['signals'].items():
                        if sid in c.get('evidence_by_source',{}) and cid not in visible and not c.get('missing_from_latest'):
                            c['missing_from_latest']=True
                            state['review_tasks'].setdefault(cid+'/missing',dict(id=cid+'/missing',signal_id=cid,account_id=c['account_id'],version=c['version'],status='pending',reason='Prior observation no longer found in this bounded source view; not proof of resolution.',created_at=stamp))
                            log['source_rechecks'].append(cid)
                    cp['semantic_sha256']=fingerprint
                else:
                    attempt['outcome']='unchanged'
                cp.update(last_success=stamp,raw_sha256=result.get('raw_sha256',cp.get('raw_sha256')),
                          **result.get('validators',{}))
            except Exception as exc:
                attempt.update(outcome='failed',reason=type(exc).__name__+': '+str(exc)[:250])
            finally:
                raw=None
            log['attempts'].append(attempt)
            if checkpoint: checkpoint(state)
    for key in ('new_accounts','new_signals','changed_signals','historical_first_observed','source_rechecks'):
        log[key]=sorted(set(log[key]))
    log['changed_signals']=[cid for cid in log['changed_signals'] if cid not in log['new_signals']]
    log['attempts'].sort(key=lambda a:a['source'])
    log['ended_at']=datetime.now(timezone.utc).isoformat()
    log['status']='partial' if any(a['outcome'] in {'failed','blocked'} for a in log['attempts']) else 'complete'
    state['last_attempt_date']=today.isoformat()
    if log['status']=='complete': state['last_complete_date']=today.isoformat()
    state['runs'].append(deepcopy(log));state.pop('active_run',None)
    if checkpoint: checkpoint(state)
    return log


def worklist(state,log):
    attempts={canonical(a['url']):a for a in log['attempts']}
    cards={}
    for original in state['reviewed_cards']:
        c=deepcopy(original);aid=c['account_id']
        sources={canonical(o['url']) for o in c['observations']}
        unchanged=all(attempts.get(url,{}).get('outcome') in {'success','unchanged'} and
                      state['checkpoints'].get(attempts[url]['source'],{}).get('raw_sha256')==state['baseline_sources'].get(url,{}).get('response_sha256') for url in sources)
        c.update(live_signals=[],carry_forward=True,live_check='unchanged reviewed evidence' if unchanged else 'source recheck or changed document; review pending',
                 review_status=c['review_status'] if unchanged else 'prior Day 5 facts carried forward; current source review pending',
                 material_pending=c['material_pending'] or not unchanged)
        if not unchanged: c['fingerprint']=digest([original['fingerprint'],'recheck_pending',[(u,state['checkpoints'].get(attempts.get(u,{}).get('source'),{}).get('raw_sha256'),attempts.get(u,{}).get('outcome') in {'failed','blocked'}) for u in sorted(sources)]])
        cards[aid]=c
    for c in state['signals'].values():
        aid=c['account_id']
        if aid not in cards:
            cards[aid]=dict(account_id=aid,name=state['accounts'][aid]['name'],recommended_tier='investigate' if c.get('publication_date') and (date.fromisoformat(log['local_date'])-date.fromisoformat(c['publication_date'])).days<=183 else 'monitor',observations=[],live_signals=[],carry_forward=False,
                why_hypothesis='Candidate wording may concern operating or fundraising work; relevance is unassessed.',alternative='Routine or positive activity may explain the publication.',
                unknowns='Factual accuracy, current status, relevance, identity/eligibility where unresolved, budget, authority and willingness.',
                route='None verified.',next_step='Review the original source and decide whether the candidate supports a factual observation.',material_pending=True,review_status='pending',fingerprint='')
        cards[aid]['live_signals'].append(c)
    for aid in log['new_accounts']:
        if aid not in cards:
            cards[aid]=dict(account_id=aid,name=state['accounts'][aid]['name'],recommended_tier='monitor',observations=[],live_signals=[],carry_forward=False,
                why_hypothesis='New candidate account; no service-relevance signal established.',alternative='Registry evidence alone supplies identity context.',unknowns='Eligibility and current need.',
                route='None verified.',next_step='Resolve identity and scope before looking for a current non-award signal.',material_pending=True,review_status='identity review pending',fingerprint=digest([aid,'identity_pending']))
    for aid,c in cards.items():
        signals=sorted(c['live_signals'],key=lambda s:s['id'])
        if signals:
            c['fingerprint']=digest([c['fingerprint'],[(s['id'],s['version'],s.get('missing_from_latest',False)) for s in signals]])
            c['review_status']='pending new or changed evidence review; historical facts remain separately labelled'
        c['requires_attention']=bool(c['material_pending'] or signals or aid in log['new_accounts'])
    return dict(as_of=log['local_date'],run_id=log['id'],execution=log['execution'],run_status=log['status'],cards=sorted(cards.values(),key=lambda c:c['name'].casefold()),
        counts=dict(new_accounts=len(log['new_accounts']),new_signal_candidates=len(log['new_signals']),changed_signal_candidates=len(log['changed_signals']),
            historical_first_observed=len(log['historical_first_observed']),historical_source_rechecks=len(set(log['source_rechecks'])),
            cards_requiring_attention=sum(c['requires_attention'] for c in cards.values()),unique_cards=len(cards),pending_review_tasks=sum(t['status']=='pending' for t in state['review_tasks'].values())),
        collection=log['attempts'],missed_dates=log['missed_dates'],coverage_gap=log['coverage_gap'],outreach='manual')


def render(data):
    n=data['counts']
    lines=['# Live daily worklist','',f"{data['as_of']} (Vancouver). Execution: {data['execution']}; status: {data['run_status']}.", '',
        f"New accounts: **{n['new_accounts']}**. New signal candidates: **{n['new_signal_candidates']}**. Changed signal candidates: **{n['changed_signal_candidates']}**. Cards requiring attention: **{n['cards_requiring_attention']}**. Unique cards: {n['unique_cards']}.",'',
        f"Newly observed older/undated candidates: {n['historical_first_observed']}. Historical-source rechecks in this run: {n['historical_source_rechecks']}. Pending review tasks: {n['pending_review_tasks']}.",'',
        'New/changed counts describe candidates, not verified needs or buying intent. Source review remains supervised. Old observations keep their original publication dates; retrieval today does not make them new developments. Outreach is manual. Public output excludes private decisions.','',
        '## Review queue','']
    for tier in ('act','investigate','monitor','suppress'):
        lines+=['### '+tier.title(),'']
        cards=[c for c in data['cards'] if c.get('effective_tier',c['recommended_tier'])==tier]
        if not cards: lines+=['None.','']
        for c in cards:
            lines+=['#### '+c['name'],'',f"`{c['account_id']}`. Review: **{c['review_status']}**. Attention: {'yes' if c['requires_attention'] else 'no'}.",'']
            for o in c['observations']:
                lines.append(f"- Historical carry-forward, published {o['publication_date'] or 'unknown'}: {o['fact']} [Source]({o['url']})")
            for s in c['live_signals']:
                lines.append(f"- **Pending {s['category']}**, publication {s['publication_date'] or 'unknown'}, event date unknown. {s['fact']} [Source]({s['url']}). First seen {s['first_seen']}; {'historical baseline recheck' if s['baseline_replay'] else 'candidate observation'}.")
            lines+=['','Possible relevance, hypothesis: '+c['why_hypothesis'],'','Alternative: '+c['alternative'],'','Unknown: '+c['unknowns'],'','Route: '+c['route'],'','Next step: '+c['next_step'],'']
            if data.get('private_output') and c.get('owner_feedback'):
                f=c['owner_feedback'];lines+=['Private decision: '+f['decision']+'. '+f['reason'], 'Re-review required.' if c['decision_needs_review'] else 'Decision preserved for unchanged evidence.','']
    lines+=['## Collection outcomes','','| Source | Outcome | HTTP | Last attempt (UTC) |','|---|---|---:|---|']
    for a in data['collection']: lines.append(f"| {a['source']} | {a['outcome']} | {a.get('http','')} | {a['at']} |")
    lines+=['','Missed dates: '+(', '.join(data['missed_dates']) or 'none identified from the saved daily checkpoint')+'.',data['coverage_gap'],'',
        'Failed/blocked sources retain prior successful checkpoints. Unchanged means a successful no-change check, not a failed fetch. The selected source set spans BC/WA and all four non-award categories; giving-directory and register pages are not comprehensive news coverage. GVFB first-party hold remains active. No nationwide completeness claim.','',
        '[Run record](run.json) · [Pending claims for supervised review](review-queue.json)','']
    return '\n'.join(lines)



class Network:
    """Respect per-origin robots; HTTP failures never imply permission or no change."""
    def __init__(self):
        self.robots={};self.lock=threading.Lock()
    def __call__(self,url,checkpoint):
        parsed=urlsplit(url);origin=parsed.scheme+'://'+parsed.netloc
        with self.lock:
            if origin not in self.robots:
                code,raw,_=collect.fetch(origin+'/robots.txt',{})
                if code==200:
                    parser=RobotFileParser();parser.parse(raw.decode('utf8','replace').splitlines());self.robots[origin]=parser
                elif code in {404,410}: self.robots[origin]=None
                else: raise PermissionError('robots.txt unavailable, HTTP '+str(code))
            parser=self.robots[origin]
        if parser is not None and not parser.can_fetch('TributaryResearch',url):
            raise PermissionError('robots.txt disallows this endpoint')
        return collect.fetch(url,checkpoint)


def execute(directory,out,feedback_db=None,retrieve=None,at=None,sources=None,execution='manual_live',jobs=6,reviewer=None):
    upstream=retrieve or Network()
    responses={}
    def retrieve(url,checkpoint):
        key=canonical(url)
        if key not in responses:responses[key]=upstream(url,checkpoint)
        return responses[key]
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    path=directory/'state.json'
    with (directory/'runner.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        state=read(path) if path.exists() else initial_state()
        if state.get('version')!=VERSION:
            raise ValueError('Runtime state version differs; preserve it and migrate explicitly before collecting')
        if execution=='scheduled_local' and not scheduled_due(state,at or datetime.now(timezone.utc)):
            return dict(skipped=True,reason='Before daily window or a collection attempt already completed today; no scheduled collection executed.')
        log=run(state,sources or inventory(),retrieve,at,lambda s:save(path,s),execution,jobs)
        data=worklist(state,log)
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        # Raw collection is diagnostic, never the owner publication.
        save(out/'collection-worklist.json',data);(out/'collection-worklist.md').write_text(render(data))
        from tributary.source_review import prepare, apply, publish, render_owner
        packet=prepare(state,retrieve,cache_dir=directory/'source-cache')
        save(out/'source-review-request.json',packet)
        reviewed=False
        if reviewer and packet['groups']:
            try:
                apply(state,packet,reviewer(packet));reviewed=True
            except Exception as exc:
                save(out/'reviewer-error.json',dict(error=type(exc).__name__+': '+str(exc)))
        owner=publish(state,data,packet,out,reviewed)
        save(path,state)
        save(out/'worklist.json',owner);(out/'worklist.md').write_text(render_owner(owner))
        data['owner_counts']=owner['counts'];data['verification']=owner['verification']
        save(out/'run.json',log);save(out/'review-queue.json',sorted(state['review_tasks'].values(),key=lambda t:t['id']))
        if feedback_db and Path(feedback_db).exists():
            store=Feedback(feedback_db)
            try:
                private=store.overlay(owner)
                private['queue_counts']=private['counts']
                private['counts']=deepcopy(owner['counts'])
            finally: store.close()
            dest=private_destination(directory/'private-latest');dest.mkdir(mode=0o700,exist_ok=True)
            os.chmod(dest,0o700)
            save(dest/'worklist.json',private);(dest/'worklist.md').write_text(render_owner(private))
            for name in ('worklist.json','worklist.md'): os.chmod(dest/name,0o600)
        return data


def scheduled_due(state,at,hour=8):
    local=at.astimezone(TZ)
    if state.get('active_run'): return True
    return local.hour>=hour and state.get('last_attempt_date')!=local.date().isoformat()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state-dir',type=Path,default=ROOT/'out/daily')
    p.add_argument('--out',type=Path)
    p.add_argument('--feedback-db',type=Path,default=Path(os.environ.get('TRIBUTARY_FEEDBACK_DB',ROOT/'out/private/owner-feedback.sqlite')))
    p.add_argument('--scheduled',action='store_true')
    args=p.parse_args()
    day=datetime.now(TZ).date().isoformat()
    out=args.out or args.state_dir/'runs'/day/('scheduled' if args.scheduled else datetime.now(timezone.utc).strftime('%H%M%S'))
    data=execute(args.state_dir,out,args.feedback_db,execution='scheduled_local' if args.scheduled else 'manual_live')
    if data.get('skipped'):
        print(json.dumps(data,sort_keys=True));return
    # Stable local entry point for the newest dated output. No automatic publication.
    latest=args.state_dir/'latest';latest.mkdir(exist_ok=True)
    for name in ('worklist.json','worklist.md','run.json','review-queue.json','collection-worklist.json','collection-worklist.md','source-review-request.json','owner-worklist.json','owner-worklist.md','research-queue.json','dispositions.md'):
        temp=latest/(name+'.tmp');temp.write_bytes((out/name).read_bytes());temp.replace(latest/name)
    print(json.dumps(dict(output=str(out),collection_counts={k:v for k,v in data['counts'].items() if k not in {'cards_requiring_attention','unique_cards'}},owner_counts=data['owner_counts'],verification=data['verification']),sort_keys=True))


if __name__=='__main__': main()
