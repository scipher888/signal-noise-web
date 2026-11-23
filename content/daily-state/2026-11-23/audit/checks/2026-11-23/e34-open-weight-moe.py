import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-open-weight-moe', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Ant Group LingSante', 'quote': 'open-weight mixture-of-experts model'}


def check(ctx):
    return ctx.require('lingsante', r'open-weight Mixture-of-Experts model')


if __name__ == '__main__':
    run_cli(CLAIM, check)
