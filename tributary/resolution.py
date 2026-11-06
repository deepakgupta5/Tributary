"""Resolve the saved Day 2 batch offline. No source files are modified."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "OutBound/evidence"


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def normalize(name):
    return " ".join(re.findall(r"[a-z0-9]+", name.lower()))


def identity(key, name, matches):
    if re.fullmatch(r"\d{9}(RR\d{4})?", key):
        return key, "Day 2 register identifier", None
    candidates = matches.get(normalize(name), [])
    if len(candidates) == 1:
        row = candidates[0]
        return row["EIN"], f"Unique normalized IRS name in Washington; filing city {row['CITY']}", None
    if candidates:
        question = "Which EIN belongs to this recipient? Compare an official address or domain for " + ", ".join(r["EIN"] for r in candidates)
    elif "Clean Greens Farm" in name:
        question = "Does the award agreement name Black Dollar Days Task Force or the farm as grantee? Obtain the payee EIN."
    elif "Washington Chapter" in name:
        question = "Does the Washington chapter have its own EIN or use the parent or a sponsor as payee?"
    elif "(" in name or name.isupper():
        question = f"Which official legal name and EIN does the funder associate with the award label {name}?"
    else:
        question = f"Which legal entity received the award listed as {name}? Obtain the recipient or fiscal sponsor's legal name and EIN from the funder."
    return key, "Publisher label; legal identity open", question


def attach_award(events, account_id, award_key, item_id, item):
    # award_key identifies a recipient's award within a funder round. A second
    # document needs the same supported award reference to join the event.
    eid = "award-" + hashlib.sha256(json.dumps([account_id, award_key]).encode()).hexdigest()[:24]
    event = events.setdefault(eid, dict(account_id=account_id,award_key=award_key,evidence={}))
    event["evidence"][item_id] = {k:item[k] for k in ("url","locator","fact","publication_date","event_date")}
    return eid


def resolve(state, inventory, prior, lookup):
    sources = {s["id"]:s for s in inventory}
    matches = defaultdict(list)
    for row in lookup["rows"]:
        matches[normalize(row["NAME"])].append(row)
    names = {r["id"]:r["body"]["name"] for r in prior["subjects"]}
    endpoints = {s["id"]:s["body"]["endpoint"] for s in prior["seed_sources"]}
    original = {names[d["child"]]:endpoints[d["parent"]] for d in prior["discoveries"]
                if d["parent"] in endpoints}
    run = state["runs"][0]
    new = set(run["new_accounts"])
    accounts, events, ledger, documents = {}, {}, {}, {}
    for attempt in run["attempts"]:
        source = sources[attempt["source"]]
        for key in attempt["additions"]:
            if key in ledger:
                raise ValueError("Repeated input key: "+key)
            item = next(v["item"] for v in state["items"][key] if v["retrieved_at"]==attempt["at"])
            old = item["account"]
            name = state["accounts"][old]
            aid, basis, question = identity(old,name,matches)
            row = accounts.setdefault(aid,dict(name=name,discovery=original.get(name,item["url"]),
                basis=basis,question=question,events=[],inputs=[],registration="unchecked"))
            row["inputs"].append(key)
            url = item["url"]
            documents.setdefault(url,[]).append(key)
            eid = None
            if source["id"] == "food":
                eid = attach_award(events,aid,"Seattle/Food Equity Fund/2026",key,item)
                if eid not in row["events"]:
                    row["events"].append(eid)
            elif source["id"] not in {"irs","cra"}:
                raise ValueError("Unclassified input: "+key)
            ledger[key] = dict(account_id=aid,day2_account=old,new_candidate=old in new,
                               source=url,event_id=eid)
    if (set(ledger) != set(state["items"]) or
            new != {v["day2_account"] for v in ledger.values() if v["new_candidate"]}):
        raise ValueError("Input ledger mismatch")
    return dict(accounts=accounts,events=events,documents=documents,ledger=ledger,
                outside_batch=sorted(state["accounts"][k] for k in set(state["accounts"])-
                                     {v["day2_account"] for v in ledger.values()}),
                counts=dict(accounts=len(accounts),items=len(ledger),new_candidates=len(new),
                    known_items=sum(not r["new_candidate"] for r in ledger.values()),
                    events=len(events),dated_accounts=sum(bool(a["events"]) for a in accounts.values()),
                    registry_only=sum(not a["events"] for a in accounts.values()),
                    manual=sum(bool(a["question"]) for a in accounts.values())))


def export(out):
    result = resolve(load(EVIDENCE/"day-2/state.json"),load(ROOT/"OutBound/data/day2-sources.json"),
                     load(EVIDENCE/"live_runs/session-001/records.json"),load(EVIDENCE/"day-3/irs-lookup.json"))
    reviewed = load(EVIDENCE/"day-3/identity-review.json")
    for aid, finding in reviewed.items():
        row = result["accounts"][aid]
        row["reviewed_relationship"] = finding
        role = finding["role"]
        row["basis"] = role.replace("_"," ") + ": " + finding["name"]
        row["question"] = None
        if role == "fundraising_host":
            row["question"] = "Which legal entity operates the pantry, and does it have its own EIN?"
        elif role == "chapter":
            row["question"] = "Does the Washington chapter have its own EIN or operate under a parent?"
        elif role not in {"operating_entity","program_parent"}:
            raise ValueError("Unknown reviewed relationship: " + role)
    for event in result["events"].values():
        event["contract_payee"] = None
    result["counts"].update(day2_new_candidates=result["counts"]["new_candidates"],day3_discoveries=0,
                            manual=sum(bool(a["question"]) for a in result["accounts"].values()))
    out.mkdir(exist_ok=True,parents=True)
    save(out/"worklist.json",result)
    lines = ["# Account worklist", "", "First Day 2 batch. Registry identity is period-specific. "
             "Current registration remains unchecked, including for Greater Vancouver Food Bank Society.", "",
             "| Organization | Identifier and identity evidence | First discovery | Event and dates | Review question |",
             "|---|---|---|---|---|"]
    lines.insert(2,"31 Day 2 discoveries plus three previously known accounts. Day 3 discoveries: zero. Award contract payees remain unverified.\n")
    exceptions = ["# Identity exceptions", "", "Two recipient identities need follow-up. Contract payee verification is a separate award-level question.", ""]
    for aid,row in sorted(result["accounts"].items(),key=lambda pair:pair[1]["name"].casefold()):
        source = row["discovery"]
        refs = []
        for eid in row["events"]:
            for ev in result["events"][eid]["evidence"].values():
                refs.append(f"{ev['fact']} [Announced {ev['publication_date']}]({ev['url']}); award date {ev['event_date'] or 'unknown'}.")
        q = row["question"]
        evidence = row["basis"]
        identifier = aid
        if aid in reviewed:
            finding = reviewed[aid]
            identifier = (finding["ein"] or "unknown EIN") + " (" + finding["role"].replace("_"," ") + ")"
            evidence += f" · [identity research]({finding['source']})"
        if q:
            exceptions.append(f"- **{row['name']}** — {identifier} · {evidence}. {q} [Award row]({source})")
        lines.append(f"| {row['name']} | {identifier} · {evidence} | "
                     f"[{row['inputs'][0].split('/')[0]}]({source}) | {' '.join(refs) or 'Registry evidence only'} | {q or '—'} |")
    lines += ["", "Outside this batch (earlier Seattle housing pilot): "+", ".join(result["outside_batch"])+".",
              "", "Each registry row or recipient row has an entry in the [structured reconciliation](worklist.json)."]
    (out/"worklist.md").write_text("\n".join(lines)+"\n")
    (out/"exceptions.md").write_text("\n".join(exceptions)+"\n")
    print(json.dumps(result["counts"],sort_keys=True))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    export(parser.parse_args().output)
