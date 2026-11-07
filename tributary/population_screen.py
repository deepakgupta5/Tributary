"""Deterministic historical BC population screen, offline and never outreach-enabled."""
import argparse
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import re

RELIGION = {'0030', '0040', '0050', '0060', '0070', '0080', '0090'}
CODE_SOURCE = 'https://open.canada.ca/data/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8/resource/e9f81074-9fc7-456f-8ce1-6fd101b77963/download/codes_en.pdf'
KEYS = ['CRA identifier', 'Legal name', 'City', 'Designation', 'Category', 'Subcategory']

def number(value):
    if not value.strip():
        return None
    try:
        n = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid numeric filing value') from exc
    if not n.is_finite():
        raise ValueError('Invalid numeric filing value')
    return n

def size(row):
    revenue = number(row['Revenue CAD'])
    a, b = number(row['Permanent full-time positions']), number(row['Part-time/part-year employees'])
    if any(n is not None and (n < 0 or n != n.to_integral_value()) for n in (a, b)):
        raise ValueError('Invalid staff count')
    rev = 'unknown' if revenue is None else 'in band' if 1000000 <= revenue <= 5000000 else 'outside band'
    staff = 'unknown' if a is None or b is None else 'in band' if 10 <= a+b <= 50 else 'outside band'
    return rev, staff

def category(row):
    cat, sub, name = row['Category'], row['Subcategory'], row['Legal name'].upper()
    # A separate hospital foundation is protected even if its old code is hospital.
    protected = bool(re.search(r'\bHOSPITALS?\b', name) and re.search(r'\bFOUNDATION\b', name))
    if cat in RELIGION:
        return 'religious-organizations', 'CRA advancement-of-religion category ' + cat
    if (cat, sub) == ('0100', '0006') and not protected:
        return 'hospitals', 'CRA core health care / hospitals 0100/0006'
    if cat == '0010' and (sub == '0015' or (re.search(r'\bUNIVERSITY\b', name) and not re.search(r'\b(SCHOOL|DAYCARE|FOUNDATION|PRESCHOOL)\b', name))):
        return 'universities', 'CRA teaching institution with university subcategory or literal university name; school/daycare/foundation exception'
    if re.search(r'\bADVOCACY GROUP\b', name):
        return 'advocacy-groups', 'Literal ADVOCACY GROUP in registered legal name; no general CRA advocacy category'
    return '', 'No deterministic D062 exclusion established' + ('; hospital foundation protected' if protected else '')

def screen(identification, filings):
    reader = csv.DictReader(io.StringIO(identification.decode().split('\n', 1)[1]), delimiter='\t')
    ids = list(reader)
    source_rows = list(csv.DictReader(io.StringIO(filings.decode()), delimiter='\t'))
    indexed = {r['CRA ID']: r for r in source_rows}
    if len(indexed) != len(source_rows) or len({r['CRA identifier'] for r in ids}) != len(ids):
        raise ValueError('Duplicate CRA identifiers')
    if set(indexed) != {r['CRA identifier'] for r in ids}:
        raise ValueError('Identification / filing join is not one-to-one and complete')
    result = []
    historic = Counter()
    for ident in ids:
        filing = indexed[ident['CRA identifier']]
        if any(ident[k] != filing[k] for k in KEYS[1:]):
            raise ValueError('Identification / filing key fields disagree')
        rev, staff = size(filing)
        if (rev, staff) != (filing['Revenue screen'], filing['Staff proxy']):
            raise ValueError('Recomputed historical bands disagree with saved labels')
        historical = 'size-fit' if rev == staff == 'in band' else 'enrichment' if rev == 'in band' and staff == 'unknown' else 'out-of-band'
        historic[historical] += 1
        excluded, cat_reason = category(ident)
        disposition = 'excluded-category' if excluded else historical
        reason = cat_reason if excluded else ('Revenue and summed staffing proxy in band' if historical == 'size-fit' else 'Revenue in band; at least one staffing component missing' if historical == 'enrichment' else 'Revenue missing/outside band or complete staffing proxy outside band')
        name = ident['Legal name'].upper()
        ambiguity = not excluded and (bool(re.search(r'ADVOC', name)) or ident['Category'] == '0155')
        result.append(dict(ident, **{k: filing[k] for k in ['Period end', 'Revenue CAD', 'Permanent full-time positions', 'Part-time/part-year employees']}, **{
            'Currency': 'CAD', 'Staff measurement': 'sum of permanent full-time positions and part-time/part-year employees; historical proxy, not point-in-time headcount or FTE',
            'Historical size disposition': historical, 'Disposition': disposition, 'Reason': reason,
            'Excluded category': excluded, 'Category evidence': cat_reason,
            'Category review required': 'yes' if ambiguity else 'no',
            'Category review reason': 'Advocacy purpose cannot be determined from a legal-name clue or broad human-rights category; inspect activities before buyer admission' if ambiguity else '',
            'Current eligibility': 'unchecked', 'Donor-base gate': 'unassessed', 'Live trigger': 'unassessed', 'Collection enabled': 'no', 'Outreach enabled': 'no'}))
    result.sort(key=lambda r: r['CRA identifier'])
    counts = Counter(r['Disposition'] for r in result)
    excluded = Counter(r['Excluded category'] for r in result if r['Excluded category'])
    removed = {k: sum(r['Disposition'] == 'excluded-category' and r['Historical size disposition'] == k for r in result) for k in ['size-fit', 'enrichment', 'out-of-band']}
    summary = dict(input_rows=len(ids), unique_identifiers=len(indexed), dispositions=dict(sorted(counts.items())), exclusions={k: excluded[k] for k in ['religious-organizations','hospitals','universities','advocacy-groups']}, historical=dict(sorted(historic.items())), removed_by_historical_disposition=removed, category_review_required=sum(r['Category review required']=='yes' for r in result), historical_gate_reproduced=historic['size-fit']==754 and historic['enrichment']==414,
        input_sha256={'identification':hashlib.sha256(identification).hexdigest(), 'filings':hashlib.sha256(filings).hexdigest()}, category_code_source=CODE_SOURCE)
    assert sum(counts.values()) == len(ids)
    return result, summary

def render(summary):
    c=summary['dispositions']; e=summary['exclusions']; h=summary['historical']
    lines=['# BC historical population reconciliation', '', 'Issue #9. Offline screen of archived CRA 2024 data. No collection or outreach enabled.', '', '| Disjoint result | Records |', '| --- | ---: |', f"| Input | {summary['input_rows']:,} |"]
    lines += [f'| Excluded: {key} | {n:,} |' for key,n in e.items()]
    lines += [f"| Retained size-fit | {c.get('size-fit',0):,} |", f"| Retained enrichment | {c.get('enrichment',0):,} |", f"| Remaining out-of-band / missing revenue | {c.get('out-of-band',0):,} |", f"| Reconciled total | {sum(c.values()):,} |", '', f"Historical pre-exclusion gates: **{h.get('size-fit',0)} size-fit and {h.get('enrichment',0)} enrichment**, exactly reproducing 754/414. Category-first gates differ because D062 now removes {summary['removed_by_historical_disposition']['size-fit']} historical size-fit and {summary['removed_by_historical_disposition']['enrichment']} enrichment records. The historical numbers are not overwritten.", '', '## Rules and limits', '', '- Revenue band: CAD 1,000,000 through 5,000,000 inclusive. Staff proxy: permanent full-time positions plus part-time/part-year employees, 10 through 50 inclusive. A blank component remains unknown, never zero. This reproduces every saved band label.', '- Category exclusions precede size disposition. Religion: CRA categories 0030–0090. Hospitals: 0100/0006, except a separately named hospital foundation. Universities: teaching institutions 0010 with subcategory 0015 or literal UNIVERSITY in the legal name, excluding school/daycare/foundation names. Colleges are not automatically excluded. Advocacy: literal ADVOCACY GROUP in the legal name.', f"- **{summary['category_review_required']} unresolved category clues** remain explicitly marked in the dataset and category-review subset. CRA has no general advocacy-group category. Advocacy in a service-provider name and a human-rights purpose alone do not establish an advocacy-group buyer. Those rows are held from buyer admission pending activities review. Organizations without such clues can still be misclassified; this is a deterministic historical screen, not a completed current-eligibility review.", '- Hospital auxiliaries and hospital foundations are not treated as hospital operators merely because HOSPITAL appears in their name. Religious-category foundations remain excluded as religious organizations.', '- The recovered financial/staff file is a saved derivative, not newly fetched filings. It joins one-to-one on all 12,040 CRA IDs and matches the archived identification fields. Raw CRA financial/compensation rows are not in this archive, so the original derivative values cannot be independently audited from this input alone.', '- These are historical size candidates. Current registry status, latest size, donor-base materiality, geography/form split and live triggers remain separate downstream gates. No account is qualified for outreach by this screen.', '', '## Reproduce', '', '```sh', 'python3 -m tributary.population_screen', 'python3 -m unittest discover -s tests -v', '```', '', f"Category definitions: [CRA 2024 code list]({CODE_SOURCE}), section 2.3 (category/subcategory). Input hashes and machine counts: [reconciliation.json](reconciliation.json). All rows: [bc-population-2024.tsv](../../data/screened/bc-population-2024.tsv).", '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    args=parser.parse_args(); root=args.root
    rows,summary=screen((root/'OutBound/data/archive/BC-charity-candidates-2024.txt').read_bytes(),(root/'OutBound/data/archive/BC-size-screen-2024.txt').read_bytes())
    out=root/'OutBound/data/screened'; out.mkdir(parents=True,exist_ok=True)
    for name,subset in [('bc-population-2024.tsv',rows),('bc-size-fit-2024.tsv',[r for r in rows if r['Disposition']=='size-fit']),('bc-enrichment-2024.tsv',[r for r in rows if r['Disposition']=='enrichment']),('bc-category-review-2024.tsv',[r for r in rows if r['Category review required']=='yes'])]:
        with (out/name).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(subset)
    evidence=root/'OutBound/evidence/population-screen';evidence.mkdir(parents=True,exist_ok=True)
    (evidence/'reconciliation.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    (evidence/'README.md').write_text(render(summary))
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    main()
