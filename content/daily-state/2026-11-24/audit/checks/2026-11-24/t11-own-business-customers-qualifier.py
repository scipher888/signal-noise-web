import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-own-business-customers-qualifier', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Anthropic customer study', 'quote': 'its own business customers'}


def check(ctx):
    return ctx.require('anthropic', r'58 of Anthropic.s enterprise customers|They.re all Anthropic customers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
