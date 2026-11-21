import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 's16-real-signal', 'artifact': 'short', 'type': 'opinion', 'story': 'Close', 'quote': 'The real signal only appears when you execute under real constraints'}


def check(ctx):
    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')


if __name__ == '__main__':
    run_cli(CLAIM, check)
