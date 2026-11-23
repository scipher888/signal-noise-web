import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-in-half-number', 'artifact': 'takeaways', 'type': 'number', 'story': 'METR AI agent time horizon', 'quote': 'in half'}


def check(ctx):
    return ctx.require('metr', r'halving the time horizon of the agent')


if __name__ == '__main__':
    run_cli(CLAIM, check)
