import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's10-2700', 'artifact': 'short', 'type': 'comparison', 'story': 'Airbnb', 'quote': "Even a 2,700-word prompt couldn't close the gap"}


def check(ctx):
    return ctx.require('airbnb', r"2,700 word prompt couldn't")


if __name__ == '__main__':
    run_cli(CLAIM, check)
