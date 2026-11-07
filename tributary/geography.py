"""Canonical locality and form routing for the retained BC historical population."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re

FIELDS = ['Canonical locality','Geography status','Geography reason','Geography authority','Geography source','Geography evidence basis','Organization route','Stage route','Stage hold reason']

def normalize_locality(value):
    return ' '.join(re.sub(r'[^A-Z0-9 ]', ' ', value.upper()).split())

def validate_rules(rules):
    corridor = rules['corridor_localities']
    remote = rules['known_non_corridor_localities']
    if len(set(corridor)) != len(corridor) or len(set(remote)) != len(remote) or set(corridor) & set(remote):
        raise ValueError('Duplicate or conflicting geography rules')
    if any(normalize_locality(name) != name or not name for name in corridor + remote):
        raise ValueError('Geography rule keys must be canonical')
    for name, alias in rules['aliases'].items():
        if normalize_locality(name) != name or name in corridor or name in remote:
            raise ValueError('Invalid or conflicting alias')
        if alias['canonical_locality'] not in set(corridor) | set(remote) or not alias['source']:
            raise ValueError('Alias target/source missing')

def classify_locality(raw, rules):
    key = normalize_locality(raw)
    alias = rules['aliases'].get(key)
    canonical = alias['canonical_locality'] if alias else key
    source = alias['source'] if alias else 'OutBound/frameworks/BC_CONVERSATION_PLAN.md, Decision 3; decisions/DECISIONS.md D060/D066'
    if canonical in rules['corridor_localities']:
        status = 'in-corridor'
        reason = alias['basis'] if alias else 'Exact canonical locality in the owner-approved D060/D066 corridor'
    elif canonical in rules['known_non_corridor_localities']:
        status, reason = 'remote-monitor', 'Archived BC locality outside the named D060/D066 corridor'
    else:
        status, reason = 'needs-review', 'Blank or unrecognized locality; no fuzzy match or inferred corridor admission'
    return canonical, status, reason, source

def route_population(population, rules):
    validate_rules(rules)
    if len({r['CRA identifier'] for r in population}) != len(population):
        raise ValueError('Duplicate CRA identifiers')
    rows=[]
    for original in population:
        if original['Disposition'] not in {'size-fit','enrichment'}:
            continue
        row=dict(original)
        canonical, geo, reason, source=classify_locality(row['City'],rules)
        form = 'operating-organization' if row['Designation']=='C' else 'funder-intermediary' if row['Designation'] in {'A','B'} else 'needs-review'
        hold=[]
        if row['Buyer admission held']!='no' or row['Category review required']!='no':
            hold.append('Prior population/category admission hold remains active')
        if geo=='needs-review':hold.append('Geography unresolved')
        if form=='needs-review':hold.append('CRA designation unresolved')
        if hold:
            route = 'held-review'
        elif geo == 'in-corridor':
            route = 'pool-a' if form == 'operating-organization' else 'corridor-funder-intermediary'
        else:
            route = 'remote-operating-monitor' if form == 'operating-organization' else 'remote-funder-intermediary-monitor'
        row.update(dict(zip(FIELDS,[canonical,geo,reason,'D060; D066',source,'CRA 2024 historical mailing locality only; current operating/service geography unchecked',form,route,'; '.join(hold)])))
        rows.append(row)
    rows.sort(key=lambda r:r['CRA identifier'])
    counts=Counter(r['Stage route'] for r in rows)
    before=Counter(r['Disposition'] for r in rows)
    cross=Counter((r['Stage route'],r['Disposition']) for r in rows)
    result=dict(input_population_rows=len(population),retained_input_rows=len(rows),retained_input_size_dispositions=dict(sorted(before.items())),stage_routes=dict(sorted(counts.items())),route_size_counts={route:{size:cross[route,size] for size in ['size-fit','enrichment']} for route in sorted(counts)},geography_counts=dict(sorted(Counter(r['Geography status'] for r in rows).items())),form_counts=dict(sorted(Counter(r['Organization route'] for r in rows).items())),raw_localities=len({r['City'] for r in rows}),canonical_localities=len({r['Canonical locality'] for r in rows}),alias_rows=sum(normalize_locality(r['City']) in rules['aliases'] for r in rows),authority=['D060','D066'],operating_geography_verified=False,donor_base_gate='unassessed',live_trigger_gate='unassessed',outreach_enabled=False)
    assert sum(counts.values())==sum(before.values())==len(rows)
    return rows,result

def render(summary):
    lines=['# Canonical BC geography and form stage', '', 'Applies D060 and owner boundary decision D066 to the retained Issue #9 population.', '', f"Input: **{summary['retained_input_rows']} retained records**, comprising {summary['retained_input_size_dispositions'].get('size-fit',0)} historical size-fit and {summary['retained_input_size_dispositions'].get('enrichment',0)} staffing-enrichment records. The other population dispositions are not reconsidered by this stage.", '', '| Disjoint route | Size-fit | Enrichment | Total |','| --- | ---: | ---: | ---: |']
    for route,parts in summary['route_size_counts'].items():
        lines.append(f"| {route} | {parts['size-fit']} | {parts['enrichment']} | {sum(parts.values())} |")
    lines += [f"| **Total** | **{summary['retained_input_size_dispositions'].get('size-fit',0)}** | **{summary['retained_input_size_dispositions'].get('enrichment',0)}** | **{summary['retained_input_rows']}** |", '', '## Interpretation', '', '- Pool A is the in-corridor operating-organization research pool, with size-fit and incomplete-staffing records labelled separately. It is not an outreach-ready list.', '- Foundations (CRA A/B) retain a separate funder/intermediary route regardless of geography. Their combined file includes corridor and remote rows; the route column distinguishes them.', '- D066 explicitly includes Delta, Mission and White Rock. The remaining corridor is the D060 named localities, including Coquitlam. Aldergrove maps to the Langley routing area using the [Township community page](https://www.tol.ca/en/the-township/aldergrove.aspx).', '- Canonical locality is a routing area. The source supplies historical mailing locality, not current operating address, service area or travel time. Langley and North Vancouver addresses do not distinguish City from Township/District. No one-hour driving-time verification is claimed.', '- Case, punctuation and whitespace are normalized. Only explicit aliases are applied; no fuzzy matching. Unrecognized or blank localities and unknown CRA designations enter held-review. Prior category/admission holds are preserved.', '- D065 remains applied: PLAN excluded before this stage; PACE retained only as a category disposition, with operating status still unchecked. The 28 moot out-of-band records do not enter the 896-record geography input.', '- Current registry/operating status, donor-base materiality and live triggers are unassessed. Collection and outreach remain disabled. This stage performs no fresh collection or prospect enrichment.', '', '## Outputs', '', '- [All retained records and routes](../../data/geography/bc-geography-2024.tsv)', '- [Pool A](../../data/geography/bc-pool-a-2024.tsv)', '- [Funder/intermediary list, corridor and remote](../../data/geography/bc-funder-intermediaries-2024.tsv)', '- [Remote/monitor, operating organizations and foundations](../../data/geography/bc-remote-monitor-2024.tsv)', '- [Held geography/form review](../../data/geography/bc-geography-review-2024.tsv)', '- [Per-locality reconciliation](../../data/geography/locality-reconciliation.tsv)', '- [Machine reconciliation and input/rule hashes](reconciliation.json)', '', 'The funder list overlaps the remote list for remote foundations. Use the disjoint route table above when summing; do not add downloadable subset row counts.', '', '```sh', 'python3 -m tributary.geography', 'python3 -m unittest discover -s tests -v', '```', '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path('.'));args=parser.parse_args();root=args.root
    source=root/'OutBound/data/screened/bc-population-2024.tsv';rulefile=root/'OutBound/data/bc-geography-rules.json'
    raw=source.read_bytes();rulebytes=rulefile.read_bytes();rules=json.loads(rulebytes)
    population=list(csv.DictReader(io.StringIO(raw.decode()),delimiter='\t'))
    rows,summary=route_population(population,rules)
    summary['input_sha256']=hashlib.sha256(raw).hexdigest();summary['rules_sha256']=hashlib.sha256(rulebytes).hexdigest()
    out=root/'OutBound/data/geography';out.mkdir(parents=True,exist_ok=True)
    subsets={'bc-geography-2024.tsv':rows,'bc-pool-a-2024.tsv':[r for r in rows if r['Stage route']=='pool-a'],'bc-funder-intermediaries-2024.tsv':[r for r in rows if r['Organization route']=='funder-intermediary'],'bc-remote-monitor-2024.tsv':[r for r in rows if r['Geography status']=='remote-monitor'],'bc-geography-review-2024.tsv':[r for r in rows if r['Stage route']=='held-review']}
    for name, subset in subsets.items():
        with (out/name).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(population[0])+FIELDS,delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(subset)
    local=Counter((r['City'],r['Canonical locality'],r['Geography status'],r['Organization route'],r['Disposition'],r['Stage route']) for r in rows)
    with (out/'locality-reconciliation.tsv').open('w',newline='') as f:
        writer=csv.writer(f,delimiter='\t',lineterminator='\n');writer.writerow(['Raw locality','Canonical locality','Geography status','Organization route','Historical size disposition','Stage route','Records'])
        for key,count in sorted(local.items()):writer.writerow([*key,count])
    evidence=root/'OutBound/evidence/canonical-geography';evidence.mkdir(parents=True,exist_ok=True)
    (evidence/'reconciliation.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');(evidence/'README.md').write_text(render(summary));print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
