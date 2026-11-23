import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-25b-active-per-token', 'artifact': 'episode', 'type': 'number', 'story': 'Ant Group LingSante', 'quote': '25 billion active per token'}


def check(ctx):
    return ctx.require('lingsante', r'activates 25 billion parameters per token')


if __name__ == '__main__':
    run_cli(CLAIM, check)
