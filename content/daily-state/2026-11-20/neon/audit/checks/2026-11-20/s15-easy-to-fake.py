import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's15-easy-to-fake', 'artifact': 'short', 'type': 'opinion', 'story': 'Close', 'quote': 'Polished prose and top-line scores are easy to fake'}


def check(ctx):
    s = ctx.find('society', r'a convincing paper could still describe a flawed experiment')
    return ctx.need('society', s, 'opinion stated as fact; sources show prose can mislead reviewers, not that scores are "easy to fake"')


if __name__ == '__main__':
    run_cli(CLAIM, check)
