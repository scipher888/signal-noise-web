import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e15-codebase-overfit', 'artifact': 'episode', 'type': 'attribution', 'story': 'METR chart debate', 'quote': 'They flagged possible codebase overfitting'}


def check(ctx):
    return ctx.require('metr', r'various types of overfitting', r'small parts of the codebase could have leaked into training data')


if __name__ == '__main__':
    run_cli(CLAIM, check)
