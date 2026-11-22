import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's05-doubling-3-6-months', 'artifact': 'short', 'type': 'number', 'story': 'AI Verification & Riemann Proof', 'quote': 'doubling every 3.6 months'}


def check(ctx):
    return ctx.require('metr', r'doubling roughly every 3\.6\d* months')


if __name__ == '__main__':
    run_cli(CLAIM, check)
