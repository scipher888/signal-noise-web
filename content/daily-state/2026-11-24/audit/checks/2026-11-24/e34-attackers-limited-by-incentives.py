import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-attackers-limited-by-incentives', 'artifact': 'episode', 'type': 'opinion', 'story': 'CSET Cyber Report', 'quote': 'That could just be reporting lag, or it could mean something deeper: attackers are not limited by technical capability'}


def check(ctx):
    s = ctx.find('openai', r'If the limiting factor constraining cyber attacks was the threat of jail and missiles')
    return ctx.need('openai', s, 'Opinion/hypothesis in CSET report; check whether episode overstates conditional framing as settled fact')


if __name__ == '__main__':
    run_cli(CLAIM, check)
