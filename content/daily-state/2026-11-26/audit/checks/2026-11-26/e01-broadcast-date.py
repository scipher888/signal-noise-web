import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e01-broadcast-date', 'artifact': 'episode', 'type': 'number', 'story': 'Broadcast', 'quote': 'Daily State of AI for Thursday, November 26, 2026'}


def check(ctx):
    return ctx.require('framing', r'Daily State of AI.{0,30}Thursday,? November 26,? 2026', note='A story publication date is not a broadcast date.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
