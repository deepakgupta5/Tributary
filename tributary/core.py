"""Versioned records, explicit review packets, admission, and accounting."""
import hashlib
import json
import sqlite3
from datetime import datetime, timezone

KINDS = {'organization', 'source', 'evidence', 'finding'}
STAGES = ('qc', 'researcher', 'skeptic', 'fact_checker')
REQUIRED = {
    'organization': ('identity', 'eligibility'),
    'source': ('identity', 'access', 'handling', 'utility'),
    'finding': ('identity', 'evidence'),
}
VERDICTS = {'verified', 'partly_verified', 'contradicted', 'unverifiable', 'pending'}
CLAIM_VERDICTS = VERDICTS | {'reviewed_hypothesis'}


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


class Store:
    def __init__(self, path=':memory:'):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS records(
          id TEXT, version INTEGER, kind TEXT NOT NULL, body TEXT NOT NULL,
          collector TEXT NOT NULL, created TEXT NOT NULL,
          PRIMARY KEY(id,version));
        CREATE TABLE IF NOT EXISTS reviews(
          id TEXT PRIMARY KEY, subject TEXT NOT NULL, version INTEGER NOT NULL,
          stage TEXT NOT NULL, packet_hash TEXT NOT NULL, body TEXT NOT NULL,
          created TEXT NOT NULL, packet TEXT,
          FOREIGN KEY(subject,version) REFERENCES records(id,version));
        CREATE TABLE IF NOT EXISTS decisions(
          id INTEGER PRIMARY KEY, subject TEXT NOT NULL, version INTEGER NOT NULL,
          fingerprint TEXT NOT NULL, state TEXT NOT NULL, reasons TEXT NOT NULL,
          run_id TEXT NOT NULL, created TEXT NOT NULL,
          FOREIGN KEY(subject,version) REFERENCES records(id,version));
        CREATE TABLE IF NOT EXISTS history(
          seq INTEGER PRIMARY KEY, event_key TEXT UNIQUE NOT NULL,
          type TEXT NOT NULL, body TEXT NOT NULL, created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS runs(
          id TEXT PRIMARY KEY, body TEXT NOT NULL, created TEXT NOT NULL);
        ''')
        # Legacy reviews did not preserve inputs. Never invent/backfill a packet.
        if 'packet' not in {r['name'] for r in self.db.execute('PRAGMA table_info(reviews)')}:
            self.db.execute('ALTER TABLE reviews ADD COLUMN packet TEXT')
            self.db.commit()

    def close(self):
        self.db.close()

    def event(self, kind, body, key=None):
        key = key or digest([kind, body])
        self.db.execute('INSERT OR IGNORE INTO history(event_key,type,body,created) VALUES(?,?,?,?)',
                        (key, kind, encode(body), now()))

    def get(self, rid, version=None):
        if version is None:
            row = self.db.execute('SELECT * FROM records WHERE id=? ORDER BY version DESC LIMIT 1', (rid,)).fetchone()
        else:
            row = self.db.execute('SELECT * FROM records WHERE id=? AND version=?', (rid, version)).fetchone()
        require(row is not None, 'Unknown record: ' + rid)
        return {**dict(row), 'body': json.loads(row['body'])}

    def current(self):
        return [self.get(r[0]) for r in self.db.execute('SELECT DISTINCT id FROM records ORDER BY id')]

    def validate_record(self, rid, kind, body):
        require(isinstance(rid, str) and rid and kind in KINDS, 'Invalid ID/kind')
        require(isinstance(body, dict) and body.get('synthetic') is True, 'Synthetic records only')
        require(isinstance(body.get('dependencies', []), list), 'Invalid dependencies')
        require(len(set(body.get('dependencies', []))) == len(body.get('dependencies', [])), 'Duplicate dependency')
        for dep in body.get('dependencies', []):
            require(dep != rid, 'Self dependency')
            self.get(dep)
        if kind == 'evidence':
            require(self.get(body.get('source', ''))['kind'] == 'source', 'Evidence requires source')
            require(isinstance(body.get('paragraphs'), dict), 'Missing evidence paragraphs')
            require(all(isinstance(k, str) and isinstance(v, str) for k, v in body['paragraphs'].items()), 'Invalid paragraph')
            require(isinstance(body.get('available'), bool), 'Missing availability')
            date = body.get('publication_date')
            if date is not None:
                try:
                    datetime.strptime(date, '%Y-%m-%d')
                except (ValueError, TypeError):
                    raise Invalid('Malformed publication date')
            else:
                require(bool(body.get('date_unknown_reason')), 'Unknown date needs reason')
        else:
            require(isinstance(body.get('name'), str) and bool(body['name'].strip()), 'Missing subject name')
            require(isinstance(body.get('claims'), list), 'Missing claim ledger')
            ids = [c.get('id') for c in body['claims']]
            require(all(isinstance(i, str) and i for i in ids) and len(ids) == len(set(ids)), 'Invalid claim IDs')
            require(isinstance(body.get('details'), dict), 'Missing required-detail checklist')
            if kind == 'finding':
                require(self.get(body.get('organization', ''))['kind'] == 'organization', 'Finding requires organization')
                require(body['organization'] in body.get('dependencies', []), 'Organization must be dependency')
            for claim in body['claims']:
                require(isinstance(claim.get('text'), str) and bool(claim['text']), 'Empty claim')
                require(claim.get('type') in {'number', 'quote', 'paraphrase', 'hypothesis'}, 'Invalid claim type')
                require(isinstance(claim.get('material'), bool), 'Claim materiality required')
                require(isinstance(claim.get('evidence'), list), 'Evidence list required')
                for eid in claim['evidence']:
                    require(self.get(eid)['kind'] == 'evidence', 'Claim must cite evidence')
                    require(eid in body.get('dependencies', []), 'Evidence must be dependency')
        encode(body)

    def put(self, rid, kind, body, collector):
        """All substantive data changes create versions; cosmetic labels are external."""
        require(isinstance(collector, str) and bool(collector), 'Collector execution required')
        self.validate_record(rid, kind, body)
        existing = self.db.execute('SELECT 1 FROM records WHERE id=?', (rid,)).fetchone()
        before = {r['id']: self.fingerprint(r['id']) for r in self.current()}
        version = 1
        if existing:
            prior = self.get(rid)
            require(prior['kind'] == kind, 'Record kind cannot change')
            if prior['body'] == body:
                return prior['version'], False
            version = prior['version'] + 1
        with self.db:
            self.db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',
                            (rid, version, kind, encode(body), collector, now()))
            # Cycle detection happens before commit, including indirect cycles.
            after = {r['id']: self.fingerprint(r['id']) for r in self.current()}
            self.event('record_created' if version == 1 else 'record_revised', {'id': rid, 'version': version})
            for affected, old in before.items():
                if after[affected] != old:
                    self.event('checks_reopened', {'id': affected, 'cause': rid,
                               'old_fingerprint': old, 'new_fingerprint': after[affected], 'stages': list(STAGES)})
        return version, True

    def fingerprint(self, rid, seen=()):
        require(rid not in seen, 'Dependency cycle')
        record = self.get(rid)
        return digest({'id': rid, 'version': record['version'], 'body': record['body'],
                       'dependencies': {d: self.fingerprint(d, seen + (rid,))
                                        for d in record['body'].get('dependencies', [])}})

    def discover(self, parent, child, method, run_id):
        p, c = self.get(parent), self.get(child)
        require((p['kind'], c['kind']) in {('source', 'organization'), ('organization', 'source')}, 'Invalid discovery direction')
        body = {'parent': parent, 'candidate': child, 'direction': p['kind'] + '_to_' + c['kind'],
                'method': method, 'first_seen_run': run_id, 'next_action': 'four_checkpoint_review'}
        with self.db:
            self.event('discovery', body, digest(['discovery', parent, child, method]))

    def ingest(self, run_id, items):
        """One disposition per attempted item, including failed inputs; retries are runs."""
        previous = self.db.execute('SELECT body FROM runs WHERE id=?', (run_id,)).fetchone()
        input_hash = digest(items)
        if previous:
            saved = json.loads(previous[0])
            require(saved['input_hash'] == input_hash, 'Run ID reused with changed input')
            if saved['status'] != 'running':
                return saved
            result = saved
        else:
            result = {'id': run_id, 'input_hash': input_hash, 'items': [], 'status': 'running', 'input_count': len(items)}

        def persist():
            result['counts'] = {k: sum(x['disposition'] == k for x in result['items']) for k in ('unique', 'duplicate', 'quarantined')}
            result['pending_count'] = len(items) - len(result['items'])
            result['reconciled'] = sum(result['counts'].values()) + result['pending_count'] == len(items)
            with self.db:
                self.db.execute('INSERT INTO runs VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body',
                                (run_id, encode(result), now()))
        persist()
        for index in range(len(result['items']), len(items)):
            item = items[index]
            try:
                require(isinstance(item, dict), 'Malformed input item')
                version, changed = self.put(item['id'], 'evidence', item['body'], 'collector:' + run_id)
                disposition = 'unique' if changed else 'duplicate'
                outcome = {'index': index, 'id': item['id'], 'version': version, 'disposition': disposition}
            except (Invalid, KeyError, TypeError) as exc:
                outcome = {'index': index, 'id': item.get('id') if isinstance(item, dict) else None, 'disposition': 'quarantined', 'reason': str(exc)}
            result['items'].append(outcome)
            persist()
        result['status'] = 'partial' if result['counts']['quarantined'] else 'complete'
        persist()
        return result

    def packet(self, rid, stage):
        require(stage in STAGES, 'Unknown stage')
        subject = self.get(rid)
        require(subject['kind'] in REQUIRED, 'Evidence is reviewed through its consuming records')
        dependencies = {}

        def collect(record):
            for dep in record['body'].get('dependencies', []):
                if dep not in dependencies:
                    d = self.get(dep)
                    dependencies[dep] = {'id': dep, 'version': d['version'], 'kind': d['kind'], 'body': d['body']}
                    collect(d)
        collect(subject)
        predecessors = {}
        for prior in STAGES[:STAGES.index(stage)]:
            r = self.latest_review(rid, prior)
            if r:
                predecessors[prior] = r['body']
        packet = {'contract_version': 2, 'subject': {'id': rid, 'version': subject['version'],
                  'kind': subject['kind'], 'body': subject['body']}, 'stage': stage,
                  'fingerprint': self.fingerprint(rid), 'dependencies': dependencies,
                  'prior_reviews': predecessors, 'required_details': list(REQUIRED[subject['kind']])}
        return packet

    def latest_review(self, rid, stage):
        rows = self.db.execute('SELECT * FROM reviews WHERE subject=? AND stage=? ORDER BY rowid DESC', (rid, stage))
        for row in rows:
            if row['packet'] is None:
                continue  # unverifiable historical input; a new execution is required
            r = self.get_review(row['id'])
            if r['packet_hash'] == digest(self.packet(rid, stage)):
                return r
        return None

    def get_review(self, execution_id):
        """Inspect the saved input independently of current source/review versions."""
        row = self.db.execute('SELECT * FROM reviews WHERE id=?', (execution_id,)).fetchone()
        require(row is not None, 'Unknown review execution')
        result = {**dict(row), 'body': json.loads(row['body']),
                  'packet': json.loads(row['packet']) if row['packet'] is not None else None}
        result['input_state'] = 'preserved' if result['packet'] is not None else 'unavailable_legacy'
        if result['packet'] is not None:
            require(digest(result['packet']) == result['packet_hash'], 'Stored review packet hash mismatch')
        return result

    def review(self, packet, output):
        rid, stage = packet['subject']['id'], packet['stage']
        require(packet == self.packet(rid, stage), 'Stale or altered review packet')
        subject = self.get(rid)
        require(set(STAGES[:STAGES.index(stage)]) <= set(packet['prior_reviews']), 'Missing prior checkpoint')
        for key in ('execution_id', 'actor', 'reason', 'context'):
            require(isinstance(output.get(key), str) and bool(output[key].strip()), 'Missing ' + key)
        require(output.get('basis') in {'fixture_replay', 'coding_session'}, 'Invalid execution basis')
        require(output.get('completed') in (True, False) and isinstance(output.get('completed'), bool), 'Completion required')
        require(output.get('outcome') in {'passed', 'incomplete', 'failed'}, 'Invalid outcome')
        require(output['completed'] or output['outcome'] != 'passed', 'Incomplete execution cannot pass')
        # Traceability check only: a caller-controlled ID is not a security boundary.
        if stage == 'qc':
            collectors = {subject['collector']} | {self.get(d)['collector'] for d in packet['dependencies']}
            require(output['execution_id'] not in collectors, 'Collector cannot submit QC for its own output')
        claims = {c['id']: c for c in subject['body']['claims']}
        if stage == 'researcher':
            require(set(output.get('claim_ids', [])) == set(claims), 'Researcher must account for full ledger')
            require(len(output['claim_ids']) == len(claims), 'Duplicate researcher claim')
        if stage == 'skeptic':
            issues = output.get('issues')
            require(isinstance(issues, list), 'Issues required')
            require(len({i['id'] for i in issues}) == len(issues), 'Duplicate issue')
            for issue in issues:
                require(issue.get('claim_id') in claims or issue.get('detail') in REQUIRED[subject['kind']], 'Issue target unknown')
                require(isinstance(issue.get('material'), bool) and bool(issue.get('reason')), 'Issue materiality/reason required')
        if stage == 'fact_checker':
            checks = output.get('checks', [])
            require(len(checks) == len(claims) and {c['claim_id'] for c in checks} == set(claims), 'Every claim needs exactly one check')
            require(set(output.get('details', {})) == set(REQUIRED[subject['kind']]), 'Required detail checks incomplete')
            for value in output['details'].values():
                require(isinstance(value, dict) and value.get('status') in VERDICTS and bool(value.get('reason')), 'Invalid detail check')
                if value['status'] == 'verified':
                    require(value.get('evidence') in packet['dependencies'], 'Required detail lacks evidence')
                    ev = self.get(value['evidence'])
                    require(ev['kind'] == 'evidence' and ev['body']['available'] and value.get('locator') in ev['body']['paragraphs'], 'Required detail lacks available locator')
            for check in checks:
                require(check.get('status') in CLAIM_VERDICTS and bool(check.get('reason')), 'Invalid claim check')
                hypothesis = claims[check['claim_id']]['type'] == 'hypothesis'
                if hypothesis:
                    require(check['status'] in {'reviewed_hypothesis', 'pending'}, 'Hypothesis cannot receive a factual verdict')
                else:
                    require(check['status'] != 'reviewed_hypothesis', 'Factual claim cannot receive hypothesis disposition')
                require(check.get('corroboration') in {'single_origin', 'independent', 'unknown'}, 'Corroboration required')
                if check['status'] == 'verified':
                    evidence = check.get('evidence')
                    require(evidence in claims[check['claim_id']]['evidence'], 'Check evidence not cited by claim')
                    ev = self.get(evidence)
                    require(ev['body']['available'] and check.get('locator') in ev['body']['paragraphs'], 'Unavailable evidence or locator')
            issues = packet['prior_reviews']['skeptic']['issues']
            resolutions = output.get('resolutions', {})
            require(set(resolutions) == {i['id'] for i in issues}, 'Every skeptic issue needs disposition')
            for resolution in resolutions.values():
                require(resolution.get('status') in {'supported_as_written', 'corrected', 'limitation_retained', 'unresolved'} and bool(resolution.get('reason')), 'Invalid issue disposition')
        review_id = output['execution_id']
        with self.db:
            existing = self.db.execute('SELECT * FROM reviews WHERE id=?', (review_id,)).fetchone()
            if existing:
                require(existing['packet_hash'] == digest(packet) and existing['body'] == encode(output), 'Execution ID reused')
                require(existing['packet'] == encode(packet), 'Historical packet unavailable or different; use a new execution')
                return review_id
            self.db.execute('INSERT INTO reviews(id,subject,version,stage,packet_hash,body,created,packet) VALUES(?,?,?,?,?,?,?,?)',
                            (review_id, rid, subject['version'], stage, digest(packet), encode(output), now(), encode(packet)))
        return review_id

    def blockers(self, rid):
        record = self.get(rid)
        require(record['kind'] in REQUIRED, 'Not an admission subject')
        body, reasons = record['body'], []
        if not body['claims']:
            reasons.append('Missing admission claim ledger')
        for field in REQUIRED[record['kind']]:
            if body['details'].get(field) != 'resolved':
                reasons.append('Required detail unresolved: ' + field)
        if record['kind'] == 'organization' and body.get('category') not in {'service_delivery', 'foundation', 'umbrella'}:
            reasons.append('Eligibility category undecided or outside starting scope')
        if record['kind'] == 'organization' and not body.get('geography'):
            reasons.append('Required geography unresolved')
        if record['kind'] == 'source' and not body.get('endpoint'):
            reasons.append('Required endpoint unresolved')
        if record['kind'] == 'finding':
            if self.status(body['organization']) != 'admitted':
                reasons.append('Organization not currently admitted')
            for eid in {eid for claim in body['claims'] for eid in claim['evidence']}:
                source = self.get(eid)['body']['source']
                if source not in body.get('dependencies', []):
                    reasons.append('Cited source missing admission dependency: ' + source)
                if self.status(source) != 'approved_for_collection':
                    reasons.append('Source not currently approved: ' + source)
        for stage in STAGES:
            review = self.latest_review(rid, stage)
            if not review or not review['body']['completed'] or review['body']['outcome'] != 'passed':
                reasons.append('Checkpoint missing/stale/not passed: ' + stage)
        fact = self.latest_review(rid, 'fact_checker')
        if fact:
            result = fact['body']
            claims = {c['id']: c for c in body['claims']}
            for field, check in result['details'].items():
                if check['status'] != 'verified':
                    reasons.append('Required detail not verified: ' + field)
            for check in result['checks']:
                claim = claims[check['claim_id']]
                if claim['type'] == 'hypothesis' and claim['material']:
                    reasons.append('Material hypothesis cannot establish required fact: ' + check['claim_id'])
                elif claim['material'] and check['status'] != 'verified':
                    reasons.append('Material claim not verified: ' + check['claim_id'])
                if check['status'] == 'pending':
                    reasons.append('Claim not checked: ' + check['claim_id'])
            skeptic = self.latest_review(rid, 'skeptic')['body']
            for issue in skeptic['issues']:
                resolution = result['resolutions'][issue['id']]['status']
                if issue['material'] and resolution != 'supported_as_written':
                    # Corrections require a revised record and a fresh review chain.
                    reasons.append('Material issue requires resolution/revision: ' + issue['id'])
        return reasons

    def status(self, rid):
        record = self.get(rid)
        rows = self.db.execute('SELECT * FROM decisions WHERE subject=? ORDER BY id DESC', (rid,)).fetchall()
        if rows and rows[0]['fingerprint'] == self.decision_fingerprint(rid):
            if rows[0]['state'] in {'approved', 'admitted', 'approved_for_collection'} and self.blockers(rid):
                return 'awaiting_recheck'
            return rows[0]['state']
        if rows:
            return 'awaiting_recheck'
        return 'candidate'

    def decision_fingerprint(self, rid):
        return digest([self.fingerprint(rid), {s: (self.latest_review(rid, s) or {}).get('id') for s in STAGES}])

    def decide(self, rid, run_id):
        reasons = self.blockers(rid)
        record = self.get(rid)
        state = 'pending' if reasons else {'source': 'approved_for_collection', 'organization': 'admitted', 'finding': 'approved'}[record['kind']]
        fp = self.decision_fingerprint(rid)
        with self.db:
            prior = self.db.execute('SELECT * FROM decisions WHERE subject=? ORDER BY id DESC', (rid,)).fetchone()
            if not prior or (prior['fingerprint'], prior['state']) != (fp, state):
                self.db.execute('INSERT INTO decisions(subject,version,fingerprint,state,reasons,run_id,created) VALUES(?,?,?,?,?,?,?)',
                                (rid, record['version'], fp, state, encode(reasons), run_id, now()))
        return {'id': rid, 'state': state, 'blockers': reasons}

    def snapshot(self):
        return {'states': {r['id']: self.status(r['id']) for r in self.current() if r['kind'] in REQUIRED},
                'cursor': self.db.execute('SELECT COALESCE(MAX(seq),0) FROM history').fetchone()[0]}

    def reconcile(self, opening):
        closing = self.snapshot()['states']
        cursor, opening = opening['cursor'], opening['states']
        approved = {'admitted', 'approved_for_collection', 'approved'}
        new = set(closing) - set(opening)
        pending_open = {k for k, v in opening.items() if v not in approved}
        changed = {json.loads(r[0])['id'] for r in self.db.execute(
            "SELECT body FROM history WHERE type='checks_reopened' AND seq>?", (cursor,))}
        reopened = {k for k in opening if opening[k] in approved and (k in changed or closing.get(k) not in approved)}
        population = pending_open | new | reopened
        admitted = {k for k in population if closing.get(k) in approved}
        pending = population - admitted
        active_open = {k for k, v in opening.items() if v in approved}
        active_close = {k for k, v in closing.items() if v in approved}
        audits = [json.loads(r[0]) for r in self.db.execute('SELECT body FROM runs ORDER BY id')]
        discrepancies = []
        for run in audits:
            actual = {k: sum(i['disposition'] == k for i in run['items']) for k in ('unique', 'duplicate', 'quarantined')}
            if actual != run['counts'] or sum(actual.values()) + run.get('pending_count', 0) != run['input_count']:
                discrepancies.append('Ingestion mismatch: ' + run['id'])
        require(set(opening) <= set(closing), 'Records disappeared')
        return {'opening_pending': len(pending_open), 'new_candidates': len(new), 'reopened': len(reopened),
                'admitted': len(admitted), 'closing_pending': len(pending), 'population_ids': sorted(population),
                'candidate_balance': len(pending_open) + len(new) + len(reopened) == len(admitted) + len(pending),
                'opening_active': len(active_open), 'activations': len(active_close - active_open),
                'inactivations': len(active_open - active_close), 'closing_active': len(active_close),
                'stock_balance': len(active_open) + len(active_close - active_open) - len(active_open - active_close) == len(active_close),
                'discrepancies': discrepancies, 'passed': not discrepancies,
                'incomplete_runs': [r['id'] for r in audits if r['status'] != 'complete'],
                'limits': 'Distinct candidate work per period; repeated revisions of one subject are coalesced in counts and retained individually in history. No merge/exclusion execution or scheduler. Retries are attempts, not new sources.'}
