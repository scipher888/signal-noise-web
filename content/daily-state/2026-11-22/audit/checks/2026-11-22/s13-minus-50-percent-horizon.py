import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's13-minus-50-percent-horizon', 'artifact': 'short', 'type': 'number', 'story': 'AI Verification & Riemann Proof', 'quote': '-50% horizon'}


def check(ctx):
    return ctx.require('metr', r'roughly equivalent to halving the time horizon')


if __name__ == '__main__':
    run_cli(CLAIM, check)
