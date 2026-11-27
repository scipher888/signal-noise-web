import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-apology-timing', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': 'After Oxford philosopher Toby Ord criticized it on that basis, METR CEO Beth Barnes apologized publicly yesterday'}


def check(ctx):
    q = ctx.find('bethmaybarnes', r'^Sorry!')
    return ctx.need('bethmaybarnes', q, 'Public apology; need a dated post establishing November 26 and the chronology relative to Ord’s criticism.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
