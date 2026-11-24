import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-arcsin-290x', 'artifact': 'episode', 'type': 'number', 'story': 'Quantum Circuits', 'quote': '290 times for arcsin'}


def check(ctx):
    return ctx.require('deepmind', r'290x speedup for arcsin')


if __name__ == '__main__':
    run_cli(CLAIM, check)
