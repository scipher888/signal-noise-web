import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-2700', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': "even a 2,700-word prompt couldn't close the gap"}


def check(ctx):
    return ctx.require('airbnb', r"2,700 word prompt couldn't|detailed prompt improves classification quality but doesn't close the gap")


if __name__ == '__main__':
    run_cli(CLAIM, check)
