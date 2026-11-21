import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e24-101', 'artifact': 'episode', 'type': 'number', 'story': 'Society', 'quote': '101-step citation chain'}


def check(ctx):
    return ctx.require('society', r'longest citation chain reached 101 steps')


if __name__ == '__main__':
    run_cli(CLAIM, check)
