import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-published-only-lean', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'he published only the Lean code'}


def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')


if __name__ == '__main__':
    run_cli(CLAIM, check)
