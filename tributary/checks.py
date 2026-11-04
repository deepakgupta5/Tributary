"""Narrow deterministic checks, never semantic or independent verification."""
from decimal import Decimal, InvalidOperation
from .core import Invalid, require, VERDICTS


def amount_equal(actual, expected):
    """Amounts must retain currency, unit, period and target/actual basis."""
    fields = ('currency', 'unit', 'period', 'basis', 'value')
    require(set(actual) == set(expected) == set(fields), 'Incomplete amount metadata')
    try:
        a, b = Decimal(str(actual['value'])), Decimal(str(expected['value']))
        require(a.is_finite() and b.is_finite(), 'Nonfinite amount')
        return a == b and all(actual[k] == expected[k] for k in fields if k != 'value')
    except InvalidOperation:
        raise Invalid('Malformed decimal amount')


def shortfall(target, actual):
    require(all(target[k] == actual[k] for k in ('currency', 'unit', 'period')), 'Incomparable amounts')
    require(target['basis'] == 'target' and actual['basis'] == 'actual', 'Wrong amount basis')
    # Reuse metadata and finite-value checks.
    amount_equal(target, target)
    amount_equal(actual, actual)
    return str(Decimal(str(target['value'])) - Decimal(str(actual['value'])))


def evaluate(expected, observed):
    """Score saved outputs only after role execution; missing checks stay counted."""
    require(len({r['id'] for r in observed}) == len(observed), 'Duplicate observed ID')
    require(all(r['id'] in expected and r['status'] in VERDICTS for r in observed), 'Unknown observed ID/status')
    require(all(v in VERDICTS - {'pending'} for v in expected.values()), 'Invalid expected status')
    actual = {r['id']: r['status'] for r in observed}
    defects = {k for k, v in expected.items() if v != 'verified'}
    caught = {k for k in defects if actual.get(k) in {'contradicted', 'partly_verified'} or
              (expected[k] == 'unverifiable' and actual.get(k) == 'unverifiable')}
    controls = set(expected) - defects
    return {'eligible': len(expected), 'checked': sum(actual.get(k, 'pending') != 'pending' for k in expected),
            'defects': len(defects), 'caught': len(caught), 'missed': len(defects - caught),
            'false_verification': sum(actual.get(k) == 'verified' for k in defects),
            'correct_controls': len(controls), 'false_rejection': sum(actual.get(k) in {'contradicted', 'partly_verified'} for k in controls),
            'control_abstentions': sum(actual.get(k) == 'unverifiable' for k in controls),
            'exact_status_matches': sum(actual.get(k) == v for k, v in expected.items())}
