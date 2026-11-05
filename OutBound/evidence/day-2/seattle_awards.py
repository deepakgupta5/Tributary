"""Collect a supervised slice of Seattle's dated housing award table."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

URL = "https://housing.seattle.gov/2026-uos-rfq-awards/"
NAMES = {"Bellwether Housing", "Chief Seattle Club", "Compass Housing Alliance"}


class AwardRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = []
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr":
            self.rows.append(self.row)


def collect(path):
    state = json.loads(path.read_text()) if path.exists() else {"accounts": {}, "events": {}, "attempts": []}
    attempt = {"at": datetime.now(timezone.utc).isoformat(), "url": URL}
    try:
        page = subprocess.check_output(["curl", "-fLsS", "--max-time", "30", URL]).decode()
        parser = AwardRows()
        parser.feed(page)
        rows = [row for row in parser.rows if row and row[0] in NAMES]
        if ("February 6, 2026" not in page or len(rows) != len(NAMES)
                or {row[0] for row in rows} != NAMES):
            raise ValueError("Publication date or selected award rows changed")
        batch = {}
        for name, amount, units in rows:
            if not re.fullmatch(r"\$[0-9,]+", amount):
                raise ValueError("Unexpected award format")
            key = "seattle-uos-2026/" + name
            batch[key] = {"account": name, "amount_usd": int(amount[1:].replace(",", "")),
                          "announcement_date": "2026-02-06", "source": URL,
                          "locator": "Eligible Organization table, " + name + " row",
                          "review": "candidate"}
        new = changed = 0
        for key, event in batch.items():
            versions = state["events"].setdefault(key, [])
            if not versions:
                new += 1
            elif versions[-1] == event:
                continue
            else:
                changed += 1
            versions.append(event)
        added = len(NAMES - state["accounts"].keys())
        state["accounts"].update({name: {"identity": "publisher name only"} for name in NAMES})
        attempt.update(outcome="success" if new or changed else "unchanged",
                       new_accounts=added, new_events=new, revised=changed, duplicates=len(rows)-new-changed,
                       selected_rows_sha256=hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest())
    except (subprocess.SubprocessError, ValueError) as error:
        attempt.update(outcome="failed", error=str(error))
    state["attempts"].append(attempt)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    temp.replace(path)
    print(json.dumps(attempt))
    return attempt["outcome"] != "failed"


if __name__ == "__main__":
    sys.exit(0 if collect(Path(sys.argv[1])) else 1)
