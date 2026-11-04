"""Lossless synthetic exports and deterministic Markdown rendering."""
import json
from .core import REQUIRED, STAGES, encode


def coverage(claims, checks):
    eligible = {c['id'] for c in claims}
    submitted = eligible & set(checks)
    completed = {cid for cid in submitted if checks[cid]['status'] != 'pending'}
    return {'eligible': len(eligible), 'submitted': len(submitted), 'completed': len(completed),
            'pending': len(eligible - completed), 'unsubmitted': len(eligible - submitted)}


def export(store, directory, demonstration):
    tables = {}
    for table, order in [('records', 'id,version'), ('reviews', 'rowid'), ('decisions', 'id'), ('history', 'seq'), ('runs', 'id')]:
        tables[table] = [dict(row) for row in store.db.execute(f'SELECT * FROM {table} ORDER BY {order}')]
        for row in tables[table]:
            for key in ('body', 'reasons', 'packet'):
                if key in row and row[key] is not None:
                    row[key] = json.loads(row[key])
    statuses = {r['id']: {'state': store.status(r['id']), 'blockers': store.blockers(r['id'])}
                for r in store.current() if r['kind'] in REQUIRED}
    bases = sorted({r['body']['basis'] for r in tables['reviews']})
    data = {'schema_version': 2, 'synthetic_only': True, 'execution_bases': bases,
            'tables': tables, 'current_status': statuses, 'demonstration': demonstration}
    data['claim_coverage'] = {}
    for record in store.current():
        if record['kind'] in REQUIRED:
            review = store.latest_review(record['id'], 'fact_checker')
            checks = {c['claim_id']: c for c in review['body']['checks']} if review else {}
            data['claim_coverage'][record['id']] = coverage(record['body']['claims'], checks)
    (directory / 'records.json').write_text(json.dumps(data, indent=2) + '\n')
    with (directory / 'records.jsonl').open('w') as stream:
        for table, rows in tables.items():
            for row in rows:
                stream.write(encode({'group': table, 'record': row}) + '\n')
    (directory / 'demonstration.json').write_text(json.dumps(demonstration, indent=2) + '\n')
    basis_note = ('Hand-authored fixture replay; no actual coding-session role review performed.' if bases == ['fixture_replay'] else
                  'Recorded execution bases: ' + ', '.join(bases) + '; context separation must be assessed from the records.')
    lines = ['# Synthetic Tributary report', '',
             '**Basis: ' + basis_note + ' No model accuracy, live-source feasibility, or owner usefulness is established by this report.**', '',
             'All names and evidence are fictional. Source locators use synthetic references.', '',
             '## Register and approval queue', '']
    def order(record):
        kind, body = record['kind'], record['body']
        group = record['id'] if kind == 'organization' else body.get('organization', '~sources')
        return (group, 0 if kind == 'organization' else 1, record['id'])
    current_group = None
    for record in sorted(store.current(), key=order):
        rid, body = record['id'], record['body']
        if record['kind'] not in REQUIRED:
            continue
        group = record['id'] if record['kind'] == 'organization' else body.get('organization', '~sources')
        if group != current_group:
            lines += ['## ' + ('Sources' if group == '~sources' else 'Organization group: ' + group), '']
            current_group = group
        lines += [f'### {rid}: {body["name"]}', '',
                  f'Kind: {record["kind"]}; version: {record["version"]}; state: **{statuses[rid]["state"]}**.', '']
        for reason in statuses[rid]['blockers']:
            lines.append('- Blocker: ' + reason)
        for limitation in body.get('limitations', []):
            lines.append('- Limitation: ' + limitation)
        if body.get('optional'):
            lines.append('- Optional information: ' + json.dumps(body['optional']))
        if body.get('duplicate_candidates'):
            lines.append('- Unresolved possible duplicate: ' + ', '.join(body['duplicate_candidates']))
        lines += ['', '| Checkpoint | Execution | Completion / outcome |', '| --- | --- | --- |']
        for stage in STAGES:
            review = store.latest_review(rid, stage)
            if review:
                lines.append(f'| {stage} | {review["id"]} | {review["body"]["completed"]} / {review["body"]["outcome"]} |')
            else:
                lines.append(f'| {stage} | unavailable | pending or stale |')
        fact = store.latest_review(rid, 'fact_checker')
        checks = {c['claim_id']: c for c in fact['body']['checks']} if fact else {}
        basis = fact['body']['basis'] if fact else 'pending'
        counts = data['claim_coverage'][rid]
        lines += ['', f'Claim-check coverage: {counts["completed"]}/{counts["eligible"]} completed; '
                  f'{counts["submitted"]} submitted; {counts["pending"]} pending '
                  f'({counts["unsubmitted"]} unsubmitted) ({basis}).', '']
        for claim in body['claims']:
            check = checks.get(claim['id'], {})
            label = check.get('status', 'pending')
            if claim['type'] == 'hypothesis':
                label = 'hypothesis — ' + label + ' (not a verified fact)'
            lines += [f'- **{claim["id"]} — {label} [{basis}]:** {claim["text"]}',
                      f'  Evidence: {check.get("evidence", "unavailable")} / {check.get("locator", "unavailable")}; {check.get("reason", "Check pending.")}',
                      f'  Corroboration: {check.get("corroboration", "unknown")}; this is separate from source-faithfulness.']
            if check.get('correction'):
                lines.append('  Correction: ' + check['correction'])
        skeptic = store.latest_review(rid, 'skeptic')
        if skeptic and skeptic['body']['issues']:
            lines += ['', 'Skeptic issues and dispositions:', '']
            for issue in skeptic['body']['issues']:
                resolution = fact['body']['resolutions'].get(issue['id'], {}) if fact else {}
                lines.append(f'- {issue["id"]}: {issue["reason"]} Material: {issue["material"]}. '
                             f'Disposition: {resolution.get("status", "pending")}; {resolution.get("reason", "Unperformed")}.')
        if fact:
            lines += ['', 'Context record: ' + fact['body']['context']]
        if record['kind'] == 'finding':
            lines += ['', 'Organization: ' + body['organization'], '',
                      'Route investigation: ' + body.get('route_status', 'not_investigated')]
            if body.get('hypothesis'):
                lines += ['', 'Hypothesis (not a verified fact): ' + body['hypothesis']]
            for alternative in body.get('alternatives', []):
                lines.append('- Alternative: ' + alternative)
        lines.append('')
    lines += ['## Discovery and coverage', '',
              'Demonstrated categories: fictional BC community reporting, organization publication, and Washington funder record.',
              'No real endpoint was attempted. No geographic completeness percentage is claimed.', '']
    for event in tables['history']:
        if event['type'] == 'discovery':
            b = event['body']
            lines.append(f'- {b["direction"]}: {b["parent"]} → {b["candidate"]}; {b["method"]}.')
    lines += ['', '## Reconciliation', '', '```json', json.dumps(demonstration, indent=2), '```', '',
              '## Limits', '',
              'Review IDs and packets provide traceability, not reviewer independence. Semantic verdicts here are scripted. No authentication boundary prevents a trusted local operator editing SQLite directly. No live retrieval, scheduler, merge engine, paid dependency, or provider API is included.', '']
    (directory / 'report.md').write_text('\n'.join(lines))
