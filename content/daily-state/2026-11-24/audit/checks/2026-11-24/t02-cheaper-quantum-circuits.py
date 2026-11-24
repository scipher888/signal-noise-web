import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-cheaper-quantum-circuits', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Google DeepMind quantum circuits', 'quote': 'cheaper quantum circuits'}


def check(ctx):
    return ctx.require('deepmind', r'8× cheaper|cut the required computing cost')


if __name__ == '__main__':
    run_cli(CLAIM, check)
