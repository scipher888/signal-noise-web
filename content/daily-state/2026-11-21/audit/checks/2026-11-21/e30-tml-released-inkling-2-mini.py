import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-tml-released-inkling-2-mini', 'artifact': 'episode', 'type': 'attribution', 'story': 'Inkling 2 Mini', 'quote': 'Thinking Machines Lab just released Inkling 2 Mini'}


def check(ctx):
    return ctx.require('thinking', r'Thinking Machines Lab', r'Today we are releasing Inkling 2 Mini')


if __name__ == '__main__':
    run_cli(CLAIM, check)
