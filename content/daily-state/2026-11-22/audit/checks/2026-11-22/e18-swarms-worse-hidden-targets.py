import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e18-swarms-worse-hidden-targets', 'artifact': 'episode', 'type': 'comparison', 'story': 'METR capability update', 'quote': 'on tasks where models had to build their own validation loops against hidden targets, swarms actually performed worse'}


def check(ctx):
    return ctx.require('metr', r'create their own feedback loops.*swarm downlift', r'evaluated on hidden', r'building good validation loops')


if __name__ == '__main__':
    run_cli(CLAIM, check)
