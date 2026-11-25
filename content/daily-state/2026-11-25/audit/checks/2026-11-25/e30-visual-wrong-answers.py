import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-visual-wrong-answers', 'artifact': 'episode', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'Nearly three-quarters of wrong answers are basic visual perception mistakes'}


def check(ctx):
    return ctx.require('kaggle', r'Visual perception drives 74% of wrong answers')


if __name__ == '__main__':
    run_cli(CLAIM, check)
