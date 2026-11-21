import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-headlines-miss', 'artifact': 'episode', 'type': 'opinion', 'story': 'Intro', 'quote': 'all three headlines miss the best part'}


def check(ctx):
    return ctx.need(None, None, 'opinion / framing; not checkable against sources')


if __name__ == '__main__':
    run_cli(CLAIM, check)
