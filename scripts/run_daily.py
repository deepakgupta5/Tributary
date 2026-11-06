#!/usr/bin/env python3
"""The same local command is used manually and by the native Mac scheduler."""
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0,str(ROOT))
config=ROOT/'out/schedule/config.json'
if config.exists():
    settings=json.loads(config.read_text())
    if settings.get('feedback_db'):
        os.environ.setdefault('TRIBUTARY_FEEDBACK_DB',settings['feedback_db'])
from tributary.daily import main
main()
