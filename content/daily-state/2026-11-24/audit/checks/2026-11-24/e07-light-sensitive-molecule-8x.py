import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-light-sensitive-molecule-8x', 'artifact': 'episode', 'type': 'number', 'story': 'Quantum Circuits', 'quote': '8 times for simulating a light-sensitive molecule'}


def check(ctx):
    return ctx.require('deepmind', r'light-sensitive molecule.*8× cheaper')


if __name__ == '__main__':
    run_cli(CLAIM, check)
