"""Bounded Day 2 collection. Run with python3 -m tributary.collect DIRECTORY."""
import argparse
import csv
from datetime import date, datetime, timezone
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import subprocess
import tempfile
import fcntl
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree
from calendar import monthrange

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "OutBound/data/day2-sources.json"
KNOWN = {"107449787RR0001": "Greater Vancouver Food Bank Society",
         "911090450": "Food Lifeline", "463115382": "Nurturing Roots"}
PILOT = ("Bellwether Housing", "Chief Seattle Club", "Compass Housing Alliance")


def fetch(url, previous):
    args = ["curl", "-sSL", "--max-time", "60", "--max-filesize", "35000000"]
    for key, header in [("etag", "If-None-Match"), ("last-modified", "If-Modified-Since")]:
        if previous.get(key):
            args.extend(["-H", header + ": " + previous[key]])
    with tempfile.TemporaryDirectory() as directory:
        headers = Path(directory) / "headers"
        raw = subprocess.check_output([*args, "-D", str(headers), "-w", "\n%{http_code}", url])
        body, code = raw.rsplit(b"\n", 1)
        lines = headers.read_text(encoding="latin1").strip().split("\n\n")[-1].splitlines()
        fields = dict((k.lower(), v.strip()) for k, _, v in
                      (line.partition(":") for line in lines if ":" in line))
        return int(code), body, {k: fields[k] for k in ("etag", "last-modified") if k in fields}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "td", "th", "h2", "li"):
            self.parts = []

    def handle_endtag(self, tag):
        if tag in ("p", "td", "th", "h2", "li"):
            self.blocks.append(" ".join("".join(self.parts).split()))
            self.parts = []


def extract(source, raw):
    sid = source["id"]
    if sid == "contracts":
        data = json.loads(raw)
        for row in data["results"]:
            if row["awarded"] == "Yes":
                yield (row["bid_number"] + "/" + row["vendor_name"], row["vendor_name"], None,
                       "City procurement award " + row["bid_number"], None, row["award_date"], source["url"])
        return
    if sid == "housing-feed":
        channel = ElementTree.fromstring(raw).find("channel")
        if channel is None:
            raise ValueError("Missing RSS channel")
        for entry in channel.findall("item"):
            pub = parsedate_to_datetime(entry.findtext("pubDate")).date().isoformat()
            link = entry.findtext("link")
            summary = " ".join(entry.findtext(field,"") for field in ("title","description"))
            for name in PILOT:
                if name.casefold() in summary.casefold():
                    yield (link+"#"+name, name, None, "Seattle housing news mentions "+name,
                           pub, None, link)
        return
    if sid in ("irs", "cra"):
        us = sid == "irs"
        key, name, city, region = ("EIN","NAME","CITY","STATE") if us else ("BN","Legal Name","City","Province")
        rows = csv.DictReader(io.StringIO(raw.decode("utf-8-sig" if us else "latin1")))
        if not {key, name, city, region} <= set(rows.fieldnames or []):
            raise ValueError("Register header mismatch")
        for row in rows:
            if row[region] != source["geography"]:
                continue
            if row[key] not in KNOWN and not ("FOOD BANK" in row[name].upper() and
                    row[city].upper() in {"SEATTLE","TACOMA","VANCOUVER","BURNABY","SURREY"}):
                continue
            yield (row[key], row[name], row[key], f"{row[name]} listed in {row[city]}; " + (
                "tax period " + row["TAX_PERIOD"] if us else "2024 charity identification file"),
                None, None, source["url"])
        return
    parser = Blocks()
    parser.feed(raw.decode("utf8"))
    blocks = parser.blocks
    awards = []
    if sid == "food":
        start = blocks.index("2026 Food Equity Fund Awards")
        for line in blocks[start+1:]:
            match = re.fullmatch(r"\$([\d,]+) to (.+?)\s*\*?", line)
            if match:
                awards.append((match[2].strip(), match[1]))
    elif sid == "housing":
        for name in (*PILOT, "Solid Ground", "Plymouth Housing Group"):
            amount = blocks[blocks.index(name)+1]
            if not re.fullmatch(r"\$[\d,]+", amount):
                raise ValueError("Invalid award table")
            awards.append((name, amount[1:]))
    if not awards:
        raise ValueError("No recognizable award rows")
    for name, amount in awards:
        yield (name, name, None, f"City announced USD {amount} in {('Food Equity Fund' if sid=='food' else 'urgent operating support')} funding for {name}.",
               source["published"], None, source["url"])


def initial():
    accounts = dict(KNOWN)
    accounts.update({f"WA:{n.casefold()}": n for n in PILOT})
    return dict(accounts=accounts, items={}, sources={}, runs=[], batch=1)


def run(state, inventory, retrieve=fetch, advance=False):
    if advance:
        state["batch"] = min(state["batch"]+1, max(s.get("batch",1) for s in inventory))
    before = set(state["accounts"])
    log = []
    for src in inventory:
        sid = src["id"]
        last = state["sources"].setdefault(sid, {"last_success":None,"checkpoint":{}})
        if src.get("batch",1) > state["batch"]:
            continue
        at = datetime.now(timezone.utc).isoformat()
        today = date.fromisoformat(at[:10])
        start = today.replace(year=today.year-1, day=min(today.day,monthrange(today.year-1,today.month)[1]))
        if src.get("published") and not (start <= date.fromisoformat(src["published"]) <= today):
            continue
        attempt = dict(source=sid, at=at, additions=[], revisions=[], duplicates=0)
        log.append(attempt)
        last["last_attempt"] = at
        if src.get("hold"):
            attempt.update(outcome="blocked", reason=src["hold"])
            continue
        try:
            cp = last["checkpoint"]
            code, raw, validators = retrieve(src["url"], cp)
            attempt["http"] = code
            if code in (401,403):
                attempt.update(outcome="blocked", reason=f"HTTP {code}")
                continue
            if code == 304 and cp:
                attempt.update(outcome="unchanged")
                last["last_success"] = at
                continue
            if code != 200:
                raise ValueError(f"HTTP {code}")
            digest = hashlib.sha256(raw).hexdigest()
            unchanged = digest == cp.get("sha256")
            rows = [] if unchanged else [r for r in extract(src,raw) if
                not (r[4] or r[5]) or start <= date.fromisoformat(r[4] or r[5]) <= today]
            for locator, name, official, note, pub, event, url in rows:
                account = official or next((k for k,n in state["accounts"].items()
                    if n.casefold()==name.casefold()), f"{src['geography']}:{name.casefold()}")
                state["accounts"].setdefault(account,name)
                item = dict(account=account, locator=locator, fact=note, url=url,
                            publication_date=pub, event_date=event)
                key = sid + "/" + locator
                history = state["items"].setdefault(key,[])
                if history and history[-1]["item"] == item:
                    attempt["duplicates"] += 1
                    continue
                attempt["revisions" if history else "additions"].append(key)
                history.append(dict(retrieved_at=at,item=item))
            attempt["outcome"] = "unchanged" if unchanged else "success"
            last.update(last_success=at, checkpoint=dict(sha256=digest, **validators))
        except (OSError, ValueError, subprocess.SubprocessError, csv.Error, ElementTree.ParseError, IndexError, KeyError, TypeError) as exc:
            attempt.update(outcome="failed", reason=str(exc))
    state["runs"].append(dict(attempts=log,new_accounts=sorted(set(state["accounts"])-before),
                              batch=state["batch"]))


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("directory",type=Path)
    cli.add_argument("--advance",action="store_true",help="activate the next bounded backfill page")
    args = cli.parse_args()
    args.directory.mkdir(parents=True,exist_ok=True)
    path = args.directory/"state.json"
    with (args.directory/".collector.lock").open("a") as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        state = json.loads(path.read_text()) if path.exists() else initial()
        run(state,json.loads(INVENTORY.read_text()),advance=args.advance)
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n")
        temp.replace(path)
        print([(a["source"],a["outcome"],len(a["additions"])) for a in state["runs"][-1]["attempts"]])


if __name__ == "__main__":
    main()
