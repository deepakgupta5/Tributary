"""Native current-login launchd registration. No paid service or model calls.

The plist stays in the writable checkout. Registration is active in this GUI login;
login/reboot auto-loading requires placing it in ~/Library/LaunchAgents, which this
managed session cannot write. Do not claim that persistence is installed.
"""
import argparse
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys

from tributary.daily import ROOT, save

LABEL='com.autonomybridge.tributary.daily'


def definition(root=ROOT,python=sys.executable):
    return dict(Label=LABEL,ProgramArguments=[str(python),str(root/'scripts/run_daily.py'),'--scheduled'],
        WorkingDirectory=str(root),StartCalendarInterval=dict(Minute=5),RunAtLoad=True,
        StandardOutPath=str(root/'out/schedule/launchd.stdout.log'),StandardErrorPath=str(root/'out/schedule/launchd.stderr.log'))


def install():
    directory=ROOT/'out/schedule';directory.mkdir(parents=True,exist_ok=True)
    path=directory/(LABEL+'.plist')
    path.write_bytes(plistlib.dumps(definition()))
    target='gui/'+str(os.getuid())+'/'+LABEL
    prior=subprocess.run(['/bin/launchctl','print',target],capture_output=True,text=True)
    if prior.returncode==0:
        if str(path) not in prior.stdout: raise RuntimeError('Label belongs to another registration; refusing to replace it')
    else:
        subprocess.run(['/bin/launchctl','bootstrap','gui/'+str(os.getuid()),str(path)],capture_output=True,text=True,check=True)
    check=subprocess.run(['/bin/launchctl','print',target],capture_output=True,text=True,check=True)
    if LABEL not in check.stdout or str(path) not in check.stdout: raise RuntimeError('Registration verification failed')
    proof=dict(registered=True,mechanism='native launchd GUI-login job',label=LABEL,plist=str(path),
        trigger='hourly at minute 05 plus bootstrap/wake catch-up; daily collection guard at/after 08:00 Vancouver',
        additional_cost=0,automatic_model_calls=False,reboot_login_autoload=False,scheduled_collection_observed=False,
        limitation='The job is registered for this login. Persistent login/reboot loading is not installed because the managed session cannot write ~/Library/LaunchAgents.',
        command=definition()['ProgramArguments'])
    save(directory/'launchd-registration.json',proof)
    return proof


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');args=p.parse_args()
    if args.verify:
        r=subprocess.run(['/bin/launchctl','print','gui/'+str(os.getuid())+'/'+LABEL],capture_output=True,text=True)
        print(json.dumps(dict(registered=r.returncode==0,label=LABEL,details=r.stdout if r.returncode==0 else r.stderr)))
    else: print(json.dumps(install(),sort_keys=True))


if __name__=='__main__': main()
