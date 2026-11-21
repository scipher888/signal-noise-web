import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e20-projected-30-hours-or-months', 'artifact': 'episode', 'type': 'number', 'story': 'AI task-horizon analysis', 'quote': 'projected autonomous horizons of thirty hours, or even months'}


def check(ctx):
    return ctx.require('naam', r'30\s*[–-]\s*40 hours', r'tasks that take months')


if __name__ == '__main__':
    run_cli(CLAIM, check)
