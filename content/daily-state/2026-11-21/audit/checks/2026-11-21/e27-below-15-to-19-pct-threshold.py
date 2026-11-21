import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-below-15-to-19-pct-threshold', 'artifact': 'episode', 'type': 'comparison', 'story': 'AI task-horizon analysis', 'quote': 'far below the fifteen to nineteen percent threshold needed for runaway self-improvement'}


def check(ctx):
    return ctx.require('naam', r'well short of the 15-19% threshold for a self-sustaining AI recursive self-improvement loop')


if __name__ == '__main__':
    run_cli(CLAIM, check)
