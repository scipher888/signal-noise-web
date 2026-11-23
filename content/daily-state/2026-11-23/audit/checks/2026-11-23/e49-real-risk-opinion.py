import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-real-risk-opinion', 'artifact': 'episode', 'type': 'opinion', 'story': 'Overview', 'quote': 'That is a real risk'}


def check(ctx):
    return ctx.need(None, None, 'Editorial opinion; not verifiable from sources')


if __name__ == '__main__':
    run_cli(CLAIM, check)
