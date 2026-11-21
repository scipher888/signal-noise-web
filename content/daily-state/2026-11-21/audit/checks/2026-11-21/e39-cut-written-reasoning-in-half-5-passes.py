import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e39-cut-written-reasoning-in-half-5-passes', 'artifact': 'episode', 'type': 'number', 'story': 'Inkling 2 Mini', 'quote': 'cut its written reasoning in half at five passes'}


def check(ctx):
    return ctx.require('thinking', r'Reasoning at 5 passes was less than half as long as at 1 pass')


if __name__ == '__main__':
    run_cli(CLAIM, check)
