import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't03-not-independently-verified', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Riemann Hypothesis proof claim', 'quote': 'the proof has not been independently verified yet'}


def check(ctx):
    return ctx.require('artificialanlys', r'awaiting independent verification')


if __name__ == '__main__':
    run_cli(CLAIM, check)
