"""BC geography preserves population decisions and only routes approved localities."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from tributary.geography import classify_locality, normalize_locality, route_population

ROOT=Path(__file__).resolve().parents[1]

class GeographyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.population=list(csv.DictReader((ROOT/'OutBound/data/screened/bc-population-2024.tsv').open(),delimiter='\t'))
        cls.rules=json.loads((ROOT/'OutBound/data/bc-geography-rules.json').read_text())
        cls.rows,cls.summary=route_population(cls.population,cls.rules)

    def test_reconciliation_and_foundation_split(self):
        s=self.summary
        self.assertEqual(s['retained_input_rows'],896)
        self.assertEqual(s['retained_input_size_dispositions'],{'enrichment':345,'size-fit':551})
        self.assertEqual(s['stage_routes'],{'corridor-funder-intermediary':168,'pool-a':323,'remote-funder-intermediary-monitor':41,'remote-operating-monitor':364})
        self.assertEqual(sum(s['stage_routes'].values()),896)
        self.assertEqual(s['route_size_counts']['pool-a'],{'size-fit':231,'enrichment':92})
        expected={r['CRA identifier'] for r in self.population if r['Disposition'] in {'size-fit','enrichment'}}
        self.assertEqual({r['CRA identifier'] for r in self.rows},expected)
        self.assertEqual(len(self.rows),len(expected))
        self.assertTrue(all(r['Designation']=='C' for r in self.rows if r['Stage route']=='pool-a'))
        self.assertEqual(sum(r['Organization route']=='funder-intermediary' for r in self.rows),209)

    def test_canonical_aliases_and_d066_explicit_boundary(self):
        self.assertEqual(normalize_locality(' fort st. john '),normalize_locality('FORT ST JOHN'))
        self.assertEqual(classify_locality('aldergrove',self.rules)[:2],('LANGLEY','in-corridor'))
        for locality in ['Delta','Mission','White Rock','Coquitlam','Port Moody','Pitt Meadows']:
            self.assertEqual(classify_locality(locality,self.rules)[1],'in-corridor')
        self.assertEqual(classify_locality('Victoria',self.rules)[1],'remote-monitor')
        for locality in ['','Vancuver','NEW UNKNOWN LOCALITY']:
            self.assertEqual(classify_locality(locality,self.rules)[1],'needs-review')

    def test_prior_holds_unknown_locality_and_designation_block_route(self):
        source=next(r for r in self.population if r['City']=='VANCOUVER' and r['Designation']=='C' and r['Disposition']=='size-fit')
        for changes in [{'Buyer admission held':'yes'},{'Category review required':'yes'},{'Designation':'X'},{'City':'VANCUVER'}]:
            changed=dict(source,**changes)
            rows,summary=route_population([changed],self.rules)
            self.assertEqual(rows[0]['Stage route'],'held-review')
            self.assertTrue(rows[0]['Stage hold reason'])
        with self.assertRaises(ValueError):route_population([source,source],self.rules)
        bad=json.loads(json.dumps(self.rules));bad['known_non_corridor_localities'].append('VANCOUVER')
        with self.assertRaises(ValueError):route_population([source],bad)

    def test_d065_and_unassessed_gates_preserved(self):
        by_id={r['CRA identifier']:r for r in self.rows}
        self.assertNotIn('131516320RR0001',by_id)
        self.assertEqual(by_id['898116462RR0001']['Category review status'],'retained-service-delivery')
        self.assertEqual(by_id['898116462RR0001']['Current eligibility'],'unchecked')
        for row in self.rows:
            self.assertEqual(row['Donor-base gate'],'unassessed')
            self.assertEqual(row['Live trigger'],'unassessed')
            self.assertEqual(row['Collection enabled'],'no')
            self.assertEqual(row['Outreach enabled'],'no')
        original={r['CRA identifier']:r for r in self.population}
        self.assertTrue(all(all(row[k]==v for k,v in original[row['CRA identifier']].items()) for row in self.rows))

    def test_repeat_outputs_identical_and_population_untouched(self):
        source=ROOT/'OutBound/data/screened/bc-population-2024.tsv'
        paths=sorted((ROOT/'OutBound/data/geography').glob('*.tsv'))+[(ROOT/'OutBound/evidence/canonical-geography/reconciliation.json'),(ROOT/'OutBound/evidence/canonical-geography/README.md'),source]
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,'-m','tributary.geography','--root',str(ROOT)],cwd=ROOT,check=True,capture_output=True)
        self.assertEqual(before,{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        with (ROOT/'OutBound/data/geography/bc-geography-2024.tsv').open() as f:
            self.assertEqual(list(csv.DictReader(f,delimiter='\t')),self.rows)
        with (ROOT/'OutBound/data/geography/locality-reconciliation.tsv').open() as f:
            self.assertEqual(sum(int(r['Records']) for r in csv.DictReader(f,delimiter='\t')),896)
