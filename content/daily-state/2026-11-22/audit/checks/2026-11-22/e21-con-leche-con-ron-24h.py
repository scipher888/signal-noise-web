import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e21-con-leche-con-ron-24h', 'artifact': 'episode', 'type': 'attribution', 'story': 'Riemann Hypothesis proof', 'quote': 'Independent proof checkers like con-leche and con-ron certified the entire proof in twenty-four hours'}


def check(ctx):
    return ctx.require('lean', r'Over the past day', r'con-leche and con-ron checkers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
