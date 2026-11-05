"""Compact organization worklist built from the auditable record store."""
import json

from .core import STAGES


def _fact_checks(store, rid):
    review = store.latest_review(rid, 'fact_checker')
    if not review:
        return None, {}
    return review, {item['claim_id']: item for item in review['body']['checks']}


def _detail_state(review, detail):
    if not review:
        return 'unchecked'
    status = review['body'].get('details', {}).get(detail, {}).get('status', 'pending')
    return 'verified' if status == 'verified' else 'open'


def _source_reference(store, check):
    evidence_id = check.get('evidence')
    if not evidence_id:
        return None
    evidence = store.get(evidence_id)
    if evidence['kind'] != 'evidence':
        return None
    body = evidence['body']
    return {
        'evidence_id': evidence_id,
        'url': body.get('source_url'),
        'locator': check.get('locator'),
        'publication_date': body.get('publication_date'),
        'retrieved_at': body.get('retrieved_at'),
    }


def _finding_card(store, finding):
    rid, body = finding['id'], finding['body']
    fact, checks = _fact_checks(store, rid)
    observations, hypotheses, unresolved, references = [], [], [], []
    for claim in body['claims']:
        check = checks.get(claim['id'], {})
        status = check.get('status', 'pending')
        item = {'claim_id': claim['id'], 'text': claim['text'], 'status': status}
        if claim['type'] == 'hypothesis':
            hypotheses.append(item)
        elif status == 'verified':
            observations.append(item)
        else:
            unresolved.append(item)
        reference = _source_reference(store, check)
        if reference and reference not in references:
            references.append(reference)
    return {
        'finding_id': rid,
        'title': body['name'],
        'review_state': 'reviewed' if store.status(rid) == 'approved' else 'under_review',
        'observations': observations,
        'hypotheses': hypotheses,
        'unresolved_claims': unresolved,
        'limitations': body.get('limitations', []),
        'route_status': body.get('route_status', 'not_investigated'),
        'references': references,
        'checkpoint_completion': {
            stage: bool(store.latest_review(rid, stage)) for stage in STAGES
        },
    }


def build_worklist(store):
    current = store.current()
    organizations = [record for record in current if record['kind'] == 'organization']
    findings = [record for record in current if record['kind'] == 'finding']
    cards = []
    for organization in organizations:
        rid, body = organization['id'], organization['body']
        fact, _ = _fact_checks(store, rid)
        account_findings = [_finding_card(store, finding) for finding in findings
                            if finding['body']['organization'] == rid]
        reviewed = any(item['review_state'] == 'reviewed' for item in account_findings)
        signal_state = ('reviewed_signal' if reviewed else
                        'signal_under_review' if account_findings else 'no_signal_identified')
        gaps = list(body.get('limitations', []))
        if _detail_state(fact, 'identity') != 'verified':
            gaps.append('Current identity needs verification.')
        if _detail_state(fact, 'eligibility') != 'verified':
            gaps.append('Current in-scope operating or eligibility status needs verification.')
        gaps = list(dict.fromkeys(gaps))
        cards.append({
            'account_id': rid,
            'name': body['name'],
            'discovery_state': 'discovered',
            'register_state': store.status(rid),
            'identity_state': _detail_state(fact, 'identity'),
            'eligibility_state': _detail_state(fact, 'eligibility'),
            'signal_review_state': signal_state,
            'business_relevance': 'unreviewed_private',
            'geography': body.get('geography', []),
            'category': body.get('category'),
            'open_questions': gaps,
            'signals': account_findings,
            'next_action': ('review_signal' if signal_state == 'signal_under_review' else
                            'investigate_relevance' if signal_state == 'reviewed_signal' else
                            'find_current_signal'),
        })
    priority = {'reviewed_signal': 0, 'signal_under_review': 1, 'no_signal_identified': 2}
    cards.sort(key=lambda card: (priority[card['signal_review_state']], card['name']))
    return {
        'contract_version': 1,
        'purpose': 'Daily research input for private outbound decisions',
        'accounts': cards,
        'counts': {
            'accounts': len(cards),
            'reviewed_signal': sum(c['signal_review_state'] == 'reviewed_signal' for c in cards),
            'signal_under_review': sum(c['signal_review_state'] == 'signal_under_review' for c in cards),
            'no_signal_identified': sum(c['signal_review_state'] == 'no_signal_identified' for c in cards),
        },
    }


def render_markdown(worklist):
    lines = ['# Daily nonprofit account worklist', '',
             'This is a research queue for private outbound decisions. Verified observations, '
             'hypotheses, unresolved questions, and commercial relevance remain separate.', '',
             f'Accounts: {worklist["counts"]["accounts"]}; '
             f'reviewed signals: {worklist["counts"]["reviewed_signal"]}; '
             f'signals under review: {worklist["counts"]["signal_under_review"]}; '
             f'accounts without an identified signal: {worklist["counts"]["no_signal_identified"]}.', '']
    sections = [
        ('reviewed_signal', 'Accounts with reviewed signals'),
        ('signal_under_review', 'Accounts with signals under review'),
        ('no_signal_identified', 'Discovered accounts awaiting a signal'),
    ]
    for state, title in sections:
        accounts = [card for card in worklist['accounts'] if card['signal_review_state'] == state]
        if not accounts:
            continue
        lines += ['## ' + title, '']
        for account in accounts:
            lines += [f'### {account["name"]}', '',
                      f'Account ID: `{account["account_id"]}`  ',
                      f'Identity: **{account["identity_state"]}**; eligibility: **{account["eligibility_state"]}**; '
                      f'register: **{account["register_state"]}**  ',
                      f'Commercial relevance: **{account["business_relevance"]}**  ',
                      f'Next action: **{account["next_action"]}**', '']
            for signal in account['signals']:
                lines += [f'**{signal["title"]}** ({signal["review_state"]})', '']
                for observation in signal['observations']:
                    lines.append('- Verified observation: ' + observation['text'])
                for hypothesis in signal['hypotheses']:
                    lines.append('- Hypothesis: ' + hypothesis['text'])
                for unresolved in signal['unresolved_claims']:
                    lines.append(f'- Unresolved claim ({unresolved["status"]}): {unresolved["text"]}')
                for limitation in signal['limitations']:
                    lines.append('- Limitation: ' + limitation)
                for reference in signal['references']:
                    date = reference.get('publication_date') or 'publication date unknown'
                    lines.append(f'- Source: {reference.get("url") or "unavailable"} '
                                 f'({date}; locator: {reference.get("locator") or "unavailable"})')
                lines.append('')
            if account['open_questions']:
                lines.append('Open questions:')
                lines.append('')
                lines.extend('- ' + question for question in account['open_questions'])
                lines.append('')
    lines += ['## Audit', '',
              'The detailed report, exact review packets, and structured records remain available '
              'beside this worklist. This view does not establish need, budget, authority, or willingness to engage.', '']
    return '\n'.join(lines)


def export_worklist(store, directory):
    worklist = build_worklist(store)
    (directory / 'worklist.json').write_text(json.dumps(worklist, indent=2, ensure_ascii=False) + '\n')
    (directory / 'worklist.md').write_text(render_markdown(worklist))
    return worklist
