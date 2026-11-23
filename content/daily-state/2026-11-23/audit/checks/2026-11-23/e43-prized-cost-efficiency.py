import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e43-prized-cost-efficiency', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Ant Group LingSante', 'quote': 'prized mainly for cost efficiency'}


def check(ctx):
    return ctx.require('lingsante', r'performance.cost Pareto frontier', r'relatively low inference cost')


if __name__ == '__main__':
    run_cli(CLAIM, check)
