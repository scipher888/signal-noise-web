import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's10-claimed-proof-only-lean', 'artifact': 'short', 'type': 'qualifier', 'story': 'Riemann Hypothesis Proof', 'quote': 'Claimed Proof Shipped Only in Lean'}


def check(ctx):
    return ctx.require('alpoge', r'decided to only present Lean')


if __name__ == '__main__':
    run_cli(CLAIM, check)
