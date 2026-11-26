import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't24-deliberately', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'deliberately'}


def check(ctx):
    q = ctx.find('framing', r'he explicitly declines to vouch for the specifics')
    return ctx.need('framing', q, 'Explicit reservation about specifics; intent about naming RSA cannot be inferred.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
