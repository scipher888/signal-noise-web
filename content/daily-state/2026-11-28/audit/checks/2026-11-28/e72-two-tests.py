import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e72-two-tests', 'artifact': 'episode', 'type': 'number', 'story': 'Alignment evaluations', 'quote': 'in two tests'}


def check(ctx):
    return ctx.require('gpt', r'in two tests, they were more likely to omit mentioning obstacles')


if __name__ == '__main__':
    run_cli(CLAIM, check)
