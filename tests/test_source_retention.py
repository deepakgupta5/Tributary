"""No full original may survive a collection/review command."""
from argparse import Namespace
from datetime import datetime,timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tributary import daily,source_review as sr
from tributary.checkpoint_audit import execute as checkpoint,STAGES
from test_source_review import state,verdicts,HTML,collection

MARKER='UNRETAINED_FULL_ORIGINAL_END_a941'
RAW=HTML.replace(b'</article>',('<p>'+('Transient original context. '*150)+MARKER+'</p></article>').encode())
SOURCE=dict(id='retention-fixture',kind='feed',url='https://example.test/feed',account_id='911090450',account_ids=['911090450'])
FEED=b'<rss><channel><item><title>Food Lifeline update</title><link>https://example.test/original</link><pubDate>Thu, 05 Nov 2026 12:00:00 GMT</pubDate><description>Food Lifeline reports growing demand and more clients.</description></item></channel></rss>'

class RetentionTests(unittest.TestCase):
    def test_daily_cache_removed_after_success_failure_and_unfinished_review(self):
        for mode in ('success','failure','unfinished'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as folder:
                base=Path(folder);paths=[];original_prepare=sr.prepare
                def capture(*a,**kw):
                    packet=original_prepare(*a,**kw)
                    paths.extend(Path(g['original_cache']) for g in packet['groups'])
                    self.assertTrue(paths);self.assertTrue(all(p.exists() for p in paths))
                    return packet
                def reviewer(packet):
                    self.assertTrue(all(p.exists() for p in paths))
                    self.assertTrue(any(MARKER in p.read_text() for p in paths))
                    if mode=='failure':raise RuntimeError('Synthetic reviewer failure')
                    results=verdicts(packet);chain=[]
                    answers={v['signal_id']:dict(actor='retention fixture',result='pass',reason='Synthetic source checked') for v in results['verdicts']}
                    for stage in STAGES:chain.append(checkpoint(stage,packet,answers,chain[-1] if chain else None,results))
                    return dict(verdicts_packet=results,checkpoints=chain)
                retrieve=lambda url,cp:(200,FEED if url==SOURCE['url'] else RAW,{})
                with patch.object(sr,'prepare',side_effect=capture):
                    daily.execute(base/'state',base/'public',retrieve=retrieve,at=datetime(2026,11,6,6,tzinfo=timezone.utc),sources=[SOURCE],jobs=1,reviewer=None if mode=='unfinished' else reviewer)
                self.assertTrue(all(not p.exists() and not p.parent.parent.exists() for p in paths))
                self.assertFalse((base/'state/source-cache').exists())
                for file in base.rglob('*'):
                    if file.is_file():self.assertNotIn(MARKER,file.read_text())
                saved=daily.read(base/'state/state.json')
                for doc in saved['source_review']['documents'].values():
                    self.assertNotIn('original_cache',doc)
                    self.assertTrue(all('text' not in p for p in doc['paragraphs'].values()))

    def test_command_exception_unwinds_temp_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            paths=[];original=sr.prepare
            def capture(*args,**kwargs):
                packet=original(*args,**kwargs);paths.extend(Path(g['original_cache']) for g in packet['groups']);return packet
            with patch.object(sr,'prepare',side_effect=capture),patch.object(sr,'publish',side_effect=RuntimeError('Injected publication failure')):
                with self.assertRaises(RuntimeError):
                    daily.execute(Path(folder)/'state',Path(folder)/'public',retrieve=lambda url,cp:(200,FEED if url==SOURCE['url'] else RAW,{}),at=datetime(2026,11,6,6,tzinfo=timezone.utc),sources=[SOURCE],jobs=1)
            self.assertTrue(paths);self.assertTrue(all(not p.exists() for p in paths))

    def test_prepare_command_cleans_original_before_later_desktop_review(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);out=base/'latest';daily.save(base/'state.json',state());daily.save(out/'collection-worklist.json',collection())
            args=Namespace(action='prepare',state_dir=base,out=out,verdicts=None)
            with patch.object(sr,'Network',return_value=lambda *_:(200,RAW,{})):
                sr._main(args)
            packet=daily.read(out/'source-review-request.json')
            self.assertTrue(packet['groups']);self.assertTrue(all(not Path(g['original_cache']).exists() for g in packet['groups']))
            self.assertNotIn(MARKER,(base/'state.json').read_text())
            # Later checks cannot read an expired original from 304 metadata.
            s=daily.read(base/'state.json');later=sr.prepare(s,lambda *_:(304,b'',{}))
            self.assertTrue(all(g['original_cache'] is None for g in later['groups']))
            with tempfile.TemporaryDirectory() as cache:
                fresh=sr.prepare(s,lambda *_:(200,RAW,{}),cache)
                self.assertTrue(all(Path(g['original_cache']).exists() for g in fresh['groups']))
                self.assertEqual({f['signal_id'] for g in fresh['groups'] for f in g['flags']},set(s['signals']))

    def test_legacy_full_cache_removed_without_touching_feedback_or_excerpts(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);old=root/'source-cache'/('a'*24)/(('b'*64)+'.json')
            daily.save(old,dict(document_version='b'*64,paragraphs={'p':dict(text=MARKER)}))
            unrelated=root/'source-cache/notes.json';daily.save(unrelated,dict(note='Keep this unrelated file'))
            feedback=root/'feedback.sqlite';feedback.write_bytes(b'private decisions stay unchanged')
            metadata=root/'state.json';daily.save(metadata,dict(hash='abc',checking_excerpt='Permitted bounded excerpt'))
            before=metadata.read_bytes();self.assertEqual(sr.purge_legacy_cache(root),1)
            self.assertFalse(old.exists());self.assertTrue(unrelated.exists());self.assertEqual(metadata.read_bytes(),before)
            self.assertEqual(feedback.read_bytes(),b'private decisions stay unchanged');self.assertEqual(sr.purge_legacy_cache(root),0)

if __name__=='__main__':unittest.main()
