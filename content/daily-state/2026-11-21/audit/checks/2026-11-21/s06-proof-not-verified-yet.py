import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's06-proof-not-verified-yet', 'artifact': 'short', 'type': 'qualifier', 'story': 'Riemann Hypothesis Proof', 'quote': "The claimed math proof isn't verified yet"}


def check(ctx):
    return ctx.require('artificialanlys', r'awaiting independent verification')


if __name__ == '__main__':
    run_cli(CLAIM, check)
