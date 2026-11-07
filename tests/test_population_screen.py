"""Historical population conservation, explicit gates, and repeatability."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from tributary.population_screen import category, number, screen, size

ROOT = Path(__file__).resolve().parents[1]

class PopulationScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ident = (ROOT/'OutBound/data/archive/BC-charity-candidates-2024.txt').read_bytes()
        cls.filing = (ROOT/'OutBound/data/archive/BC-size-screen-2024.txt').read_bytes()
        cls.rows, cls.summary = screen(cls.ident, cls.filing)
        cls.by_id = {r['CRA identifier']:r for r in cls.rows}

    def test_population_conservation_and_historical_reproduction(self):
        s=self.summary
        self.assertEqual(len(self.rows),12040)
        self.assertEqual(len(self.by_id),12040)
        self.assertEqual(sum(s['dispositions'].values()),12040)
        self.assertEqual(s['historical']['size-fit'],754)
        self.assertEqual(s['historical']['enrichment'],414)
        for key in ['size-fit','enrichment','out-of-band']:
            self.assertEqual(s['historical'][key],s['dispositions'][key]+s['removed_by_historical_disposition'][key])
        self.assertEqual(sum(s['exclusions'].values()),s['dispositions']['excluded-category'])

    def test_staff_components_missing_not_zero_and_boundaries(self):
        def row(rev,a,b):return {'Revenue CAD':rev,'Permanent full-time positions':a,'Part-time/part-year employees':b}
        self.assertEqual(size(row('1000000','1','9')),('in band','in band'))
        self.assertEqual(size(row('5000000','25','25')),('in band','in band'))
        self.assertEqual(size(row('5000001','25','26')),('outside band','outside band'))
        self.assertEqual(size(row('2000000','20','')),('in band','unknown'))
        self.assertEqual(size(row('2000000','10','0')),('in band','in band'))
        self.assertEqual(size(row('-1','10','0')),('outside band','in band'))
        for value in ['NaN','Infinity','garbage']:
            with self.assertRaises(ValueError):number(value)
        with self.assertRaises(ValueError):size(row('1000000','-1','10'))

    def test_hospital_foundation_and_education_exceptions(self):
        self.assertEqual(self.by_id['889291399RR0001']['Excluded category'],'')
        self.assertEqual(self.by_id['119048205RR0001']['Excluded category'],'hospitals')
        self.assertEqual(self.by_id['108161779RR0001']['Excluded category'],'universities')
        self.assertEqual(self.by_id['108032988RR0001']['Excluded category'],'')
        self.assertEqual(self.by_id['887333482RR0001']['Excluded category'],'')
        self.assertEqual(self.by_id['802507145RR0001']['Excluded category'],'')

    def test_ambiguous_advocacy_not_silently_excluded(self):
        r=self.by_id['802374942RR0001']
        self.assertEqual(r['Category review required'],'yes')
        self.assertEqual(r['Excluded category'],'')
        self.assertEqual(self.by_id['890669864RR0001']['Excluded category'],'advocacy-groups')
        self.assertTrue(all(r['Outreach enabled']=='no' and r['Collection enabled']=='no' for r in self.rows))

    def test_duplicate_missing_and_disagreeing_join_fail(self):
        for changed in [self.filing+self.filing.splitlines(keepends=True)[1], b'\n'.join(self.filing.splitlines()[:-1]), self.filing.replace(b'100 MILE HOUSE',b'ALTERED CITY',1)]:
            with self.assertRaises(ValueError):screen(self.ident,changed)

    def test_committed_outputs_match_and_repeat_bytes(self):
        expected=json.loads((ROOT/'OutBound/evidence/population-screen/reconciliation.json').read_text())
        self.assertEqual(expected,self.summary)
        paths=list((ROOT/'OutBound/data/screened').glob('*.tsv'))+list((ROOT/'OutBound/evidence/population-screen').glob('reconciliation.json'))+[(ROOT/'OutBound/evidence/population-screen/README.md')]
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,'-m','tributary.population_screen','--root',str(ROOT)],check=True,capture_output=True,cwd=ROOT)
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
        with (ROOT/'OutBound/data/screened/bc-population-2024.tsv').open() as f:
            self.assertEqual(list(csv.DictReader(f,delimiter='\t')),self.rows)
