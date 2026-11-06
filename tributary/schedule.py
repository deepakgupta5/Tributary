"""Register a zero-additional-cost native Mac cron trigger without model calls.

The trigger polls hourly at :05. Python's Vancouver-time guard collects once per
local day at/after 08:00, and catches up at the next trigger when the Mac resumes.
Only the marked Tributary block is changed; unrelated cron entries are preserved.
"""
import argparse
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

from tributary.daily import ROOT, save

BEGIN='# BEGIN TRIBUTARY DAILY (managed)'
END='# END TRIBUTARY DAILY (managed)'


def block(root=ROOT,python=sys.executable):
    command=shlex.join([str(python),str(root/'scripts/run_daily.py'),'--scheduled'])
    log=shlex.quote(str(root/'out/schedule/daily.log'))
    return '\n'.join([BEGIN,'5 * * * * '+command+' >> '+log+' 2>&1',END])


def replace(existing,newblock):
    if (BEGIN in existing)!=(END in existing): raise ValueError('Incomplete existing Tributary block; refusing to modify crontab')
    if BEGIN in existing:
        before,tail=existing.split(BEGIN,1)
        _,after=tail.split(END,1)
        return before+newblock+after
    return existing+('' if not existing or existing.endswith('\n') else '\n')+newblock+'\n'


def current():
    result=subprocess.run(['/usr/bin/crontab','-l'],capture_output=True,text=True)
    if result.returncode and 'no crontab' not in result.stderr.lower():
        raise RuntimeError(result.stderr.strip())
    return result.stdout if result.returncode==0 else ''


def install(feedback_db=None):
    directory=ROOT/'out/schedule';directory.mkdir(parents=True,exist_ok=True)
    if feedback_db: save(directory/'config.json',dict(feedback_db=str(Path(feedback_db).resolve())))
    desired=block()
    existing=current();replacement=replace(existing,desired)
    # The native crontab interface owns registration. No direct edits to system
    # spool files or LaunchAgents directories, and no elevated permissions.
    with tempfile.NamedTemporaryFile(mode='w',dir=directory,delete=False) as stream:
        path=Path(stream.name);stream.write(replacement)
    try:
        subprocess.run(['/usr/bin/crontab',str(path)],capture_output=True,text=True,check=True)
    finally: path.unlink(missing_ok=True)
    registered=current()
    if desired not in registered: raise RuntimeError('Scheduler registration did not verify')
    proof=dict(registered=True,mechanism='native user crontab',trigger='hourly at minute 05',collection='once per Vancouver calendar day at/after 08:00, next available trigger',timezone='America/Vancouver',
        entry=desired,additional_cost=0,automatic_model_calls=False,scheduled_execution_observed=False,
        warning='Registration is verified, not a later cron execution. Mac availability, network and macOS background-file access still govern execution.')
    save(directory/'registration.json',proof)
    return proof


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--feedback-db',type=Path);p.add_argument('--verify',action='store_true')
    args=p.parse_args()
    if args.verify: print(json.dumps(dict(registered=block() in current(),entry=block()),sort_keys=True))
    else: print(json.dumps(install(args.feedback_db),sort_keys=True))


if __name__=='__main__': main()
