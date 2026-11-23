import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-independent-checkers-24h', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Riemann Hypothesis Lean proof', 'quote': 'independent checkers certifying it in 24 hours'}


def check(ctx):
    return ctx.require('lean', r'Over the past day', r'several independent checkers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
