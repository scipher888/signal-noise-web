import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-12of50', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Blueprint', 'quote': 'human baseline was tested on just twelve apartments out of fifty'}


def check(ctx):
    return ctx.require('blueprint', r'Human baseline tested on subset of 12 apartments only', r'processes 50 apartments')


if __name__ == '__main__':
    run_cli(CLAIM, check)
