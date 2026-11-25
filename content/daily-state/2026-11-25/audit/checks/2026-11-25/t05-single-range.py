import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't05-single-range', 'artifact': 'takeaways', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'score 96 to 98 percent'}


def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1')


if __name__ == '__main__':
    run_cli(CLAIM, check)
