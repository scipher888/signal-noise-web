import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e16-kaggle-owner', 'artifact': 'episode', 'type': 'attribution', 'story': "Humanity's First Exam", 'quote': 'Google-owned Kaggle'}


def check(ctx):
    return ctx.require('kaggle', r'Kaggle is owned by Google')


if __name__ == '__main__':
    run_cli(CLAIM, check)
