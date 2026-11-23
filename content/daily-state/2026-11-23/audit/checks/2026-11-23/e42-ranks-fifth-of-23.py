import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-ranks-fifth-of-23', 'artifact': 'episode', 'type': 'number', 'story': 'Ant Group LingSante', 'quote': 'LingSante actually ranks fifth out of twenty-three configurations'}


def check(ctx):
    return ctx.require('lingsante', r'ranked fifth among the 23 model configurations evaluated')


if __name__ == '__main__':
    run_cli(CLAIM, check)
