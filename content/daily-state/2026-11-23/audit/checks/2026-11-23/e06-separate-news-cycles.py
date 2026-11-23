import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-separate-news-cycles', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Overview', 'quote': 'Most people are treating these as two separate news cycles'}


def check(ctx):
    return ctx.need(None, None, 'Editorial observation about public reception; not verifiable from sources')


if __name__ == '__main__':
    run_cli(CLAIM, check)
