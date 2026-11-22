import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e14-metr-lifecycle-cost-metric', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR capability update', 'quote': 'METR introduced a new metric called Lifecycle Cost—an estimate of what it takes to build, run, and score a task as a reinforcement learning environment'}


def check(ctx):
    return ctx.require('metr', r'introduce Lifecycle Cost.*RL training environment', r'develop.*run and score the task 100 times')


if __name__ == '__main__':
    run_cli(CLAIM, check)
