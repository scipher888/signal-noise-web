import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-0902', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': 'Quality hit 0.902 max F1'}


def check(ctx):
    return ctx.require('gemma', r'0\.563 to 0\.902 max F1')


if __name__ == '__main__':
    run_cli(CLAIM, check)
