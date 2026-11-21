import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's11-examples-thresholds', 'artifact': 'short', 'type': 'number', 'story': 'Airbnb', 'quote': 'Hundreds of thousands of real examples'}


def check(ctx):
    return ctx.require('airbnb', r'hundreds of thousands of in-domain examples did what', r'Scores let you choose your tradeoff')


if __name__ == '__main__':
    run_cli(CLAIM, check)
