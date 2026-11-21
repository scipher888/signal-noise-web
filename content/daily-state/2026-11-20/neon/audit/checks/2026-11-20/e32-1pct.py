import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-1pct', 'artifact': 'episode', 'type': 'number', 'story': 'Airbnb', 'quote': 'costs fell to about one percent at high volume'}


def check(ctx):
    return ctx.require('gemma', r'~1% of frontier API spend at high volume', note='relative cost vs frontier APIs; "fell" is loose but the figure matches')


if __name__ == '__main__':
    run_cli(CLAIM, check)
