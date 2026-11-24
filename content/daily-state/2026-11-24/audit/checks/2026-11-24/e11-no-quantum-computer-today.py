import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e11-no-quantum-computer-today', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Quantum Circuits', 'quote': 'no quantum computer on earth can run them today'}


def check(ctx):
    return ctx.require('deepmind', r"cannot test resource-intensive quantum circuits on.*today's small quantum processors", r'more computational resources than the first error-corrected quantum computers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
