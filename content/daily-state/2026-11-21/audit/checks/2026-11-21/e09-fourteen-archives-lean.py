import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-fourteen-archives-lean', 'artifact': 'episode', 'type': 'number', 'story': 'Riemann Hypothesis proof', 'quote': 'fourteen archives of Lean code'}


def check(ctx):
    return ctx.require('alpoge', r'lean\.tar\.gz\.part01.*part14')


if __name__ == '__main__':
    run_cli(CLAIM, check)
