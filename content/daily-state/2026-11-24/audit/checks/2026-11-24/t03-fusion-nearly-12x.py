import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-fusion-nearly-12x', 'artifact': 'takeaways', 'type': 'number', 'story': 'Google DeepMind quantum circuits', 'quote': 'costs cut by nearly 12 times for an inertial confinement fusion simulation'}


def check(ctx):
    return ctx.require('deepmind', r'inertial confinement fusion', r'computing cost.*11\.8×')


if __name__ == '__main__':
    run_cli(CLAIM, check)
