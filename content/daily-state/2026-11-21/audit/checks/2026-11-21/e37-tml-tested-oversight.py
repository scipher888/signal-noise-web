import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e37-tml-tested-oversight', 'artifact': 'episode', 'type': 'attribution', 'story': 'Inkling 2 Mini', 'quote': 'Thinking Machines tested what that means for oversight'}


def check(ctx):
    return ctx.require('thinking', r'oversee and understand what the model does', r'measured the impact of looping on both performance and monitorability')


if __name__ == '__main__':
    run_cli(CLAIM, check)
