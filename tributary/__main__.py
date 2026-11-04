"""Run with python -m tributary. Operational commands, not assistant handoffs."""
import argparse
import json
import sys
from pathlib import Path

from .core import Invalid, ROLES, Store


def main():
    parser = argparse.ArgumentParser(description="Bounded synthetic evidence collection and versioned review")
    parser.add_argument("--db", default="tributary.sqlite")
    commands = parser.add_subparsers(dest="command", required=True)
    collect = commands.add_parser("collect", help="Collect synthetic source records from JSON")
    collect.add_argument("input", type=Path)
    role = commands.add_parser("role-input", help="Export the current versioned evidence packet")
    role.add_argument("role", choices=ROLES)
    submit = commands.add_parser("submit", help="Validate and persist a role output JSON")
    submit.add_argument("input", type=Path)
    commands.add_parser("report", help="Render current results; fail if missing or stale")
    args = parser.parse_args()
    store = Store(args.db)
    try:
        if args.command == "collect":
            result = store.collect(json.loads(args.input.read_text()))
        elif args.command == "role-input":
            result = store.role_input(args.role)
        elif args.command == "submit":
            result = store.submit(json.loads(args.input.read_text()))
        else:
            print(store.report(), end="")
            return 0
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.command == 'collect' and result['status'] == 'failed':
            return 2
        return 0
    except (Invalid, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    finally:
        store.close()


if __name__ == "__main__":
    sys.exit(main())
