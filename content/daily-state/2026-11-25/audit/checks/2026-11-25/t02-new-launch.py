import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't02-new-launch', 'artifact': 'takeaways', 'type': 'qualifier', 'story': "Humanity's First Exam", 'quote': 'new'}


def check(ctx):
    return ctx.require('kaggle', r'Today, @GoogleDeepMind is launching Humanity.s First Exam')


if __name__ == '__main__':
    run_cli(CLAIM, check)
