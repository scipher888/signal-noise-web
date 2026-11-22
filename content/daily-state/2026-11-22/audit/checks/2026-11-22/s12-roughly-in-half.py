import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's12-roughly-in-half', 'artifact': 'short', 'type': 'qualifier', 'story': 'AI Verification & Riemann Proof', 'quote': 'roughly in half'}


def check(ctx):
    return ctx.require('metr', r'very roughly equivalent to halving')


if __name__ == '__main__':
    run_cli(CLAIM, check)
