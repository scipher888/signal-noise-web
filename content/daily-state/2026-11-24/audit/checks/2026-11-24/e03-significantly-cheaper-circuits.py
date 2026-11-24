import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-significantly-cheaper-circuits', 'artifact': 'episode', 'type': 'comparison', 'story': 'Quantum Circuits', 'quote': 'significantly cheaper quantum circuits'}


def check(ctx):
    return ctx.require('deepmind', r'8× cheaper|cut the required computing cost.*11\.8×', r'improvements are significant')


if __name__ == '__main__':
    run_cli(CLAIM, check)
