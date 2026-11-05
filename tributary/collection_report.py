"""Render the selected saved run, using evidence versions current at collection."""
import argparse
import json
from pathlib import Path


def render(state, number):
    run = state["runs"][number-1]
    new = set(run["new_accounts"])
    lines = [f"# Collection run {number}", "",
             f"New candidate accounts: {len(new)}. Backfill batch: {run['batch']}.", "",
             "| Source | Outcome | New items | Revised items | Retrieved / attempted (UTC) |",
             "|---|---|---:|---:|---|"]
    for a in run["attempts"]:
        lines.append(f"| {a['source']} | {a['outcome']} | {len(a['additions'])} | {len(a['revisions'])} | {a['at']} |")
    for title, is_new in [("New candidate accounts", True), ("Items at previously known accounts", False)]:
        lines += ["", "## "+title, ""]
        count = 0
        for a in run["attempts"]:
            for key in a["additions"] + a["revisions"]:
                item = next(v["item"] for v in state["items"][key] if v["retrieved_at"] == a["at"])
                if (item["account"] in new) != is_new:
                    continue
                count += 1
                lines.append(f"- **{state['accounts'][item['account']]}** — {item['fact']}. "
                             f"Published {item['publication_date'] or 'unknown'}; event date "
                             f"{item['event_date'] or 'unknown / inapplicable'}. "
                             f"[{item['locator']}]({item['url']})")
        if count == 0:
            lines.append("Zero new or revised items.")
    lines += ["", "## Interpretation and gaps", "",
              "Award announcements supply a funder relationship to investigate. All items are collection candidates. "
              "Commercial relevance, budget, purchasing authority and willingness to engage are unknown.",
              "", "Greater Vancouver Food Bank Society is monitored under BN 107449787RR0001. "
              "The 2024 filing identifies the account. Current registration remains unchecked and event strength unassessed.",
              "", "This English-language slice covers selected BC and Washington sources. Other Canadian jurisdictions, "
              "local journalism, sector coverage and comprehensive procurement coverage remain gaps. "
              "Housing archive batch 2 requires an explicit continuation. The two-page funder backfill is bounded."]
    return "\n".join(lines)+"\n"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("state",type=Path)
    p.add_argument("number",type=int)
    p.add_argument("output",type=Path)
    args = p.parse_args()
    args.output.write_text(render(json.loads(args.state.read_text()),args.number))
