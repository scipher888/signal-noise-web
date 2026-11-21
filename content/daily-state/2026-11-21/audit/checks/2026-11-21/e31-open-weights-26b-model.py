import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e31-open-weights-26b-model', 'artifact': 'episode', 'type': 'number', 'story': 'Inkling 2 Mini', 'quote': 'an open-weights, twenty-six-billion-parameter model'}


def check(ctx):
    return ctx.require('thinking', r'26\.4B total parameters', r'released with open weights')


if __name__ == '__main__':
    run_cli(CLAIM, check)
