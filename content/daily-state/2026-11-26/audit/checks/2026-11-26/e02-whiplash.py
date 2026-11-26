import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-whiplash', 'artifact': 'episode', 'type': 'opinion', 'story': 'Two headlines', 'quote': 'you probably felt whiplash between two stories'}


def check(ctx):
    return ctx.need(None, None, 'Audience reaction is conjectural.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
