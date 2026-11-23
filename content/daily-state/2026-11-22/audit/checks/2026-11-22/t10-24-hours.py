import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't10-24-hours', 'artifact': 'takeaways', 'type': 'number', 'story': 'Riemann Hypothesis Lean proof', 'quote': '24 hours'}


def check(ctx):
    return ctx.require('lean', r'Over the past day')


if __name__ == '__main__':
    run_cli(CLAIM, check)
