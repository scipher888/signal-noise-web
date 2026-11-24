import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't10-58-own-business-customers', 'artifact': 'takeaways', 'type': 'number', 'story': 'Anthropic customer study', 'quote': '58 of its own business customers'}


def check(ctx):
    return ctx.require('anthropic', r'58 of Anthropic.s enterprise customers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
