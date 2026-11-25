import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-stark-drop', 'artifact': 'episode', 'type': 'opinion', 'story': "Humanity's First Exam", 'quote': 'The drop-off is stark'}


def check(ctx):
    return ctx.need('kaggle', ctx.find('kaggle', r'Top five models reach 96%–98% pass@1.*85\.6%'), 'Stark is an assessment of the measured difference.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
