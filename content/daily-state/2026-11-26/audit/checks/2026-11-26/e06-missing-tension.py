import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e06-missing-tension', 'artifact': 'episode', 'type': 'opinion', 'story': 'Two headlines', 'quote': "What they're missing is the tension between them"}


def check(ctx):
    return ctx.need(None, None, 'Editorial interpretation.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
