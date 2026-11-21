import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's09-matched-35ms-1pct', 'artifact': 'short', 'type': 'comparison', 'story': 'Airbnb', 'quote': 'matched frontier APIs in 35 milliseconds at one percent of the cost'}


def check(ctx):
    return ctx.require('gemma', r'matching top frontier APIs', r'35ms median latency', r'~1% of frontier API spend')


if __name__ == '__main__':
    run_cli(CLAIM, check)
