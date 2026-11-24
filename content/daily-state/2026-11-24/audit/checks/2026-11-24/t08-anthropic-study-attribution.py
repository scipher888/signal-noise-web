import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-anthropic-study-attribution', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Anthropic customer study', 'quote': "Anthropic's study"}


def check(ctx):
    return ctx.require('anthropic', r'Working with AI.*Anthropic')


if __name__ == '__main__':
    run_cli(CLAIM, check)
