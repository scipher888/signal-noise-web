import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-matched-1pct', 'artifact': 'episode', 'type': 'comparison', 'story': 'Airbnb', 'quote': 'matched frontier APIs at one percent of the cost'}


def check(ctx):
    return ctx.require('airbnb', r'matches frontier-level quality .*roughly 1% of the cost')


if __name__ == '__main__':
    run_cli(CLAIM, check)
