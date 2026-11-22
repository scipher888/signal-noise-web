import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's07-17m-lines', 'artifact': 'short', 'type': 'number', 'story': 'AI Verification & Riemann Proof', 'quote': '17M lines'}


def check(ctx):
    return ctx.require('lean', r'17 million lines of code')


if __name__ == '__main__':
    run_cli(CLAIM, check)
