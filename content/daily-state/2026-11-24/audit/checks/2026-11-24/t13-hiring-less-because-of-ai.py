import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't13-hiring-less-because-of-ai', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Anthropic customer study', 'quote': 'hiring less because of AI'}


def check(ctx):
    return ctx.require('anthropic', r'hiring less due to AI|reduced hiring due to AI')


if __name__ == '__main__':
    run_cli(CLAIM, check)
