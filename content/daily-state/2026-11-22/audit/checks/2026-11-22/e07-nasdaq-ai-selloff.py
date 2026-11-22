import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-nasdaq-ai-selloff', 'artifact': 'episode', 'type': 'attribution', 'story': 'Nasdaq AI sell-off', 'quote': 'the Nasdaq sold off hard as investors questioned whether the AI trade is actually paying off'}


def check(ctx):
    return ctx.require('dkthomp', r'Nasdaq.*AI Trade')


if __name__ == '__main__':
    run_cli(CLAIM, check)
