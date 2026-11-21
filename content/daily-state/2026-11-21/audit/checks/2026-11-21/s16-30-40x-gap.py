import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's16-30-40x-gap', 'artifact': 'short', 'type': 'number', 'story': 'AI Autonomous Horizons', 'quote': '30–40x gap'}


def check(ctx):
    return ctx.require('naam', r'33–41× at 80%')


if __name__ == '__main__':
    run_cli(CLAIM, check)
