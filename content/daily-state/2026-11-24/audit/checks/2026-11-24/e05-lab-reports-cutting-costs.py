import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-lab-reports-cutting-costs', 'artifact': 'episode', 'type': 'attribution', 'story': 'Quantum Circuits', 'quote': 'The lab reports cutting computing costs'}


def check(ctx):
    return ctx.require('deepmind', r'cut the required computing cost')


if __name__ == '__main__':
    run_cli(CLAIM, check)
