import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from tributary.resolution import export
from tributary.resolution import EVIDENCE, ROOT, load, resolve, identity, attach_award


class ResolutionTests(unittest.TestCase):
    def test_reviewed_exports_preserve_snapshot_and_separate_host_parent_payee(self):
        old = load(EVIDENCE/"day-3/original/worklist.json")
        with TemporaryDirectory() as directory:
            path = Path(directory)
            export(path)
            current = load(path/"worklist.json")
            queue = (path/"exceptions.md").read_text()
            worklist = (path/"worklist.md").read_text()
        self.assertEqual(old["ledger"],current["ledger"])
        self.assertEqual(set(old["accounts"]),set(current["accounts"]))
        self.assertEqual(set(old["events"]),set(current["events"]))
        self.assertEqual(current["counts"]["day3_discoveries"],0)
        self.assertEqual(current["counts"]["manual"],2)
        for aid, research in load(EVIDENCE/"day-3/identity-review.json").items():
            row = current["accounts"][aid]
            self.assertEqual(row["reviewed_relationship"],research)
            self.assertIn(research["name"],worklist)
            self.assertEqual(row["name"] in queue,research["role"] in {"chapter","fundraising_host"})
            if research["ein"]:
                self.assertIn(research["ein"],worklist)
        self.assertIn("31-1580932 (fundraising host)",queue)
        self.assertTrue(all(e["contract_payee"] is None for e in current["events"].values()))

    def test_ambiguous_name_stays_provisional(self):
        key, _, question = identity("WA:club","Club",{"club":[{"EIN":"123"},{"EIN":"456"}]})
        self.assertEqual(key,"WA:club")
        self.assertIn("123, 456",question)

    def test_award_relationships_and_duplicate_reporting(self):
        events = {}
        row = dict(url="https://example.org/releases",locator="row 1",fact="Award",
                   publication_date="2026-01-03",event_date=None)
        first = attach_award(events,"org1","award1","item1",row)
        second = attach_award(events,"org2","award1","item2",row)
        third = attach_award(events,"org1","award2","item3",row)
        again = attach_award(events,"org1","award1","item4",dict(row,url="https://example.org/news"))
        self.assertEqual(first,again)
        self.assertEqual(len({first,second,third}),3)
        self.assertEqual(len(events[first]["evidence"]),2)

    def test_registry_only_and_prior_discovery(self):
        r = resolve(load(EVIDENCE/"day-2/state.json"),load(ROOT/"OutBound/data/day2-sources.json"),
                    load(EVIDENCE/"live_runs/session-001/records.json"),load(EVIDENCE/"day-3/irs-lookup.json"))
        self.assertEqual(r["accounts"]["107449787RR0001"]["events"],[])
        self.assertEqual(r["accounts"]["107449787RR0001"]["registration"],"unchecked")
        self.assertIn("irs.gov",r["accounts"]["463115382"]["discovery"])
        self.assertIn("frontporch.seattle.gov",r["accounts"]["800579830"]["discovery"])
        self.assertEqual(len(r["ledger"]),35)
