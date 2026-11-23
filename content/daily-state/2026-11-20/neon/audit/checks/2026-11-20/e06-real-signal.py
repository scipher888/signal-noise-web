import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-real-signal', 'artifact': 'episode', 'type': 'opinion', 'story': 'Intro', 'quote': 'The real signal only shows up when you execute under real constraints'}


def check(ctx):
    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')


if __name__ == '__main__':
    run_cli(CLAIM, check)
