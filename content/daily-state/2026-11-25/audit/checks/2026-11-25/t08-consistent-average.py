import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't08-consistent-average', 'artifact': 'takeaways', 'type': 'number', 'story': "Humanity's First Exam", 'quote': 'average under 86 percent'}


def check(ctx):
    return ctx.require('kaggle', r'Top five models reach.*average only 85\.6% on family pass\^4')


if __name__ == '__main__':
    run_cli(CLAIM, check)
