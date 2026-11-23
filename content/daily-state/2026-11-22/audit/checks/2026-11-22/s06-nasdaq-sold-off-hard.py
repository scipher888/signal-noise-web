import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's06-nasdaq-sold-off-hard', 'artifact': 'short', 'type': 'qualifier', 'story': 'AI Verification & Riemann Proof', 'quote': 'the Nasdaq sold off hard'}


def check(ctx):
    return ctx.require('dkthomp', r'Nasdaq absolutely vomits up all over itself')


if __name__ == '__main__':
    run_cli(CLAIM, check)
