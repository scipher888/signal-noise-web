import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't11-combined-comparison', 'artifact': 'takeaways', 'type': 'comparison', 'story': "Humanity's First Exam", 'quote': 'the top five models score 96 to 98 percent on a single try of simple tasks but average under 86 percent when required to be consistent across four variations'}


def check(ctx):
    return ctx.require('kaggle', r'Top five models reach 96%–98% pass@1 and 100% family pass@4, yet average only 85\.6% on family pass\^4', r'whether models get simple tasks right every time, not just once', r'in 136 four-prompt families')


if __name__ == '__main__':
    run_cli(CLAIM, check)
