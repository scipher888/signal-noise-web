import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-folding-task', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Protein design', 'quote': 'predict how a whole protein folds from its sequence alone'}


def check(ctx):
    return ctx.require('openai', r'predict a whole protein.s structure from its sequence alone')


if __name__ == '__main__':
    run_cli(CLAIM, check)
