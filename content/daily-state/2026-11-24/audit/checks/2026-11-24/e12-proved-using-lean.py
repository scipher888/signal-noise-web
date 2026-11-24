import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-proved-using-lean', 'artifact': 'episode', 'type': 'attribution', 'story': 'Quantum Circuits', 'quote': 'every single circuit was mathematically proved using Lean'}


def check(ctx):
    return ctx.require('deepmind', r'proved each result using Lean')


if __name__ == '__main__':
    run_cli(CLAIM, check)
