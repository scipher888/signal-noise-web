import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-metr-doubling-3-6-months', 'artifact': 'episode', 'type': 'number', 'story': 'METR capability update', 'quote': 'the length of tasks frontier models can complete is still doubling roughly every 3.6 months'}


def check(ctx):
    return ctx.require('metr', r'time horizons are doubling roughly every 3\.6\d* months')


if __name__ == '__main__':
    run_cli(CLAIM, check)
